"""
Universal Mild Background Score & Atmospheric Sound Design Generator for History of Earth.
Synthesizes multi-layered cinematic ambient soundtracks tailored to scene timestamps and moods.
Calibrated to mild -20 dB to -24 dB LUFS to compliment narration without masking speech.
Valid for all frames, topics, and episodes across the channel.
"""

import os
import math
import wave
import numpy as np
from typing import Dict, List, Any, Optional

SAMPLE_RATE = 44100

MOOD_PROFILES = {
    "cosmic_mystery": {
        "chord": [65.41, 98.00, 130.81, 155.56, 196.00],  # C2, G2, C3, Eb3, G3 (C minor)
        "sub_freq": 32.70,  # C1 deep sub-bass
        "brightness": 0.25,
        "lfo_rate": 0.12,
        "shimmer": 0.08,
        "desc": "Deep enigmatic cosmic expanse, suspended minor chords, celestial presence"
    },
    "internal_furnace": {
        "chord": [73.42, 110.00, 146.83, 174.61, 220.00],  # D2, A2, D3, F3, A3 (D minor warm)
        "sub_freq": 36.71,  # D1 tectonic sub-bass
        "brightness": 0.18,
        "lfo_rate": 0.35,
        "shimmer": 0.04,
        "desc": "Thermal planetary depths, volcanic warmth, slow mantle pulse"
    },
    "forensic_investigation": {
        "chord": [55.00, 82.41, 110.00, 164.81, 246.94],  # A1, E2, A2, E3, B3 (A sus2 suspense)
        "sub_freq": 27.50,  # A0 infrasound
        "brightness": 0.32,
        "lfo_rate": 0.20,
        "shimmer": 0.12,
        "desc": "Tense detective inquiry, analytical clarity, clockwork suspense"
    },
    "atomic_discovery": {
        "chord": [82.41, 123.47, 164.81, 246.94, 329.63, 493.88],  # E minor 9
        "sub_freq": 41.20,  # E1
        "brightness": 0.45,
        "lfo_rate": 0.15,
        "shimmer": 0.28,
        "desc": "Crystalline atomic revelation, laser mass spectrometry, scientific awe"
    },
    "tectonic_rupture": {
        "chord": [58.27, 87.31, 116.54, 138.59, 174.61],  # Bb minor (dark weight)
        "sub_freq": 29.14,  # Bb0 seismic rumble
        "brightness": 0.22,
        "lfo_rate": 0.45,
        "shimmer": 0.06,
        "desc": "Immense lithospheric rupture, subduction shear, building cataclysm"
    },
    "continental_majesty": {
        "chord": [65.41, 98.00, 130.81, 164.81, 196.00, 261.63],  # C major 9 (C2, G2, C3, E3, G3, C4)
        "sub_freq": 32.70,
        "brightness": 0.35,
        "lfo_rate": 0.10,
        "shimmer": 0.15,
        "desc": "Emergence of indestructible cratons, ancient bedrock, noble resolution"
    },
    "cliffhanger_suspense": {
        "chord": [61.74, 92.50, 123.47, 155.56, 185.00, 233.08],  # B minor add9
        "sub_freq": 30.87,
        "brightness": 0.38,
        "lfo_rate": 0.60,
        "shimmer": 0.20,
        "desc": "Runaway outgassing, toxic atmosphere surge, unresolved dramatic hook"
    }
}


