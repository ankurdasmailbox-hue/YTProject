"""
Automated Multi-Platform Social Media Publishing Pipeline for History of Earth.
Generates and posts optimized content packages (Reels & Long-form Videos)
for Episodes 1 through 5 to Facebook Page and Instagram.

Target Channels:
- Facebook Page: History of Earth (ID: 61595168183529)
- Instagram: @earthhistoryanimated (https://www.instagram.com/earthhistoryanimated/)

Implements the 2026 Meta Algorithm Growth Strategy:
- Theatrical 9:16 safe-zone vertical Reels (32-38s sweet spot)
- Hook-first curiosity captions engineered for high DM shares & saves
- Strategic 5-hashtag semantic SEO clusters
"""

import os
import sys
import json
import time
from typing import Dict, List, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.meta_publisher import MetaPublisher, DEFAULT_FB_PAGE_ID, DEFAULT_IG_USERNAME

# Configuration for the First 5 Episodes
EPISODE_SOCIAL_PACKAGES = [
    {
        "episode_id": "hadean_landscape_01",
        "era": "Hadean",
        "pillar": "Landscape",
        "working_title": "A World of Fire and Rain",
        "youtube_url": "https://youtu.be/JkW7JcWnEzg",
        "reel_short_id": "short_01_theia_collision",
        "fb_copy": {
            "title": "When a Mars-Sized Planet Smashed into Earth at 25,000 MPH 💥🌍",
            "caption": (
                "4.5 billion years ago, Earth did not have solid ground. It was an incandescent ocean of boiling magma.\n\n"
                "Then, an ancient protoplanet named Theia collided with the infant Earth at 25,000 miles per hour, "
                "vaporizing billions of tons of rock into orbit to forge our Moon. Here is what that planetary cataclysm actually looked like.\n\n"
                "🎬 Watch the full documentary on our YouTube channel: History of Earth.\n\n"
                "💬 What would you do if you could witness this from orbit for 60 seconds? Drop your thoughts below! 👇\n\n"
                "#EarthHistory #PlanetaryScience #SpaceDocumentary #Astronomy #Catastrophe #Geology"
            )
        },
        "ig_copy": {
            "title": "When a Planet Hit Earth at 25,000 MPH",
            "caption": (
                "When a planet hit Earth at 25,000 MPH... 💥🪐\n\n"
                "4.5 billion years ago, our infant planet collided with Theia—a Mars-sized protoplanet. "
                "The kinetic energy liquefied the entire planetary crust, creating a 1,000-kilometer-deep magma ocean "
                "and ejecting the debris that condensed into our Moon.\n\n"
                "📌 Save this reel for your astronomy & deep-time science notes!\n"
                "🚀 Share this with someone who loves planetary physics!\n\n"
                "Full investigation on our channel: History of Earth (Link in bio)\n\n"
                "#EarthHistory #PlanetaryScience #SpaceFacts #Astronomy #AncientEarth #ScienceReels #DeepTime"
            )
        }
    },
    {
        "episode_id": "hadean_map_02",
        "era": "Hadean",
        "pillar": "Map",
        "working_title": "The Planet With No Plates",
        "youtube_url": "https://youtu.be/Jkw7JcWnEzg",
        "reel_short_id": "short_01_stagnant_lid",
        "fb_copy": {
            "title": "Earth Had No Tectonic Plates For 500 Million Years — How Did It Survive? 🌋",
            "caption": (
                "Look at the ground beneath your feet. 4.4 billion years ago, it did not exist.\n\n"
                "Before continents wandered the globe, Earth was trapped in a single, unbroken rocky shell called the 'stagnant lid'. "
                "Without plate tectonics to vent heat, internal mantle temperatures surged, creating colossal volcanic 'heat pipes' "
                "that flooded the surface with boiling basalt.\n\n"
                "🎬 Watch the full deep-time investigation on YouTube: History of Earth.\n\n"
                "💬 Do you think continents were necessary for life to evolve? Let's discuss in the comments! 👇\n\n"
                "#EarthHistory #PlateTectonics #GeologyDocumentary #DeepTime #Science #Volcanoes"
            )
        },
        "ig_copy": {
            "title": "Earth Had No Tectonic Plates For 500M Years",
            "caption": (
                "Earth was trapped in a single rocky prison for 500 million years... 🌋🔒\n\n"
                "Before Pangaea or any continents existed, Earth had zero plate tectonics. "
                "Our planet was locked inside an unbroken 'stagnant lid'. Massive volcanic chimneys were the only way "
                "the interior could cool down, until gravity caused the first slab rollback and ignited Earth's very first subduction zone.\n\n"
                "📌 Save this reel to explore planetary geology!\n"
                "🚀 Share with a geology lover!\n\n"
                "Full video on our channel: History of Earth (Link in bio)\n\n"
                "#EarthHistory #PlateTectonics #Geology #AncientEarth #ScienceFacts #DeepTime #PlanetEarth"
            )
        }
    },
    {
        "episode_id": "hadean_air_ocean_03",
        "era": "Hadean",
        "pillar": "Air & Ocean",
        "working_title": "The Sky Was Poison and the Rain Never Stopped",
        "youtube_url": "https://youtu.be/d_Xeu3MUHzM",
        "reel_short_id": "short_01_green_ocean",
        "fb_copy": {
            "title": "Why Earth's First Ocean Was Emerald Green, Not Blue 🌊🧪",
            "caption": (
                "Forget blue oceans and white fluffy clouds. 4.4 billion years ago, Earth looked like an alien world.\n\n"
                "Our atmosphere was a crushing 200-atmosphere pressure cooker of toxic steam, sulfur, and carbon dioxide. "
                "When the planet finally cooled below 374°C, it triggered centuries of continuous boiling downpours—filling "
                "an ocean so saturated with dissolved ferrous iron that the entire sea turned a vivid emerald green.\n\n"
                "🎬 Watch the full documentary on YouTube: History of Earth.\n\n"
                "💬 Could you survive the crushing 200-atmosphere poison sky? Tell us below! 👇\n\n"
                "#EarthHistory #GreenOcean #PlanetaryScience #AncientEarth #Geology #Oceanography"
            )
        },
        "ig_copy": {
            "title": "Why Earth's First Ocean Was Green",
            "caption": (
                "Earth’s first ocean wasn't blue... it was emerald green! 🌊🧪\n\n"
                "Under a 200-atmosphere toxic steam sky, ancient rain fell for centuries onto boiling basalt. "
                "With zero free oxygen in the atmosphere, billions of tons of dissolved iron stayed dissolved in seawater, "
                "turning the global Hadean ocean emerald green.\n\n"
                "📌 Save this reel for deep-time oceanography facts!\n"
                "🚀 Send to a friend who loves science mysteries!\n\n"
                "Full documentary on our channel: History of Earth (Link in bio)\n\n"
                "#EarthHistory #Ocean #Geology #PlanetaryScience #AncientEarth #DeepTime #ScienceReels"
            )
        }
    },
    {
        "episode_id": "hadean_life_then_04",
        "era": "Hadean",
        "pillar": "Life Then",
        "working_title": "The Planet Before Life — Genesis in the Abyss",
        "youtube_url": "https://youtu.be/8KNT1FjIsoY",
        "reel_short_id": "short_01_dead_rocks_code",
        "fb_copy": {
            "title": "How Dead Rocks Learned to Code: The 4.2-Billion-Year Genesis 🧬⚡",
            "caption": (
                "Life did not start in a warm sunlit pond. It started 4,000 meters beneath a pitch-black boiling ocean.\n\n"
                "Inside porous alkaline hydrothermal chimneys, ancient rocks created natural 200-millivolt proton batteries. "
                "Microscopic mineral honeycomb pores concentrated organic molecules, catalyzing the miracle where chemistry "
                "became biology—and LUCA, the single ancestor of all living creatures, was born.\n\n"
                "🎬 Watch the complete investigation on YouTube: History of Earth.\n\n"
                "💬 What fascinates you most about the origin of life? Share your perspective below! 👇\n\n"
                "#OriginOfLife #LUCA #Astrobiology #Biology #DeepSea #Evolution #EarthHistory"
            )
        },
        "ig_copy": {
            "title": "When Dead Rocks Learned to Code",
            "caption": (
                "When dead rocks learned to code... 🧬⚡\n\n"
                "4.2 billion years ago in the deep sea abyss, alkaline hydrothermal chimneys acted as Earth's first natural batteries. "
                "The 200mV proton gradient between vent fluids and seawater drove the synthesis of the first RNA molecules, "
                "turning inorganic minerals into living cells.\n\n"
                "📌 Save this reel for biology and origin of life notes!\n"
                "🚀 Share with a science enthusiast!\n\n"
                "Watch the full story on our channel: History of Earth (Link in bio)\n\n"
                "#OriginOfLife #Biology #Evolution #Astrobiology #EarthHistory #ScienceFacts #DeepTime"
            )
        }
    },
    {
        "episode_id": "hadean_leap_05",
        "era": "Hadean",
        "pillar": "Leap",
        "working_title": "When Rocks Learned to Cool — The Zircon Code",
        "youtube_url": "https://youtu.be/am-lPM1EUgw",
        "reel_short_id": "short_01_oldest_rock_earth",
        "fb_copy": {
            "title": "The 4.4-Billion-Year-Old Rock That Broke Geology 💎🔍",
            "caption": (
                "Over 99.9% of Earth's earliest crust was completely destroyed. Only one witness survived.\n\n"
                "In the red dirt of Western Australia's Jack Hills, geologists discovered microscopic zircon crystals "
                "dating to 4.404 billion years ago. Trapped inside their atomic lattices were oxygen isotopes and titanium atoms "
                "proving that cool liquid water and granitic proto-continents existed hundreds of millions of years earlier than textbooks claimed.\n\n"
                "🎬 Watch the full forensic investigation on YouTube: History of Earth.\n\n"
                "💬 Imagine holding a crystal older than our continents. What does that feel like? Tell us below! 👇\n\n"
                "#EarthHistory #Zircon #OldestRock #Geology #DeepTime #ScienceDocumentary #Australia"
            )
        },
        "ig_copy": {
            "title": "The 4.4B-Year-Old Rock That Broke Geology",
            "caption": (
                "The 4.4-billion-year-old rock that broke modern geology... 💎✨\n\n"
                "Hidden in Western Australia's Jack Hills, microscopic zircon grain W74/2-36 is the oldest surviving piece of Earth ever found. "
                "Its chemical code revealed something impossible: Earth had cool liquid oceans and continents just 160 million years after forming!\n\n"
                "📌 Save this reel for fascinating geology trivia!\n"
                "🚀 Share with a curious mind!\n\n"
                "Full documentary on our channel: History of Earth (Link in bio)\n\n"
                "#Geology #AncientEarth #Zircon #EarthHistory #ScienceReels #DeepTime #PlanetaryScience"
            )
        }
    }
]


