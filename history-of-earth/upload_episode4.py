"""
YouTube Publisher Script for Episode 4:
"Hadean: The Planet Before Life — Genesis in the Abyss".
Publishes:
1. Master Episode (final_episode.mp4) with PUBLIC visibility, soft SRT caption track, and custom thumbnail.
2. Vertical Short 1 (short_01_dead_rocks_code.mp4) with PUBLIC visibility.
3. Vertical Short 2 (short_02_natural_proton_battery.mp4) with PUBLIC visibility.
4. Updates state machine and Gate B review file with live watch URLs.
"""

import os
import sys
import json
import time

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from agents.publisher import (
    get_authenticated_service,
    upload_video,
    upload_caption,
    upload_thumbnail,
    GLOBAL_QUOTA_TRACKER
)
from pipeline.state_machine import transition


def main():
    print("=" * 85)
    print("PUBLISHING EPISODE 4 & SHORTS TO YOUTUBE (VISIBILITY: PUBLIC)")
    print("Title: 'Hadean: The Planet Before Life — Genesis in the Abyss'")
    print("=" * 85)

    episode_id = "hadean_life_then_04"
    episode_dir = os.path.join(PROJECT_ROOT, "output", episode_id)
    video_path = os.path.join(episode_dir, "final_episode.mp4")
    srt_path = os.path.join(episode_dir, "en.srt")
    meta_path = os.path.join(episode_dir, "metadata.json")
    thumb_path = os.path.join(episode_dir, "hadean_life_then_04_thumb_candidate_a.png")
    shorts_meta_file = os.path.join(episode_dir, "shorts", "shorts_metadata.json")
    client_secrets = os.path.join(PROJECT_ROOT, "client_secret.json")
    token_file = os.path.join(PROJECT_ROOT, "token.json")
    db_path = os.path.join(PROJECT_ROOT, "state.db")

    if not os.path.exists(client_secrets):
        print(f"[ERROR] '{client_secrets}' not found.")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Step 1: Authenticate with YouTube Data API v3
    print("\n[STEP 1] Authenticating with YouTube Data API v3...")
    youtube = get_authenticated_service(client_secrets_file=client_secrets, token_file=token_file)
    print("  [OK] Authenticated successfully with YouTube API.")

    # Step 2: Upload Master Episode as PUBLIC
    print(f"\n[STEP 2] Uploading Master Video ({metadata['title']}) as PUBLIC...")
    upload_res = upload_video(youtube, video_path=video_path, metadata=metadata, privacy_status="public")
    main_video_id = upload_res["video_id"]
    main_url = f"https://youtu.be/{main_video_id}"
    print("  [SUCCESS] Master Video Uploaded!")
    print(f"  --> Video ID: {main_video_id}")
    print(f"  --> Watch URL: {main_url}")
    print(f"  --> Privacy Status: {upload_res['privacy_status'].upper()}")

    # Step 3: Attach English Soft Captions (en.srt)
    print(f"\n[STEP 3] Uploading English Subtitle Track (en.srt)...")
    if os.path.exists(srt_path):
        try:
            caption_res = upload_caption(youtube, video_id=main_video_id, srt_path=srt_path, language="en", name="English (Default)")
            print(f"  [SUCCESS] Subtitle track attached! Caption ID: {caption_res.get('caption_id')}")
        except Exception as exc:
            print(f"  [WARNING] Caption upload notice: {exc}")
    else:
        print("  [SKIP] Subtitle track file not found.")

    # Step 4: Upload Custom High-CTR Thumbnail
    print(f"\n[STEP 4] Setting High-CTR Custom Thumbnail (Candidate A)...")
    if os.path.exists(thumb_path):
        try:
            thumb_res = upload_thumbnail(youtube, video_id=main_video_id, thumbnail_path=thumb_path)
            if thumb_res.get("success"):
                print("  [SUCCESS] Custom thumbnail applied successfully!")
            else:
                print(f"  [NOTE] Custom thumbnail status: {thumb_res.get('error')}")
        except Exception as exc:
            print(f"  [WARNING] Thumbnail upload notice: {exc}")

    # Step 5: Upload Vertical Shorts as PUBLIC
    print(f"\n[STEP 5] Uploading Vertical 9:16 Shorts as PUBLIC...")
    published_shorts = []
    if os.path.exists(shorts_meta_file):
        with open(shorts_meta_file, "r", encoding="utf-8") as f:
            shorts_list = json.load(f)

        for s_idx, s in enumerate(shorts_list, 1):
            short_path = s["file_path"]
            if not os.path.exists(short_path):
                print(f"  [SKIP] Short video file not found: {short_path}")
                continue

            s_meta = {
                "title": s["title"],
                "description": s["description"],
                "tags": s["tags"],
                "categoryId": "28"
            }
            print(f"\n  --> Uploading Short {s_idx}/{len(shorts_list)}: '{s['title']}'...")
            try:
                s_upload = upload_video(youtube, video_path=short_path, metadata=s_meta, privacy_status="public")
                s_vid_id = s_upload["video_id"]
                s_url = f"https://youtube.com/shorts/{s_vid_id}"
                print(f"      [SUCCESS] Short Uploaded! ID: {s_vid_id}")
                print(f"      [WATCH URL] {s_url}")
                published_shorts.append({
                    "title": s["title"],
                    "video_id": s_vid_id,
                    "url": s_url
                })
            except Exception as e:
                print(f"      [WARNING] Error uploading Short {s_idx}: {e}")

    # Step 6: Transition State Machine
    print("\n[STEP 6] Updating Pipeline State...")
    transition(episode_id, "published", note=f"Published to YouTube (Main: {main_video_id})", db_path=db_path)

    # Step 7: Update Gate B HTML Review File
    gate_b_file = os.path.join(PROJECT_ROOT, "review", "gate_b_review_ep4.html")
    if os.path.exists(gate_b_file):
        with open(gate_b_file, "r", encoding="utf-8") as f:
            html = f.read()

        status_old = '<span class="badge badge-green">Status: ASSEMBLED & COMPLIANT</span>'
        status_new = f'<span class="badge badge-green">Status: PUBLISHED</span> | <a href="{main_url}" target="_blank" style="color: #38bdf8; font-weight: bold;">Watch on YouTube ({main_video_id}) &rarr;</a>'
        html = html.replace(status_old, status_new)

        with open(gate_b_file, "w", encoding="utf-8") as f:
            f.write(html)
        print("  [OK] Updated Gate B review dashboard with live YouTube link.")

    print("\n" + "=" * 85)
    print("EPISODE 4 & SHORTS PUBLISHING COMPLETE!")
    print(f"Master Video: {main_url}")
    for ps in published_shorts:
        print(f"Short: {ps['title']} -> {ps['url']}")
    print("=" * 85)


if __name__ == "__main__":
    main()
