"""
Cinematic 3D Procedural Animation Engine for History of Earth — Episode 7:
"The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss"
Era: Archean: Eoarchean // Pillar: Landscape // Clean Cinematic Master (Zero Burned-in Subtitles)

Major Production Standards:
1. Authentic Archean Geology & Field Investigation Visuals:
   - Act 1: Canadian Shield reconnaissance, sub-arctic tundra, winding dark Acasta River.
   - Act 2: Bedrock outcrop geology expedition, rock hammer scale, S-fold tectonic foliation.
   - Act 3: Petrographic TTG mineralogy (Tonalite-Trondhjemite-Granodiorite) & buoyancy physics.
   - Act 4: Sensitive High Resolution Ion Microprobe (SHRIMP) U-Pb geochronology & oscillatory zircons.
   - Act 5: The Iceland Geodynamic Analogue: Plume-driven low-pressure melting of thick basalt plateau.
   - Act 6: The 4.2 Ga Hafnium Isotopic Ghost: Pre-existing crustal recycling and memory.
   - Act 7: The Unsinkable Cratonic Keel: 250-km deep lithospheric root & transition to LUCA.
2. 100% Genuine Living Motion (Zero Still Frames):
   - Continuous 3D camera pan/tilt/zoom, particle systems, dynamic graphs, and HUD telemetry on every frame.
3. Clean Video Stream:
   - Pristine subtitle-free master video; soft captions exported to en.srt.
"""

import os
import sys
import math
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"

WIDTH = 1920
HEIGHT = 1080
FPS = 30

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "scenes")


def _get_font(size: int, bold: bool = True):
    """Fallback-safe font loader with bold preferences."""
    try:
        font_names = (
            ["segoeuib.ttf", "arialbd.ttf", "consola.ttf", "arial.ttf"]
            if bold
            else ["segoeui.ttf", "arial.ttf", "consola.ttf"]
        )
        for font_name in font_names:
            font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()


def _load_pre_scaled_bg(filename: str, target_w=2304, target_h=1296):
    """Loads and pre-scales background scene plates for smooth 3D camera pan/crop."""
    p = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(p):
        try:
            im = Image.open(p).convert("RGB")
            return im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"  [WARN] Failed to load {filename}: {e}")
    return None


# Pre-cache high-resolution background plates (2304x1296 = 1.2x of 1080p)
BG_ACT_01 = _load_pre_scaled_bg("acasta_river_canadian_tundra.jpg")
BG_ACT_02 = _load_pre_scaled_bg("acasta_outcrop_geology_expedition.jpg")
BG_ACT_03 = _load_pre_scaled_bg("acasta_ttg_gneiss_macro.jpg")
BG_ACT_04 = _load_pre_scaled_bg("shrimp_zircon_acasta_geochronology.jpg")
BG_ACT_05 = _load_pre_scaled_bg("eoarchean_iceland_protocontinent.jpg")
BG_ACT_06 = _load_pre_scaled_bg("hafnium_isotope_crustal_recycling.jpg")
BG_ACT_07 = _load_pre_scaled_bg("slave_craton_lithospheric_keel.jpg")


