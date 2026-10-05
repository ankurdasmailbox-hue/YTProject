"""
Remaster Episode 4 Master Video & Vertical Shorts:
1. Audio Loudness: Exactly -14.0 LUFS (YouTube broadcast standard) and -1.5 dBTP.
2. Video Resolution: 2560x1440 QHD (1440p) via high-fidelity Lanczos + unsharp.
   Forces YouTube to encode with VP09 / AV01 codec at 12-18 Mbps (no more AVC1 blur!).
3. Color Space: BT.709 explicit tags with closed 1s GOP.
4. Vertical Shorts: Regenerated with -14.0 LUFS audio and high-bitrate video.
"""

import os
import sys
import json
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from agents.editor_assembler import assemble_full_movie
from pipeline.shorts_generator import generate_episode_shorts
from build_episode4 import generate_gate_b_html

episode_id = "hadean_life_then_04"
episode_dir = os.path.join(PROJECT_ROOT, "output", episode_id)
soundtrack_file = os.path.join(episode_dir, "mild_background_score.mp3")
master_srt = os.path.join(episode_dir, "en.srt")
final_video = os.path.join(episode_dir, "final_episode.mp4")

act_clips = [os.path.join(episode_dir, f"act_{i:02d}_rendered.mp4") for i in range(1, 8)]

print("=" * 85)
print("REMASTERING EPISODE 4 MASTER VIDEO (1440p QHD + -14.0 LUFS BROADCAST AUDIO)")
print("=" * 85)

print("\n[STEP 1] Assembling 1440p Master Video with Broadcast Loudness Normalization...")
t0 = time.time()
render_stats = assemble_full_movie(
    act_clips=act_clips,
    ambient_music_path=soundtrack_file,
    srt_path=master_srt,
    output_mp4_path=final_video,
    burn_subtitles=False
)
t1 = time.time()
print(f"  [OK] Master Video Rendered: {final_video}")
print(f"       Resolution: 2560x1440 (1440p QHD) | Size: {render_stats['size_mb']} MB in {t1-t0:.1f}s")

print("\n[STEP 2] Regenerating Mobile Vertical Shorts with Broadcast Audio...")
shorts_meta = generate_episode_shorts(episode_id, final_video, episode_dir)
for s in shorts_meta:
    print(f"  [OK] Short: {s['title']} ({s['file_size_mb']} MB)")

print("\n[STEP 3] Updating Gate B Review Dashboard...")
with open(os.path.join(episode_dir, "metadata.json"), "r", encoding="utf-8") as f:
    metadata = json.load(f)

with open(os.path.join(episode_dir, "retention_audit.json"), "r", encoding="utf-8") as f:
    retention_report = json.load(f)

thumbs = [
    os.path.join(episode_dir, f"{episode_id}_thumb_candidate_a.png"),
    os.path.join(episode_dir, f"{episode_id}_thumb_candidate_b.png"),
    os.path.join(episode_dir, f"{episode_id}_thumb_candidate_c.png")
]

script_data = {
    "shot_list": [
        {"shot_id": 1, "scene_title": "THE SILENT CRADLE", "camera_move": "orbital_descent_with_telemetry", "mood": "cosmic_mystery", "duration_sec": 54, "timestamp_start": "00:00", "timestamp_end": "00:54", "narration_segment": "Look at your hands..."},
        {"shot_id": 2, "scene_title": "THE 4,000-METER ABYSS", "camera_move": "deep_abyssal_sonar_dive", "mood": "internal_furnace", "duration_sec": 54, "timestamp_start": "00:54", "timestamp_end": "01:48", "narration_segment": "For decades, science believed..."},
        {"shot_id": 3, "scene_title": "TOWERS OF SERPENTINIZATION", "camera_move": "colossal_spire_cinematic_dolly", "mood": "tectonic_rupture", "duration_sec": 49, "timestamp_start": "01:48", "timestamp_end": "02:37", "narration_segment": "Piercing the abyssal darkness..."},
        {"shot_id": 4, "scene_title": "THE NATURAL PROTON BATTERY", "camera_move": "chemiosmotic_voltage_zoom", "mood": "atomic_discovery", "duration_sec": 50, "timestamp_start": "02:37", "timestamp_end": "03:27", "narration_segment": "Look closer at the boundary..."},
        {"shot_id": 5, "scene_title": "THE ROCK THAT LEARNED TO CODE", "camera_move": "microscopic_pore_labyrinth_dive", "mood": "atomic_discovery", "duration_sec": 54, "timestamp_start": "03:27", "timestamp_end": "04:21", "narration_segment": "Zoom in millions of times..."},
        {"shot_id": 6, "scene_title": "THE PROTO-CELL AWAKENING", "camera_move": "macro_protocell_birth_drift", "mood": "continental_majesty", "duration_sec": 50, "timestamp_start": "04:21", "timestamp_end": "05:11", "narration_segment": "For millions of years..."},
        {"shot_id": 7, "scene_title": "THE COMING CATACLYSM (CLIFFHANGER)", "camera_move": "asteroid_impact_supernova_sweep", "mood": "cliffhanger_suspense", "duration_sec": 55, "timestamp_start": "05:11", "timestamp_end": "06:06", "narration_segment": "The spark had caught..."}
    ]
}

approved_claims = [
    {
        "text": "Alkaline hydrothermal vents formed by ultramafic serpentinization on the Hadean ocean floor produced continuous fluxes of hydrogen, methane, and warm alkaline fluids (pH 9-11) into a mildly acidic ocean.",
        "citation": "Martin & Russell (2007), Phil. Trans. R. Soc. B 362",
        "source_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2442388/"
    },
    {
        "text": "Natural pH and proton gradients across thin semi-permeable iron-monosulfide (mackinawite) chimney walls provided an abiotic proton-motive force (~200 mV) driving early carbon fixation before cellular membranes evolved.",
        "citation": "Lane & Martin (2012), Cell 151",
        "source_url": "https://www.cell.com/cell/fulltext/S0092-8674(12)01430-8"
    }
]

review_file = generate_gate_b_html(
    episode_id=episode_id,
    episode_dir=episode_dir,
    final_video=final_video,
    thumbs=thumbs,
    shorts_meta=shorts_meta,
    metadata=metadata,
    script_data=script_data,
    approved_claims=approved_claims,
    retention_report=retention_report,
    total_dur=366.0
)

print(f"  [OK] Updated Gate B Dashboard: {review_file}")
print("\n" + "=" * 85)
print("REMASTER COMPLETE! Master Video: 2560x1440 QHD @ -14.0 LUFS")
print("=" * 85)
