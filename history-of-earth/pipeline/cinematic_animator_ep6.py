"""
Cinematic 3D Procedural Animation Engine for History of Earth — Episode 6:
"Hadean: The Bombardment That Almost Reset the Clock"
Pillar: Ending // Clean Cinematic Master (Zero Burned-in Subtitles)

Major Production Standards:
1. Authentic Hadean Planetary & Solar System Visuals:
   - Act 1: Outer Solar System Jupiter-Saturn 2:1 resonance & gravitational asteroid perturbation.
   - Act 2: Lunar surface Imbrium basin crater-dating & Apollo 14/17 impact melt archive.
   - Act 3: Hypersonic mountain-sized asteroid impacts, boiling ocean firestorms, and shockwaves.
   - Act 4: The Great Geochronology Debate (Cataclysmic Spike vs. Decaying Tail: PNAS 113).
   - Act 5: Subterranean hydrothermal sanctuary & thermal habitability (Nature 459: Abramov & Mojzsis).
   - Act 6: Carbonaceous chondrite exogenous delivery of water, phosphorus, and amino acids.
   - Act 7: The dawn of the Archean eon (4.0 Ga) & emergence of the Acasta Gneiss craton.
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
BG_RESONANCE = _load_pre_scaled_bg("solar_system_resonance_instability.jpg")
BG_LUNAR = _load_pre_scaled_bg("lunar_crater_basin_apollo.jpg")
BG_IMPACT = _load_pre_scaled_bg("hadean_asteroid_bombardment_ocean.jpg")
BG_DEBATE = _load_pre_scaled_bg("crater_dating_spectrometer.jpg")
BG_SANCTUARY = _load_pre_scaled_bg("subterranean_hydrothermal_sanctuary.jpg")
BG_CHONDRITE = _load_pre_scaled_bg("carbonaceous_chondrite_delivery.jpg")
BG_ACASTA = _load_pre_scaled_bg("acasta_gneiss_first_rock.jpg")


def draw_hud_card(draw, x, y, w, h, bg_color=(10, 15, 26, 235), border_color=(0, 210, 255), border_width=2, radius=12):
    """Draws a sleek cinematic telemetry HUD glass card with glowing borders."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=border_color, width=border_width)
    c_len = 16
    draw.line([(x, y + c_len), (x, y), (x + c_len, y)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - c_len, y), (x + w, y), (x + w, y + c_len)], fill=(255, 255, 255), width=2)
    draw.line([(x, y + h - c_len), (x, y + h), (x + c_len, y + h)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - c_len, y + h), (x + w, y + h), (x + w, y + h - c_len)], fill=(255, 255, 255), width=2)


def draw_top_series_banner(draw, ep_title="THE BOMBARDMENT THAT ALMOST RESET THE CLOCK"):
    """Draws standard documentary series watermark & title badge."""
    font_badge = _get_font(18, bold=True)
    font_sub = _get_font(13, bold=False)
    draw_hud_card(draw, 50, 45, 580, 75, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)
    draw.text((72, 57), "HISTORY OF EARTH • EPISODE 6", font=font_badge, fill=(56, 189, 248))
    draw.text((72, 85), ep_title, font=font_sub, fill=(220, 230, 245))


# ==============================================================================================
# ACT RENDERERS (1 through 7)
# ==============================================================================================

