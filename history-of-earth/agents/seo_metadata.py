"""
SEO & Metadata Agent for History of Earth.
Generates compliant metadata JSON adhering to YouTube guidelines, including
high-retention titles, sourced description bullet lists, and timestamped chapters.
"""

import os
import json
from typing import Dict, List, Any

def generate_metadata(
    episode_id: str,
    era: str,
    pillar: str,
    working_title: str,
    hook: str,
    approved_claims: List[Dict[str, Any]],
    shot_list: List[Dict[str, Any]],
    output_dir: str,
    privacy_status: str = "unlisted"
) -> Dict[str, Any]:
    """Generates the comprehensive metadata JSON for the episode."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. High-CTR, policy-compliant title
    # Pattern: [Era/Event] — [Stakes / Phenomenon]
    title = f"{era}: {working_title}"

    # 2. Description with Hook, Sourced Fact Citations, and Chapters
    # 2. Description with Hook, Sourced Fact Citations, Chapters, and Viral Hashtags
    viral_hashtags = [
        "#EarthHistory",
        "#PlateTectonics",
        "#Geology",
        "#ScienceDocumentary",
        "#Pangaea",
        "#Hadean",
        "#AncientEarth",
        "#DeepTime",
        "#Science",
        "#SpaceDocumentary",
        "#HistoryOfEarth"
    ]
    hashtag_str = " ".join(viral_hashtags)

    description_lines = [
        f"{hook}.",
        "",
        "Before continents wandered the globe, Earth was trapped in a single, unbroken rocky shell capping a boiling mantle. "
        "Discover the forensic scientific detective story of how the primordial 'stagnant lid' was shattered, "
        "how the first subduction zone ignited, and how the ancient ancestors of Pangaea were born 4.4 billion years ago.",
        "",
        hashtag_str,
        "",
        "--- VERIFIED SCIENTIFIC SOURCES & ACADEMIC CITATIONS ---"
    ]

    for idx, claim in enumerate(approved_claims, 1):
        source = claim.get("source_url", "Scientific Consensus")
        description_lines.append(f"• Fact {idx}: {claim['text']}")
        description_lines.append(f"  Source: {source}")

    description_lines.append("")
    description_lines.append("--- CHAPTERS ---")
    chapters = []
    for shot in shot_list:
        ts = shot.get("timestamp_start", "00:00")
        seg = shot.get("scene_title") or shot.get("segment_type", "scene").replace("_", " ").title()
        description_lines.append(f"{ts} - {seg}")
        chapters.append({"time": ts, "title": seg})

    description_lines.append("")
    description_lines.append("🔔 Subscribe to History of Earth and ring the bell to explore all 4.5 billion years of planetary evolution!")
    description_lines.append(hashtag_str)

    description = "\n".join(description_lines)

    # 3. Comprehensive High-Ranking Search Tags (maximum discoverability, strictly general-audience compliant)
    if pillar.lower() == "map":
        tags = [
            "plate tectonics",
            "how plate tectonics started",
            "what came before pangaea",
            "stagnant lid earth",
            "earth history documentary",
            "hadean eon",
            "how continents formed",
            "jack hills zircon",
            "oldest rock on earth",
            "first subduction zone",
            "primordial earth animation",
            "geology documentary",
            "earth science",
            "deep time",
            "formation of continents",
            "craton formation",
            "pilbara craton",
            "ancient earth 4 billion years ago",
            "history of earth",
            "space documentary"
        ]
    else:
        tags = [
            era.lower(),
            f"{era.lower()} eon",
            pillar.lower(),
            "geologic time",
            "magma ocean",
            "theia impact",
            "jack hills zircon",
            "planetary evolution",
            "earth science documentary",
            "earth history",
            "origin of earth"
        ]

    metadata = {
        "episode_id": episode_id,
        "title": title,
        "description": description,
        "tags": tags,
        "category_id": "27",  # 27 = Education
        "privacy_status": privacy_status,
        "playlist_ids": [],
        "captions": [
            {"language": "en", "path": f"output/{episode_id}/en.srt", "kind": "primary"}
        ],
        "thumbnail_path": f"output/{episode_id}/{episode_id}_thumb_candidate_a.png",
        "made_for_kids": False,
        "altered_content_disclosure": False,
        "licence_ledger_ref": "assets/licence_ledger.csv",
        "chapters": chapters
    }

    out_file = os.path.join(output_dir, "metadata.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return metadata


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "test_seo")
    m = generate_metadata(
        episode_id="hadean_landscape_01",
        era="Hadean",
        pillar="Landscape",
        working_title="A World of Fire and Rain",
        hook="Earth had no solid ground for 500 million years",
        approved_claims=[{"text": "Earth formed ~4.54 Ga.", "source_url": "https://en.wikipedia.org/wiki/Hadean"}],
        shot_list=[{"timestamp_start": "00:00", "segment_type": "cold_open"}],
        output_dir=out
    )
    print("Generated Metadata Title:", m["title"])
    print("Saved to:", os.path.join(out, "metadata.json"))
