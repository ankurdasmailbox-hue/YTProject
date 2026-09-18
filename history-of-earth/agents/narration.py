"""
Narration Agent for History of Earth (Cinematic Acting Engine).
Generates dramatic movie-acting voiceover using SSML (prosody, deliberate pacing, dramatic pauses)
and strictly enforces a 2-line maximum for all on-screen subtitles.
"""

import os
import re
import asyncio
import edge_tts
import subprocess
from typing import Dict, List, Any, Optional

DEFAULT_VOICE = "en-US-ChristopherNeural"


def format_srt_timestamp(seconds: float) -> str:
    """Formats float seconds into standard SRT timestamp hh:mm:ss,ms."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def split_into_two_line_chunks(text: str, max_chars_per_line: int = 38) -> List[str]:
    """
    Splits text into concise subtitle cues strictly formatted as 1 or 2 lines.
    Never exceeds 2 lines per subtitle card.
    """
    # Clean text of markdown or headers
    clean_text = re.sub(r"===.*?===", "", text).strip()
    words = clean_text.split()
    
    cues = []
    current_words = []
    
    for word in words:
        current_words.append(word)
        # Group into ~7-10 words per subtitle cue
        if len(current_words) >= 8 or word.endswith((".", "!", "?", "—", ":")):
            chunk_str = " ".join(current_words)
            # Format chunk into 1 or 2 lines
            if len(chunk_str) <= max_chars_per_line:
                cues.append(chunk_str)
            else:
                # Find midpoint break
                half = len(current_words) // 2
                line1 = " ".join(current_words[:half])
                line2 = " ".join(current_words[half:])
                cues.append(f"{line1}\n{line2}")
            current_words = []

    if current_words:
        chunk_str = " ".join(current_words)
        if len(chunk_str) <= max_chars_per_line:
            cues.append(chunk_str)
        else:
            half = len(current_words) // 2
            line1 = " ".join(current_words[:half])
            line2 = " ".join(current_words[half:])
            cues.append(f"{line1}\n{line2}")

    return cues


async def _generate_cinematic_audio(text: str, voice: str, output_path: str) -> None:
    """
    Renders voice with cinematic acting prosody:
    Measured, resonant delivery with dramatic pauses between sentences.
    """
    # Prepare text with dramatic sentence spacing
    dramatic_text = text.replace(". ", "... ").replace("! ", "... ").replace("—", "... ")
    communicate = edge_tts.Communicate(dramatic_text, voice, rate="-4%", pitch="-1Hz")
    await communicate.save(output_path)


def synthesize_narration(
    script_data: Dict[str, Any],
    output_dir: str,
    voice: str = DEFAULT_VOICE,
    ffmpeg_exe: str = "ffmpeg"
) -> Dict[str, Any]:
    """
    Synthesizes the entire movie script into a high-impact audio narration
    and generates strictly 2-line maximum synchronized subtitles.
    """
    os.makedirs(output_dir, exist_ok=True)
    shot_list = script_data.get("shot_list", [])

    try:
        import imageio_ffmpeg
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_bin = ffmpeg_exe

    scene_audio_paths = []
    srt_cards = []
    current_time_offset = 0.0

    for idx, shot in enumerate(shot_list, 1):
        shot_text = shot["narration_segment"].strip()
        shot_audio_file = os.path.join(output_dir, f"act_{idx:02d}_narration.mp3")

        # Synthesize with cinematic acting
        asyncio.run(_generate_cinematic_audio(shot_text, voice, shot_audio_file))

        # Measure exact audio length
        dur_cmd = [ffmpeg_bin, "-i", shot_audio_file, "-f", "null", "-"]
        proc = subprocess.run(dur_cmd, capture_output=True, text=True)
        dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
        if dur_match:
            h, m, s = dur_match.groups()
            chunk_dur = int(h) * 3600 + int(m) * 60 + float(s)
        else:
            chunk_dur = shot.get("duration_sec", 30.0)

        scene_audio_paths.append(shot_audio_file)

        # Generate strictly 2-line subtitle cards for this act
        cues = split_into_two_line_chunks(shot_text, max_chars_per_line=38)
        time_per_cue = chunk_dur / max(len(cues), 1)

        for c_idx, cue in enumerate(cues):
            start_t = current_time_offset + (c_idx * time_per_cue)
            end_t = start_t + time_per_cue - 0.15
            card_num = len(srt_cards) + 1
            srt_cards.append(
                f"{card_num}\n"
                f"{format_srt_timestamp(start_t)} --> {format_srt_timestamp(end_t)}\n"
                f"{cue}\n"
            )

        current_time_offset += chunk_dur

    # Concatenate all act audio files
    concat_list_file = os.path.join(output_dir, "concat_acts.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for p in scene_audio_paths:
            f.write(f"file '{p.replace(chr(92), '/')}'\n")

    master_audio_path = os.path.join(output_dir, "master_narration.mp3")
    concat_cmd = [
        ffmpeg_bin, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        master_audio_path
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    master_srt_path = os.path.join(output_dir, "en.srt")
    with open(master_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_cards) + "\n")

    return {
        "master_audio_path": master_audio_path,
        "master_srt_path": master_srt_path,
        "total_duration_sec": round(current_time_offset, 2),
        "act_audio_files": scene_audio_paths,
        "total_subtitle_cards": len(srt_cards)
    }


if __name__ == "__main__":
    sample = {
        "shot_list": [
            {
                "narration_segment": "Look at the ground beneath your feet. It feels solid. Permanent. Safe. Four and a half billion years ago, there was no ground.",
                "duration_sec": 12
            }
        ]
    }
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "test_subtitles")
    res = synthesize_narration(sample, out)
    print("SRT Generated:")
    with open(res["master_srt_path"], "r") as f:
        print(f.read())