def draw_hud_card(draw, x, y, w, h, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2, radius=12):
    """Draws a sleek cinematic telemetry HUD glass card with glowing borders."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=border_color, width=border_width)
    c_len = 16
    draw.line([(x, y + c_len), (x, y), (x + c_len, y)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - c_len, y), (x + w, y), (x + w, y + c_len)], fill=(255, 255, 255), width=2)
    draw.line([(x, y + h - c_len), (x, y + h), (x + c_len, y + h)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - c_len, y + h), (x + w, y + h), (x + w, y + h - c_len)], fill=(255, 255, 255), width=2)


def draw_top_series_banner(draw, ep_title="THE FIRST SOLID ROCK • THE 4.03-BILLION-YEAR-OLD ACASTA GNEISS"):
    """Draws standard documentary series watermark & title badge."""
    font_badge = _get_font(18, bold=True)
    font_sub = _get_font(13, bold=False)
    draw_hud_card(draw, 50, 45, 620, 75, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)
    draw.text((72, 57), "HISTORY OF EARTH • EPISODE 7", font=font_badge, fill=(56, 189, 248))
    draw.text((72, 85), ep_title, font=font_sub, fill=(220, 230, 245))


# ==============================================================================================
# ACT RENDERERS (1 through 7)
# ==============================================================================================

def render_act_01_frames(duration_sec: float, fps: int = FPS):
    """Act 1: Canadian Shield reconnaissance, sub-arctic tundra, winding dark Acasta River."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_01 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.05 + 0.35 * prog))
            crop_y = int(max_dy * (0.08 + 0.18 * math.sin(prog * math.pi)))
            cropped = BG_ACT_01.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(25, 30, 42))

        draw = ImageDraw.Draw(img)

        # Dynamic sub-arctic mist & wind sweep lines
        for m_i in range(6):
            my = int(HEIGHT * 0.45 + m_i * 35 + math.sin(t * 1.5 + m_i) * 15)
            mx_start = int((t * 140 + m_i * 320) % (WIDTH + 400) - 300)
            draw.line([(mx_start, my), (mx_start + 180, my)], fill=(180, 205, 230, 90), width=2)

        # Telemetry Card: Canadian Shield Reconnaissance
        px, py = WIDTH - 540, 65
        cw, ch = 490, 420
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)

        draw.text((px + 25, py + 25), "CANADIAN SHIELD SURVEY", font=font_title, fill=(56, 189, 248))
        draw.text((px + 25, py + 58), "SLAVE CRATON • NORTHWEST TERRITORIES", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "LOCATION: ACASTA RIVER VALLEY", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 125), "COORDINATES: 65°10' N, 115°34' W", font=font_data, fill=(255, 255, 255))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(40, 60, 90), width=1)
        draw.text((px + 25, py + 175), "CRATONIC STATUS:", font=font_data, fill=(56, 189, 248))
        draw.text((px + 25, py + 205), "• EARLIEST SURVIVING CONTINENTAL CRUST", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• SURVIVAL RATIO: < 0.001% OF HADEAN CRUST", font=font_small, fill=(239, 68, 68))
        draw.text((px + 25, py + 265), "• AGE: 4.020 - 4.031 BILLION YEARS", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• GLACIAL SCOUR: 2-MILE LAURENTIDE ICE SHEET", font=font_small, fill=(250, 204, 21))

        # Geological Time Progress Bar
        gauge_w = int((cw - 54) * min(1.0, prog * 1.2))
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 365], outline=(56, 189, 248), width=1)
        if gauge_w > 0:
            draw.rectangle([px + 27, py + 347, px + 27 + gauge_w, py + 363], fill=(56, 189, 248))
        draw.text((px + 25, py + 375), f"CONTINENTAL CRUST ACCRETION: {98.8 - prog * 0.4:.1f}% VANISHED", font=font_small, fill=(148, 163, 184))

        draw_top_series_banner(draw, "ACT 1: THE VANISHED CRADLE • EXPEDITION TO THE SLAVE CRATON")
        yield np.array(img)


