"""
Tri-Platform Packaging Engine for History of Earth.
Simultaneously generates optimized content packages for:
1. YouTube (1080p Master + soft SRT + 3 A/B titles + high-RPM tags + chapters)
2. Facebook (16:9 Page Video + 9:16 Reel copy + comment debate question)
3. Instagram (9:16 Reel hook + micro-blog caption + DM share/save triggers + 5 semantic tags)

Adheres strictly to the 2026 platform specifications and growth strategies.
"""

import os
import json
from typing import Dict, List, Any, Optional


def generate_tri_platform_package(
    episode_id: str,
    era: str,
    pillar: str,
    working_title: str,
    hook: str,
    approved_claims: List[Dict[str, Any]],
    shot_list: List[Dict[str, Any]],
    output_dir: str
) -> Dict[str, Any]:
    """Generates and persists the complete 3-platform packaging bundle."""
    os.makedirs(output_dir, exist_ok=True)
    norm_pillar = pillar.strip().lower()

    # ---------------------------------------------------------
    # 1. YOUTUBE SPECIFICATIONS & PACKAGING
    # ---------------------------------------------------------
    yt_titles = [
        f"{working_title} — The Untold Story of {era}",
        f"When Earth Changed Forever: Inside the {era} {pillar}",
        f"What Science Got Wrong About the {era}: {working_title}"
    ]

    yt_description_lines = [
        f"{hook}. Discover the untold scientific story of how our planet survived its most violent dawn.",
        "",
        f"From the extreme geological forces of the {era} to the shaping of modern Earth, explore the peer-reviewed forensic investigation into {working_title.lower()}.",
        "",
        "#EarthHistory #PlanetaryScience #DeepTime #GeologyDocumentary #Science #Trending #LearnOnYouTube #ScienceFacts",
        "",
        "--- VERIFIED SCIENTIFIC SOURCES & CITATIONS ---"
    ]
    for idx, claim in enumerate(approved_claims, 1):
        src = claim.get("source_url") or claim.get("citation", "Peer-Reviewed Academic Consensus")
        yt_description_lines.append(f"• Fact {idx}: {claim['text']}")
        yt_description_lines.append(f"  Source: {src}")

    yt_description_lines.append("")
    yt_description_lines.append("--- TIMESTAMPS & CHAPTERS ---")
    chapters = []
    for shot in shot_list:
        ts = shot.get("timestamp_start", "00:00")
        title = shot.get("scene_title") or shot.get("segment_type", "Scene").replace("_", " ").title()
        yt_description_lines.append(f"{ts} - {title}")
        chapters.append({"time": ts, "title": title})

    youtube_pkg = {
        "platform": "youtube",
        "primary_title": yt_titles[0],
        "ab_titles": yt_titles,
        "description": "\n".join(yt_description_lines),
        "tags": [
            "earth history documentary",
            "planetary science",
            "deep time geology",
            "ancient earth",
            "geology documentary",
            f"{era.lower()} eon",
            f"{norm_pillar} documentary",
            "history of earth",
            "science documentary",
            "trending science",
            "learn on youtube",
            "science facts"
        ],
        "hashtags": [
            "#EarthHistory",
            "#PlanetaryScience",
            "#DeepTime",
            "#GeologyDocumentary",
            "#Science",
            "#Trending",
            "#LearnOnYouTube",
            "#ScienceFacts"
        ],
        "category_id": "27",
        "aspect_ratio": "16:9 (1920x1080 / 2560x1440 QHD)",
        "captions": "en.srt (Soft Captions Delivery)"
    }

    # ---------------------------------------------------------
    # 2. FACEBOOK SPECIFICATIONS & PACKAGING
    # ---------------------------------------------------------
    fb_debate_questions = {
        "landscape": "What would you do if you could witness this geological inferno from orbit for 60 seconds? Tell us below! 👇",
        "map": "Do you think continental landmasses were required for intelligent life to evolve? Let's discuss! 👇",
        "air": "Could modern humans survive under a 200-atmosphere poison sky with zero oxygen? Drop your thoughts! 👇",
        "ocean": "Would you explore an emerald green iron ocean? Tell us your thoughts below! 👇",
        "life": "What is the most mind-bending fact about the origin of life to you? Share your perspective! 👇",
        "leap": "Imagine holding a crystal older than Earth's continents. What does that feel like? Drop your reaction! 👇",
        "ending": "Could humanity survive a planetary asteroid bombardment of this scale? Let's discuss in the comments! 👇"
    }
    debate_q = next((q for k, q in fb_debate_questions.items() if k in norm_pillar), "What fascinates you most about this deep-time discovery? Tell us below! 👇")

    fb_hashtags = [
        "#EarthHistory",
        "#PlanetaryScience",
        "#GeologyDocumentary",
        "#Trending",
        "#ViralReels",
        "#DidYouKnow",
        f"#{era.replace(' ', '')}"
    ]

    fb_caption = (
        f"{hook} 🌍\n\n"
        f"During the {era}, Earth underwent one of the most violent transformations in planetary history: {working_title}.\n\n"
        f"🎬 Watch the full 10-minute deep-time investigation on our YouTube channel: History of Earth.\n\n"
        f"💬 {debate_q}\n\n"
        f"{' '.join(fb_hashtags)}"
    )

    facebook_pkg = {
        "platform": "facebook",
        "page_id": "1279963101878153",
        "page_name": "Earth History Animated",
        "video_title": f"{working_title} — {era} Documentary 💥🌍",
        "post_caption": fb_caption,
        "reel_title": working_title,
        "aspect_ratios": ["16:9 for Page Video (>3:01m)", "9:16 for Facebook Reels (32-38s)"],
        "monetization_gate": "In-Stream Ads (>3:01m) + Performance Bonus",
        "hashtags": fb_hashtags
    }

    # ---------------------------------------------------------
    # 3. INSTAGRAM SPECIFICATIONS & PACKAGING
    # ---------------------------------------------------------
    ig_hashtags = [
        "#EarthHistory",
        "#PlanetaryScience",
        "#DeepTime",
        "#TrendingReels",
        "#ScienceFacts",
        "#ExplorePage",
        "#DidYouKnow"
    ]

    ig_caption = (
        f"{hook}... 🪐✨\n\n"
        f"During the {era}, our planet looked completely alien compared to today. {working_title} changed the course of planetary evolution forever.\n\n"
        f"📌 Save this reel for your deep-time science notes!\n"
        f"🚀 Send this to a friend who loves planetary science & space mysteries!\n\n"
        f"Full documentary on our channel: History of Earth (Link in bio)\n\n"
        f"{' '.join(ig_hashtags)}"
    )

    instagram_pkg = {
        "platform": "instagram",
        "username": "earthhistoryanimated",
        "account_id": "17841425908563266",
        "reel_title": working_title,
        "caption": ig_caption,
        "aspect_ratio": "9:16 Vertical (1080x1920)",
        "duration_sweet_spot": "32 – 38 seconds",
        "ranking_levers": ["DM Shares Multiplier", "Save for Later", "Seamless Audio Loop (>100% completion)"],
        "hashtags": ig_hashtags
    }

    # Consolidated Package
    tri_package = {
        "episode_id": episode_id,
        "era": era,
        "pillar": pillar,
        "working_title": working_title,
        "youtube": youtube_pkg,
        "facebook": facebook_pkg,
        "instagram": instagram_pkg
    }

    pkg_path = os.path.join(output_dir, "tri_platform_package.json")
    with open(pkg_path, "w", encoding="utf-8") as f:
        json.dump(tri_package, f, indent=2)

    return tri_package


if __name__ == "__main__":
    sample = generate_tri_platform_package(
        episode_id="hadean_ending_06",
        era="Hadean",
        pillar="Ending",
        working_title="The Bombardment That Almost Reset the Clock",
        hook="A storm of mountain-sized asteroids hammered the infant Earth - did it sterilize the crust or spark biology?",
        approved_claims=[{"text": "Late Heavy Bombardment cratering records.", "source_url": "https://nature.com"}],
        shot_list=[{"timestamp_start": "00:00", "scene_title": "THE FINAL CATACLYSM"}],
        output_dir="."
    )
    print("Generated Tri-Platform Package:", json.dumps(sample, indent=2))
