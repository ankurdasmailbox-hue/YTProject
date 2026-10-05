"""
Retention & Curiosity-Loop Engine for History of Earth.
Adopts high-retention YouTube engineering principles:
1. "Win the first 5 seconds" (Audits cold-open for pattern interrupts, bans weak intros).
2. "45-second micro-curiosity loops" (Scans exposition to prevent viewer drop-off).
3. Pacing & Cadence Calculator (Validates 130-145 WPM documentary speed).
4. Automated retention prompt generator for free-tier LLMs (Gemini / Ollama).
100% Zero-Subscription, Local Python.
"""

import re
from typing import Dict, List, Any, Optional

# Banned weak openers that cause immediate viewer bounce
BANNED_OPENERS = [
    "welcome back",
    "welcome to",
    "hello guys",
    "in today's video",
    "today we will",
    "today we're going to",
    "in this video",
    "have you ever wondered",
    "before we begin",
    "make sure to subscribe",
    "let's dive in",
    "let's get started"
]

# High-tension triggers and curiosity-loop indicators
CURIOSITY_INDICATORS = [
    "how did",
    "why did",
    "what happened",
    "impossible",
    "mystery",
    "secret",
    "puzzle",
    "shattered",
    "catastrophe",
    "they were wrong",
    "yet against all odds",
    "the answer was hiding",
    "here is the mystery",
    "uncovered an impossible",
    "something was missing",
    "could not explain",
    "threatened to destroy",
    "tipping point",
    "until now",
    "what came before",
    "what if"
]


def audit_cold_open(script_text: str) -> Dict[str, Any]:
    """
    Audits the first 5-10 seconds of narration (first ~25 words).
    Ensures strict adherence to Rule #1: Win the First 5 Seconds.
    """
    # Extract first sentence/paragraph
    cleaned = re.sub(r"===.*?===", "", script_text).strip()
    first_paragraph = cleaned.split("\n\n")[0] if "\n\n" in cleaned else cleaned
    first_words = first_paragraph.split()[:25]
    opening_snippet = " ".join(first_words)
    opening_lower = opening_snippet.lower()

    violations = []
    for banned in BANNED_OPENERS:
        if banned in opening_lower:
            violations.append(f"Weak opening detected: '{banned}'. Open with conflict or cognitive shock instead.")

    # Check for sensory / conflict words
    conflict_words = ["fire", "poison", "kill", "shatter", "obliterate", "broken", "death", "scream", "nightmare", "danger", "dead", "unbroken"]
    has_conflict = any(cw in opening_lower for cw in conflict_words)

    score = 100
    if violations:
        score -= 50
    if not has_conflict:
        score -= 20

    return {
        "passed": len(violations) == 0,
        "score": max(0, score),
        "opening_text": opening_snippet + ("..." if len(cleaned.split()) > 25 else ""),
        "violations": violations,
        "has_high_stakes_contrast": has_conflict,
        "recommendation": "Great opening!" if (not violations and has_conflict) else "Start directly with the sensory shock, catastrophe, or impossible question."
    }


