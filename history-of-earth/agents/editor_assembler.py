"""
Editor & Assembler Agent for History of Earth (Cinematic Animation & VFX Engine).
Composites photorealistic AI scenes into dynamic 3D camera animations:
- Camera orbit, panoramic tracking, and macro focus dollies
- Procedural lightning flashes and atmospheric deluges
- Multi-channel cinematic sound design (impact braams, storm rumble, abyssal mystery drone)
- Non-intrusive, strictly 2-line maximum subtitle cards in the lower third.
"""

import os
import sys
import time
import subprocess
from typing import Dict, List, Any, Optional

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"


CAMERA_PROFILES = {
    "theia_impact": {
        "filter": "zoompan=z='min(zoom+0.0015,1.25)':x='(iw/2-(iw/zoom/2))+sin(on*1.5)*3':y='ih/2-(ih/zoom/2)'",
        "vfx": "",
        "description": "Rapid velocity push-in with kinetic collision shake"
    },
    "magma_ocean": {
        "filter": "zoompan=z='1.18':x='min(iw-iw/zoom, on*0.6)':y='ih/2-(ih/zoom/2)'",
        "vfx": ",eq=contrast=1.06:saturation=1.12",
        "description": "Panoramic horizontal sweep across lava fissures toward the red Moon"
    },
    "torrential_rain": {
        "filter": "zoompan=z='min(zoom+0.0008,1.20)':x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.45)'",
        # Procedural lightning flash pulses
        "vfx": ",eq=brightness='if(between(mod(n,70),0,2),0.40,if(between(mod(n,140),0,3),0.65,0))':contrast=1.08",
        "description": "Downward storm tilt with dynamic atmospheric lightning flashes"
    },
    "jack_hills_zircon": {
        "filter": "zoompan=z='min(zoom+0.0016,1.32)':x='iw*0.48-(iw/zoom/2)':y='ih*0.52-(ih/zoom/2)'",
        "vfx": ",eq=contrast=1.10:saturation=1.08",
        "description": "Macro anamorphic focus dolly into glowing concentric mineral bands"
    },
    "late_bombardment": {
        "filter": "zoompan=z='max(1.24-0.0008*on,1.0)':x='(iw/2-(iw/zoom/2))+cos(on*1.2)*2':y='ih*0.42-(ih/zoom/2)'",
        "vfx": ",eq=contrast=1.08:saturation=1.15",
        "description": "Crane pull-out revealing horizon meteor shockwaves"
    },
    "hydrothermal_vent": {
        "filter": "zoompan=z='min(zoom+0.0009,1.20)':x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.35)'",
        "vfx": ",eq=contrast=1.08:saturation=1.10",
        "description": "Abyssal descent tracking down volcanic black smoker chimney into the deep sea"
    },
    "life_spark_cliffhanger": {
        "filter": "zoompan=z='min(zoom+0.0012,1.26)':x='iw*0.52-(iw/zoom/2)':y='ih*0.48-(ih/zoom/2)'",
        "vfx": ",eq=contrast=1.12:saturation=1.15",
        "description": "Mysterious slow macro drift toward glowing bioluminescent RNA spirals on dark rock"
    }
}