def render_act_02_frames(duration_sec: float, fps: int = FPS):
    """Act 2: Bedrock outcrop geology expedition, rock hammer scale, S-fold foliation analysis."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_02 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.35 - 0.25 * prog))
            crop_y = int(max_dy * (0.05 + 0.30 * prog))
            cropped = BG_ACT_02.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(35, 38, 45))

        draw = ImageDraw.Draw(img)

        # Dynamic magnifying survey reticle analyzing gneiss outcrop
        rx = int(WIDTH * 0.50 + math.sin(t * 1.2) * 80)
        ry = int(HEIGHT * 0.65 + math.cos(t * 0.9) * 45)
        draw.ellipse([rx - 65, ry - 65, rx + 65, ry + 65], outline=(250, 204, 21), width=2)
        draw.line([(rx - 90, ry), (rx + 90, ry)], fill=(250, 204, 21), width=1)
        draw.line([(rx, ry - 90), (rx, ry + 90)], fill=(250, 204, 21), width=1)

        # Outcrop Telemetry Card (Left)
        px, py = 50, 140
        cw, ch = 520, 430
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(250, 204, 21), border_width=2)

        draw.text((px + 25, py + 25), "BEDROCK GEOLOGY EXPEDITION", font=font_title, fill=(250, 204, 21))
        draw.text((px + 25, py + 58), "BOWRING & WILLIAMS 1999 CONSENSUS", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "FORMATION: ACASTA GNEISS COMPLEX", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "GEOLOGICAL NATURE: INTACT BEDROCK", font=font_data, fill=(56, 189, 248))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(60, 55, 40), width=1)
        draw.text((px + 25, py + 175), "FIELD EVIDENCE & SIGNIFICANCE:", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 205), "• NOT A DETRITAL GRAIN: CONTINUOUS ROCK MASS", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• SURVIVED 4 BILLION YEARS OF OROGENIES", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• FOLIATION: POLYDEFORMED AMPHIBOLITE FACIES", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• CRUSTAL IDENTITY: PROTO-CONTINENTAL EMBRYO", font=font_small, fill=(250, 204, 21))

        # Dynamic sample status
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 375], fill=(30, 45, 65), outline=(56, 189, 248), width=1)
        draw.text((px + 35, py + 352), "STATUS: PEER-REVIEWED OLDEST INTACT ROCK", font=font_data, fill=(74, 222, 128))

        draw_top_series_banner(draw, "ACT 2: EXPEDITION INTO DEEP TIME • DISCOVERY OF INTACT 4.03 Ga BEDROCK")
        yield np.array(img)


def render_act_03_frames(duration_sec: float, fps: int = FPS):
    """Act 3: Petrographic TTG mineralogy (Tonalite-Trondhjemite-Granodiorite) & buoyancy physics."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_03 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.10 + 0.35 * prog))
            crop_y = int(max_dy * (0.25 - 0.15 * math.sin(prog * math.pi)))
            cropped = BG_ACT_03.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(20, 22, 28))

        draw = ImageDraw.Draw(img)

        # Microscopic mineral crosshair grid
        cx, cy = int(WIDTH * 0.48), int(HEIGHT * 0.45)
        for ring_r in [120, 240, 360]:
            draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], outline=(56, 189, 248, 80), width=1)

        # TTG Mineralogy HUD Card (Right)
        px, py = WIDTH - 560, 80
        cw, ch = 510, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(74, 222, 128), border_width=2)

        draw.text((px + 25, py + 25), "PETROGRAPHIC ARCHITECTURE", font=font_title, fill=(74, 222, 128))
        draw.text((px + 25, py + 58), "THE TTG CRATONIC FORMULA", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "SUITE: TONALITE-TRONDHJEMITE-GRANODIORITE", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "DENSITY: 2.70 g/cm³ (BUOYANT CRUST)", font=font_data, fill=(56, 189, 248))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(40, 70, 50), width=1)
        draw.text((px + 25, py + 175), "MINERAL MODAL COMPOSITION:", font=font_data, fill=(74, 222, 128))
        draw.text((px + 25, py + 205), "• PLAGIOCLASE FELDSPAR [NaAlSi3O8]: 55 - 65%", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• QUARTZ [SiO2]: 20 - 30% (SILICA RICH)", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• BIOTITE / AMPHIBOLE: 10 - 15% (MAFIC BANDS)", font=font_small, fill=(250, 204, 21))
        draw.text((px + 25, py + 295), "• BUOYANCY CONTRAST vs BASALT (3.0 g/cm³): +10%", font=font_small, fill=(74, 222, 128))

        # Buoyancy Gauge
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 365], outline=(74, 222, 128), width=1)
        draw.rectangle([px + 27, py + 347, px + int((cw - 54) * 0.90), py + 363], fill=(74, 222, 128))
        draw.text((px + 25, py + 375), "CRUSTAL FLOATING POTENTIAL: PERMANENT", font=font_small, fill=(148, 163, 184))

        draw_top_series_banner(draw, "ACT 3: THE ANATOMY OF THE FIRST ROCK • TTG MOLECULAR PROTOTYPE")
        yield np.array(img)


