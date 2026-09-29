"""
YouTube Shorts Publisher Script for History of Earth.
Publishes vertical 9:16 Shorts to YouTube with 'public' visibility,
attaches optimized tags/hashtags, and records Video IDs.
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

from agents.publisher import get_authenticated_service, upload_video
from pipeline.state_machine import transition

def main():
    print("=" * 80)
    print("PUBLISHING EPISODE SHORTS TO YOUTUBE (VISIBILITY: PUBLIC)")
    print("=" * 80)

    client_secrets = os.path.join(PROJECT_ROOT, "client_secret.json")
    token_file = os.path.join(PROJECT_ROOT, "token.json")
    shorts_meta_file = os.path.join(PROJECT_ROOT, "output", "hadean_landscape_01", "shorts", "shorts_metadata.json")
    db_path = os.path.join(PROJECT_ROOT, "state.db")

    if not os.path.exists(client_secrets):
        print(f"[ERROR] Client secrets not found at {client_secrets}")
        sys.exit(1)

    if not os.path.exists(shorts_meta_file):
        print(f"[ERROR] Shorts metadata not found at {shorts_meta_file}")
        sys.exit(1)

    with open(shorts_meta_file, "r", encoding="utf-8") as f:
        shorts_list = json.load(f)

    print("\n[STEP 1] Authenticating with YouTube Data API v3...")
    youtube = get_authenticated_service(client_secrets_file=client_secrets, token_file=token_file)
    print("  [OK] Authenticated successfully with YouTube API.")

    published_shorts = []

    for idx, short_meta in enumerate(shorts_list, 1):
        rel_path = short_meta["file_path"]
        video_path = os.path.join(PROJECT_ROOT, rel_path)
        if not os.path.exists(video_path):
            # Try direct path
            video_path = os.path.join(PROJECT_ROOT, "output", "hadean_landscape_01", "shorts", os.path.basename(rel_path))

        print(f"\n[STEP {idx + 1}] Uploading Short {idx}/{len(shorts_list)}:")
        print(f"  Title: {short_meta['title']}")
        print(f"  File: {video_path}")
        print(f"  Visibility: PUBLIC")

        upload_payload = {
            "title": short_meta["title"],
            "description": short_meta["description"],
            "tags": [t.replace("#", "") for t in short_meta["tags"]],
            "category_id": "27"
        }

        res = upload_video(youtube, video_path=video_path, metadata=upload_payload, privacy_status="public")
        video_id = res["video_id"]
        shorts_url = f"https://youtube.com/shorts/{video_id}"

        print(f"  [SUCCESS] Short Published!")
        print(f"  --> Video ID: {video_id}")
        print(f"  --> URL: {shorts_url}")
        print(f"  --> Status: {res['privacy_status'].upper()}")

        short_meta["youtube_video_id"] = video_id
        short_meta["youtube_url"] = shorts_url
        short_meta["published_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        published_shorts.append(short_meta)

    # Save updated metadata with live URLs
    with open(shorts_meta_file, "w", encoding="utf-8") as f:
        json.dump(published_shorts, f, indent=2)

    print("\n" + "=" * 80)
    print("ALL SHORTS SUCCESSFULLY PUBLISHED TO YOUTUBE:")
    for s in published_shorts:
        print(f" - {s['title']} -> {s['youtube_url']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
