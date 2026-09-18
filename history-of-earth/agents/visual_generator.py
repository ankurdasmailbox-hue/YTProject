"""
Visual Generator Agent for History of Earth.
Generates multi-layer stylized 2D flat scientific vector illustrations
for parallax scenes adhering strictly to style_bible.json.
"""

import os
from typing import Dict, List, Any
from PIL import Image, ImageDraw

HADEAN_COLORS = {
    "magma": (211, 47, 47),
    "molten_lava": (255, 87, 34),
    "basalt": (33, 33, 33),
    "atmospheric_haze": (78, 52, 46),
    "deep_ocean": (26, 35, 126),
    "steam": (236, 239, 241)
}


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    hex_clean = hex_str.lstrip("#")
    return tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))


def generate_scene_layers(
    shot_id: int,
    output_dir: str,
    segment_type: str = "core_evidence",
    width: int = 2400,
    height: int = 1080
) -> Dict[str, str]:
    """
    Generates Background (RGB), Midground (RGBA), and Foreground (RGBA)
    layers styled specifically for each scene in the Hadean eon.
    """
    os.makedirs(output_dir, exist_ok=True)
    prefix = f"shot_{shot_id:02d}"

    bg_path = os.path.join(output_dir, f"{prefix}_bg.png")
    mg_path = os.path.join(output_dir, f"{prefix}_mg.png")
    fg_path = os.path.join(output_dir, f"{prefix}_fg.png")

    # 1. Background Layer (RGB)
    bg_img = Image.new("RGB", (width, height))
    bg_draw = ImageDraw.Draw(bg_img)
    # Atmospheric gradient
    for y in range(height):
        factor = y / height
        r = int(78 * (1 - factor) + 211 * factor * 0.5)
        g = int(52 * (1 - factor) + 47 * factor * 0.3)
        b = int(46 * (1 - factor) + 47 * factor * 0.2)
        bg_draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Distinct planetary features per segment
    if segment_type == "cold_open":
        # Distant collision / glowing debris cloud
        bg_draw.ellipse([width//2 - 200, 200, width//2 + 200, 600], fill=(255, 120, 50))
    elif segment_type == "editorial_conclusion":
        # Early dark rain clouds parting with golden rim light
        bg_draw.polygon([(0, 400), (600, 250), (1400, 380), (width, 220), (width, height), (0, height)], fill=(40, 30, 45))
    else:
        # Distant volcanic volcanic horizon
        bg_draw.polygon([(0, 550), (450, 380), (900, 580), (1500, 350), (2100, 520), (width, 420), (width, height), (0, height)], fill=(60, 25, 20))
    bg_img.save(bg_path, "PNG")

    # 2. Midground Layer (RGBA with Transparency)
    mg_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    mg_draw = ImageDraw.Draw(mg_img)
    # Churning magma lakes & basalt plateaus
    mg_draw.polygon([(0, 650), (400, 600), (900, 670), (1500, 590), (2000, 680), (width, 610), (width, height), (0, height)], fill=(211, 47, 47, 255))
    # Molten lava rivers
    mg_draw.polygon([(200, 700), (600, 660), (1100, 750), (1700, 690), (width, 780), (width, height), (0, height)], fill=(255, 87, 34, 255))
    # Cooling dark basalt formations
    mg_draw.ellipse([300, 720, 800, 880], fill=(33, 33, 33, 255))
    mg_draw.ellipse([1200, 700, 1800, 920], fill=(33, 33, 33, 255))
    mg_img.save(mg_path, "PNG")

    # 3. Foreground Layer (RGBA with Transparency)
    fg_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(fg_img)
    # Sharp basaltic jagged silhouettes framing viewport
    fg_draw.polygon([(0, 250), (320, 480), (220, 780), (450, height), (0, height)], fill=(20, 18, 18, 255))
    fg_draw.polygon([(width - 350, 320), (width, 520), (width, height), (width - 500, height)], fill=(18, 16, 16, 255))
    # Glowing lava crack on foreground rock
    fg_draw.line([(80, 550), (150, 700), (110, 850)], fill=(255, 100, 40, 255), width=4)
    fg_img.save(fg_path, "PNG")

    return {
        "background": bg_path,
        "midground": mg_path,
        "foreground": fg_path
    }


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "test_visuals")
    layers = generate_scene_layers(1, out_dir, segment_type="cold_open")
    print("Generated layers for Scene 1:")
    for k, v in layers.items():
        print(f"  {k}: {v} (Exists: {os.path.exists(v)})")
