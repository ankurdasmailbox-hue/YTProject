"""
YouTube Publisher Script for Episode 3: "Hadean: The Sky Was Poison and the Rain Never Stopped".
Publishes:
1. Master Episode (final_episode.mp4) with PUBLIC visibility, soft SRT caption track, and custom thumbnail.
2. Vertical Short 1 (short_01_green_ocean.mp4) with PUBLIC visibility.
3. Vertical Short 2 (short_02_poison_atmosphere.mp4) with PUBLIC visibility.
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
    print("PUBLISHING EPISODE 3 & SHORTS TO YOUTUBE (VISIBILITY: PUBLIC)")
    print("Title: 'Earth Had a Green Ocean and a Poison Sky For 500 Million Years'")
    print("=" * 85)

    episode_id = "hadean_air_ocean_03"
    episode_dir = os.path.join(PROJECT_ROOT, "output", episode_id)
    video_path = os.path.join(episode_dir, "final_episode.mp4")
    srt_path = os.path.join(episode_dir, "en.srt")
    meta_path = os.path.join(episode_dir, "metadata.json")
    thumb_path = os.path.join(episode_dir, "hadean_air_ocean_03_thumb_candidate_a.png")
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

        for idx, short_meta in enumerate(shorts_list, 1):
            short_file = short_meta.get("file_path", "")
            if not os.path.isabs(short_file):
                short_file = os.path.join(PROJECT_ROOT, short_file)

            clean_title = short_meta["title"].replace(" #Shorts #Shorts", " #Shorts")
            if not clean_title.endswith("#Shorts"):
                clean_title = f"{clean_title} #Shorts"

            print(f"\n  --> Uploading Short {idx}/{len(shorts_list)}: '{clean_title}'...")
            upload_payload = {
                "title": clean_title,
                "description": f"{short_meta['description']}\n\nWatch full episode: {main_url}",
                "tags": [t.replace("#", "") for t in short_meta.get("tags", [])],
                "category_id": "27"
            }

            try:
                res_short = upload_video(youtube, video_path=short_file, metadata=upload_payload, privacy_status="public")
                s_id = res_short["video_id"]
                s_url = f"https://youtube.com/shorts/{s_id}"
                print(f"  [SUCCESS] Short {idx} Published!")
                print(f"  --> Short Video ID: {s_id}")
                print(f"  --> Short URL: {s_url}")
                short_meta["youtube_video_id"] = s_id
                short_meta["youtube_url"] = s_url
                short_meta["published_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                published_shorts.append(short_meta)
            except Exception as exc:
                print(f"  [ERROR] Uploading short {idx} failed: {exc}")

        # Update shorts metadata
        with open(shorts_meta_file, "w", encoding="utf-8") as f:
            json.dump(published_shorts, f, indent=2)

    # Step 6: Update State Machine
    print("\n[STEP 6] Updating Pipeline State Machine...")
    transition(episode_id, "published", note=f"Published to YouTube (Main: {main_video_id})", db_path=db_path)
    print("  [OK] Episode state transitioned to 'published'.")

    # Step 7: Update Gate B Review HTML with live watch URLs
    review_file = os.path.join(PROJECT_ROOT, "review", "gate_b_review_ep3.html")
    if os.path.exists(review_file):
        with open(review_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = html_content.replace(
            '<span class="badge badge-green">Status: ASSEMBLED &amp; QC PASSED</span>',
            f'<span class="badge badge-green">Status: PUBLISHED</span> | <a href="{main_url}" target="_blank" style="color: #38bdf8; font-weight: bold;">Watch on YouTube ({main_video_id}) &rarr;</a>'
        )

        with open(review_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("  [OK] Updated Gate B review file with live watch links.")

    print("\n" + "=" * 85)
    print("EPISODE 3 & SHORTS PUBLISHING COMPLETE!")
    print(f"Master Episode: {metadata['title']}")
    print(f"Watch URL: {main_url}")
    for s in published_shorts:
        print(f"Short: {s['title']} -> {s['youtube_url']}")
    print("=" * 85)


if __name__ == "__main__":
    main()
