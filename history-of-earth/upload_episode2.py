"""
YouTube Upload Script for Episode 2: "The Planet With No Plates — Before Continents Were Born".
Uploads the 100% animated master video with viral hashtags, high-ranking search tags,
English subtitle track, and high-CTR thumbnail candidate.
"""

import os
import sys
import json

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
    print("UPLOADING EPISODE 2 TO YOUTUBE: 'Hadean: The Planet With No Plates'")
    print("=" * 85)

    episode_id = "hadean_map_02"
    episode_dir = os.path.join(PROJECT_ROOT, "output", episode_id)
    video_path = os.path.join(episode_dir, "final_episode.mp4")
    srt_path = os.path.join(episode_dir, "en.srt")
    meta_path = os.path.join(episode_dir, "metadata.json")
    thumb_path = os.path.join(episode_dir, "hadean_map_02_thumb_candidate_a.png")
    client_secrets = os.path.join(PROJECT_ROOT, "client_secret.json")
    token_file = os.path.join(PROJECT_ROOT, "token.json")
    db_path = os.path.join(PROJECT_ROOT, "state.db")

    if not os.path.exists(client_secrets):
        print(f"[ERROR] '{client_secrets}' not found.")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Step 1: Authenticate
    print("\n[STEP 1] Authenticating with YouTube Data API v3...")
    youtube = get_authenticated_service(client_secrets_file=client_secrets, token_file=token_file)
    print("  [OK] Authenticated successfully.")

    # Step 2: Upload Video
    # Use unlisted by default per project spec or user can switch to public
    privacy = metadata.get("privacy_status", "unlisted")
    print(f"\n[STEP 2] Uploading master video ({metadata['title']}) as {privacy.upper()}...")
    upload_res = upload_video(youtube, video_path=video_path, metadata=metadata, privacy_status=privacy)
    video_id = upload_res["video_id"]
    print("  [SUCCESS] Video Uploaded!")
    print(f"  --> Video ID: {video_id}")
    print(f"  --> Watch URL: https://youtu.be/{video_id}")
    print(f"  --> Privacy Status: {upload_res['privacy_status']}")

    # Step 3: Upload Captions
    print(f"\n[STEP 3] Uploading English Subtitle Track (en.srt)...")
    try:
        caption_res = upload_caption(youtube, video_id=video_id, srt_path=srt_path, language="en", name="English (Default)")
        print(f"  [SUCCESS] Subtitle track attached! Caption ID: {caption_res['caption_id']}")
    except Exception as exc:
        print(f"  [WARNING] Caption upload encountered: {exc}")

    # Step 4: Upload Custom Thumbnail
    print(f"\n[STEP 4] Setting High-CTR Custom Thumbnail...")
    if os.path.exists(thumb_path):
        thumb_res = upload_thumbnail(youtube, video_id=video_id, thumbnail_path=thumb_path)
        if thumb_res.get("success"):
            print("  [SUCCESS] Custom thumbnail applied successfully!")
        else:
            print(f"  [NOTE] Custom thumbnail status: {thumb_res.get('error')}")

    # Step 5: Update State Machine
    print("\n[STEP 5] Updating State Database...")
    transition(episode_id, "published", note=f"Uploaded to YouTube (ID: {video_id})", db_path=db_path)
    print("  [OK] State transitioned to 'published'.")

    print("\n" + "=" * 85)
    print(f"EPISODE 2 YOUTUBE UPLOAD COMPLETE!")
    print(f"Title: {metadata['title']}")
    print(f"Watch URL: https://youtu.be/{video_id}")
    print(f"Hashtags: #EarthHistory #PlateTectonics #Geology #ScienceDocumentary #Pangaea")
    print("=" * 85)


if __name__ == "__main__":
    main()