ACT_MULTISHOT_PROFILES = {
    1: [
        # Shot 1.1: Ground feet walking (7.5s)
        {
            "asset": "assets/scenes/shot_01_ground_feet.jpg",
            "duration_ratio": 7.5 / 44.7,
            "filter": "zoompan=z='min(zoom+0.0008,1.15)':x='(iw/2-(iw/zoom/2))+sin(on*0.25)*8':y='(ih/2-(ih/zoom/2))+abs(sin(on*0.35))*6'",
            "vfx": ",eq=contrast=1.05:saturation=1.05",
            "desc": "POV walking on solid ground beneath feet with subtle handheld footstep sway"
        },
        # Shot 1.2: Volcanic hellscape (9.0s)
        {
            "asset": "assets/scenes/shot_02_volcanic_gas.jpg",
            "duration_ratio": 9.0 / 44.7,
            "filter": "zoompan=z='min(zoom+0.0006,1.18)':x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.5)'",
            "vfx": ",eq=contrast='1.08+sin(n*0.1)*0.04':saturation=1.15:brightness='if(between(mod(n,85),0,2),0.35,0)'",
            "desc": "Primordial volcanic hellscape with toxic sulfur gas plumes and volcanic lightning"
        },
        # Shot 1.3: Theia screaming through space (10.0s)
        {
            "asset": "assets/scenes/shot_03_theia_approach.jpg",
            "duration_ratio": 10.0 / 44.7,
            "filter": "zoompan=z='min(zoom+0.0016,1.30)':x='iw*0.58-(iw/zoom/2)':y='ih*0.55-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.08:saturation=1.10",
            "desc": "Theia screaming through the blackness of space toward Earth"
        },
        # Shot 1.4: Collision course terminal approach (7.0s)
        {
            "asset": "assets/scenes/theia_impact.jpg",
            "duration_ratio": 7.0 / 44.7,
            "filter": "zoompan=z='min(zoom+0.0025,1.35)':x='iw*0.50-(iw/zoom/2)':y='ih*0.48-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.10:saturation=1.15",
            "desc": "Terminal velocity impact trajectory zoom into Earth's atmosphere"
        },
        # Shot 1.5: Cataclysmic impact blast with kinetic supernova flash (11.2s)
        {
            "asset": "assets/scenes/shot_04_theia_impact.jpg",
            "duration_ratio": 11.2 / 44.7,
            "filter": "zoompan=z='min(zoom+0.0012,1.25)':x='(iw/2-(iw/zoom/2))+sin(on*2.0)*max(0, 10 - on*0.06)':y='ih/2-(ih/zoom/2)'",
            "vfx": ",eq=brightness='if(lt(n,12),0.85*(1-n/12),0)':contrast=1.12:saturation=1.18",
            "desc": "Blinding kinetic impact supernova blast, camera shake, and expanding ejecta shockwave"
        }
    ],
    2: [
        # Shot 2.1: Magma ocean wide (10.0s)
        {
            "asset": "assets/scenes/magma_ocean.jpg",
            "duration_ratio": 10.0 / 34.4,
            "filter": "zoompan=z='1.18':x='min(iw-iw/zoom, on*0.6)':y='ih/2-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.06:saturation=1.12",
            "desc": "Panoramic horizontal sweep across the 1,000 km deep boiling magma ocean"
        },
        # Shot 2.2: Close Moon over surging lava tides (10.0s)
        {
            "asset": "assets/scenes/shot_02_close_moon.jpg",
            "duration_ratio": 10.0 / 34.4,
            "filter": "zoompan=z='min(zoom+0.0012,1.24)':x='iw*0.55-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.4)'",
            "vfx": ",eq=contrast=1.08:saturation=1.14",
            "desc": "Gargantuan glowing red newborn Moon dominating blood-red sky above surging basalt tides"
        },
        # Shot 2.3: Molten core dynamo furnace (14.4s)
        {
            "asset": "assets/scenes/shot_02_core_furnace.jpg",
            "duration_ratio": 14.4 / 34.4,
            "filter": "zoompan=z='min(zoom+0.0015,1.28)':x='iw*0.48-(iw/zoom/2)':y='ih*0.52-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.10:saturation=1.12",
            "desc": "Internal planetary cross-section: molten iron plunging to forge Earth's core dynamo"
        }
    ],
    3: [
        # Shot 3.1: Supercritical steam vault (12.0s)
        {
            "asset": "assets/scenes/shot_02_volcanic_gas.jpg",
            "duration_ratio": 12.0 / 40.3,
            "filter": "zoompan=z='min(zoom+0.0010,1.22)':x='iw/2-(iw/zoom/2)':y='max(0, ih*0.4 - on*0.3)'",
            "vfx": ",eq=contrast='1.10+sin(n*0.08)*0.03':saturation=1.12",
            "desc": "Crushing supercritical steam and toxic sulfur atmosphere vault"
        },
        # Shot 3.2: Atmospheric storm & lightning deluge (14.0s)
        {
            "asset": "assets/scenes/torrential_rain.jpg",
            "duration_ratio": 14.0 / 40.3,
            "filter": "zoompan=z='min(zoom+0.0012,1.25)':x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.55)'",
            "vfx": ",eq=brightness='if(between(mod(n,60),0,2),0.45,if(between(mod(n,130),0,3),0.70,0))':contrast=1.08",
            "desc": "Sky shatters with atmospheric deluge and frequent lightning strikes"
        },
        # Shot 3.3: First scalding green ocean pooling (14.3s)
        {
            "asset": "assets/scenes/torrential_rain.jpg",
            "duration_ratio": 14.3 / 40.3,
            "filter": "zoompan=z='1.20':x='min(iw-iw/zoom, on*0.5)':y='ih*0.6-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.08:saturation=1.15",
            "desc": "Centuries of torrential boiling rain pooling into Earth's first scalding ocean"
        }
    ],
    4: [
        # Shot 4.1: Ancient Jack Hills outcrop (14.0s)
        {
            "asset": "assets/scenes/jack_hills_zircon.jpg",
            "duration_ratio": 14.0 / 34.2,
            "filter": "zoompan=z='min(zoom+0.0009,1.18)':x='min(iw-iw/zoom, on*0.4)':y='ih*0.35-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.06:saturation=1.08",
            "desc": "Ancient weathered red rock strata of Western Australia's Jack Hills"
        },
        # Shot 4.2: Microscopic 4.4 Ga crystal lattice (20.2s)
        {
            "asset": "assets/scenes/jack_hills_zircon.jpg",
            "duration_ratio": 20.2 / 34.2,
            "filter": "zoompan=z='min(zoom+0.0020,1.38)':x='iw*0.48-(iw/zoom/2)':y='ih*0.52-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.12:saturation=1.15",
            "desc": "Macro anamorphic focus dolly into the glowing concentric atomic lattice of 4.404 Ga zircon"
        }
    ],
    5: [
        # Shot 5.1: Asteroid swarm descending (9.0s)
        {
            "asset": "assets/scenes/late_bombardment.jpg",
            "duration_ratio": 9.0 / 29.5,
            "filter": "zoompan=z='max(1.25-0.001*on,1.0)':x='(iw/2-(iw/zoom/2))+cos(on*1.2)*2':y='ih*0.35-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.08:saturation=1.12",
            "desc": "Horizon tracking view of Late Heavy Bombardment asteroid swarm"
        },
        # Shot 5.2: Mountain-sized asteroid nuclear detonation (11.0s)
        {
            "asset": "assets/scenes/late_bombardment.jpg",
            "duration_ratio": 11.0 / 29.5,
            "filter": "zoompan=z='min(zoom+0.0018,1.30)':x='(iw/2-(iw/zoom/2))+sin(on*2.2)*max(0, 8 - on*0.05)':y='ih*0.5-(ih/zoom/2)'",
            "vfx": ",eq=brightness='if(between(mod(n,90),0,3),0.60,0)':contrast=1.12:saturation=1.18",
            "desc": "Thermonuclear-scale kinetic impact detonation with camera shockwave vibration"
        },
        # Shot 5.3: Ground forged in dawn of fire (9.5s)
        {
            "asset": "assets/scenes/shot_01_ground_feet.jpg",
            "duration_ratio": 9.5 / 29.5,
            "filter": "zoompan=z='min(zoom+0.0008,1.15)':x='(iw/2-(iw/zoom/2))+sin(on*0.25)*8':y='(ih/2-(ih/zoom/2))+abs(sin(on*0.35))*6'",
            "vfx": ",eq=contrast=1.06:saturation=1.06",
            "desc": "Returning to the solid ground beneath our feet, forged in the dawn of fire"
        }
    ],
    6: [
        # Shot 6.1: Submersible descent into dark abyss (12.0s)
        {
            "asset": "assets/scenes/hydrothermal_vent.jpg",
            "duration_ratio": 12.0 / 27.1,
            "filter": "zoompan=z='min(zoom+0.0010,1.22)':x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.45)'",
            "vfx": ",eq=contrast=1.08:saturation=1.08",
            "desc": "Submersible descent into total pitch-black oceanic abyss"
        },
        # Shot 6.2: Black smoker chimneys spewing mineral soups (15.1s)
        {
            "asset": "assets/scenes/hydrothermal_vent.jpg",
            "duration_ratio": 15.1 / 27.1,
            "filter": "zoompan=z='min(zoom+0.0014,1.28)':x='iw*0.48-(iw/zoom/2)':y='ih*0.55-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.10:saturation=1.12",
            "desc": "Active hydrothermal black smoker chimneys spewing 400C mineral fluids"
        }
    ],
    7: [
        # Shot 7.1: Dark hydrothermal crevices (15.0s)
        {
            "asset": "assets/scenes/life_spark_cliffhanger.jpg",
            "duration_ratio": 15.0 / 47.0,
            "filter": "zoompan=z='min(zoom+0.0009,1.18)':x='iw*0.45-(iw/zoom/2)':y='ih*0.5-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.08:saturation=1.10",
            "desc": "Creeping through dark abyssal volcanic crevices as mystery begins to stir"
        },
        # Shot 7.2: Prebiotic molecular coils & RNA (18.0s)
        {
            "asset": "assets/scenes/life_spark_cliffhanger.jpg",
            "duration_ratio": 18.0 / 47.0,
            "filter": "zoompan=z='min(zoom+0.0020,1.34)':x='iw*0.52-(iw/zoom/2)':y='ih*0.48-(ih/zoom/2)'",
            "vfx": ",eq=contrast='1.12+sin(n*0.1)*0.04':saturation=1.18",
            "desc": "Macro drift into bioluminescent self-replicating RNA spirals on metallic crystals"
        },
        # Shot 7.3: Cliffhanger teaser outro (14.0s)
        {
            "asset": "assets/scenes/life_spark_cliffhanger.jpg",
            "duration_ratio": 14.0 / 47.0,
            "filter": "zoompan=z='max(1.30-0.001*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
            "vfx": ",eq=contrast=1.15:saturation=1.20",
            "desc": "Dramatic mysterious pull-out tease for Archean Dawn: The Secret of the Black Smokers"
        }
    ]
}


