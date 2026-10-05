"""
Simultaneous Tri-Platform Publisher for Episode 7:
"The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss"

Publishes simultaneously across all 3 platforms:
1. YouTube (Master 1080p Video + Soft SRT + Thumbnail + 2 Vertical Shorts)
   - Outro CTA cross-promotes Facebook Page & Instagram.
2. Facebook Page (Earth History Animated, ID: 1279963101878153)
   - Full 16:9 Video (>3:01m for In-Stream ads) + Vertical Reel.
   - Outro CTA asks viewer to like, comment, follow and subscribe to YouTube channel.
3. Instagram (@earthhistoryanimated, ID: 17841425908563266)
   - 9:16 Vertical Reel + Multi-Part feed versions.
   - Outro CTA asks viewer to like, comment, follow and subscribe to YouTube channel.
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
    upload_thumbnail
)
from agents.meta_publisher import MetaPublisher
from pipeline.state_machine import transition


def main():
    print("=" * 85)
    print("SIMULTANEOUS TRI-PLATFORM PUBLISHING: EPISODE 7")
    print("Title: 'The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss'")
    print("Target Platforms: [1] YouTube  [2] Facebook Page  [3] Instagram Reels")
    print("=" * 85)

    episode_id = "archean_landscape_07"
    episode_dir = os.path.join(PROJECT_ROOT, "output", episode_id)
    video_path = os.path.join(episode_dir, "final_episode.mp4")
    fb_video_path = os.path.join(episode_dir, "facebook_full_episode.mp4")
    part1_path = os.path.join(episode_dir, "part_01_the_vanished_crust.mp4")
    part2_path = os.path.join(episode_dir, "part_02_the_4_billion_year_secret.mp4")
    srt_path = os.path.join(episode_dir, "en.srt")
    thumb_path = os.path.join(episode_dir, f"{episode_id}_thumb_candidate_a.png")
    tri_pkg_path = os.path.join(episode_dir, "tri_platform_package.json")
    shorts_dir = os.path.join(episode_dir, "shorts")
    shorts_meta_file = os.path.join(shorts_dir, "shorts_metadata.json")

    client_secrets = os.path.join(PROJECT_ROOT, "client_secret.json")
    token_file = os.path.join(PROJECT_ROOT, "token.json")
    env_file = os.path.join(PROJECT_ROOT, ".env")
    db_path = os.path.join(PROJECT_ROOT, "state.db")

    if not os.path.exists(tri_pkg_path):
        print(f"[ERROR] '{tri_pkg_path}' not found. Run build_episode7.py first.")
        sys.exit(1)

    with open(tri_pkg_path, "r", encoding="utf-8") as f:
        tri_pkg = json.load(f)

    yt_spec = tri_pkg.get("youtube", {})
    fb_spec = tri_pkg.get("facebook", {})
    ig_spec = tri_pkg.get("instagram", {})

    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "episode_id": episode_id,
        "youtube": {},
        "facebook": {},
        "instagram": {}
    }

    # =========================================================================
    # 1. YOUTUBE PUBLISHING (Master Long-Form + Soft Captions + Shorts)
    # =========================================================================
    print("\n" + "-" * 75)
    print("[PLATFORM 1/3: YOUTUBE MASTER & SHORTS]")
    print("-" * 75)

    yt_service = None
    try:
        yt_service = get_authenticated_service(client_secrets_file=client_secrets, token_file=token_file)
        print("  [OK] Authenticated with YouTube Data API v3.")
    except Exception as e:
        print(f"  [ERROR] YouTube Auth failed: {e}")

    if yt_service:
        yt_metadata = {
            "title": yt_spec.get("primary_title", "The 4-Billion-Year-Old Rock That Broke Geology — The Acasta Gneiss"),
            "description": yt_spec.get("description", "Deep time planetary science investigation."),
            "tags": yt_spec.get("tags", []),
            "categoryId": yt_spec.get("category_id", "27")
        }

        print(f"  --> Uploading Master Video ({yt_metadata['title']}) as PUBLIC...")
        yt_upload = upload_video(yt_service, video_path=video_path, metadata=yt_metadata, privacy_status="public")
        yt_vid_id = yt_upload["video_id"]
        yt_url = f"https://youtu.be/{yt_vid_id}"
        print(f"      [SUCCESS] Master Video Uploaded! ID: {yt_vid_id}")
        print(f"      [WATCH URL] {yt_url}")

        results["youtube"]["master_video_id"] = yt_vid_id
        results["youtube"]["master_url"] = yt_url

        # Soft Captions
        if os.path.exists(srt_path):
            try:
                cap_res = upload_caption(yt_service, video_id=yt_vid_id, srt_path=srt_path, language="en", name="English (Default)")
                print(f"      [SUCCESS] Soft captions attached! Caption ID: {cap_res.get('caption_id')}")
                results["youtube"]["caption_id"] = cap_res.get("caption_id")
            except Exception as e:
                print(f"      [WARNING] Caption upload notice: {e}")

        # Custom Thumbnail
        if os.path.exists(thumb_path):
            try:
                th_res = upload_thumbnail(yt_service, video_id=yt_vid_id, thumbnail_path=thumb_path)
                if th_res.get("success"):
                    print("      [SUCCESS] High-CTR Custom Thumbnail Candidate A applied!")
                    results["youtube"]["thumbnail_applied"] = True
            except Exception as e:
                print(f"      [WARNING] Thumbnail upload notice: {e}")

        # Vertical Shorts Upload
        published_shorts = []
        if os.path.exists(shorts_meta_file):
            with open(shorts_meta_file, "r", encoding="utf-8") as f:
                shorts_list = json.load(f)

            for s_idx, s in enumerate(shorts_list, 1):
                short_path = s["file_path"]
                if not os.path.exists(short_path):
                    continue

                s_meta = {
                    "title": s["title"],
                    "description": s["description"],
                    "tags": s["tags"],
                    "categoryId": "28"
                }
                print(f"  --> Uploading Short {s_idx}/{len(shorts_list)}: '{s['title']}'...")
                try:
                    s_up = upload_video(yt_service, video_path=short_path, metadata=s_meta, privacy_status="public")
                    s_id = s_up["video_id"]
                    s_link = f"https://youtube.com/shorts/{s_id}"
                    print(f"      [SUCCESS] Short Uploaded! ID: {s_id}")
                    print(f"      [WATCH URL] {s_link}")
                    published_shorts.append({"title": s["title"], "id": s_id, "url": s_link})
                except Exception as e:
                    print(f"      [WARNING] Error uploading Short {s_idx}: {e}")

        results["youtube"]["shorts"] = published_shorts

    # =========================================================================
    # 2. FACEBOOK PAGE PUBLISHING (Full 16:9 Video + Vertical Reel + Multi-Part)
    # =========================================================================
    print("\n" + "-" * 75)
    print("[PLATFORM 2/3: FACEBOOK PAGE VIDEO & REEL]")
    print("-" * 75)

    meta_pub = MetaPublisher(env_file=env_file)
    fb_title = fb_spec.get("video_title", "The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss")
    fb_caption = fb_spec.get("post_caption", "Deep time investigation.")

    # 2A. Full 16:9 Video (>3:01m)
    target_fb_video = fb_video_path if os.path.exists(fb_video_path) else video_path
    print(f"  --> Publishing Full Video to Facebook Page ID {meta_pub.fb_page_id}...")
    fb_res = meta_pub.publish_facebook_video(
        video_path=target_fb_video,
        title=fb_title,
        description=fb_caption,
        is_reel=False
    )
    print(f"      FB Full Video Status: {fb_res.get('status')}")
    if fb_res.get("video_id"):
        print(f"      [SUCCESS] Facebook Video ID: {fb_res.get('video_id')}")
        print(f"      [POST URL] https://www.facebook.com/{fb_res.get('video_id')}")
    results["facebook"]["full_video"] = fb_res

    # 2B. Facebook Reel (9:16 Vertical Short 1)
    target_fb_reel = os.path.join(shorts_dir, "short_01_oldest_intact_rock.mp4")
    if os.path.exists(target_fb_reel):
        print(f"  --> Publishing 9:16 Reel to Facebook Page...")
        fb_reel_res = meta_pub.publish_facebook_video(
            video_path=target_fb_reel,
            title="The Oldest Rock on Earth Is 4.03 Billion Years Old",
            description=fb_caption,
            is_reel=True
        )
        print(f"      FB Reel Status: {fb_reel_res.get('status')}")
        results["facebook"]["reel"] = fb_reel_res

    # =========================================================================
    # 3. INSTAGRAM REELS & MULTI-PART PUBLISHING
    # =========================================================================
    print("\n" + "-" * 75)
    print("[PLATFORM 3/3: INSTAGRAM REELS & MULTI-PART]")
    print("-" * 75)

    target_ig_reel = os.path.join(shorts_dir, "short_01_oldest_intact_rock.mp4")
    ig_caption = ig_spec.get("caption", "The 4.03-Billion-Year-Old Acasta Gneiss #EarthHistory #Science")
    print(f"  --> Publishing 9:16 Vertical Reel to @{meta_pub.ig_username}...")
    print(f"      Video Source: {os.path.basename(target_ig_reel)}")

    ig_res = meta_pub.publish_instagram_reel(
        video_url_or_path=target_ig_reel,
        caption=ig_caption
    )
    print(f"      IG Status: {ig_res.get('status')}")
    if ig_res.get("media_id"):
        print(f"      [SUCCESS] Instagram Media ID: {ig_res.get('media_id')}")
    results["instagram"]["reel"] = ig_res

    # Multi-Part cuts check
    if os.path.exists(part1_path):
        print(f"  --> Multi-Part cuts ready for episodic feed / carousel posts:")
        print(f"      - Part 1: {os.path.basename(part1_path)} ({(os.path.getsize(part1_path)/(1024*1024)):.1f} MB)")
        print(f"      - Part 2: {os.path.basename(part2_path)} ({(os.path.getsize(part2_path)/(1024*1024)):.1f} MB)")
        results["instagram"]["multi_part_ready"] = True

    # =========================================================================
    # 4. AUDIT & LOGGING
    # =========================================================================
    log_path = os.path.join(PROJECT_ROOT, "output", "social_publishing_log.json")
    existing_log = {"posts": []}
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as lf:
                existing_log = json.load(lf)
        except Exception:
            pass

    existing_log["posts"].append(results)
    with open(log_path, "w", encoding="utf-8") as lf:
        json.dump(existing_log, lf, indent=2)

    transition(episode_id, "published", note=f"Simultaneously published across YouTube, Facebook, and Instagram", db_path=db_path)

    # Update Gate B dashboard with live links
    gate_b_file = os.path.join(PROJECT_ROOT, "review", "gate_b_review_ep7.html")
    if os.path.exists(gate_b_file):
        with open(gate_b_file, "r", encoding="utf-8") as f:
            html = f.read()

        yt_link_str = f'<a href="{results["youtube"].get("master_url", "#")}" target="_blank" style="color: #38bdf8; font-weight: bold;">YouTube Live &rarr;</a>'
        fb_id = results["facebook"].get("full_video", {}).get("video_id", "")
        fb_link_str = f'<a href="https://www.facebook.com/{fb_id}" target="_blank" style="color: #1877f2; font-weight: bold;">Facebook Live &rarr;</a>' if fb_id else '<span style="color: #64748b;">Facebook Simulated</span>'
        ig_link_str = f'<a href="https://www.instagram.com/{meta_pub.ig_username}/" target="_blank" style="color: #ec4899; font-weight: bold;">Instagram Live &rarr;</a>'

        status_old = '<span class="badge badge-green">Status: ASSEMBLED & COMPLIANT</span>'
        status_new = f'<span class="badge badge-green">Status: PUBLISHED ACROSS ALL 3 PLATFORMS</span> | {yt_link_str} | {fb_link_str} | {ig_link_str}'
        html = html.replace(status_old, status_new)

        with open(gate_b_file, "w", encoding="utf-8") as f:
            f.write(html)
        print("  [OK] Updated Gate B review dashboard with live multi-platform links.")

    print("\n" + "=" * 85)
    print("TRI-PLATFORM PUBLISHING COMPLETED FOR EPISODE 7!")
    if results["youtube"].get("master_url"):
        print(f"[YOUTUBE]   {results['youtube']['master_url']}")
    if fb_id:
        print(f"[FACEBOOK]  https://www.facebook.com/{fb_id}")
    print(f"[INSTAGRAM] @{meta_pub.ig_username}")
    print("=" * 85)

    return results


if __name__ == "__main__":
    main()
