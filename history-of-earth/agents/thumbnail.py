"""
Thumbnail Agent for History of Earth (Upgraded High-CTR A/B Engine).
Adopts YouTube CTR engineering principles:
1. "Obsess Over CTR": Produces 3 tested thumbnail variants with distinct focal angles.
2. Bold, high-contrast typography (2-4 words max, large impact font with drop shadow & stroke).
3. Dramatic curiosity gaps & focal contrast.
4. Top-left era badge for brand recognizability across playlists.
100% Zero-Subscription, Local Python / Pillow.
"""

import os
import math
from typing import Dict, List, Any
from PIL import Image, ImageDraw, ImageFont

DEFAULT_PALETTE = {
    "magma": (220, 38, 38),
    "molten": (249, 115, 22),
    "basalt": (15, 23, 42),
    "deep_space": (10, 15, 30),
    "sky_hell": (45, 15, 10),
    "white": (255, 255, 255),
    "yellow_glow": (250, 204, 21),
    "badge_bg": (2, 132, 199)
}

FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"
FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def get_fonts(main_size: int = 76, sub_size: int = 38, badge_size: int = 24):
    """Loads high-impact bold fonts with graceful fallback."""
    try:
        if os.path.exists(FONT_IMPACT):
            font_main = ImageFont.truetype(FONT_IMPACT, main_size)
        elif os.path.exists(FONT_ARIAL_BOLD):
            font_main = ImageFont.truetype(FONT_ARIAL_BOLD, main_size)
        else:
            font_main = ImageFont.load_default()
    except Exception:
        font_main = ImageFont.load_default()

    try:
        if os.path.exists(FONT_ARIAL_BOLD):
            font_sub = ImageFont.truetype(FONT_ARIAL_BOLD, sub_size)
            font_badge = ImageFont.truetype(FONT_ARIAL_BOLD, badge_size)
        else:
            font_sub = ImageFont.load_default()
            font_badge = ImageFont.load_default()
    except Exception:
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    return font_main, font_sub, font_badge


def draw_text_with_outline(
    draw: ImageDraw.ImageDraw,
    pos: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill_color: tuple[int, int, int] = (255, 255, 255),
    outline_color: tuple[int, int, int] = (0, 0, 0),
    outline_width: int = 5,
    drop_shadow: bool = True
):
    """Draws punchy YouTube thumbnail text with heavy outline and drop shadow."""
    x, y = pos
    if drop_shadow:
        # Drop shadow
        draw.text((x + 6, y + 6), text, font=font, fill=(0, 0, 0, 200))
    # Outline & Main Text
    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill_color,
        stroke_width=outline_width,
        stroke_fill=outline_color
    )