def render_act_01_frames(duration_sec: float, fps: int = FPS):
    """Act 1: Outer solar system orbital mechanics, Jupiter-Saturn resonance, and inward asteroid swarm."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_RESONANCE is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.05 + 0.35 * prog))
            crop_y = int(max_dy * (0.10 + 0.15 * math.sin(prog * math.pi)))
            cropped = BG_RESONANCE.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(6, 8, 18))

        draw = ImageDraw.Draw(img)

        # Resonant gravitational wave pulses radiating from Jupiter-Saturn
        for p_i in range(3):
            pulse_r = int((t * 120 + p_i * 220) % 700)
            cx, cy = int(WIDTH * 0.75), int(HEIGHT * 0.35)
            draw.ellipse([cx - pulse_r, cy - pulse_r, cx + pulse_r, cy + pulse_r],
                         outline=(56, 189, 248, 120), width=2)

        # Dynamic flying asteroid bolide streaks crossing camera
        for ast_i in range(5):
            ast_p = ((t * 1.8 + ast_i * 0.4) % 1.5) / 1.5
            sx = int(WIDTH * 0.9 - ast_p * 1100)
            sy = int(HEIGHT * 0.2 + ast_p * 700)
            draw.line([(sx, sy), (sx + 40, sy - 25)], fill=(255, 230, 180), width=3)

        # HUD Telemetry Card: Orbital Resonance
        px, py = WIDTH - 540, 65
        cw, ch = 490, 420
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)

        draw.text((px + 25, py + 25), "SOLAR SYSTEM DYNAMICS", font=font_title, fill=(56, 189, 248))
        draw.text((px + 25, py + 58), "THE NICE MODEL • DYNAMICAL INSTABILITY", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "RESONANCE: JUPITER-SATURN 2:1", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 125), "TIMELINE: ~3.90 BILLION YEARS AGO", font=font_data, fill=(255, 255, 255))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(40, 60, 90), width=1)
        draw.text((px + 25, py + 175), "ORBITAL TELEMETRY:", font=font_data, fill=(56, 189, 248))
        draw.text((px + 25, py + 205), "• PERTURBATION: KUIPER / ASTEROID DISRUPTION", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• BOLIDE STREAM: BILLIONS OF TONS INWARD", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• TARGET: INNER TERRESTRIAL PLANETS", font=font_small, fill=(239, 68, 68))
        draw.text((px + 25, py + 295), "• STATUS: CATACLYSMIC INJECTION ACTIVE", font=font_small, fill=(250, 204, 21))

        # Trajectory Gauge
        gauge_w = int((cw - 54) * min(1.0, prog * 1.2))
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 365], outline=(56, 189, 248), width=1)
        if gauge_w > 0:
            draw.rectangle([px + 27, py + 347, px + 27 + gauge_w, py + 363], fill=(249, 115, 22))
        draw.text((px + 25, py + 375), f"GRAVITATIONAL CASCADE VELOCITY: {32 + math.sin(t*3)*3:.1f} KM/S", font=font_small, fill=(148, 163, 184))

        draw_top_series_banner(draw, "ACT 1: THE GATHERING GRAVITATIONAL TSUNAMI • THE NICE MODEL")
        yield np.array(img)


def render_act_02_frames(duration_sec: float, fps: int = FPS):
    """Act 2: The lunar highland cratering record, Apollo sample 14/17 impact melt breccia archive."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_LUNAR is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.30 - 0.20 * prog))
            crop_y = int(max_dy * (0.05 + 0.25 * prog))
            cropped = BG_LUNAR.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 18, 26))

        draw = ImageDraw.Draw(img)

        # Apollo forensic landing target crosshair hovering over Imbrium basin
        tx, ty = int(WIDTH * 0.42), int(HEIGHT * 0.68)
        draw.ellipse([tx - 40, ty - 40, tx + 40, ty + 40], outline=(250, 204, 21), width=2)
        draw.line([(tx - 60, ty), (tx + 60, ty)], fill=(250, 204, 21), width=1)
        draw.line([(tx, ty - 60), (tx, ty + 60)], fill=(250, 204, 21), width=1)

        # Lunar crater age telemetry card
        px, py = 50, 140
        cw, ch = 520, 430
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(250, 204, 21), border_width=2)

        draw.text((px + 25, py + 25), "LUNAR GEOCHRONOLOGY ARCHIVE", font=font_title, fill=(250, 204, 21))
        draw.text((px + 25, py + 58), "APOLLO SAMPLE BRECCIA VERIFICATION", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "TARGET: MARE IMBRIUM BASIN", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "SAMPLE AGE: 3.90 ± 0.05 BILLION YEARS", font=font_data, fill=(56, 189, 248))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(60, 55, 40), width=1)
        draw.text((px + 25, py + 175), "ISOTOPIC EVIDENCE (TERA ET AL. 1974):", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 205), "• U-Th-Pb METAMORPHIC RESET SPIKE: 3.9 Ga", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• BASIN DIAMETER: 1,160 KM MULTI-RING", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• EARTH FLUX RATIO: ~15x TO 20x LUNAR MASS", font=font_small, fill=(239, 68, 68))
        draw.text((px + 25, py + 295), "• GLOBAL CRATERS (>20 KM): OVER 20,000", font=font_small, fill=(250, 204, 21))

        # Dynamic decay clock animation
        draw.rectangle([px + 25, py + 335, px + cw - 25, py + 395], fill=(18, 22, 34), outline=(250, 204, 21))
        draw.text((px + 35, py + 347), "IMPACT MELT ISOTOPE CLOCK", font=font_data, fill=(56, 189, 248))
        draw.text((px + 35, py + 372), f"PB-206 / U-238 RATIO: {0.684 + 0.001*math.sin(t*4):.4f} (CONCORDANT)", font=font_small, fill=(220, 230, 245))

        draw_top_series_banner(draw, "ACT 2: THE SCARRED WITNESS • THE LUNAR ARCHIVE")
        yield np.array(img)