def execute_social_batch_publishing() -> Dict[str, Any]:
    """
    Orchestrates automated social posting for Episodes 1 through 5.
    Dispatches to Facebook Page and Instagram Account.
    """
    meta = MetaPublisher(env_file=os.path.join(PROJECT_ROOT, ".env"))
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "facebook_page_id": DEFAULT_FB_PAGE_ID,
        "instagram_username": DEFAULT_IG_USERNAME,
        "posts": []
    }

    print("\n" + "=" * 80)
    print("HISTORY OF EARTH — MULTI-PLATFORM SOCIAL DISPATCH ENGINE")
    print(f"Target FB Page:  https://www.facebook.com/profile.php?id={DEFAULT_FB_PAGE_ID}")
    print(f"Target IG:       https://www.instagram.com/{DEFAULT_IG_USERNAME}/")
    print("=" * 80)

    for item in EPISODE_SOCIAL_PACKAGES:
        ep_id = item["episode_id"]
        ep_dir = os.path.join(PROJECT_ROOT, "output", ep_id)
        master_mp4 = os.path.join(ep_dir, "final_episode.mp4")
        reel_mp4 = os.path.join(ep_dir, "shorts", f"{item['reel_short_id']}.mp4")

        # Fallback to any available short if specific ID not found
        if not os.path.exists(reel_mp4) and os.path.exists(os.path.join(ep_dir, "shorts")):
            shorts_dir = os.path.join(ep_dir, "shorts")
            for sf in os.listdir(shorts_dir):
                if sf.endswith(".mp4"):
                    reel_mp4 = os.path.join(shorts_dir, sf)
                    break

        video_for_reel = reel_mp4 if os.path.exists(reel_mp4) else master_mp4

        print(f"\n--> Processing [{ep_id}] : {item['working_title']}")
        print(f"    Target Reel Video: {os.path.basename(video_for_reel)} ({'EXISTS' if os.path.exists(video_for_reel) else 'MISSING'})")

        # 1. Publish / Register to Facebook Page
        fb_res = meta.publish_facebook_video(
            video_path=video_for_reel,
            title=item["fb_copy"]["title"],
            description=item["fb_copy"]["caption"],
            is_reel=True
        )

        # 2. Publish / Register to Instagram
        ig_res = meta.publish_instagram_reel(
            video_url_or_path=video_for_reel,
            caption=item["ig_copy"]["caption"]
        )

        post_record = {
            "episode_id": ep_id,
            "title": item["working_title"],
            "video_file": os.path.basename(video_for_reel),
            "facebook_dispatch": fb_res,
            "instagram_dispatch": ig_res,
            "fb_caption": item["fb_copy"]["caption"],
            "ig_caption": item["ig_copy"]["caption"],
            "youtube_ref": item["youtube_url"]
        }
        results["posts"].append(post_record)

        print(f"    FB Status: {fb_res.get('status')} | IG Status: {ig_res.get('status')}")

    # Persist publishing log
    log_path = os.path.join(PROJECT_ROOT, "output", "social_publishing_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("SOCIAL DISPATCH COMPLETED FOR ALL 5 EPISODES")
    print(f"Published audit report saved to: {log_path}")
    print("=" * 80 + "\n")

    return results


if __name__ == "__main__":
    execute_social_batch_publishing()