def generate_thumbnails(
    episode_id: str,
    output_dir: str,
    era: str = "HADEAN",
    title_text: str = "NO PLATES?",
    pillar: str = "Map",
    width: int = 1280,
    height: int = 720
) -> List[str]:
    """
    Generates 3 distinct high-CTR thumbnail candidates with varying psychological focal points:
    - Candidate A: The Curiosity Paradox (e.g. 'NO PLATES?')
    - Candidate B: The Catastrophic Rupture (e.g. 'EARTH BROKE')
    - Candidate C: The Forensic Atomic Witness (e.g. '4.4B PROOF')
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_paths = []
    font_main, font_sub, font_badge = get_fonts(main_size=78, sub_size=36, badge_size=24)

    norm_pillar = pillar.strip().lower()
    norm_era = era.strip().lower()

    if "archean" in norm_era or "eoarchean" in norm_era or "acasta" in norm_pillar or "07" in norm_pillar:
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "acasta_gneiss",
                "bg_plate": "acasta_outcrop_geology_expedition.jpg",
                "curiosity_title": "4.03B YR ROCK",
                "subtext": "OLDEST ON EARTH",
                "sub_color": (56, 189, 248)  # Electric Cyan
            },
            {
                "suffix": "candidate_b",
                "focal": "shrimp_spectrometer",
                "bg_plate": "shrimp_zircon_acasta_geochronology.jpg",
                "curiosity_title": "IT SURVIVED?",
                "subtext": "THE FIRST CRUST",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_c",
                "focal": "iceland_rift",
                "bg_plate": "eoarchean_iceland_protocontinent.jpg",
                "curiosity_title": "BEFORE PLATES",
                "subtext": "FIRST CONTINENT",
                "sub_color": (74, 222, 128)  # Bright Emerald
            }
        ]
    elif "ending" in norm_pillar or "bombardment" in norm_pillar:
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "asteroid_impact",
                "bg_plate": "hadean_asteroid_bombardment_ocean.jpg",
                "curiosity_title": "DID LIFE SURVIVE?",
                "subtext": "THE LATE BOMBARDMENT",
                "sub_color": (249, 115, 22)  # Molten orange
            },
            {
                "suffix": "candidate_b",
                "focal": "lunar_cataclysm",
                "bg_plate": "late_bombardment.jpg",
                "curiosity_title": "EARTH BOMBED",
                "subtext": "3.9 BILLION YRS AGO",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_c",
                "focal": "sterilization_paradox",
                "bg_plate": "life_spark_cliffhanger.jpg",
                "curiosity_title": "RESET THE CLOCK?",
                "subtext": "OR SPARKED BIOLOGY",
                "sub_color": (56, 189, 248)  # Electric Cyan
            }
        ]
    elif "leap" in norm_pillar or "zircon" in norm_pillar:
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "zircon_crystal",
                "bg_plate": "jack_hills_zircon.jpg",
                "curiosity_title": "4.4B YEAR CLUE",
                "subtext": "SCIENCE WAS WRONG",
                "sub_color": (56, 189, 248)  # Electric Cyan
            },
            {
                "suffix": "candidate_b",
                "focal": "atomic_clock",
                "bg_plate": "jack_hills_zircon.jpg",
                "curiosity_title": "OLDEST ROCK?",
                "subtext": "THE ZIRCON CODE",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_c",
                "focal": "cool_oceans",
                "bg_plate": "hadean_emerald_sea_surface.jpg",
                "curiosity_title": "COOL OCEANS?",
                "subtext": "4.4 BILLION YRS AGO",
                "sub_color": (74, 222, 128)  # Bright Emerald
            }
        ]
    elif "life" in norm_pillar:
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "alkaline_spire",
                "bg_plate": "hadean_alkaline_vent_towers.jpg",
                "curiosity_title": "DEAD ROCKS?",
                "subtext": "LEARNED TO CODE",
                "sub_color": (56, 189, 248)  # Electric Cyan
            },
            {
                "suffix": "candidate_b",
                "focal": "proton_battery",
                "bg_plate": "hadean_mineral_nanopores_cell.jpg",
                "curiosity_title": "LIFE'S BATTERY",
                "subtext": "FORGED IN STONE",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_c",
                "focal": "first_protocell",
                "bg_plate": "hadean_first_protocell.jpg",
                "curiosity_title": "BEFORE LUCA",
                "subtext": "4.2B YEAR GENESIS",
                "sub_color": (74, 222, 128)  # Emerald green
            }
        ]
    elif "air" in norm_pillar or "ocean" in norm_pillar:
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "emerald_sea",
                "curiosity_title": "GREEN SEA?",
                "subtext": "BOILING IRON WATERS",
                "sub_color": (74, 222, 128)  # Bright emerald green
            },
            {
                "suffix": "candidate_b",
                "focal": "steam_vault",
                "curiosity_title": "POISON SKY",
                "subtext": "200 ATM PRESSURE",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_c",
                "focal": "thousand_year_rain",
                "curiosity_title": "1,000 YR RAIN",
                "subtext": "THE SKY COLLAPSED",
                "sub_color": (56, 189, 248)  # Cyan
            }
        ]
    elif norm_pillar == "map":
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "stagnant_lid",
                "curiosity_title": "NO PLATES?",
                "subtext": "500-MILLION YEAR PRISON",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_b",
                "focal": "the_first_crack",
                "curiosity_title": "EARTH BROKE",
                "subtext": "THE FIRST SUBDUCTION",
                "sub_color": DEFAULT_PALETTE["molten"]
            },
            {
                "suffix": "candidate_c",
                "focal": "zircon_crystal",
                "curiosity_title": "4.4B PROOF",
                "subtext": "SCIENCE WAS WRONG",
                "sub_color": (56, 189, 248)  # Cyan
            }
        ]
    else:
        candidates = [
            {
                "suffix": "candidate_a",
                "focal": "theia_impact",
                "curiosity_title": "PLANET SMASH",
                "subtext": "25,000 MPH COLLISION",
                "sub_color": DEFAULT_PALETTE["yellow_glow"]
            },
            {
                "suffix": "candidate_b",
                "focal": "magma_ocean",
                "curiosity_title": "NO GROUND",
                "subtext": "1,000 KM DEEP LAVA",
                "sub_color": DEFAULT_PALETTE["molten"]
            },
            {
                "suffix": "candidate_c",
                "focal": "zircon_crystal",
                "curiosity_title": "THE FIRST SEA",
                "subtext": "BEFORE WE EXISTED",
                "sub_color": (56, 189, 248)
            }
        ]

    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "scenes")

    for cand in candidates:
        bg_plate_name = cand.get("bg_plate")
        bg_plate_path = os.path.join(assets_dir, bg_plate_name) if bg_plate_name else None
        
        if bg_plate_path and os.path.exists(bg_plate_path):
            base = Image.open(bg_plate_path).convert("RGB")
            base = base.resize((width, height), Image.Resampling.LANCZOS)
            dark_mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            d_draw = ImageDraw.Draw(dark_mask)
            for x_i in range(int(width * 0.75)):
                alpha = int(210 * (1.0 - (x_i / (width * 0.75)) ** 1.5))
                d_draw.line([(x_i, 0), (x_i, height)], fill=(8, 12, 20, alpha))
            img = Image.alpha_composite(base.convert("RGBA"), dark_mask).convert("RGB")
            draw = ImageDraw.Draw(img)
        else:
            img = Image.new("RGB", (width, height), color=DEFAULT_PALETTE["sky_hell"])
            draw = ImageDraw.Draw(img)

            # 1. Atmospheric Gradient
            for y in range(height):
                ratio = y / height
                r = int(25 + 175 * ratio)
                g = int(10 + 45 * ratio)
                b = int(12 + 15 * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Hero Visual Focal Subject
        if cand["focal"] == "emerald_sea":
            # Boiling emerald-green iron waves and dark sulfur horizon
            cx, cy = width - 360, 360
            # Glowing toxic sea disc/horizon
            draw.polygon([(width - 650, 220), (width, 220), (width, height), (width - 650, height)], fill=(16, 85, 55))
            for wave_y in range(240, height, 40):
                draw.line([(width - 650, wave_y), (width, wave_y)], fill=(34, 197, 94), width=4)
                draw.line([(width - 600, wave_y + 10), (width, wave_y + 10)], fill=(74, 222, 128), width=2)
            # Ambient sulfur lightning above waves
            draw.line([(cx, 80), (cx - 40, 180), (cx + 20, 260)], fill=(255, 230, 100), width=6)

        elif cand["focal"] == "steam_vault":
            # Supercritical steam vortex & pressure rings
            cx, cy = width - 360, 300
            for radius, col in [(280, (140, 80, 25)), (220, (180, 110, 35)), (160, (220, 150, 50)), (100, (255, 210, 90))]:
                draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=col, width=8)
            # Pressure core
            draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(255, 120, 30))

        elif cand["focal"] == "thousand_year_rain":
            # Catastrophic lightning & rain deluges
            cx = width - 360
            # Dark storm clouds
            draw.ellipse([cx - 260, 0, cx + 260, 320], fill=(30, 40, 55))
            # Lightning bolts
            draw.line([(cx - 80, 120), (cx - 20, 280), (cx - 100, 450), (cx - 50, height)], fill=(255, 255, 255), width=5)
            draw.line([(cx - 80, 120), (cx - 20, 280), (cx - 100, 450), (cx - 50, height)], fill=(56, 189, 248), width=12)
            # Torrential streaks
            for rx in range(width - 550, width, 25):
                draw.line([(rx, 220), (rx - 30, 550)], fill=(120, 190, 255), width=3)
            # Giant incandescent impact body & shockwave rings
            cx, cy = width - 360, 260
            for radius, col in [(320, (180, 50, 20)), (260, (230, 90, 30)), (200, (255, 160, 40)), (140, (255, 230, 100))]:
                draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=col)
            # Ejecta rays
            for angle_offset in range(-60, 70, 20):
                draw.line([(cx - 100, cy), (cx - 480, cy + angle_offset * 4)], fill=(255, 220, 100), width=6)

        elif cand["focal"] == "stagnant_lid":
            # Planetary sphere locked in glowing tectonic grid
            cx, cy = width - 360, 300
            draw.ellipse([cx - 240, cy - 240, cx + 240, cy + 240], fill=(20, 25, 35), outline=(0, 220, 255), width=6)
            for g_i in range(1, 5):
                draw.arc([cx - 240, cy - 240, cx + 240, cy + 240], start=35 * g_i, end=35 * g_i + 50, fill=(255, 100, 30), width=5)
            # Center lock symbol / thermal glow
            draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(255, 120, 30))

        elif cand["focal"] == "asteroid_impact":
            # Mountain-sized asteroid fireball detonating into ocean
            cx, cy = width - 360, 300
            # Expanding thermal shockwaves
            for r in [280, 220, 160, 100]:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 120, 30, 180), width=4)
            # Incandescent core
            draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(255, 250, 220))
            # Blazing plasma tail streaking from top right
            draw.polygon([(cx, cy), (width, cy - 260), (width, cy - 180)], fill=(255, 80, 20))
            draw.polygon([(cx, cy), (width, cy - 240), (width, cy - 200)], fill=(255, 220, 100))

        elif cand["focal"] == "lunar_cataclysm":
            # Scarred cratered Moon with glowing impact rings
            cx, cy = width - 360, 290
            draw.ellipse([cx - 210, cy - 210, cx + 210, cy + 210], fill=(60, 65, 80), outline=(200, 215, 230), width=5)
            # Imbrium / Serenitatis impact basins with thermal orange glow
            draw.ellipse([cx - 110, cy - 90, cx - 10, cy + 10], fill=(120, 45, 25), outline=(255, 140, 40), width=3)
            draw.ellipse([cx + 20, cy - 40, cx + 110, cy + 50], fill=(100, 40, 20), outline=(255, 160, 50), width=3)
            # Impact ray streaks
            for deg in range(0, 360, 40):
                rad = math.radians(deg)
                draw.line([(cx + int(math.cos(rad) * 90), cy + int(math.sin(rad) * 90)),
                           (cx + int(math.cos(rad) * 190), cy + int(math.sin(rad) * 190))],
                          fill=(180, 195, 210), width=2)

        elif cand["focal"] == "sterilization_paradox":
            # Subterranean geothermal fracture network sheltering life
            cx, cy = width - 350, 310
            draw.ellipse([cx - 220, cy - 220, cx + 220, cy + 220], fill=(15, 25, 40))
            # Glowing cyan/emerald biological hydrothermal channels
            for f_i in range(-3, 4):
                draw.line([(cx + f_i * 45, cy - 180), (cx + f_i * 20, cy), (cx + f_i * 50, cy + 180)],
                          fill=(56, 189, 248), width=5)
                draw.line([(cx + f_i * 45, cy - 180), (cx + f_i * 20, cy), (cx + f_i * 50, cy + 180)],
                          fill=(74, 222, 128), width=2)
            # Protective basalt crust ceiling
            draw.polygon([(cx - 240, cy - 220), (cx + 240, cy - 220), (cx + 240, cy - 130), (cx - 240, cy - 130)],
                         fill=(35, 40, 55))

        elif cand["focal"] == "the_first_crack":
            # Tectonic rupture split with molten abyss
            draw.polygon([(width - 550, 0), (width, 0), (width, height), (width - 550, height)], fill=(25, 30, 40))
            # Glowing jagged rupture fault
            draw.line([(width - 450, 0), (width - 320, 300), (width - 380, height)], fill=(255, 80, 20), width=18)
            draw.line([(width - 450, 0), (width - 320, 300), (width - 380, height)], fill=(255, 255, 180), width=6)

        elif cand["focal"] == "zircon_crystal":
            # Luminescent geometric zircon crystal
            cx, cy = width - 350, 320
            # Ambient crystal aura
            draw.ellipse([cx - 200, cy - 200, cx + 200, cy + 200], fill=(30, 70, 110))
            # Faceted mineral silhouette
            pts = [
                (cx, cy - 220), (cx + 140, cy - 70), (cx + 140, cy + 120),
                (cx, cy + 220), (cx - 140, cy + 120), (cx - 140, cy - 70)
            ]
            draw.polygon(pts, fill=(56, 189, 248), outline=(255, 255, 255), width=4)
            # Internal atomic lattice glow
            draw.line([(cx, cy - 220), (cx, cy + 220)], fill=(255, 255, 255), width=3)
            draw.line([(cx - 140, cy - 70), (cx + 140, cy + 120)], fill=(255, 255, 255), width=2)
            draw.line([(cx - 140, cy + 120), (cx + 140, cy - 70)], fill=(255, 255, 255), width=2)

        else:
            # Magma lake
            draw.polygon([(0, 460), (width//2, 390), (width, 480), (width, height), (0, height)], fill=(225, 45, 15))

        # 3. Basalt Foreground Framing (Cinematic Depth)
        draw.polygon([(0, 380), (400, 560), (280, height), (0, height)], fill=DEFAULT_PALETTE["basalt"])
        draw.polygon([(width - 320, 480), (width, 580), (width, height), (width - 420, height)], fill=DEFAULT_PALETTE["basalt"])

        # 4. Top-Left Era Badge (Brand & Playlist recognition)
        badge_w, badge_h = 240, 56
        draw.rounded_rectangle([45, 45, 45 + badge_w, 45 + badge_h], radius=10, fill=DEFAULT_PALETTE["badge_bg"], outline=(255, 255, 255), width=2)
        draw_text_with_outline(
            draw, (70, 56), f"ERA: {era}", font=font_badge,
            fill_color=(255, 255, 255), outline_width=2, drop_shadow=False
        )

        # 5. Bold Curiosity Title & Subtext
        curiosity_txt = cand["curiosity_title"]
        sub_txt = cand["subtext"]
        sub_col = cand["sub_color"]

        # Main Curiosity Title (Huge 78pt Impact Font)
        draw_text_with_outline(
            draw, (55, 485), curiosity_txt, font=font_main,
            fill_color=DEFAULT_PALETTE["white"], outline_width=6, drop_shadow=True
        )

        # Subtext / Stakes (36pt Arial Bold)
        draw_text_with_outline(
            draw, (58, 585), sub_txt, font=font_sub,
            fill_color=sub_col, outline_width=4, drop_shadow=True
        )

        # Save candidate
        file_path = os.path.join(output_dir, f"{episode_id}_thumb_{cand['suffix']}.png")
        img.save(file_path, "PNG")
        generated_paths.append(file_path)

    return generated_paths


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "test_thumbnails_v2")
    thumbs = generate_thumbnails("hadean_map_02", out, era="HADEAN", pillar="Map")
    print(f"Generated {len(thumbs)} High-CTR Thumbnails in {out}:")
    for t in thumbs:
        print(" ->", t)
