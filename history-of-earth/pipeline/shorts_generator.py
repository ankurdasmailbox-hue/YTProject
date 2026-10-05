"""
Automated YouTube Shorts Funnel Generator for History of Earth.
Transforms 16:9 cinematic master footage into viral 9:16 vertical (1080x1920) Shorts.
Implements the high-velocity Shorts-to-Long-Form growth flywheel:
1. Dynamic 9:16 canvas: Ambient blurred background + crisp centered hero cut.
2. Theatrical top banner & persistent high-contrast branding.
3. Bottom CTA: 'Full Story in Linked Video' (drives long-form watch-hours for YPP).
4. Auto-generates Shorts metadata with viral tags (#Shorts #EarthHistory #Space).
100% Zero-Subscription, Local CPU FFmpeg.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Any, Optional

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"


SHORTS_PRESETS_HADEAN_01 = [
    {
        "short_id": "short_01_theia_collision",
        "title": "When a Planet Hit Earth at 25,000 MPH",
        "banner_text": "WHEN A PLANET HIT EARTH",
        "sub_banner": "4.5 BILLION YEARS AGO",
        "start_time_sec": 0,
        "duration_sec": 38,
        "cta_text": "WATCH FULL DOCUMENTARY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#LearnOnYouTube", "#EarthHistory", "#PlanetaryScience", "#ScienceFacts"]
    },
    {
        "short_id": "short_02_zircon_paradox",
        "title": "The 4.4 Billion Year Old Impossible Witness",
        "banner_text": "THE IMPOSSIBLE 4.4B YEAR CLUE",
        "sub_banner": "SCIENCE WAS WRONG ABOUT EARTH",
        "start_time_sec": 119,
        "duration_sec": 35,
        "cta_text": "FULL INVESTIGATION IN LINKED VIDEO",
        "hashtags": ["#Shorts", "#Trending", "#ScienceFacts", "#Geology", "#AncientEarth", "#DidYouKnow"]
    }
]

SHORTS_PRESETS_HADEAN_02 = [
    {
        "short_id": "short_01_stagnant_lid",
        "title": "Earth Had No Tectonic Plates For 500 Million Years",
        "banner_text": "EARTH HAD NO TECTONIC PLATES",
        "sub_banner": "THE 500M YEAR STAGNANT LID",
        "start_time_sec": 0,
        "duration_sec": 38,
        "cta_text": "WATCH FULL DOCUMENTARY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#LearnOnYouTube", "#PlateTectonics", "#Geology", "#EarthHistory"]
    },
    {
        "short_id": "short_02_heat_pipe_earth",
        "title": "How Volcanic Heat Pipes Cooled Infant Earth",
        "banner_text": "THE HEAT-PIPE FURNACE",
        "sub_banner": "BEFORE CONTINENTS EXISTED",
        "start_time_sec": 51,
        "duration_sec": 35,
        "cta_text": "FULL INVESTIGATION ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#ScienceFacts", "#GeologyDocumentary", "#AncientEarth", "#DeepTime"]
    }
]

SHORTS_PRESETS_HADEAN_03 = [
    {
        "short_id": "short_01_green_ocean",
        "title": "Why Earth's First Ocean Was Emerald Green #Shorts",
        "banner_text": "EARTH'S FIRST OCEAN WAS GREEN",
        "sub_banner": "4.4 BILLION YEARS AGO",
        "start_time_sec": 145,
        "duration_sec": 38,
        "cta_text": "FULL DOCUMENTARY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#ScienceFacts", "#EarthHistory", "#Geology", "#DidYouKnow"]
    },
    {
        "short_id": "short_02_poison_atmosphere",
        "title": "The Crushing 200-Atmosphere Poison Sky #Shorts",
        "banner_text": "THE CRUSHING POISON SKY",
        "sub_banner": "SUPERCRITICAL STEAM VAULT",
        "start_time_sec": 0,
        "duration_sec": 35,
        "cta_text": "WATCH FULL STORY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#LearnOnYouTube", "#PlanetaryScience", "#Atmosphere", "#ScienceFacts"]
    }
]

SHORTS_PRESETS_HADEAN_04 = [
    {
        "short_id": "short_01_dead_rocks_code",
        "title": "When Dead Rocks Learned to Code",
        "banner_text": "HOW DEAD ROCKS LEARNED TO CODE",
        "sub_banner": "THE 4.2B YEAR HYDROTHERMAL GENESIS",
        "start_time_sec": 130,
        "duration_sec": 38,
        "cta_text": "WATCH FULL STORY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#OriginOfLife", "#Biology", "#Evolution", "#ScienceFacts"]
    },
    {
        "short_id": "short_02_natural_proton_battery",
        "title": "Life's First Battery Wasn't Biology",
        "banner_text": "LIFES FIRST BATTERY WAS ROCK",
        "sub_banner": "THE 200mV GEOCHEMICAL ENGINE",
        "start_time_sec": 90,
        "duration_sec": 36,
        "cta_text": "FULL INVESTIGATION ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#LearnOnYouTube", "#Biochemistry", "#EarthHistory", "#DidYouKnow"]
    }
]

SHORTS_PRESETS_HADEAN_05 = [
    {
        "short_id": "short_01_oldest_rock_earth",
        "title": "The 4.4B-Year-Old Rock That Broke Geology",
        "banner_text": "THE 4.4 BILLION YR OLD ROCK",
        "sub_banner": "THE ZIRCON CODE DISCOVERY",
        "start_time_sec": 140,
        "duration_sec": 38,
        "cta_text": "FULL DOCUMENTARY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#ScienceFacts", "#Geology", "#AncientEarth", "#Zircon"]
    },
    {
        "short_id": "short_02_cool_early_oceans",
        "title": "Textbooks Were Wrong About Earth's First Ocean",
        "banner_text": "OCEANS 4.4 BILLION YRS AGO",
        "sub_banner": "THE IMPOSSIBLE OXYGEN CLUE",
        "start_time_sec": 190,
        "duration_sec": 36,
        "cta_text": "WATCH FULL STORY ON CHANNEL",
        "hashtags": ["#Shorts", "#Trending", "#LearnOnYouTube", "#EarthHistory", "#Ocean", "#DidYouKnow"]
    }
]

SHORTS_PRESETS_HADEAN_06 = [
    {
        "short_id": "short_01_asteroid_storm",
        "title": "The Asteroid Storm That Almost Reset Earth",
        "banner_text": "THE ASTEROID STORM",
        "sub_banner": "3.9 BILLION YEARS AGO",
        "start_time_sec": 65,
        "duration_sec": 38,
        "cta_text": "FULL STORY ON HISTORY OF EARTH",
        "hashtags": [
            "#Shorts",
            "#EarthHistory",
            "#Space",
            "#Asteroid",
            "#PlanetaryScience",
            "#Astronomy",
            "#Science",
            "#Extinction",
            "#DeepTime",
            "#Cosmos"
        ]
    },
    {
        "short_id": "short_02_sterilization_paradox",
        "title": "Did Asteroids Sterilize Earth Or Spark Life?",
        "banner_text": "STERILIZE OR SPARK LIFE?",
        "sub_banner": "THE SUBTERRANEAN SANCTUARY",
        "start_time_sec": 125,
        "duration_sec": 36,
        "cta_text": "WATCH FULL STORY ON CHANNEL",
        "hashtags": [
            "#Shorts",
            "#OriginOfLife",
            "#Science",
            "#Geology",
            "#AncientEarth",
            "#Evolution",
            "#NASA",
            "#Astrobiology",
            "#Viral",
            "#ScienceFacts"
        ]
    }
]

SHORTS_PRESETS_ARCHEAN_07 = [
    {
        "short_id": "short_01_oldest_intact_rock",
        "title": "The Oldest Rock on Earth Is 4.03 Billion Years Old",
        "banner_text": "THE 4.03 BILLION YR OLD ROCK",
        "sub_banner": "THE CANADIAN SHIELD ACASTA GNEISS",
        "start_time_sec": 10,
        "duration_sec": 38,
        "cta_text": "SUBSCRIBE TO HISTORY OF EARTH ON YT",
        "hashtags": [
            "#Shorts",
            "#EarthHistory",
            "#Geology",
            "#AncientEarth",
            "#Science",
            "#Trending",
            "#LearnOnYouTube",
            "#DidYouKnow",
            "#Canada",
            "#ScienceFacts"
        ]
    },
    {
        "short_id": "short_02_iceland_protocontinents",
        "title": "How Earth's First Continent Formed Without Plates",
        "banner_text": "HOW FIRST CONTINENTS FORMED",
        "sub_banner": "BEFORE PLATE TECTONICS EXISTED",
        "start_time_sec": 185,
        "duration_sec": 36,
        "cta_text": "FOLLOW & SUBSCRIBE FOR FULL DOCS",
        "hashtags": [
            "#Shorts",
            "#Geology",
            "#PlanetaryScience",
            "#OriginOfEarth",
            "#ScienceFacts",
            "#Trending",
            "#LearnOnYouTube",
            "#ExplorePage",
            "#Evolution",
            "#DidYouKnow"
        ]
    }
]


def render_vertical_short(
    master_video_path: str,
    output_path: str,
    start_time_sec: float,
    duration_sec: float,
    banner_text: str = "HISTORY OF EARTH",
    sub_banner: str = "DEEP TIME INVESTIGATION",
    cta_text: str = "FULL VIDEO LINKED BELOW"
) -> bool:
    """
    Renders a 1080x1920 vertical Short from 16:9 master footage using CPU-optimized FFmpeg.
    Layout:
      - Top Banner (120px - 280px): High-contrast title and era indicator.
      - Center Stage (656px - 1264px): 1080x608 crisp cinematic 16:9 frame.
      - Background: Ambient blurred, motion-synchronized fill.
      - Conversion CTA (1320px - 1420px): Calibrated in the mobile UI safe-zone (above YouTube channel handle/title).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Clean text strings for FFmpeg drawtext
    clean_banner = banner_text.replace("'", "").replace(":", "-")
    clean_sub = sub_banner.replace("'", "").replace(":", "-")
    clean_cta = cta_text.replace("'", "").replace(":", "-")

    # FFmpeg complex filter chain for vertical mobile delivery
    filter_complex = (
        f"[0:v]setpts=PTS-STARTPTS[v0];"
        f"[0:a]asetpts=PTS-STARTPTS,loudnorm=I=-14.0:LRA=7.0:TP=-1.5[aout];"
        f"[v0]split=2[bg_raw][fg_raw];"
        f"[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=22:5[bg];"
        f"[fg_raw]scale=1080:608[fg];"
        f"[bg][fg]overlay=0:656[canvas];"
        # Top banner background bar
        f"[canvas]drawbox=x=0:y=120:w=1080:h=160:color=black@0.75:t=fill[b1];"
        # Top Header Text
        f"[b1]drawtext=text='{clean_banner}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=140:box=0,"
        f"drawtext=text='{clean_sub}':fontcolor=yellow:fontsize=32:x=(w-text_w)/2:y=210:box=0[b2];"
        # Calibrated Mobile Safe-Zone CTA (right below center stage, avoiding bottom YouTube overlays)
        f"[b2]drawbox=x=60:y=1320:w=960:h=100:color=red@0.88:t=fill,"
        f"drawtext=text='{clean_cta}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=1355:box=0[vout]"
    )

    cmd = [
        FFMPEG_EXE,
        "-y",
        "-ss", str(start_time_sec),
        "-t", str(duration_sec),
        "-i", master_video_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "17",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:a", "aac",
        "-b:a", "320k",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    print(f"[ShortsGenerator] Rendering {output_path} ({duration_sec}s)...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ShortsGenerator Error]:", res.stderr[-500:])
        return False
    return True


def generate_episode_shorts(
    episode_id: str,
    master_video_path: str,
    output_dir: str
) -> List[Dict[str, Any]]:
    """
    Extracts and compiles all planned Shorts from an episode's master video.
    Produces MP4s and shorts_metadata.json for immediate scheduling.
    """
    shorts_dir = os.path.join(output_dir, "shorts")
    os.makedirs(shorts_dir, exist_ok=True)

    results = []
    metadata_list = []

    if "07" in episode_id or "acasta" in episode_id or "gneiss" in episode_id:
        presets = SHORTS_PRESETS_ARCHEAN_07
    elif "06" in episode_id or "ending" in episode_id or "bombardment" in episode_id:
        presets = SHORTS_PRESETS_HADEAN_06
    elif "05" in episode_id or "leap" in episode_id or "zircon" in episode_id:
        presets = SHORTS_PRESETS_HADEAN_05
    elif "04" in episode_id or "life" in episode_id:
        presets = SHORTS_PRESETS_HADEAN_04
    elif "03" in episode_id or "air" in episode_id:
        presets = SHORTS_PRESETS_HADEAN_03
    elif "02" in episode_id or "map" in episode_id:
        presets = SHORTS_PRESETS_HADEAN_02
    else:
        presets = SHORTS_PRESETS_HADEAN_01

    for preset in presets:
        out_mp4 = os.path.join(shorts_dir, f"{preset['short_id']}.mp4")
        success = render_vertical_short(
            master_video_path=master_video_path,
            output_path=out_mp4,
            start_time_sec=preset["start_time_sec"],
            duration_sec=preset["duration_sec"],
            banner_text=preset["banner_text"],
            sub_banner=preset["sub_banner"],
            cta_text=preset["cta_text"]
        )

        if success and os.path.exists(out_mp4):
            size_mb = round(os.path.getsize(out_mp4) / (1024 * 1024), 2)
            meta = {
                "short_id": preset["short_id"],
                "file_path": out_mp4,
                "file_size_mb": size_mb,
                "title": f"{preset['title']} #Shorts",
                "description": (
                    f"{preset['title']}.\n\n"
                    f"Watch the full investigation on our channel: History of Earth.\n\n"
                    f"{' '.join(preset['hashtags'])}"
                ),
                "tags": preset["hashtags"],
                "aspect_ratio": "9:16 (1080x1920)",
                "duration_sec": preset["duration_sec"]
            }
            results.append(out_mp4)
            metadata_list.append(meta)

    # Save shorts_metadata.json
    meta_path = os.path.join(shorts_dir, "shorts_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=2)

    return metadata_list


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_video = os.path.join(base, "output", "hadean_landscape_01", "act_01_rendered.mp4")
    out_dir = os.path.join(base, "output", "hadean_landscape_01")

    if os.path.exists(sample_video):
        print("Found source video:", sample_video)
        out_short = os.path.join(out_dir, "shorts", "test_theia_short.mp4")
        ok = render_vertical_short(
            master_video_path=sample_video,
            output_path=out_short,
            start_time_sec=0,
            duration_sec=15,
            banner_text="WHEN A PLANET HIT EARTH",
            sub_banner="4.5 BILLION YEARS AGO",
            cta_text="FULL STORY LINKED BELOW"
        )
        print("Short Render Result:", ok)
    else:
        print("Sample video not found at:", sample_video)