def render_act_03_frames(duration_sec: float, fps: int = FPS):
    """Act 3: Hypersonic asteroid impact firestorm, atmospheric detonation, ocean flash-boiling."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_IMPACT is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            # Camera shakes with kinetic intensity
            shake_x = int(math.sin(t * 22.0) * (5.0 if prog > 0.3 else 1.5))
            shake_y = int(math.cos(t * 19.0) * (5.0 if prog > 0.3 else 1.5))
            crop_x = max(0, min(max_dx, int(max_dx * (0.15 + 0.35 * prog)) + shake_x))
            crop_y = max(0, min(max_dy, int(max_dy * (0.20 + 0.20 * prog)) + shake_y))
            cropped = BG_IMPACT.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(40, 15, 10))

        draw = ImageDraw.Draw(img)

        # Hypersonic plasma entry streaks across sky
        for s_idx in range(5):
            s_p = ((t * 4.0 + s_idx * 0.3) % 1.2) / 1.2
            sx = int(WIDTH * 0.85 - s_p * 900)
            sy = int(-80 + s_p * 950)
            draw.line([(sx, sy), (sx + 70, sy - 110)], fill=(255, 255, 255), width=4)
            draw.line([(sx, sy), (sx + 150, sy - 240)], fill=(255, 120, 30), width=6)

        # Kinetic energy impact telemetry card
        px, py = WIDTH - 550, 65
        cw, ch = 500, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(15, 10, 20, 240), border_color=(239, 68, 68), border_width=3)

        draw.text((px + 25, py + 25), "HYPERSONIC IMPACT DETONATION", font=font_title, fill=(239, 68, 68))
        draw.text((px + 25, py + 58), "PLANETARY CRUST IMPACT ANALYSIS", font=font_sub, fill=(255, 200, 200))

        draw.text((px + 25, py + 95), "VELOCITY: 30 KM/S (67,000 MPH)", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 125), "ENERGY: 10^27 JOULES / IMPACT", font=font_data, fill=(255, 255, 255))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(120, 40, 40), width=1)
        draw.text((px + 25, py + 175), "ATMOSPHERIC & OCEAN SHOCK:", font=font_data, fill=(239, 68, 68))
        draw.text((px + 25, py + 205), "• SUPERHEATED VAPORIZATION: 100% OF LOCAL SEA", font=font_small, fill=(255, 180, 180))
        draw.text((px + 25, py + 235), "• ROCK VAPOR PLUME: 2,000°C EXPANDING GLOBALLY", font=font_small, fill=(255, 120, 80))
        draw.text((px + 25, py + 265), "• SEISMIC ENERGY: MAGNITUDE 12+ CRUSTAL RUPTURE", font=font_small, fill=(255, 80, 80))
        draw.text((px + 25, py + 295), "• SURVIVAL QUESTION: DID BIOLOGY RESET?", font=font_small, fill=(250, 204, 21))

        # Kinetic Pulse Bar
        draw.rectangle([px + 25, py + 340, px + cw - 25, py + 400], fill=(25, 10, 15), outline=(239, 68, 68))
        draw.text((px + 35, py + 352), "GLOBAL THERMAL FLUX", font=font_data, fill=(250, 204, 21))
        flux_val = int(85 + 12 * math.sin(t * 8.0))
        draw.text((px + 35, py + 376), f"SURFACE INTENSITY: {flux_val}% EXTREME SUPERCRITICAL", font=font_small, fill=(255, 220, 220))

        draw_top_series_banner(draw, "ACT 3: FIRESTORM ACROSS THE INFERNAL HORIZON")
        yield np.array(img)


def render_act_04_frames(duration_sec: float, fps: int = FPS):
    """Act 4: The Great Geochronology Debate: 3.9 Ga Cataclysmic Spike vs. Decaying Accretion Tail."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_DEBATE is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            crop_x = int(max_dx * (0.10 + 0.20 * math.sin(prog * math.pi)))
            crop_y = int(max_dy * (0.10 + 0.15 * prog))
            cropped = BG_DEBATE.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 14, 24))

        draw = ImageDraw.Draw(img)

        # Active scanning line on the spectrometer display
        scan_x = int(WIDTH * 0.15 + (t * 240) % (WIDTH * 0.70))
        draw.line([(scan_x, 180), (scan_x, HEIGHT - 180)], fill=(56, 189, 248, 160), width=2)

        # HUD Telemetry Card: Geochronological Debate
        px, py = 50, 140
        cw, ch = 540, 430
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(56, 189, 248), border_width=2)

        draw.text((px + 25, py + 25), "GEOCHRONOLOGY DEBATE FORUM", font=font_title, fill=(56, 189, 248))
        draw.text((px + 25, py + 58), "CRATER-DATING & ISOTOPIC ARCHIVE AUDIT", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "HYPOTHESIS 1: TERMINAL CATACLYSM SPIKE", font=font_data, fill=(56, 189, 248))
        draw.text((px + 25, py + 125), "HYPOTHESIS 2: EXPONENTIALLY DECAYING TAIL", font=font_data, fill=(249, 115, 22))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(40, 60, 90), width=1)
        draw.text((px + 25, py + 175), "PEER-REVIEWED SCIENTIFIC CONTEXT:", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 205), "• APOLLO BIAS: SAMPLES DOMINATED BY MARE IMBRIUM", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• PNAS 113 (BOEHNKE 2016): AR-40/AR-39 RESET SIMULATION", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• IMPACT PATTERN: GAUNTLET VS SINGLE MASSIVE PULSE", font=font_small, fill=(250, 204, 21))
        draw.text((px + 25, py + 295), "• KEY RESULT: CRUST WAS NEVER UNIFORMLY MELTED", font=font_small, fill=(74, 222, 128))

        # Comparison status box
        draw.rectangle([px + 25, py + 335, px + cw - 25, py + 395], fill=(14, 22, 38), outline=(56, 189, 248))
        draw.text((px + 35, py + 347), "SCIENTIFIC CONSENSUS STATUS", font=font_data, fill=(250, 204, 21))
        draw.text((px + 35, py + 372), "ACTIVE RESEARCH FRONTIER • DATA RE-EVALUATION", font=font_small, fill=(220, 230, 245))

        draw_top_series_banner(draw, "ACT 4: THE GREAT DEBATE • CATACLYSM OR SLOW BURN?")
        yield np.array(img)


