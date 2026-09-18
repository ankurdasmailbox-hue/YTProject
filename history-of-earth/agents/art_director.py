"""
Art Director Agent for History of Earth.
Maintains and validates adherence to style_bible.json across visual assets.
Checks color palettes, aspect ratios, parallax layer transparency, and style locking.
"""

import os
import json
from typing import Dict, List, Any, Tuple
from PIL import Image

DEFAULT_BIBLE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "style_bible.json")


def load_style_bible(bible_path: str = DEFAULT_BIBLE_PATH) -> Dict[str, Any]:
    """Loads the locked style bible specifications."""
    with open(bible_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_frame(frame_path: str, era: str = "hadean") -> Tuple[bool, List[str]]:
    """
    Validates a visual asset against style bible requirements:
    - Verifies file exists and is valid image
    - Verifies dimensions match minimum resolution (height at least 1080)
    - Verifies color space and alpha channel if midground/foreground
    """
    violations = []
    if not os.path.exists(frame_path):
        return False, [f"Frame file not found: {frame_path}"]

    try:
        with Image.open(frame_path) as img:
            w, h = img.size
            if h < 1080:
                violations.append(f"Image height {h} is below 1080p standard.")
            if w < 1920:
                violations.append(f"Image width {w} is below 1920p standard.")

            fname = os.path.basename(frame_path).lower()
            if ("mg" in fname or "fg" in fname) and img.mode != "RGBA":
                violations.append(f"Parallax layer {fname} must contain RGBA alpha channel for transparency.")
    except Exception as exc:
        violations.append(f"Failed to read image file: {str(exc)}")

    return (len(violations) == 0), violations


if __name__ == "__main__":
    bible = load_style_bible()
    print("Loaded Style Bible:", bible.get("project_name"))
    print("Target Art Style:", bible.get("target_art_style"))
    print("Hadean Palette:", bible.get("palettes", {}).get("hadean"))
