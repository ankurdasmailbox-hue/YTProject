"""
Compliance and Quality Control Agent for History of Earth.
Enforces YouTube AI-disclosure rules, general-audience child-safety protections,
variation matrix divergence, and licence ledger completeness.
"""

import os
import csv
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

BANNED_PHRASES = ["for kids", "for toddlers", "nursery rhyme", "kids learning"]


def _get_prop(obj: Any, key: str, default: Any = None) -> Any:
    """Helper to retrieve attribute from either a dict or an object."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@dataclass
class VideoSpec:
    art_style: str = "stylized_2d_flat_illustration"
    depicts_real_identifiable_person_realistically: bool = False
    contains_synthetic_voice_clone_of_real_person: bool = False
    depicts_real_event_or_place_in_a_way_that_could_mislead: bool = False


@dataclass
class MusicTrackSpec:
    filename: str = ""
    tempo_style: str = "cinematic_ambient"  # "nursery_singsong", "cinematic_ambient", "epic_documentary"
    licence_id: str = ""


@dataclass
class ScriptSpec:
    narration_register: str = "documentary-authoritative"  # "toy_mascot_framing", "documentary-authoritative"
    word_count: int = 0
    approved_claims_count: int = 0


def needs_ai_disclosure(video: Union[VideoSpec, Dict[str, Any]]) -> bool:
    """
    Based on YouTube's confirmed rule: disclosure is required only for
    REALISTIC content a viewer could mistake for real footage of a real
    person, place, or event. Stylized/clearly-animated content and AI
    used only for production assistance (scripts, editing, voice) do
    NOT require disclosure.
    Verified via YouTube's own policy language as of today; re-check
    Studio's current toggle wording periodically as policy has evolved
    since 2024 and may again.
    """
    art_style = _get_prop(video, "art_style")
    depicts_real_person = _get_prop(video, "depicts_real_identifiable_person_realistically", False)
    voice_clone = _get_prop(video, "contains_synthetic_voice_clone_of_real_person", False)
    could_mislead = _get_prop(video, "depicts_real_event_or_place_in_a_way_that_could_mislead", False)

    if art_style == "stylized_2d_flat_illustration":
        # Explicitly the category YouTube's own examples (e.g. animated
        # explainer channels) cite as NOT requiring disclosure.
        if not depicts_real_person:
            return False
    if voice_clone:
        return True
    if could_mislead:
        return True
    return False


def general_audience_check(
    metadata: Union[Dict[str, Any], Any],
    script: Union[ScriptSpec, Dict[str, Any]],
    music_track: Union[MusicTrackSpec, Dict[str, Any]]
) -> List[str]:
    """
    Automated check preventing content from reading as child-directed or violating COPPA framing.
    Any non-empty list of violations blocks Gate B.
    """
    violations: List[str] = []

    title = _get_prop(metadata, "title", "")
    description = _get_prop(metadata, "description", "")
    tags = _get_prop(metadata, "tags", [])
    if isinstance(tags, list):
        tags_str = " ".join(tags)
    else:
        tags_str = str(tags)

    text_fields = f"{title} {description} {tags_str}".lower()

    for phrase in BANNED_PHRASES:
        if phrase in text_fields:
            violations.append(f"banned phrase in metadata: '{phrase}'")

    tempo_style = _get_prop(music_track, "tempo_style", "")
    if tempo_style == "nursery_singsong":
        violations.append("music cadence reads as child-directed")

    narration_register = _get_prop(script, "narration_register", "")
    if narration_register == "toy_mascot_framing":
        violations.append("narration framing reads as child-directed")

    return violations


def check_variation_matrix(
    current_vars: Dict[str, str],
    previous_vars_list: List[Dict[str, str]],
    max_shared_dims: int = 2
) -> tuple[bool, List[str]]:
    """
    Enforces that no two consecutive uploads share more than max_shared_dims (default 2)
    across the 5 variation dimensions:
    cold_open_type, narration_register, visual_treatment, structure, pacing.
    """
    dimensions = ["cold_open_type", "narration_register", "visual_treatment", "structure", "pacing"]
    violations = []

    for prev_idx, prev_vars in enumerate(previous_vars_list):
        shared_count = 0
        shared_details = []
        for dim in dimensions:
            cur_val = current_vars.get(dim)
            prev_val = prev_vars.get(dim)
            if cur_val and prev_val and cur_val == prev_val:
                shared_count += 1
                shared_details.append(f"{dim}='{cur_val}'")

        if shared_count > max_shared_dims:
            violations.append(
                f"Shares {shared_count} dimensions with previous episode #{prev_idx+1} (max allowed {max_shared_dims}): {', '.join(shared_details)}"
            )

    is_compliant = (len(violations) == 0)
    return is_compliant, violations


def check_licence_ledger(asset_ids: List[str], ledger_csv_path: str) -> tuple[bool, List[str]]:
    """
    Verifies that every asset used in an episode exists in the licence_ledger.csv.
    """
    violations = []
    if not os.path.exists(ledger_csv_path):
        return False, [f"Licence ledger file not found at '{ledger_csv_path}'"]

    logged_ids = set()
    with open(ledger_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset_id = row.get("asset_id")
            if asset_id:
                logged_ids.add(asset_id.strip())

    for aid in asset_ids:
        if aid not in logged_ids:
            violations.append(f"Asset '{aid}' is missing from licence ledger.")

    return (len(violations) == 0), violations


if __name__ == "__main__":
    print("Testing compliance_qc.py...")
    # Test 1: AI Disclosure on Stylized 2D Illustration (standard)
    vid_normal = VideoSpec(art_style="stylized_2d_flat_illustration")
    assert not needs_ai_disclosure(vid_normal), "Stylized 2D should not require AI disclosure"
    print("  [PASS] Stylized 2D correctly exempt from AI disclosure.")

    # Test 2: AI Disclosure with Realistic Style + Voice Clone
    vid_clone = VideoSpec(art_style="realistic_cgi", contains_synthetic_voice_clone_of_real_person=True)
    assert needs_ai_disclosure(vid_clone), "Voice clone in realistic CGI must require AI disclosure"
    print("  [PASS] Realistic CGI with voice clone correctly triggers AI disclosure.")

    # Test 3: AI Disclosure with Misleading Real-Place depiction
    vid_mislead = VideoSpec(art_style="realistic_cgi", depicts_real_event_or_place_in_a_way_that_could_mislead=True)
    assert needs_ai_disclosure(vid_mislead), "Misleading real place depiction must trigger AI disclosure"
    print("  [PASS] Misleading real place depiction correctly triggers AI disclosure.")

    # Test 4: General Audience Clean Check
    meta_clean = {"title": "Hadean: World of Fire", "description": "Scientific history of Earth", "tags": ["geology", "hadean"]}
    script_clean = ScriptSpec(narration_register="documentary-authoritative")
    music_clean = MusicTrackSpec(tempo_style="cinematic_ambient")
    assert len(general_audience_check(meta_clean, script_clean, music_clean)) == 0
    print("  [PASS] Clean episode passes general audience check.")

    # Test 5: General Audience Violation Check
    meta_bad = {"title": "Earth for kids cartoon", "description": "nursery rhyme style", "tags": ["kids learning"]}
    script_bad = ScriptSpec(narration_register="toy_mascot_framing")
    music_bad = MusicTrackSpec(tempo_style="nursery_singsong")
    bad_violations = general_audience_check(meta_bad, script_bad, music_bad)
    assert len(bad_violations) >= 3, f"Expected violations, got {bad_violations}"
    print(f"  [PASS] Violations successfully caught: {len(bad_violations)} issues found.")

    print("ALL COMPLIANCE QC TESTS PASSED!")