def render_act_04_frames(duration_sec: float, fps: int = FPS):
    """Act 4: Sensitive High Resolution Ion Microprobe (SHRIMP) U-Pb geochronology & oscillatory zircons."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_04 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.20 + 0.20 * math.sin(prog * math.pi)))
            crop_y = int(max_dy * (0.10 + 0.20 * prog))
            cropped = BG_ACT_04.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(8, 12, 18))

        draw = ImageDraw.Draw(img)

        # Pulsing SHRIMP Primary Ion Beam (oxygen ion pulse on zircon)
        beam_pulse = int((t * 60) % 180)
        bx, by = int(WIDTH * 0.52), int(HEIGHT * 0.44)
        draw.ellipse([bx - beam_pulse, by - beam_pulse, bx + beam_pulse, by + beam_pulse],
                     outline=(255, 60, 60, 90), width=2)

        # Geochronology HUD Card (Left)
        px, py = 50, 140
        cw, ch = 520, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)

        draw.text((px + 25, py + 25), "SHRIMP GEOCHRONOLOGY LAB", font=font_title, fill=(56, 189, 248))
        draw.text((px + 25, py + 58), "U-Pb ISOTOPIC CLOCK DECAY VERIFICATION", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "SYSTEM: 238U -> 206Pb & 235U -> 207Pb", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 125), "CONCORDIA AGE: 4,020 ± 14 MILLION YEARS", font=font_data, fill=(74, 222, 128))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(40, 60, 90), width=1)
        draw.text((px + 25, py + 175), "ZIRCON CRYSTAL ARCHIVE:", font=font_data, fill=(56, 189, 248))
        draw.text((px + 25, py + 205), "• CATHODOLUMINESCENCE: OSCILLATORY MAGMATIC ZONES", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• PROOFS: CRYSTALLIZED IN PRIMARY MAGMA CHAMBER", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• CORE AGE: 4.02 - 4.03 Ga (OLDEST ON EARTH)", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• OVERGROWTHS: 3.75 Ga & 3.40 Ga THERMAL EVENTS", font=font_small, fill=(250, 204, 21))

        # Dynamic decay ratio ticker
        ratio_val = 0.884 + math.sin(t * 2.0) * 0.003
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 375], fill=(20, 30, 48), outline=(56, 189, 248), width=1)
        draw.text((px + 35, py + 352), f"207Pb/206Pb RATIO: {ratio_val:.5f} [CONCORDANT]", font=font_data, fill=(56, 189, 248))

        draw_top_series_banner(draw, "ACT 4: THE SHRIMP ATOMIC CLOCK • 4.02 Ga CONCORDIA DECAY SPECTRUM")
        yield np.array(img)


def render_act_05_frames(duration_sec: float, fps: int = FPS):
    """Act 5: The Iceland Geodynamic Analogue: Plume-driven low-pressure melting of thick basalt plateau."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_05 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.05 + 0.35 * prog))
            crop_y = int(max_dy * (0.15 - 0.10 * math.sin(prog * math.pi)))
            cropped = BG_ACT_05.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(18, 12, 15))

        draw = ImageDraw.Draw(img)

        # Rising magma heat vapor & volcanic sparks
        for sp_i in range(12):
            sp_x = int((WIDTH * 0.30 + sp_i * 70 + t * 45) % (WIDTH * 0.8))
            sp_y = int(HEIGHT * 0.70 - (t * 80 + sp_i * 30) % (HEIGHT * 0.4))
            draw.ellipse([sp_x, sp_y, sp_x + 3, sp_y + 3], fill=(255, 200, 80))

        # Geodynamic Iceland Analogue HUD Card (Right)
        px, py = WIDTH - 560, 80
        cw, ch = 510, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(249, 115, 22), border_width=2)

        draw.text((px + 25, py + 25), "GEODYNAMIC REGIME MODEL", font=font_title, fill=(249, 115, 22))
        draw.text((px + 25, py + 58), "REIMINK ET AL. 2014 (NATURE GEOSCIENCE)", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "TECTONIC SETTING: ICELAND-TYPE PLUME", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "SUBDUCTION STATUS: NONE REQUIRED", font=font_data, fill=(250, 204, 21))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(70, 40, 30), width=1)
        draw.text((px + 25, py + 175), "GEOCHEMICAL DIAGNOSTICS:", font=font_data, fill=(249, 115, 22))
        draw.text((px + 25, py + 205), "• REE PATTERN: FLAT HEAVY RARE-EARTHS (NO GARNET)", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• MELTING DEPTH: SHALLOW (< 30 KM / LOW PRESSURE)", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• MECHANISM: MANTLE PLUME MELTING HYDRATED BASALT", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• RESULT: WORLD'S FIRST GRANITIC PROTOCONTINENT", font=font_small, fill=(250, 204, 21))

        # Magma Flux Gauge
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 365], outline=(249, 115, 22), width=1)
        draw.rectangle([px + 27, py + 347, px + int((cw - 54) * (0.65 + 0.25 * prog)), py + 363], fill=(249, 115, 22))
        draw.text((px + 25, py + 375), "FELSIC CRUST GENERATION: ACTIVE PLUME", font=font_small, fill=(148, 163, 184))

        draw_top_series_banner(draw, "ACT 5: THE ICELAND PROTOCONTINENT • HOW EARTH FORMED CONTINENTS BEFORE PLATES")
        yield np.array(img)


