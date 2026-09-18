"""
Thumbnail Agent for History of Earth.
Generates high-CTR thumbnail candidates adhering to style_bible.json,
featuring bold subject silhouettes, high-contrast palette, and era badge.
"""

import os
from typing import Dict, List, Any
from PIL import Image, ImageDraw, ImageFont

DEFAULT_PALETTE = {
    "magma": (211, 47, 47),
    "molten": (255, 87, 34),
    "basalt": (20, 20, 20),
    "sky": (50, 20, 15),
    "white": (255, 255, 255),
    "badge_bg": (2, 132, 199)
}


def generate_thumbnails(
    episode_id: str,
    output_dir: str,
    era: str = "HADEAN",
    title_text: str = "NO PLATES",
    pillar: str = "Map",
    width: int = 1280,
    height: int = 720
) -> List[str]:
    """Generates 3 thumbnail candidates with varying compositional focal points."""
    os.makedirs(output_dir, exist_ok=True)
    generated_paths = []

    if pillar.lower() == "map":
        candidates = [
            {"suffix": "candidate_a", "focal": "stagnant_lid", "subtext": "500M YEAR SHELL"},
            {"suffix": "candidate_b", "focal": "the_first_crack", "subtext": "SUBDUCTION AWAKENS"},
            {"suffix": "candidate_c", "focal": "zircon_crystal", "subtext": "ATOMIC WITNESS"}
        ]
    else:
        candidates = [
            {"suffix": "candidate_a", "focal": "magma_ocean", "subtext": "NO SOLID GROUND"},
            {"suffix": "candidate_b", "focal": "theia_impact", "subtext": "THE 4.5B DAWN"},
            {"suffix": "candidate_c", "focal": "zircon_crystal", "subtext": "FIRST WITNESS"}
        ]

    for cand in candidates:
        img = Image.new("RGB", (width, height), color=DEFAULT_PALETTE["sky"])
        draw = ImageDraw.Draw(img)

        # Background gradient
        for y in range(height):
            ratio = y / height
            r = int(50 + 160 * ratio)
            g = int(20 + 40 * ratio)
            b = int(15 + 10 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Distinct graphic illustration based on focal point
        if cand["focal"] == "theia_impact":
            # Giant impacting sphere
            draw.ellipse([width - 500, -100, width + 100, 500], fill=(255, 120, 30))
            draw.ellipse([width - 450, -50, width + 50, 450], fill=(255, 200, 80))
        elif cand["focal"] == "stagnant_lid":
            # Solid sphere with glowing grid
            draw.ellipse([width - 520, 50, width - 40, 530], fill=(30, 35, 45), outline=(0, 200, 255), width=4)
            for g_i in range(1, 4):
                draw.arc([width - 520, 50, width - 40, 530], start=30 * g_i, end=30 * g_i + 45, fill=(255, 120, 40), width=3)
        elif cand["focal"] == "the_first_crack":
            # Fracturing plate with glowing seam
            draw.polygon([(width - 480, 100), (width, 100), (width, 500), (width - 480, 500)], fill=(40, 45, 55))
            draw.line([(width - 400, 100), (width - 240, 300), (width - 320, 500)], fill=(255, 255, 200), width=6)
            draw.line([(width - 400, 100), (width - 240, 300), (width - 320, 500)], fill=(255, 90, 30), width=12)
        elif cand["focal"] == "zircon_crystal":
            # Faceted mineral silhouette
            draw.polygon([(width//2 - 80, 200), (width//2 + 80, 200), (width//2 + 160, 400), (width//2, 550), (width//2 - 160, 400)], fill=(255, 215, 0))
        else:
            # Magma lake silhouette
            draw.polygon([(0, 450), (width//2, 380), (width, 500), (width, height), (0, height)], fill=(220, 60, 20))

        # Basalt foreground framing
        draw.polygon([(0, 350), (350, 500), (250, height), (0, height)], fill=DEFAULT_PALETTE["basalt"])
        draw.polygon([(width - 300, 400), (width, 550), (width, height), (width - 400, height)], fill=DEFAULT_PALETTE["basalt"])

        # Top-left Era Badge
        draw.rounded_rectangle([40, 40, 220, 95], radius=8, fill=DEFAULT_PALETTE["badge_bg"])
        draw.text((60, 52), f"ERA: {era}", fill=(255, 255, 255))

        # Bold Title & Subtext
        # Fallback to default font if custom font not found
        draw.text((50, 520), title_text, fill=(255, 255, 255))
        draw.text((50, 570), cand["subtext"], fill=(255, 220, 50))

        file_path = os.path.join(output_dir, f"{episode_id}_thumb_{cand['suffix']}.png")
        img.save(file_path, "PNG")
        generated_paths.append(file_path)

    return generated_paths


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "test_thumbnails")
    thumbs = generate_thumbnails("hadean_landscape_01", out)
    print(f"Generated {len(thumbs)} thumbnails:")
    for t in thumbs:
        print(" ", t)