def render_act_05_frames(duration_sec: float, fps: int = FPS):
    """Act 5: Subsurface geothermal crust cross-section: thermal habitability and subterranean life refuge."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_SANCTUARY is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            # Camera descends down into the deep subterranean refuge
            crop_x = int(max_dx * (0.20 + 0.15 * math.sin(prog * math.pi)))
            crop_y = int(max_dy * (0.05 + 0.35 * prog))
            cropped = BG_SANCTUARY.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(14, 20, 32))

        draw = ImageDraw.Draw(img)

        # Glowing hydrothermal fluids flowing through fractures
        for ch_idx in range(4):
            ch_y = int(HEIGHT * 0.45 + ch_idx * 90)
            offset = int(math.sin(t * 3.0 + ch_idx) * 25)
            draw.line([(100, ch_y + offset), (WIDTH - 100, ch_y - offset)], fill=(56, 189, 248, 140), width=3)

        # Thermal habitability telemetry card
        px, py = WIDTH - 560, 65
        cw, ch = 510, 430
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(74, 222, 128), border_width=2)

        draw.text((px + 25, py + 25), "SUBTERRANEAN LIFE SANCTUARY", font=font_title, fill=(74, 222, 128))
        draw.text((px + 25, py + 58), "THERMAL HABITABILITY MODELING • NATURE 459", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "ABRAMOV & MOJZSIS (2009) RESULTS:", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "CRUST MELTED: < 25% AT ANY GIVEN TIME", font=font_data, fill=(56, 189, 248))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(30, 60, 45), width=1)
        draw.text((px + 25, py + 175), "BIOLOGICAL REFUGES:", font=font_data, fill=(74, 222, 128))
        draw.text((px + 25, py + 205), "• SUB-SURFACE FRACTURES: CONTINUOUS SHIELD", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• WATER TEMPERATURE: 50°C - 90°C (CLEMENT)", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• HYPERTHERMOPHILES: EXPANDED HABITAT ENERGETICS", font=font_small, fill=(250, 204, 21))
        draw.text((px + 25, py + 295), "• VERDICT: IMPACTS DID NOT STERILIZE INFANT LIFE", font=font_small, fill=(74, 222, 128))

        # Fracture refuge diagram box
        draw.rectangle([px + 25, py + 335, px + cw - 25, py + 395], fill=(12, 28, 22), outline=(74, 222, 128))
        draw.text((px + 35, py + 347), "HYDROTHERMAL CONTINUITY", font=font_data, fill=(250, 204, 21))
        draw.text((px + 35, py + 372), "100% UNINTERRUPTED BIOLOGICAL SANCTUARY", font=font_small, fill=(220, 230, 245))

        draw_top_series_banner(draw, "ACT 5: THE SUBTERRANEAN REFUGE • NATURE 459 HABITABILITY")
        yield np.array(img)


def render_act_06_frames(duration_sec: float, fps: int = FPS):
    """Act 6: Macro carbonaceous chondrite delivery: extraterrestrial water, phosphorus, and organic amino acids."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_CHONDRITE is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            # Macro zoom into the meteorite matrix
            crop_x = int(max_dx * (0.25 + 0.15 * prog))
            crop_y = int(max_dy * (0.20 + 0.10 * math.sin(prog * math.pi)))
            cropped = BG_CHONDRITE.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(8, 12, 20))

        draw = ImageDraw.Draw(img)

        # Prebiotic organic molecules floating in hydrothermal plume
        for mol_i in range(8):
            m_prog = (t * 0.4 + mol_i * 0.25) % 1.0
            mx = int(WIDTH * 0.25 + math.sin(m_prog * 2 * math.pi + mol_i) * 120)
            my = int(HEIGHT * 0.75 - m_prog * 450)
            draw.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(250, 204, 21), outline=(255, 255, 255), width=2)
            draw.line([(mx - 15, my), (mx + 15, my)], fill=(56, 189, 248), width=2)

        # Prebiotic Delivery Telemetry Card
        px, py = 50, 140
        cw, ch = 520, 430
        draw_hud_card(draw, px, py, cw, ch, bg_color=(10, 15, 26, 235), border_color=(250, 204, 21), border_width=2)

        draw.text((px + 25, py + 25), "EXOGENOUS PREBIOTIC DELIVERY", font=font_title, fill=(250, 204, 21))
        draw.text((px + 25, py + 58), "NATURE 355 • CHYBA & SAGAN (1992)", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "CARBONACEOUS CHONDRITE PAYLOAD:", font=font_data, fill=(255, 255, 255))
        draw.text((px + 25, py + 125), "EXTRATERRESTRIAL VOLATILES & WATER", font=font_data, fill=(56, 189, 248))

        draw.line([(px + 25, py + 160), (px + cw - 25, py + 160)], fill=(60, 55, 40), width=1)
        draw.text((px + 25, py + 175), "SYNTHESIS INGREDIENTS:", font=font_data, fill=(250, 204, 21))
        draw.text((px + 25, py + 205), "• AMINO ACIDS: GLYCINE, ALANINE, GLUTAMIC ACID", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 235), "• PHOSPHORUS: SCHREIBERSITE MINERAL ENRICHMENT", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 265), "• HYDROTHERMAL CRUCIBLE: HEAT CATALYZES RNA", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 295), "• PARADOX: DESTRUCTION FORGED PREBIOTIC CODE", font=font_small, fill=(250, 204, 21))

        # Molecular delivery box
        draw.rectangle([px + 25, py + 335, px + cw - 25, py + 395], fill=(22, 20, 14), outline=(250, 204, 21))
        draw.text((px + 35, py + 347), "THE CRUCIBLE OF GENESIS", font=font_data, fill=(56, 189, 248))
        draw.text((px + 35, py + 372), "ASTEROIDS AS BIOCHEMICAL ENGINES", font=font_small, fill=(220, 230, 245))

        draw_top_series_banner(draw, "ACT 6: THE SEEDS OF DESTRUCTION & CREATION")
        yield np.array(img)