def render_act_06_frames(duration_sec: float, fps: int = FPS):
    """Act 6: The 4.2 Ga Hafnium Isotopic Ghost: Pre-existing crustal recycling and memory."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_06 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.25 - 0.15 * math.sin(prog * math.pi)))
            crop_y = int(max_dy * (0.05 + 0.25 * prog))
            cropped = BG_ACT_06.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 10, 20))

        draw = ImageDraw.Draw(img)

        # Isotopic circulation flows ascending from 4.2 Ga crust to magma chamber
        cx, cy = int(WIDTH * 0.50), int(HEIGHT * 0.42)
        for pulse_i in range(4):
            flow_y = int((cy + 220 - t * 75 - pulse_i * 60) % 280 + cy - 40)
            draw.line([(cx - 80, flow_y), (cx + 80, flow_y)], fill=(56, 189, 248, 110), width=3)

        # Hafnium Isotope HUD Card (Left)
        px, py = 50, 140
        cw, ch = 520, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(168, 85, 247), border_width=2)

        draw.text((px + 25, py + 25), "ISOTOPIC CRUSTAL TRACER", font=font_title, fill=(168, 85, 247))
        draw.text((px + 25, py + 58), "HAFNIUM & NEODYMIUM SYSTEMATICS", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "TRACER: 176Lu -> 176Hf & 147Sm -> 143Nd", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 125), "DISCOVERY: 4.2 - 4.3 Ga PRECURSOR CRUST", font=font_data, fill=(74, 222, 128))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(60, 40, 75), width=1)
        draw.text((px + 25, py + 175), "DEEP-TIME IMPLICATIONS:", font=font_data, fill=(168, 85, 247))
        draw.text((px + 25, py + 205), "• ACASTA WAS NOT BORN FROM PRISTINE MANTLE", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• RE-MELTED 4.2 Ga HADEAN ENRICHED CRUST", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• GEOLOGICAL BRIDGE: HADEAN OCEAN TO ARCHEAN CRUST", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• FIRST PERMANENT CRUSTAL MEMORY CONSERVED", font=font_small, fill=(250, 204, 21))

        # Hafnium Epsilon gauge
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 375], fill=(30, 20, 45), outline=(168, 85, 247), width=1)
        draw.text((px + 35, py + 352), "EPSILON-Hf (4.0 Ga): NEGATIVE [ENRICHED SOURCE]", font=font_data, fill=(168, 85, 247))

        draw_top_series_banner(draw, "ACT 6: THE 4.2-BILLION-YEAR GHOST • HAFNIUM ISOTOPES REVEAL HADEAN PRECURSORS")
        yield np.array(img)


def render_act_07_frames(duration_sec: float, fps: int = FPS):
    """Act 7: The Unsinkable Cratonic Keel: 250-km deep lithospheric root & transition to LUCA."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACT_07 is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.15 + 0.20 * prog))
            crop_y = int(max_dy * (0.05 + 0.15 * math.sin(prog * math.pi)))
            cropped = BG_ACT_07.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(6, 8, 14))

        draw = ImageDraw.Draw(img)

        # Orbital telemetry scan beam rotating over Canadian Shield
        scan_angle = (t * 40) % 360
        rad = math.radians(scan_angle)
        scx, scy = int(WIDTH * 0.50), int(HEIGHT * 0.25)
        draw.line([(scx, scy), (scx + int(math.cos(rad) * 160), scy + int(math.sin(rad) * 160))], fill=(56, 189, 248), width=2)

        # Cratonic Keel Telemetry Card (Right)
        px, py = WIDTH - 560, 80
        cw, ch = 510, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)

        draw.text((px + 25, py + 25), "SLAVE CRATON LITHOSPHERE", font=font_title, fill=(56, 189, 248))
        draw.text((px + 25, py + 58), "THE 250-KILOMETER PROTECTIVE ROOT", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "FEATURE: SUBCONTINENTAL MANTLE KEEL", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "THICKNESS: > 250 KM RIGID LITHOSPHERE", font=font_data, fill=(74, 222, 128))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(40, 60, 90), width=1)
        draw.text((px + 25, py + 175), "CONTINENTAL PRESERVATION SHIELD:", font=font_data, fill=(56, 189, 248))
        draw.text((px + 25, py + 205), "• BUOYANT DEPLETED PERIDOTITE (DIAMOND ROOT)", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• DEFLECTS CONVECTIVE MANTLE THERMAL EROSION", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• PROTECTED ACASTA BEDROCK FOR 4,000,000,000 YEARS", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• NEXT EPISODE: LUCA — THE SINGLE COMMON ANCESTOR", font=font_small, fill=(250, 204, 21))

        # Preservation Integrity Gauge
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 365], outline=(56, 189, 248), width=1)
        draw.rectangle([px + 27, py + 347, px + cw - 27, py + 363], fill=(74, 222, 128))
        draw.text((px + 25, py + 375), "CRATON SURVIVAL STATUS: INDESTRUCTIBLE", font=font_small, fill=(148, 163, 184))

        draw_top_series_banner(draw, "ACT 7: THE UNSINKABLE FORTRESS • HOW CRATONIC KEELS SAVED EARTH'S FIRST ROCK")
        yield np.array(img)