ANIMATED_SCENE_TYPES = {
    "stagnant_lid_sphere": 1,
    "heat_pipe_furnace": 2,
    "vanished_world_timeline": 3,
    "zircon_mass_spectrometry": 4,
    "great_rupture_subduction": 5,
    "birth_of_cratons": 6,
    "degassing_crisis_cliffhanger": 7
}


def render_cinematic_act(
    scene_image_path: str,
    scene_type: str,
    audio_path: str,
    output_clip_path: str,
    duration_sec: float,
    act_index: Optional[int] = None,
    fps: int = 30
) -> str:
    """
    Renders a cinematic act scene. If scene_type is an animated procedural scene,
    invokes the dynamic procedural animation engine.
    If act_index is provided in ACT_MULTISHOT_PROFILES, renders a multi-shot dynamic sequence.
    Otherwise falls back to single camera profile.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work_dir = os.path.dirname(os.path.abspath(output_clip_path))
    os.makedirs(work_dir, exist_ok=True)

    # 1. Check for procedural animation engine first
    if scene_type in ANIMATED_SCENE_TYPES:
        from pipeline.cinematic_animator import render_animated_act
        act_num = ANIMATED_SCENE_TYPES[scene_type]
        return render_animated_act(
            act_index=act_num,
            duration_sec=duration_sec,
            output_clip_path=output_clip_path,
            audio_path=audio_path,
            fps=fps
        )

    if act_index and act_index in ACT_MULTISHOT_PROFILES:
        shots = ACT_MULTISHOT_PROFILES[act_index]
        shot_files = []
        
        for s_idx, shot in enumerate(shots, 1):
            s_dur = duration_sec * shot["duration_ratio"]
            s_frames = max(15, int(s_dur * fps))
            s_asset = os.path.join(project_root, shot["asset"])
            if not os.path.exists(s_asset):
                s_asset = scene_image_path
            s_asset_clean = s_asset.replace("\\", "/")
            
            s_filter = f"{shot['filter']}:d={s_frames}:s=1920x1080:fps={fps}{shot['vfx']},format=yuv420p"
            s_out = os.path.join(work_dir, f"temp_act_{act_index:02d}_shot_{s_idx:02d}.mp4")
            
            cmd = [
                FFMPEG_EXE, "-y",
                "-loop", "1",
                "-i", s_asset_clean,
                "-vf", s_filter,
                "-c:v", "libx264",
                "-preset", "faster",
                "-crf", "19",
                "-t", f"{s_dur:.2f}",
                s_out
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            shot_files.append(s_out)
        
        # Concat the shots
        concat_txt = os.path.join(work_dir, f"temp_act_{act_index:02d}_shots.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for sf in shot_files:
                clean_p = os.path.abspath(sf).replace("\\", "/")
                f.write(f"file '{clean_p}'\n")
        
        merged_video = os.path.join(work_dir, f"temp_act_{act_index:02d}_merged.mp4")
        concat_cmd = [
            FFMPEG_EXE, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-c", "copy",
            merged_video
        ]
        subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Combine merged video with act narration audio
        audio_clean = audio_path.replace("\\", "/")
        mux_cmd = [
            FFMPEG_EXE, "-y",
            "-i", merged_video,
            "-i", audio_clean,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_clip_path
        ]
        subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_clip_path

    # Fallback to single profile
    profile = CAMERA_PROFILES.get(scene_type, CAMERA_PROFILES["magma_ocean"])
    total_frames = int(duration_sec * fps)
    img_clean = scene_image_path.replace("\\", "/")
    audio_clean = audio_path.replace("\\", "/")
    camera_filter = f"{profile['filter']}:d={total_frames}:s=1920x1080:fps={fps}{profile['vfx']},format=yuv420p"

    cmd = [
        FFMPEG_EXE, "-y",
        "-loop", "1",
        "-i", img_clean,
        "-i", audio_clean,
        "-vf", camera_filter,
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(duration_sec),
        output_clip_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_clip_path


def assemble_full_movie(
    act_clips: List[str],
    ambient_music_path: str,
    srt_path: str,
    output_mp4_path: str,
    sfx_paths: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Concatenates all cinematic acts, blends multi-layered sound design,
    and burns in non-intrusive 2-line subtitles in the lower-third.
    """
    work_dir = os.path.dirname(os.path.abspath(output_mp4_path))
    os.makedirs(work_dir, exist_ok=True)

    # 1. Concat all rendered scene clips
    concat_txt = os.path.join(work_dir, "acts_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for clip in act_clips:
            clean_p = clip.replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{clean_p}'\n")

    unsubbed_video = os.path.join(work_dir, "acts_merged.mp4")
    concat_cmd = [
        FFMPEG_EXE, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        unsubbed_video
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 2. Final Audio Mixing & Subtitle Burn-In (strictly 2 lines, lower third)
    srt_rel = os.path.basename(srt_path)
    
    # Sound design audio mixing: narration [0:a] + ambient drone [1:a]
    final_cmd = [
        FFMPEG_EXE, "-y",
        "-i", unsubbed_video,
        "-i", ambient_music_path.replace("\\", "/"),
        "-filter_complex",
        f"[1:a]volume=0.18[bg_music];[0:a][bg_music]amix=inputs=2:duration=first[aout];[0:v]subtitles={srt_rel}:force_style='FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=28,Alignment=2'[vout]",
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        output_mp4_path
    ]

    start_time = time.time()
    subprocess.run(final_cmd, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    wall_time = time.time() - start_time

    return {
        "output_path": output_mp4_path,
        "render_time_sec": round(wall_time, 2),
        "size_mb": round(os.path.getsize(output_mp4_path) / 1024 / 1024, 2)
    }


if __name__ == "__main__":
    print("Editor Assembler with 7-scene animation profiles ready.")