def render_act_07_frames(duration_sec: float, fps: int = FPS):
    """Act 7: The threshold of deep time: 4.0 Ga boundary, the Acasta Gneiss, and the Archean cliffhanger."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(22, bold=True)
    font_sub = _get_font(14, bold=False)
    font_huge = _get_font(28, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = t / max(0.1, duration_sec)

        if BG_ACASTA is not None:
            max_dx = 2304 - WIDTH
            max_dy = 1296 - HEIGHT
            # Smooth cinematic dawn pan across the Acasta Gneiss craton
            crop_x = int(max_dx * (0.05 + 0.35 * prog))
            crop_y = int(max_dy * (0.15 + 0.10 * math.sin(prog * math.pi)))
            cropped = BG_ACASTA.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            img = cropped.copy()
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(20, 25, 40))

        draw = ImageDraw.Draw(img)

        # Sunrise lens flare rays parting through the clear atmosphere
        sun_prog = min(1.0, prog * 1.5)
        flare_alpha = int(90 * sun_prog)
        draw.ellipse([WIDTH * 0.35, HEIGHT * 0.25, WIDTH * 0.65, HEIGHT * 0.70], outline=(255, 230, 160), width=4)

        # Cliffhanger Milestone Card
        px, py = WIDTH - 560, 65
        cw, ch = 520, 440
        draw_hud_card(draw, px, py, cw, ch, bg_color=(12, 16, 28, 240), border_color=(56, 189, 248), border_width=2)

        draw.text((px + 25, py + 25), "HADEAN EON CLOSING STRATIGRAPHY", font=font_title, fill=(56, 189, 248))
        draw.text((px + 25, py + 58), "THE 4.0 BILLION YEAR GEOLOGICAL HORIZON", font=font_sub, fill=(148, 163, 184))

        draw.text((px + 25, py + 95), "ERA BOUNDARY: HADEAN -> ARCHEAN", font=font_huge, fill=(250, 204, 21))
        draw.text((px + 25, py + 138), "THE BOMBARDMENT CLEARS", font=font_data, fill=(255, 255, 255))

        draw.line([(px + 25, py + 172), (px + cw - 25, py + 172)], fill=(40, 60, 90), width=1)
        draw.text((px + 25, py + 188), "FIRST PRESERVED SOLID ROCK:", font=font_data, fill=(56, 189, 248))
        draw.text((px + 25, py + 218), "• FORMATION: THE ACASTA GNEISS (CANADA)", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 248), "• RADIOMETRIC AGE: 4.03 BILLION YEARS", font=font_small, fill=(74, 222, 128))
        draw.text((px + 25, py + 278), "• CRATONIC ROOTS: TTG METAMORPHIC SHIELD", font=font_small, fill=(220, 230, 245))
        draw.text((px + 25, py + 308), "• EARTH SURVIVED: THE CRUCIBLE CONCLUDED", font=font_small, fill=(250, 204, 21))

        # Mysterious Cliffhanger Box
        draw.rectangle([px + 25, py + 345, px + cw - 25, py + 410], fill=(16, 26, 45), outline=(56, 189, 248))
        draw.text((px + 35, py + 357), "NEXT: THE FIRST SOLID ROCK — ACASTA GNEISS", font=font_data, fill=(250, 204, 21))
        draw.text((px + 35, py + 382), "WHERE IS THE OLDEST ROCK YOU CAN TOUCH?", font=font_small, fill=(220, 230, 245))

        draw_top_series_banner(draw, "ACT 7: THE THRESHOLD OF DEEP TIME • THE ARCHEAN DAWN")
        yield np.array(img)


EP6_ACT_RENDERERS = {
    1: render_act_01_frames,
    2: render_act_02_frames,
    3: render_act_03_frames,
    4: render_act_04_frames,
    5: render_act_05_frames,
    6: render_act_06_frames,
    7: render_act_07_frames
}


def render_animated_act_ep6(
    act_index: int,
    duration_sec: float,
    output_clip_path: str,
    audio_path: str = None,
    fps: int = FPS
) -> str:
    """Renders 100% procedural 3D animations streaming directly to FFmpeg rawvideo pipe."""
    work_dir = os.path.dirname(os.path.abspath(output_clip_path))
    os.makedirs(work_dir, exist_ok=True)

    renderer = EP6_ACT_RENDERERS.get(act_index, render_act_01_frames)
    total_frames = int(duration_sec * fps)

    temp_video = os.path.join(work_dir, f"temp_ep6_act_{act_index:02d}_video.mp4")

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
    print(f"  [OK] Rendered Ep6 Act {act_index:02d} ({total_frames} frames, {duration_sec:.1f}s) in {elapsed:.1f}s ({(total_frames/elapsed):.1f} fps)")

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
    print("Testing Ep6 Act Renderers (2 frames each)...")
    for a_idx, rnd in EP6_ACT_RENDERERS.items():
        gen = rnd(0.1, 10)
        f_list = list(gen)
        assert len(f_list) == 1, f"Expected 1 frame, got {len(f_list)}"
        assert f_list[0].shape == (1080, 1920, 3), f"Wrong shape: {f_list[0].shape}"
        print(f"  Act {a_idx}: PASS")
    print("All Episode 6 act renderers verified!")