EP7_ACT_RENDERERS = {
    1: render_act_01_frames,
    2: render_act_02_frames,
    3: render_act_03_frames,
    4: render_act_04_frames,
    5: render_act_05_frames,
    6: render_act_06_frames,
    7: render_act_07_frames
}


def render_animated_act_ep7(
    act_index: int,
    duration_sec: float,
    output_clip_path: str,
    audio_path: str = None,
    fps: int = FPS
) -> str:
    """Renders 100% procedural 3D animations streaming directly to FFmpeg rawvideo pipe."""
    work_dir = os.path.dirname(os.path.abspath(output_clip_path))
    os.makedirs(work_dir, exist_ok=True)

    renderer = EP7_ACT_RENDERERS.get(act_index, render_act_01_frames)
    total_frames = int(duration_sec * fps)

    temp_video = os.path.join(work_dir, f"temp_ep7_act_{act_index:02d}_video.mp4")

    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-t", f"{duration_sec:.2f}",
        temp_video
    ]

    t0 = time.time()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for frame in renderer(duration_sec, fps):
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    t1 = time.time()
    elapsed = max(0.01, t1 - t0)
    print(f"  [OK] Rendered Ep7 Act {act_index:02d} ({total_frames} frames, {duration_sec:.1f}s) in {elapsed:.1f}s ({(total_frames/elapsed):.1f} fps)")

    if audio_path and os.path.exists(audio_path):
        mux_cmd = [
            FFMPEG_EXE, "-y",
            "-i", temp_video,
            "-i", audio_path.replace("\\", "/"),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_clip_path
        ]
        subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(temp_video):
            os.remove(temp_video)
        return output_clip_path

    return temp_video


if __name__ == "__main__":
    print("Testing Ep7 Act Renderers (2 frames each)...")
    for a_idx, rnd in EP7_ACT_RENDERERS.items():
        gen = rnd(0.1, 10)
        f_list = list(gen)
        assert len(f_list) == 1, f"Expected 1 frame, got {len(f_list)}"
        assert f_list[0].shape == (1080, 1920, 3), f"Wrong shape: {f_list[0].shape}"
        print(f"  Act {a_idx}: PASS")
    print("All Episode 7 act renderers verified!")
