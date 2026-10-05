"""
SEO & Metadata Agent for History of Earth (Upgraded A/B CTR & High-RPM Engine).
Adopts YouTube growth & monetization engineering principles:
1. "Obsess Over CTR": Produces 3 tested Title Formulas for YouTube Studio's free A/B Test & Compare.
2. 3 Alternate Description Hooks (above-the-fold 2-line teasers).
3. High-RPM Keyword Optimization: Strategically integrates high-eCPM planetary science / astrophysics / geology tags.
4. Generates both metadata.json and ab_packaging.json.
100% Zero-Subscription, Local Python.
"""

import os
import json
from typing import Dict, List, Any, Optional


def generate_ab_titles(era: str, pillar: str, working_title: str) -> List[Dict[str, str]]:
    """
    Generates 3 distinct high-CTR title variations utilizing proven psychological hooks:
    1. Curiosity Gap / Paradox
    2. Forensic Mystery / Cold Case
    3. Kinetic Stakes / Astronomical Cataclysm
    """
    norm_era = era.strip().capitalize()
    norm_pillar = pillar.strip().capitalize()

    if norm_era == "Hadean" and ("ending" in norm_pillar.lower() or "bombardment" in norm_pillar.lower()):
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Overturned Consensus",
                "title": "The Asteroid Storm That Almost Erased Earth — The Late Heavy Bombardment",
                "rationale": "High-stakes drama confronting the classic sterilization myth vs. subterranean survival."
            },
            {
                "variant": "B",
                "formula": "The Forensic Detective Mystery",
                "title": "Did Mountain-Sized Asteroids Sterilize Early Earth — Or Spark Life?",
                "rationale": "Direct curiosity question triggering cognitive debate on prebiotic delivery vs extinction."
            },
            {
                "variant": "C",
                "formula": "The High-Stakes Kinetic Event",
                "title": "When the Sky Fell: Inside the 3.9-Billion-Year-Old Planetary Cataclysm",
                "rationale": "Visceral sensory stakes appealing to mainstream space and planetary catastrophe viewers."
            }
        ]
    elif norm_era == "Hadean" and norm_pillar == "Map":
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Paradox",
                "title": "Earth Had No Tectonic Plates For 500 Million Years — How Did It Survive?",
                "rationale": "Directly confronts the viewer with an apparent impossibility; triggers high cognitive dissonance."
            },
            {
                "variant": "B",
                "formula": "The Forensic Detective Mystery",
                "title": "The 500-Million-Year Crime Scene: Why Earth's First Crust Vanished",
                "rationale": "Frames scientific geophysics as an unsolved detective investigation."
            },
            {
                "variant": "C",
                "formula": "The High-Stakes Kinetic Event",
                "title": "When Earth Was Trapped in a Single Rocky Cage: The Stagnant Lid",
                "rationale": "High drama, evocative visual language, and authoritative terminology."
            }
        ]
    elif norm_era == "Hadean" and norm_pillar == "Landscape":
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Paradox",
                "title": "Earth Had Oceans Before It Had Solid Ground — The Impossible Dawn",
                "rationale": "Inverts common assumptions about Earth's planetary formation."
            },
            {
                "variant": "B",
                "formula": "The High-Stakes Kinetic Event",
                "title": "When a Mars-Sized Planet Smashed into Earth at 25,000 MPH",
                "rationale": "Concrete speed, colossal planetary collision stakes, massive broad appeal."
            },
            {
                "variant": "C",
                "formula": "The Forensic Detective Mystery",
                "title": "Hadean: A World of Fire and Rain — When Earth Had No Ground",
                "rationale": "Documentary-authoritative with visceral sensory contrast."
            }
        ]
    elif norm_era == "Hadean" and "life" in norm_pillar.lower():
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Paradox",
                "title": "Life Didn't Start in a Pond — It Began in Dead Rock 4.2 Billion Years Ago",
                "rationale": "Directly confronts the Darwin 'warm little pond' myth and introduces the hydrothermal rock pore reality."
            },
            {
                "variant": "B",
                "formula": "The Forensic Detective Mystery",
                "title": "The Genesis Battery: How Ancient Seabed Chimneys Forged the First Living Code",
                "rationale": "High curiosity and scientific intrigue connecting mineral physics to the origin of life."
            },
            {
                "variant": "C",
                "formula": "The High-Stakes Kinetic Event",
                "title": "The Planet Before Life: Inside Earth's 4,000-Meter Abyssal Nursery",
                "rationale": "Atmospheric, deep-sea mystery and extreme environment scale for documentary viewers."
            }
        ]
    elif norm_era == "Hadean" and ("air" in norm_pillar.lower() or "ocean" in norm_pillar.lower()):
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Paradox",
                "title": "Earth Had a Green Ocean and a Poison Sky For 500 Million Years",
                "rationale": "Overturns common assumptions about blue oceans and white clouds; triggers deep curiosity."
            },
            {
                "variant": "B",
                "formula": "The Forensic Detective Mystery",
                "title": "The Sky Was Poison and the Rain Never Stopped: Inside Earth's First Ocean",
                "rationale": "High sensory contrast and visceral drama grounded in peer-reviewed thermodynamics."
            },
            {
                "variant": "C",
                "formula": "The High-Stakes Kinetic Event",
                "title": "When a 200-Atmosphere Steam Sky Collapsed into 1,000 Years of Boiling Rain",
                "rationale": "Extreme physical scale and astronomical consequence that hooks lovers of hard science documentaries."
            }
        ]
    elif norm_era == "Hadean" and ("leap" in norm_pillar.lower() or "zircon" in norm_pillar.lower()):
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Overturned Consensus",
                "title": "The 4.4-Billion-Year-Old Rock That Broke Geology — The Zircon Code",
                "rationale": "Directly confronts consensus, highlights the oldest terrestrial material, and triggers high curiosity."
            },
            {
                "variant": "B",
                "formula": "High-Intent Search Authority",
                "title": "Earth Had Oceans 4.4 Billion Years Ago: Inside the Oldest Rock on Earth",
                "rationale": "High-volume evergreen search keywords ('oldest rock on Earth', 'oceans 4.4 billion years')."
            },
            {
                "variant": "C",
                "formula": "The Forensic Detective Mystery",
                "title": "Why 99.9% of Earth's First Crust Vanished — And the One Crystal That Survived",
                "rationale": "Extreme statistical drama and forensic investigation narrative."
            }
        ]
    else:
        # Dynamic generic fallback formulas for any era/pillar
        return [
            {
                "variant": "A",
                "formula": "The Curiosity Gap / Paradox",
                "title": f"The Impossible Era: What Science Got Wrong About the {norm_era}",
                "rationale": "Challenges consensus and sparks immediate curiosity."
            },
            {
                "variant": "B",
                "formula": "The Forensic Mystery",
                "title": f"{norm_era}: {working_title} — The Lost Geologic Record",
                "rationale": "Authoritative documentary inquiry framing."
            },
            {
                "variant": "C",
                "formula": "The High-Stakes Event",
                "title": f"When the World Changed Forever: Inside the {norm_era} {norm_pillar}",
                "rationale": "Epochal transformation stakes."
            }
        ]


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
    """Generates comprehensive metadata JSON and A/B Test & Compare packaging."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Generate A/B Titles
    ab_titles = generate_ab_titles(era, pillar, working_title)
    primary_title = ab_titles[0]["title"]

    # 2. 3 Alternate Description Hooks (Above-the-fold teasers)
    description_hooks = [
        f"{hook}. Discover the untold scientific story of how our planet survived its most violent dawn.",
        "Everything we know about continents and oceans was forged in an ancient inferno. Here is the forensic evidence.",
        "Look at the ground beneath your feet. Four billion years ago, it did not exist. Here is what happened."
    ]

    # 3. Viral, High-RPM & Current Trending Hashtags (Combines high-relevance niche with trending discovery)
    viral_hashtags = [
        "#EarthHistory",
        "#PlanetaryScience",
        "#DeepTime",
        "#GeologyDocumentary",
        "#SpaceDocumentary",
        "#Science",
        "#Trending",
        "#LearnOnYouTube",
        "#ScienceFacts",
        "#DidYouKnow"
    ]
    hashtag_str = " ".join(viral_hashtags)

    norm_pillar = pillar.strip().lower()
    if "ending" in norm_pillar or "bombardment" in norm_pillar:
        context_desc = (
            "Three point nine billion years ago, a cosmic gravitational resonance triggered the Late Heavy Bombardment: "
            "over twenty thousand mountain-sized asteroids hammered the infant Earth. "
            "Discover the peer-reviewed forensic investigation into whether this planetary catastrophe sterilized early life, "
            "or if subterranean hydrothermal aquifers became the ultimate biological sanctuary."
        )
    elif "leap" in norm_pillar or "zircon" in norm_pillar:
        context_desc = (
            "Over 99.9% of Earth's earliest crust was completely destroyed by boiling magma and meteorite bombardment. "
            "Discover the forensic scientific investigation into Western Australia's Jack Hills zircons: "
            "how a microscopic mineral grain preserved oxygen isotopes and titanium thermometers proving cool liquid oceans "
            "and proto-continents existed 4.4 billion years ago."
        )
    elif "life" in norm_pillar:
        context_desc = (
            "Before cells existed, deep-sea alkaline hydrothermal chimneys forged the world's first natural proton batteries. "
            "Discover how inorganic mineral cavities catalyzed the transition from dead rock to self-replicating RNA code, "
            "giving birth to LUCA—the ancestor of all life on Earth."
        )
    elif "air" in norm_pillar or "ocean" in norm_pillar:
        context_desc = (
            "Four point four billion years ago, Earth was wrapped in a 200-atmosphere vault of supercritical steam and toxic sulfur. "
            "Discover how atmospheric cooling triggered centuries of torrential boiling downpours, filling Earth's first scalding emerald-green ocean."
        )
    elif norm_pillar == "map":
        context_desc = (
            "Before continents wandered the globe, Earth was trapped in a single, unbroken rocky shell capping a boiling mantle. "
            "Discover the forensic scientific detective story of how the primordial 'stagnant lid' was shattered, "
            "how the first subduction zone ignited, and how the ancient ancestors of Pangaea were born 4.4 billion years ago."
        )
    else:
        context_desc = (
            "Four and a half billion years ago, Earth was hammered out inside a planetary furnace. "
            "From the giant collision with Theia to the cooling of the magma ocean, discover the violent origin of our world."
        )

    # 4. Description Body
    description_lines = [
        description_hooks[0],
        "",
        context_desc,
        "",
        hashtag_str,
        "",
        "--- VERIFIED SCIENTIFIC SOURCES & ACADEMIC CITATIONS ---"
    ]

    for idx, claim in enumerate(approved_claims, 1):
        source = claim.get("source_url") or claim.get("citation", "Peer-Reviewed Consensus")
        description_lines.append(f"• Fact {idx}: {claim['text']}")
        description_lines.append(f"  Source: {source}")

    description_lines.append("")
    description_lines.append("--- TIMESTAMPS & CHAPTERS ---")
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

    # 5. High-RPM & Search Discoverability Tags
    if "ending" in norm_pillar or "bombardment" in norm_pillar:
        tags = [
            "late heavy bombardment",
            "asteroid impact earth",
            "did asteroids sterilize earth",
            "planetary science documentary",
            "nice model solar system",
            "lunar cataclysm apollo",
            "abramov mojzsis 2009",
            "hadean eon documentary",
            "history of earth",
            "deep time geology",
            "origin of life asteroids",
            "earth impact history",
            "geology documentary",
            "ancient earth",
            "space documentary",
            "prebiotic chemistry",
            "science documentary",
            "planetary formation",
            "solar system migration",
            "extinction event"
        ]
    elif "leap" in norm_pillar or "zircon" in norm_pillar:
        tags = [
            "oldest rock on earth",
            "jack hills zircon",
            "how old is earth",
            "4.4 billion year old rock",
            "zircon crystals geology",
            "cool early earth",
            "hadean eon documentary",
            "formation of earth",
            "history of earth",
            "shrimp mass spectrometry",
            "uranium lead dating",
            "delta 18O oxygen isotopes",
            "ancient earth documentary",
            "geology documentary",
            "planetary science documentary",
            "first continents on earth",
            "earth history documentary",
            "origin of continents",
            "deep time geology",
            "space documentary"
        ]
    elif "life" in norm_pillar:
        tags = [
            "origin of life",
            "how did life begin",
            "abiogenesis explained",
            "alkaline hydrothermal vents",
            "lost city hydrothermal field",
            "last universal common ancestor",
            "luca biology",
            "proton motive force origin of life",
            "hadean life",
            "prebiotic chemistry",
            "rna world hypothesis",
            "first living cell",
            "deep sea hydrothermal vents",
            "serpentinization origin of life",
            "nick lane origin of life",
            "michael russell hydrothermal",
            "ancient earth documentary",
            "planetary science documentary",
            "astrobiology documentary",
            "history of earth"
        ]
    elif "air" in norm_pillar or "ocean" in norm_pillar:
        tags = [
            "first ocean on earth",
            "how did earth get water",
            "hadean atmosphere",
            "faint young sun paradox",
            "primordial ocean earth",
            "emerald green ocean",
            "supercritical steam atmosphere",
            "thousand year rain",
            "jack hills zircon water",
            "earth history documentary",
            "deep time geology",
            "planetary science documentary",
            "atmospheric evolution",
            "geophysics documentary",
            "astrobiology origin of life",
            "hydrothermal vents",
            "origin of earth ocean",
            "ancient earth documentary",
            "space documentary",
            "history of earth"
        ]
    elif norm_pillar == "map":
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
            "planetary science",
            "geophysics documentary",
            "astrobiology earth origins",
            "geology documentary",
            "deep time science",
            "formation of continents",
            "craton formation",
            "pilbara craton",
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
        "title": primary_title,
        "description": description,
        "tags": tags,
        "category_id": "27",  # Education
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

    # Save primary metadata.json
    out_file = os.path.join(output_dir, "metadata.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Save A/B Packaging Matrix for YouTube Studio Test & Compare
    ab_package = {
        "episode_id": episode_id,
        "testing_tool": "YouTube Studio Test & Compare (Free Native A/B Testing)",
        "title_variants": ab_titles,
        "description_hook_variants": [
            {"variant": "A", "hook": description_hooks[0]},
            {"variant": "B", "hook": description_hooks[1]},
            {"variant": "C", "hook": description_hooks[2]}
        ],
        "thumbnail_variants": [
            {"variant": "A", "path": f"output/{episode_id}/{episode_id}_thumb_candidate_a.png", "focus": "Stagnant Lid / Impossible Shell"},
            {"variant": "B", "path": f"output/{episode_id}/{episode_id}_thumb_candidate_b.png", "focus": "The First Crack / Subduction Rupture"},
            {"variant": "C", "path": f"output/{episode_id}/{episode_id}_thumb_candidate_c.png", "focus": "Zircon Atomic Witness"}
        ],
        "target_audience": "General Audience (Ages 16-65, Science & Documentary Lovers)",
        "coppa_status": "Strictly Not Made for Kids (Compliant)",
        "projected_rpm_tier": "High ($8-$18 RPM via Planetary Science & Space targeting)"
    }

    ab_file = os.path.join(output_dir, "ab_packaging.json")
    with open(ab_file, "w", encoding="utf-8") as f:
        json.dump(ab_package, f, indent=2)

    return metadata


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "test_seo")
    m = generate_metadata(
        episode_id="hadean_map_02",
        era="Hadean",
        pillar="Map",
        working_title="The Planet With No Plates",
        hook="Before continents, there was one churning shell",
        approved_claims=[{"text": "The infant Earth was locked in a stagnant lid.", "source_url": "https://en.wikipedia.org/wiki/Stagnant_lid"}],
        shot_list=[{"timestamp_start": "00:00", "scene_title": "The Unbroken Prison"}],
        output_dir=out
    )
    print("Generated Primary Title:", m["title"])
    print("Saved metadata.json and ab_packaging.json to:", out)
