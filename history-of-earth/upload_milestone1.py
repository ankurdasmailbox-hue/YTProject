"""
YouTube Publisher Script for Milestone 1.
Uploads the rendered episode "Hadean: A World of Fire and Rain" as UNLISTED,
uploads the soft SRT caption track, and logs runtime quota usage.
"""

import os
import sys
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from agents.publisher import get_authenticated_service, upload_video, upload_caption, GLOBAL_QUOTA_TRACKER
from pipeline.state_machine import transition

def main():
    print("=" * 80)
    print("UPLOADING MILESTONE 1 EPISODE TO YOUTUBE (UNLISTED)")
    print("=" * 80)

    episode_id = "hadean_landscape_01"
    episode_dir = os.path.join(PROJECT_ROOT, "output", episode_id)
    video_path = os.path.join(episode_dir, "final_episode.mp4")
    srt_path = os.path.join(episode_dir, "en.srt")
    meta_path = os.path.join(episode_dir, "metadata.json")
    client_secrets = os.path.join(PROJECT_ROOT, "client_secret.json")
    token_file = os.path.join(PROJECT_ROOT, "token.json")
    db_path = os.path.join(PROJECT_ROOT, "state.db")

    if not os.path.exists(client_secrets):
        print(f"[ERROR] '{client_secrets}' not found.")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print("\n[STEP 1] Authenticating with YouTube Data API v3 (OAuth 2.0)...")
    print("If this is your first time, a browser tab will open requesting your authorization.")
    youtube = get_authenticated_service(client_secrets_file=client_secrets, token_file=token_file)
    print("  [OK] Authenticated successfully.")

    print(f"\n[STEP 2] Uploading video '{metadata['title']}' as UNLISTED...")
    upload_res = upload_video(youtube, video_path=video_path, metadata=metadata, privacy_status="unlisted")
    video_id = upload_res["video_id"]
    print(f"  [SUCCESS] Video Uploaded!")
    print(f"  --> Video ID: {video_id}")
    print(f"  --> URL: https://youtu.be/{video_id}")
    print(f"  --> Privacy: {upload_res['privacy_status']}")

    print(f"\n[STEP 3] Uploading English Subtitle Track (en.srt)...")
    caption_res = upload_caption(youtube, video_id=video_id, srt_path=srt_path, language="en", name="English (Default)")
    print(f"  [SUCCESS] Subtitle track attached! Caption ID: {caption_res['caption_id']}")

    print("\n[STEP 4] Updating State Database...")
    transition(episode_id, "published", note=f"Uploaded unlisted to YouTube (ID: {video_id})", db_path=db_path)
    print("  [OK] State updated to 'published'.")

    print("\n" + "=" * 80)
    print(f"MILESTONE 1 UPLOAD COMPLETE: https://youtu.be/{video_id}")
    print("=" * 80)

if __name__ == "__main__":
    main()