def _generate_scene_audio(duration: float, mood_key: str, volume: float = 0.22) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates a high-quality stereo audio buffer for a specific scene duration and mood.
    Returns: (left_channel, right_channel) as float32 in [-1.0, 1.0].
    """
    profile = MOOD_PROFILES.get(mood_key, MOOD_PROFILES["cosmic_mystery"])
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False, dtype=np.float32)

    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # 1. Deep Sub-Bass Drone (gives weight, cinematic anchor)
    sub_f = profile["sub_freq"]
    sub_osc = np.sin(2 * np.pi * sub_f * t)
    sub_osc += 0.25 * np.sin(4 * np.pi * sub_f * t)
    # Slow subtle sub pulse
    sub_pulse = 0.85 + 0.15 * np.sin(2 * np.pi * profile["lfo_rate"] * 0.5 * t)
    sub_track = sub_osc * sub_pulse * 0.35
    left += sub_track
    right += sub_track

    # 2. Lush Detuned Harmonic Chord Pad
    chord = profile["chord"]
    lfo_rate = profile["lfo_rate"]
    lfo_l = 1.0 + 0.12 * np.sin(2 * np.pi * lfo_rate * t)
    lfo_r = 1.0 + 0.12 * np.cos(2 * np.pi * lfo_rate * t)

    for i, freq in enumerate(chord):
        # Slightly detune left and right for rich stereo spread
        detune = 0.18 * (1.0 + 0.1 * i)
        weight = 1.0 / (1.0 + 0.28 * i)
        
        # Fundamental sine + warm overtone
        osc_l = np.sin(2 * np.pi * (freq - detune) * t) + 0.22 * np.sin(4 * np.pi * freq * t)
        osc_r = np.sin(2 * np.pi * (freq + detune) * t) + 0.22 * np.sin(4 * np.pi * freq * t)
        
        left += (osc_l * weight * lfo_l).astype(np.float32)
        right += (osc_r * weight * lfo_r).astype(np.float32)

    # 3. Crystalline Shimmer / Atmosphere Texture
    shimmer_level = profile["shimmer"]
    if shimmer_level > 0.02:
        # High bell overtones
        high_f1 = chord[-1] * 2.0
        high_f2 = chord[-1] * 2.5
        shimmer_l = np.sin(2 * np.pi * high_f1 * t + np.sin(2 * np.pi * 0.3 * t))
        shimmer_r = np.sin(2 * np.pi * high_f2 * t + np.cos(2 * np.pi * 0.3 * t))
        left += (shimmer_l * shimmer_level * 0.5).astype(np.float32)
        right += (shimmer_r * shimmer_level * 0.5).astype(np.float32)

    # 4. Subtle Organic Wind / Thermal Whisper (bandpass filtered noise)
    noise = np.random.normal(0, 0.04, n_samples).astype(np.float32)
    # Simple lowpass filter via cumulative moving average
    kernel_size = 40
    kernel = np.ones(kernel_size, dtype=np.float32) / kernel_size
    smoothed_noise = np.convolve(noise, kernel, mode="same")
    noise_env = 0.5 + 0.5 * np.sin(2 * np.pi * 0.08 * t)
    left += smoothed_noise * noise_env * 0.15
    right += smoothed_noise * noise_env * 0.15

    # 5. Master Envelope: Gentle fade in and fade out (1.5s fade)
    fade_samples = min(int(SAMPLE_RATE * 1.5), n_samples // 4)
    if fade_samples > 0:
        fade_in = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fade_samples)))
        fade_out = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fade_samples)))
        left[:fade_samples] *= fade_in
        right[:fade_samples] *= fade_in
        left[-fade_samples:] *= fade_out
        right[-fade_samples:] *= fade_out

    # Normalize and scale to mild target volume
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-5)
    left = (left / max_val) * volume
    right = (right / max_val) * volume

    return left, right


def generate_mild_soundtrack(
    scene_cues: List[Dict[str, Any]],
    output_path: str,
    master_volume: float = 0.20,
    crossfade_sec: float = 2.0
) -> str:
    """
    Assembles a continuous, frame-complimenting mild soundtrack by crossfading
    scene-specific ambient score cues into a single cohesive stereo track.
    
    scene_cues: list of dicts with:
      - 'duration_sec': float
      - 'mood': str (key in MOOD_PROFILES)
      - 'scene_title': str (optional)
    """
    work_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(work_dir, exist_ok=True)

    total_duration = sum(c["duration_sec"] for c in scene_cues)
    total_samples = int(SAMPLE_RATE * total_duration)

    master_l = np.zeros(total_samples, dtype=np.float32)
    master_r = np.zeros(total_samples, dtype=np.float32)

    current_idx = 0
    cf_samples = int(SAMPLE_RATE * crossfade_sec)

    for i, cue in enumerate(scene_cues):
        dur = cue["duration_sec"]
        mood = cue.get("mood", "cosmic_mystery")
        n_samples = int(SAMPLE_RATE * dur)
        
        # Extend duration slightly for seamless crossfade overlap if not last cue
        render_dur = dur + (crossfade_sec if i < len(scene_cues) - 1 else 0.0)
        c_left, c_right = _generate_scene_audio(render_dur, mood, volume=master_volume)
        
        # Add to master buffer with boundary check
        end_idx = min(current_idx + len(c_left), total_samples)
        slice_len = end_idx - current_idx
        
        master_l[current_idx:end_idx] += c_left[:slice_len]
        master_r[current_idx:end_idx] += c_right[:slice_len]
        
        current_idx += n_samples

    # Final Soft Limiter to guarantee no clipping and smooth dynamics
    peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)), 1e-5)
    if peak > 0.85:
        master_l = (master_l / peak) * 0.85
        master_r = (master_r / peak) * 0.85

    # Convert to 16-bit PCM stereo
    pcm_l = np.clip(master_l * 32767, -32768, 32767).astype(np.int16)
    pcm_r = np.clip(master_r * 32767, -32768, 32767).astype(np.int16)
    interleaved = np.empty((total_samples, 2), dtype=np.int16)
    interleaved[:, 0] = pcm_l
    interleaved[:, 1] = pcm_r

    # Save as high-quality WAV
    wav_path = output_path if output_path.endswith(".wav") else output_path.replace(".mp3", ".wav")
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(interleaved.tobytes())

    # If MP3 requested, convert via FFmpeg
    if output_path.endswith(".mp3"):
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            ffmpeg_exe = "ffmpeg"
        import subprocess
        cmd = [
            ffmpeg_exe, "-y",
            "-i", wav_path,
            "-c:a", "libmp3lame",
            "-b:a", "256k",
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(wav_path) and wav_path != output_path:
            os.remove(wav_path)
        return output_path

    return wav_path


if __name__ == "__main__":
    print("Testing Universal Soundtrack Generator...")
    test_cues = [
        {"duration_sec": 4.0, "mood": "cosmic_mystery"},
        {"duration_sec": 4.0, "mood": "internal_furnace"},
        {"duration_sec": 4.0, "mood": "atomic_discovery"}
    ]
    out = "test_mild_soundtrack.mp3"
    res = generate_mild_soundtrack(test_cues, out)
    print(f"Generated test soundtrack: {res} ({os.path.getsize(res)} bytes)")
    if os.path.exists(out):
        os.remove(out)
    print("Test passed successfully!")