def scan_curiosity_loops(shot_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Scans sequential scenes/shots to verify whether curiosity loops or open questions
    are refreshed at least every 45-60 seconds to maintain audience retention.
    """
    loop_checkpoints = []
    long_exposition_gaps = []

    cumulative_time = 0.0

    for idx, shot in enumerate(shot_list, 1):
        dur = shot.get("duration_sec", 25)
        text = (shot.get("narration_segment") or "").lower()
        title = shot.get("scene_title", f"Shot {idx}")

        start_time = cumulative_time
        end_time = cumulative_time + dur
        cumulative_time = end_time

        # Check for curiosity hooks inside this segment
        matched_indicators = [ind for ind in CURIOSITY_INDICATORS if ind in text or "?" in text]
        has_hook = len(matched_indicators) > 0

        loop_checkpoints.append({
            "shot_id": idx,
            "scene_title": title,
            "time_range": f"{int(start_time // 60):02d}:{int(start_time % 60):02d} - {int(end_time // 60):02d}:{int(end_time % 60):02d}",
            "duration_sec": dur,
            "has_curiosity_hook": has_hook,
            "triggers_found": matched_indicators
        })

        # If a scene exceeds 45s without a curiosity hook
        if dur > 45 and not has_hook:
            long_exposition_gaps.append({
                "scene_title": title,
                "duration_sec": dur,
                "suggestion": f"Scene '{title}' lasts {dur}s without a question or tension pivot. Insert a micro-curiosity gap."
            })

    total_scenes = len(shot_list)
    hooked_scenes = sum(1 for c in loop_checkpoints if c["has_curiosity_hook"])
    retention_loop_ratio = (hooked_scenes / max(1, total_scenes)) * 100

    return {
        "total_scenes": total_scenes,
        "scenes_with_curiosity_loops": hooked_scenes,
        "curiosity_coverage_percent": round(retention_loop_ratio, 1),
        "long_exposition_warnings": long_exposition_gaps,
        "checkpoints": loop_checkpoints
    }


def analyze_pacing_and_wpm(script_text: str, total_runtime_sec: int) -> Dict[str, Any]:
    """
    Calculates words per minute (WPM).
    Optimal cinematic documentary pacing is 125 - 145 WPM.
    """
    clean_text = re.sub(r"===.*?===", "", script_text).strip()
    words = clean_text.split()
    word_count = len(words)

    runtime_min = max(0.1, total_runtime_sec / 60.0)
    wpm = round(word_count / runtime_min, 1)

    if wpm < 115:
        pacing_verdict = "Slow / dragging (below 115 WPM). Consider trimming pauses or adding visual density."
    elif 115 <= wpm <= 145:
        pacing_verdict = "Optimal (115-145 WPM). Perfect dramatic documentary acting cadence."
    elif 146 <= wpm <= 165:
        pacing_verdict = "Brisk (146-165 WPM). Good for fast-paced tech/news, slightly fast for deep time drama."
    else:
        pacing_verdict = "Too fast (>165 WPM). Risk of overwhelming viewers and muddying pronunciation."

    return {
        "word_count": word_count,
        "runtime_sec": total_runtime_sec,
        "words_per_minute": wpm,
        "pacing_verdict": pacing_verdict
    }


def audit_full_screenplay(
    script_text: str,
    shot_list: List[Dict[str, Any]],
    total_runtime_sec: int
) -> Dict[str, Any]:
    """Comprehensive screenplay retention audit."""
    cold_open_audit = audit_cold_open(script_text)
    curiosity_audit = scan_curiosity_loops(shot_list)
    pacing_audit = analyze_pacing_and_wpm(script_text, total_runtime_sec)

    # Composite Retention Score (0 - 100)
    overall_score = round(
        (cold_open_audit["score"] * 0.35) +
        (curiosity_audit["curiosity_coverage_percent"] * 0.40) +
        ((100 if "Optimal" in pacing_audit["pacing_verdict"] else 75) * 0.25),
        1
    )

    return {
        "overall_retention_score": overall_score,
        "cold_open_audit": cold_open_audit,
        "curiosity_loop_audit": curiosity_audit,
        "pacing_audit": pacing_audit,
        "retention_tier": "ELITE (>85)" if overall_score >= 85 else "SOLID (70-84)" if overall_score >= 70 else "NEEDS_OPTIMIZATION (<70)"
    }


def generate_high_retention_llm_prompt(
    era: str,
    pillar: str,
    topic: str,
    key_facts: List[str],
    runtime_target_min: int = 8
) -> str:
    """
    Generates a structured prompt incorporating Sammy's proven retention framework,
    optimized for free-tier Google Gemini or local Ollama instances.
    """
    facts_block = "\n".join([f"- {f}" for f in key_facts])
    target_words = int(runtime_target_min * 135)

    prompt = f"""
You are the Lead Screenwriter for "History of Earth", an elite cinematic science documentary YouTube channel.
Write a breathtaking, high-retention screenplay about: {topic} (Era: {era}, Pillar: {pillar}).

TARGET LENGTH: Exactly ~{target_words} words (~{runtime_target_min} minutes at 135 WPM).

STRICT RETENTION & PACING RULES:
1. RULE #1: WIN THE FIRST 5 SECONDS.
   - NEVER open with "Welcome back", "In this video", or generic introductions.
   - Start immediately with a brutal pattern interrupt: sensory shock, catastrophic conflict, or cognitive paradox that flips what the viewer expects.
2. 45-SECOND CURIOSITY LOOPS:
   - Introduce an explicit story-driven mystery question or curiosity gap every 45-60 seconds.
   - Never present raw encyclopedic facts without framing them as evidence solving a detective puzzle.
3. 7-ACT NARRATIVE CINEMATIC STRUCTURE:
   - Act 1: The Cataclysmic Cold Open (Immediate life-or-death hook)
   - Act 2: The Alien Environment (Deep sensory immersion)
   - Act 3: The Tipping Point (Physical forces reaching breaking point)
   - Act 4: The Forensic Evidence (The impossible discovery / scientific twist)
   - Act 5: The Climax / Global Impact (How Earth survived or was transformed)
   - Act 6: The Modern Legacy (Why this ancient moment dictates the ground beneath us)
   - Act 7: The Unresolved Cliffhanger (Dramatic teaser leading into the next episode)
4. TONE & REGISTER:
   - Documentary-authoritative, theatrical, conversational, visceral.
   - Avoid academic jargon without visual analogy.

GROUND TRUTH FACT CITATIONS TO INTEGRATE:
{facts_block}

Format your output with clear '=== SCENE X: TITLE ===' markers and concise camera direction cues.
"""
    return prompt.strip()


if __name__ == "__main__":
    try:
        from agents.scriptwriter import write_script
    except ImportError:
        from scriptwriter import write_script
    script_data = write_script([], pillar="Map")
    report = audit_full_screenplay(
        script_data["script_text"],
        script_data["shot_list"],
        script_data["runtime_estimate_sec"]
    )
    print("=" * 60)
    print(f"RETENTION AUDIT RESULT: {report['overall_retention_score']}/100 [{report['retention_tier']}]")
    print("Cold Open Hook Passed:", report["cold_open_audit"]["passed"])
    print("Curiosity Coverage:", f"{report['curiosity_loop_audit']['curiosity_coverage_percent']}%")
    print("Pacing:", f"{report['pacing_audit']['words_per_minute']} WPM ({report['pacing_audit']['pacing_verdict']})")
    print("=" * 60)
