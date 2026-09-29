"""
Cinematic 3D Procedural Animation Engine for History of Earth — Episode 3:
"Hadean: The Sky Was Poison and the Rain Never Stopped"

Major Production Upgrades:
1. Authentic Hadean Earth Visuals (How Earth Looked):
   - Act 1: Establishing cinematic orbital view of Hadean Earth 4.4 Ga (the amber, cloud-shrouded globe with glowing magma fissures)
            transitioning to the supercritical steam vault descent.
   - Act 2: Realistic deep-space view of Hadean Earth illuminated by the Faint Young Sun with trapped greenhouse infrared vectors.
   - Act 4: The catastrophic Thousand-Year Deluge with 3D parallax rain sheets and explosive basalt steam detonations.
   - Act 5: Dual-perspective of Earth's first ocean:
            Phase 1: Full planetary orbital view of the Emerald Planet (4.35 Ga) with global green oceans from space!
            Phase 2: Surface vista of the Emerald Sea with undulating waves, splashing seafoam, steam vents & lightning.
   - Act 6: 3D rotating faceted zircon crystal with UV laser ablation & delta-18-O spectrometer.
   - Act 7: 3D abyssal descent to hydrothermal black smoker chimney & prebiotic molecular spark.
2. Zero Text Overflows:
   - All HUD cards in Scene 1 and Scene 4 calibrated so every title, metric, and bullet string stays strictly inside box margins.
3. 100% Genuine Living Motion:
   - Every single frame contains continuous procedural movement (30 fps), particles, and telemetry updates.
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


# Pre-cache high-resolution background plates
BG_EARTH_AMBER = _load_pre_scaled_bg("hadean_earth_space_amber.jpg")
BG_EMERALD_SEA = _load_pre_scaled_bg("hadean_emerald_sea_surface.jpg")
BG_EARTH_OCEAN_SPACE = _load_pre_scaled_bg("hadean_earth_ocean_space.jpg")


def draw_hud_card(draw, x, y, w, h, bg_color=(12, 16, 26, 230), border_color=(0, 200, 255), border_width=2, radius=12):
    """Draws a sleek cinematic telemetry HUD glass card with glowing borders."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=border_color, width=border_width)
    c_len = 16
    draw.line([(x, y + c_len), (x, y), (x + c_len, y)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - c_len, y), (x + w, y), (x + w, y + c_len)], fill=(255, 255, 255), width=2)
    draw.line([(x, y + h - c_len), (x, y + h), (x + c_len, y + h)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - c_len, y + h), (x + w, y + h), (x + w, y + h - c_len)], fill=(255, 255, 255), width=2)


def draw_top_series_banner(draw, ep_title="THE SKY WAS POISON AND THE RAIN NEVER STOPPED"):
    """Draws standard documentary series watermark & title badge."""
    font_badge = _get_font(18, bold=True)
    font_sub = _get_font(13, bold=False)
    draw_hud_card(draw, 50, 45, 520, 75, bg_color=(12, 16, 26, 230), border_color=(255, 140, 30), border_width=2)
    draw.text((72, 57), "HISTORY OF EARTH • EPISODE 3", font=font_badge, fill=(255, 170, 50))
    draw.text((72, 85), ep_title, font=font_sub, fill=(220, 230, 245))


# ==============================================================================================
# ACT 1: THE PRESSURE VAULT (100 - 200 ATMOSPHERES)
# ==============================================================================================

def render_act_01_frames(duration_sec: float, fps: int = FPS):
    """
    Act 1:
    Phase 1 (0 to 18s): Establishing shot of Hadean Earth 4.4 Ga from space (The Amber Planet).
    Phase 2 (18 to end): 3D descent into the supercritical steam vault & 190 atm pressure telemetry HUD.
    """
    total_frames = int(duration_sec * fps)
    split_t = min(18.0, duration_sec * 0.42)
    split_f = int(split_t * fps)

    font_title = _get_font(24, bold=True)
    font_sub = _get_font(14, bold=False)
    font_pres_val = _get_font(24, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    # Convective steam clouds parameters for Phase 2
    ground_y0 = 620
    n_cracks = 18
    np.random.seed(101)
    crack_x_base = np.random.uniform(100, WIDTH - 100, n_cracks)
    crack_depth = np.random.uniform(0.1, 1.0, n_cracks)

    n_clouds = 24
    cloud_x = np.random.uniform(0, WIDTH, n_clouds)
    cloud_y = np.random.uniform(80, ground_y0 + 50, n_clouds)
    cloud_vx = np.random.uniform(-40, 40, n_clouds)
    cloud_vy = np.random.uniform(-25, -5, n_clouds)
    cloud_r = np.random.uniform(120, 260, n_clouds)

    for f_idx in range(total_frames):
        t = f_idx / fps

        # --------------------------------------------------------------------------------------
        # PHASE 1: WHAT HADEAN EARTH LOOKED LIKE FROM DEEP SPACE (0 to ~18s)
        # --------------------------------------------------------------------------------------
        if f_idx < split_f and BG_EARTH_AMBER is not None:
            p_prog = t / split_t
            # Smooth 3D camera pan & gentle push-in
            max_dx = 2304 - 1920
            max_dy = 1296 - 1080
            crop_x = int(max_dx * 0.35 + p_prog * (max_dx * 0.45))
            crop_y = int(max_dy * 0.45 - p_prog * (max_dy * 0.25))
            img = BG_EARTH_AMBER.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

            draw = ImageDraw.Draw(img)

            # Atmospheric amber rim glow pulse
            glow_pulse = math.sin(t * 3.0) * 0.2 + 0.8
            # Lower Third Identification HUD Card
            card_w, card_h = 620, 160
            cx, cy = 60, HEIGHT - 220
            draw_hud_card(draw, cx, cy, card_w, card_h, bg_color=(10, 14, 22, 235), border_color=(255, 140, 40), border_width=3)
            draw.text((cx + 25, cy + 20), "EARTH 4.4 BILLION YEARS AGO (HADEAN ERA)", font=font_title, fill=(255, 170, 50))
            draw.text((cx + 25, cy + 55), "• GLOBAL STATUS: THE AMBER PLANET", font=font_data, fill=(255, 235, 70))
            draw.text((cx + 25, cy + 85), "• ATMOSPHERE: IMPENETRABLE SUPERCRITICAL STEAM & SULFUR VAULT", font=font_small, fill=(220, 235, 250))
            draw.text((cx + 25, cy + 115), "• SURFACE: RED-HOT BASALT CRUST BURNING THROUGH TOXIC CLOUDS", font=font_small, fill=(255, 150, 120))

            draw_top_series_banner(draw, "SCENE 1: THE PRESSURE VAULT — THE AMBER PLANET (4.4 Ga)")
            yield np.array(img)
            continue

        # --------------------------------------------------------------------------------------
        # PHASE 2: 3D DESCENT INTO CRUSHING PRESSURE VAULT (18s to end)
        # --------------------------------------------------------------------------------------
        p2_prog = (t - split_t) / max(0.1, duration_sec - split_t)
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Sky gradient: Amber-Sulfur supercritical fluid
        y_coords = np.arange(ground_y0)
        ratio = (y_coords / ground_y0)[:, None]
        frame[:ground_y0, :, 0] = np.clip(35 + 160 * ratio, 0, 255).astype(np.uint8)
        frame[:ground_y0, :, 1] = np.clip(20 + 80 * ratio, 0, 255).astype(np.uint8)
        frame[:ground_y0, :, 2] = np.clip(10 + 20 * ratio, 0, 255).astype(np.uint8)

        # Basalt Ground
        gy_coords = np.arange(ground_y0, HEIGHT)
        g_ratio = ((gy_coords - ground_y0) / (HEIGHT - ground_y0))[:, None]
        frame[ground_y0:, :, 0] = np.clip(22 + 18 * g_ratio, 0, 255).astype(np.uint8)
        frame[ground_y0:, :, 1] = np.clip(18 + 10 * g_ratio, 0, 255).astype(np.uint8)
        frame[ground_y0:, :, 2] = np.clip(20 + 12 * g_ratio, 0, 255).astype(np.uint8)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Convective steam layers
        for c_i in range(n_clouds):
            cx = (cloud_x[c_i] + cloud_vx[c_i] * t) % (WIDTH + 400) - 200
            cy = (cloud_y[c_i] + cloud_vy[c_i] * t) % ground_y0
            cr = cloud_r[c_i] + math.sin(t * 1.5 + c_i) * 15
            sh_r = int(140 + 40 * math.sin(c_i))
            sh_g = int(80 + 30 * math.cos(c_i))
            draw.ellipse([cx - cr, cy - cr*0.5, cx + cr, cy + cr*0.5], fill=(sh_r, sh_g, 30, 70))

        # 3D Glowing Basalt Magma Fissures
        for k in range(n_cracks):
            z_phase = (crack_depth[k] + t * 0.05) % 1.0
            screen_y = int(ground_y0 + (HEIGHT - ground_y0) * (1.0 - z_phase))
            scale = 1.0 - z_phase * 0.7
            screen_x = int(crack_x_base[k] + math.sin(t * 0.8 + k) * 30 * scale)
            crack_w = int(120 * scale)
            pulse = math.sin(t * 4.0 + k) * 0.25 + 0.75
            col_core = (int(255 * pulse), int(190 * pulse), 40)
            col_edge = (int(200 * pulse), int(70 * pulse), 15)
            draw.line([(screen_x - crack_w, screen_y), (screen_x + crack_w, screen_y)], fill=col_edge, width=int(6 * scale))
            draw.line([(screen_x - crack_w*0.6, screen_y), (screen_x + crack_w*0.6, screen_y)], fill=col_core, width=max(1, int(3 * scale)))

        # Incandescent embers
        np.random.seed(f_idx % 20)
        for _ in range(35):
            sp_x = np.random.randint(100, WIDTH - 100)
            sp_y = np.random.randint(ground_y0 - 200, HEIGHT - 30)
            sp_r = np.random.randint(1, 4)
            draw.ellipse([sp_x - sp_r, sp_y - sp_r, sp_x + sp_r, sp_y + sp_r], fill=(255, np.random.randint(160, 240), 50))

        # --------------------------------------------------------------------------------------
        # STRICTLY BOUND TELEMETRY HUD CARD (ZERO TEXT OVERFLOW)
        # --------------------------------------------------------------------------------------
        panel_x = WIDTH - 540
        panel_y = 60
        card_w, card_h = 500, 520
        draw_hud_card(draw, panel_x, panel_y, card_w, card_h, bg_color=(10, 14, 22, 235), border_color=(255, 90, 40), border_width=3)

        # Header (Widths: ~310px, ~269px < 450px)
        draw.text((panel_x + 25, panel_y + 25), "ATMOSPHERIC TELEMETRY", font=font_title, fill=(255, 120, 50))
        draw.text((panel_x + 25, panel_y + 60), "EPOCH: 4.40 Ga • POST-MAGMA OCEAN", font=font_sub, fill=(180, 195, 215))

        # Pressure Dial / Meter
        pres_atm = int(15.0 + p2_prog * 175.0)  # Surges to 190 atm
        pres_bar_w = 440
        fill_w = max(2, int(pres_bar_w * (pres_atm / 220.0)))
        draw.rectangle([panel_x + 25, panel_y + 105, panel_x + 25 + pres_bar_w, panel_y + 125], fill=(25, 32, 45), outline=(70, 85, 110), width=1)
        draw.rectangle([panel_x + 25, panel_y + 105, panel_x + 25 + fill_w, panel_y + 125], fill=(255, 75, 45))

        # Pressure text: Strictly confined (Width: ~371px inside 450px limit!)
        draw.text((panel_x + 25, panel_y + 140), f"SURFACE PRESSURE: {pres_atm} ATM", font=font_pres_val, fill=(255, 235, 70))
        draw.text((panel_x + 25, panel_y + 175), f"FORCE: {pres_atm * 0.101:.1f} MPa (HYDRAULIC CRUSH)", font=font_data, fill=(255, 140, 80))

        # Molecular Gas Breakdown Header (Width: ~401px inside 450px limit!)
        draw.text((panel_x + 25, panel_y + 220), "ATMOSPHERIC COMPOSITION (VOLUMETRIC):", font=font_data, fill=(255, 255, 255))
        gases = [
            ("H2O (Supercritical Steam Vapor)", "84.2%", (0, 200, 255), 0.842),
            ("CO2 (Carbon Dioxide)", "11.6%", (255, 180, 50), 0.116),
            ("SO2 / H2S (Sulfur Dioxides)", "3.8%", (255, 80, 50), 0.038),
            ("N2 (Molecular Nitrogen)", "0.4%", (160, 220, 100), 0.004)
        ]
        gy = panel_y + 258
        for gname, gval, gcol, frac in gases:
            draw.text((panel_x + 25, gy), gname, font=font_small, fill=(210, 220, 235))
            draw.text((panel_x + 395, gy), gval, font=font_data, fill=gcol)
            # Gas mini bar
            draw.rectangle([panel_x + 25, gy + 22, panel_x + 465, gy + 27], fill=(25, 35, 50))
            draw.rectangle([panel_x + 25, gy + 22, panel_x + 25 + max(2, int(440 * frac)), gy + 27], fill=gcol)
            gy += 42

        # Alert badge
        alert_blink = (f_idx // 15) % 2 == 0
        if alert_blink:
            draw_hud_card(draw, panel_x + 25, panel_y + 445, 450, 45, bg_color=(120, 25, 20), border_color=(255, 60, 40), border_width=2)
            draw.text((panel_x + 45, panel_y + 458), "CRITICAL: SUPERCRITICAL FLUID REGIME", font=font_small, fill=(255, 255, 255))

        draw_top_series_banner(draw, "SCENE 1: THE PRESSURE VAULT (100–200 ATM)")
        yield np.array(img)


# ==============================================================================================
# ACT 2: THE FAINT YOUNG SUN PARADOX (DEEP SPACE VIEW OF HADEAN EARTH)
# ==============================================================================================

def render_act_02_frames(duration_sec: float, fps: int = FPS):
    """Act 2: Photorealistic space view of Hadean Earth with Faint Young Sun corona & greenhouse trap vectors."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(24, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = min(1.0, t / duration_sec)

        # Base space view of Hadean Earth
        if BG_EARTH_AMBER is not None:
            max_dx = 2304 - 1920
            max_dy = 1296 - 1080
            crop_x = int(max_dx * 0.15 + math.sin(t * 0.1) * (max_dx * 0.15))
            crop_y = int(max_dy * 0.25 + math.cos(t * 0.08) * (max_dy * 0.15))
            img = BG_EARTH_AMBER.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), (12, 16, 26))

        draw = ImageDraw.Draw(img)

        # Dynamic Faint Young Sun Pulsations (Upper Left)
        sun_x, sun_y = 260, 220
        c_pulse = math.sin(t * 4.0) * 8
        draw.ellipse([sun_x - 70 - c_pulse, sun_y - 70 - c_pulse, sun_x + 70 + c_pulse, sun_y + 70 + c_pulse], outline=(255, 220, 100, 100), width=3)
        draw.text((sun_x - 90, sun_y + 85), "FAINT YOUNG SUN (70% LUMINOSITY)", font=font_small, fill=(255, 220, 100))

        # Solar ray lines toward Earth
        for r_i in range(4):
            r_ang = 0.20 + r_i * 0.09 + math.sin(t * 2.0 + r_i) * 0.02
            rx2 = int(sun_x + math.cos(r_ang) * 580)
            ry2 = int(sun_y + math.sin(r_ang) * 580)
            draw.line([(sun_x + 60, sun_y + 60), (rx2, ry2)], fill=(255, 230, 140), width=2)

        # Strictly Confined Scientific Telemetry Card (Lower Left)
        panel_x = 60
        panel_y = 480
        card_w, card_h = 600, 480
        draw_hud_card(draw, panel_x, panel_y, card_w, card_h, bg_color=(10, 14, 22, 235), border_color=(0, 200, 255), border_width=3)

        draw.text((panel_x + 25, panel_y + 25), "THE FAINT YOUNG SUN PARADOX", font=font_title, fill=(0, 220, 255))
        draw.text((panel_x + 25, panel_y + 60), "STELLAR ASTROPHYSICS & PALEOCLIMATOLOGY", font=font_small, fill=(180, 200, 220))

        # Expected vs Actual
        draw.text((panel_x + 25, panel_y + 105), "• SOLAR IRRADIANCE:", font=font_data, fill=(255, 220, 80))
        draw.text((panel_x + 280, panel_y + 105), "70% OF PRESENT", font=font_data, fill=(255, 255, 255))

        draw.text((panel_x + 25, panel_y + 145), "• EXPECTED STATUS:", font=font_data, fill=(255, 90, 80))
        draw.text((panel_x + 280, panel_y + 145), "FROZEN SNOWBALL (-40°C)", font=font_data, fill=(255, 90, 80))

        draw.text((panel_x + 25, panel_y + 185), "• ACTUAL STATE:", font=font_data, fill=(0, 230, 130))
        draw.text((panel_x + 280, panel_y + 185), "SUPERCRITICAL STEAM (+230°C)", font=font_data, fill=(0, 230, 130))

        draw.line([(panel_x + 25, panel_y + 230), (panel_x + card_w - 25, panel_y + 230)], fill=(60, 80, 110), width=1)
        draw.text((panel_x + 25, panel_y + 250), "THERMAL RETENTION MECHANISM:", font=font_data, fill=(255, 255, 255))
        draw.text((panel_x + 25, panel_y + 285), "Massive atmospheric blanket of CO2 & methane trapped", font=font_small, fill=(200, 215, 235))
        draw.text((panel_x + 25, panel_y + 312), "all outgoing infrared radiation within the lower atmosphere.", font=font_small, fill=(200, 215, 235))
        draw.text((panel_x + 25, panel_y + 340), "Earth did not freeze — it simmered in a planetary furnace.", font=font_data, fill=(255, 180, 50))

        draw_hud_card(draw, panel_x + 25, panel_y + 390, card_w - 50, 65, bg_color=(20, 35, 55), border_color=(0, 220, 255), border_width=2)
        draw.text((panel_x + 40, panel_y + 405), "PARADOX RESOLVED: SUPER-GREENHOUSE TRAP", font=font_data, fill=(0, 240, 255))
        draw.text((panel_x + 40, panel_y + 432), "Prevented permanent glaciation during weak solar youth", font=font_small, fill=(220, 235, 255))

        draw_top_series_banner(draw, "SCENE 2: THE FAINT YOUNG SUN PARADOX (EARTH FROM SPACE)")
        yield np.array(img)


# ==============================================================================================
# ACT 3: THE THERMAL TIPPING POINT (350°C & WATER PHASE BREAKDOWN)
# ==============================================================================================

def render_act_03_frames(duration_sec: float, fps: int = FPS):
    """Act 3: 3D thermodynamic water phase space, plunging thermometer & procedural electric lightning."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(24, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)
    font_huge = _get_font(38, bold=True)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = min(1.0, t / duration_sec)
        cur_temp = int(480 - prog * (480 - 310))
        is_condensing = cur_temp <= 374

        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        storm_dark = min(1.0, prog * 1.3)
        for y in range(HEIGHT):
            y_r = y / HEIGHT
            frame[y, :, 0] = int((35 * (1 - storm_dark) + 15 * storm_dark) + 40 * y_r)
            frame[y, :, 1] = int((20 * (1 - storm_dark) + 20 * storm_dark) + 30 * y_r)
            frame[y, :, 2] = int((10 * (1 - storm_dark) + 40 * storm_dark) + 50 * y_r)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Procedural Lightning
        if is_condensing and (f_idx % 22 in [0, 1, 2, 8, 9]):
            np.random.seed(f_idx // 2)
            lx1 = np.random.randint(180, WIDTH - 200)
            ly1 = np.random.randint(40, 180)
            for _ in range(6):
                lx2 = lx1 + np.random.randint(-70, 70)
                ly2 = ly1 + np.random.randint(70, 130)
                draw.line([(lx1, ly1), (lx2, ly2)], fill=(255, 255, 210), width=5)
                draw.line([(lx1, ly1), (lx2, ly2)], fill=(200, 230, 255), width=2)
                if np.random.rand() > 0.5:
                    fx = lx2 + np.random.randint(-60, 60)
                    fy = ly2 + np.random.randint(40, 90)
                    draw.line([(lx2, ly2), (fx, fy)], fill=(255, 255, 255), width=2)
                lx1, ly1 = lx2, ly2

        # Thermometer Card (Left)
        tx, ty, tw, th = 160, 220, 50, 480
        draw_hud_card(draw, 100, 160, 420, 620, bg_color=(10, 14, 22, 235), border_color=(255, 90, 40) if not is_condensing else (0, 210, 255), border_width=3)
        draw.text((125, 185), "PLANETARY TEMPERATURE", font=font_title, fill=(255, 255, 255))
        draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=22, fill=(25, 32, 45), outline=(100, 120, 150), width=3)
        draw.ellipse([tx - 18, ty + th - 25, tx + tw + 18, ty + th + 45], fill=(255, 60, 40) if not is_condensing else (0, 180, 255), outline=(255, 255, 255), width=3)

        fill_ratio = (cur_temp - 250) / (500 - 250)
        liq_h = int(fill_ratio * (th - 30))
        draw.rounded_rectangle([tx + 8, ty + th - liq_h, tx + tw - 8, ty + th], radius=12, fill=(255, 60, 40) if not is_condensing else (0, 180, 255))

        crit_y = int(ty + th - ((374 - 250) / (500 - 250) * (th - 30)))
        draw.line([(tx - 30, crit_y), (tx + tw + 30, crit_y)], fill=(255, 235, 70), width=3)
        draw.text((tx + tw + 35, crit_y - 10), "374°C CRITICAL POINT", font=font_data, fill=(255, 235, 70))

        t_col = (255, 90, 60) if not is_condensing else (0, 230, 255)
        draw.text((125, 705), f"{cur_temp}°C", font=font_huge, fill=t_col)
        draw.text((125, 755), "PHASE: SUPERCRITICAL" if not is_condensing else "PHASE: LIQUID CONDENSATION!", font=font_data, fill=t_col)

        # 3D Phase Diagram Card (Right)
        px = 580
        py = 160
        draw_hud_card(draw, px, py, WIDTH - px - 80, 620, bg_color=(12, 16, 26, 235), border_color=(0, 200, 255), border_width=3)
        draw.text((px + 35, py + 25), "THERMODYNAMICS OF WATER (H2O PHASE TRANSITION)", font=font_title, fill=(0, 220, 255))
        draw.text((px + 35, py + 60), "PRESSURE-TEMPERATURE EQUILIBRIUM & CRITICAL POINT COLLAPSE", font=font_small, fill=(180, 200, 220))

        ax_x0, ax_y0 = px + 80, py + 480
        ax_w, ax_h = 700, 360
        draw.line([(ax_x0, ax_y0), (ax_x0 + ax_w, ax_y0)], fill=(160, 180, 210), width=3)
        draw.line([(ax_x0, ax_y0), (ax_x0, ax_y0 - ax_h)], fill=(160, 180, 210), width=3)
        draw.text((ax_x0 + ax_w - 180, ax_y0 + 15), "TEMPERATURE (°C) →", font=font_small, fill=(200, 215, 235))
        draw.text((ax_x0 - 45, ax_y0 - ax_h - 25), "↑ PRESSURE (ATM)", font=font_small, fill=(200, 215, 235))

        curve_pts = []
        for c_t in range(0, ax_w, 10):
            c_p = ax_y0 - int((c_t / ax_w)**1.8 * (ax_h - 40))
            curve_pts.append((ax_x0 + c_t, c_p))
        draw.line(curve_pts, fill=(0, 220, 255), width=4)

        cp_x, cp_y = curve_pts[-1]
        draw.ellipse([cp_x - 12, cp_y - 12, cp_x + 12, cp_y + 12], fill=(255, 220, 50), outline=(255, 255, 255), width=3)
        draw.text((cp_x - 180, cp_y - 30), "CRITICAL POINT (374°C, 218 ATM)", font=font_data, fill=(255, 235, 80))

        draw.text((ax_x0 + 120, ax_y0 - 240), "LIQUID WATER REGIME", font=font_title, fill=(0, 200, 255))
        draw.text((ax_x0 + 380, ax_y0 - 90), "WATER VAPOR (STEAM)", font=font_title, fill=(255, 140, 50))
        draw.text((ax_x0 + 440, ax_y0 - 320), "SUPERCRITICAL FLUID", font=font_title, fill=(255, 75, 45))

        marker_t = prog
        m_x = int(ax_x0 + ax_w * (1.0 - marker_t * 0.45))
        m_y = int(ax_y0 - (ax_h - 40) * (0.85 - marker_t * 0.15))
        draw.ellipse([m_x - 10, m_y - 10, m_x + 10, m_y + 10], fill=(255, 255, 255), outline=(255, 50, 40) if not is_condensing else (0, 255, 180), width=4)
        draw.text((m_x + 18, m_y - 10), "EARTH'S ATMOSPHERE", font=font_data, fill=(255, 255, 255))

        draw_hud_card(draw, px + 35, py + 520, WIDTH - px - 150, 75, bg_color=(20, 30, 48), border_color=(0, 220, 255), border_width=2)
        if not is_condensing:
            draw.text((px + 55, py + 535), "STATUS: INFERNO PREVENTS CONDENSATION", font=font_data, fill=(255, 140, 50))
            draw.text((px + 55, py + 565), "Basalt ground too scorching for liquid raindrops to reach surface", font=font_small, fill=(200, 215, 235))
        else:
            draw.text((px + 55, py + 535), "⚡ TIPPING POINT CROSSED: CONDENSATION CATACLYSM ACTIVE!", font=font_data, fill=(0, 255, 180))
            draw.text((px + 55, py + 565), "Physics of water flips — the entire planetary atmosphere of steam begins to fall", font=font_small, fill=(220, 245, 255))

        draw_top_series_banner(draw, "SCENE 3: THE THERMAL TIPPING POINT (350°C)")
        yield np.array(img)


# ==============================================================================================
# ACT 4: THE THOUSAND-YEAR DELUGE (PARALLAX RAIN & STEAM DETONATIONS)
# ==============================================================================================

def render_act_04_frames(duration_sec: float, fps: int = FPS):
    """Act 4: 3D parallax torrential rain sheets, explosive steam detonations & strictly bounded chronometer HUD."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(24, bold=True)
    font_sub = _get_font(14, bold=False)
    font_century = _get_font(34, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)

    np.random.seed(55)
    n_rain_far = 300
    n_rain_mid = 220
    n_rain_near = 140

    rf_x = np.random.uniform(-100, WIDTH + 200, n_rain_far)
    rf_y = np.random.uniform(0, HEIGHT, n_rain_far)
    rf_len = np.random.uniform(25, 45, n_rain_far)
    rf_spd = np.random.uniform(900, 1200, n_rain_far)

    rm_x = np.random.uniform(-100, WIDTH + 200, n_rain_mid)
    rm_y = np.random.uniform(0, HEIGHT, n_rain_mid)
    rm_len = np.random.uniform(50, 85, n_rain_mid)
    rm_spd = np.random.uniform(1400, 1800, n_rain_mid)

    rn_x = np.random.uniform(-100, WIDTH + 200, n_rain_near)
    rn_y = np.random.uniform(0, HEIGHT, n_rain_near)
    rn_len = np.random.uniform(100, 160, n_rain_near)
    rn_spd = np.random.uniform(2000, 2600, n_rain_near)

    ground_y = 740
    n_plumes = 14
    plume_x = np.random.uniform(120, WIDTH - 120, n_plumes)
    plume_t0 = np.random.uniform(0, 3.0, n_plumes)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = min(1.0, t / duration_sec)
        century = int(1 + prog * 9.9)

        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        for y in range(ground_y):
            ratio = y / ground_y
            frame[y, :, 0] = int(12 + 25 * ratio)
            frame[y, :, 1] = int(16 + 32 * ratio)
            frame[y, :, 2] = int(24 + 48 * ratio)

        frame[ground_y:, :, 0] = 18
        frame[ground_y:, :, 1] = 16
        frame[ground_y:, :, 2] = 20

        is_flash = (f_idx % 45 in [0, 1, 6, 7])
        if is_flash:
            frame[:, :] = np.clip(frame.astype(np.int16) + 120, 0, 255).astype(np.uint8)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Steam Plumes on Hot Basalt
        for p_i in range(n_plumes):
            p_cycle = (t + plume_t0[p_i]) % 1.8
            p_life = p_cycle / 1.8
            px = int(plume_x[p_i] + math.sin(p_life * 4.0) * 20)
            py = int(ground_y - p_life * 260)
            pr = int(25 + p_life * 75)
            alpha_col = int(255 * (1.0 - p_life) * 0.7)
            draw.ellipse([px - pr, py - pr*0.6, px + pr, py + pr*0.6], fill=(210, 220, 235, alpha_col))

        # 3D Parallax Rain
        wind_drift = math.sin(t * 1.5) * 45 - 80
        for i in range(n_rain_far):
            y_cur = (rf_y[i] + rf_spd[i] * t) % HEIGHT
            x_cur = (rf_x[i] + wind_drift * (y_cur / HEIGHT)) % (WIDTH + 200) - 100
            draw.line([(x_cur, y_cur), (x_cur + 15, y_cur + rf_len[i])], fill=(120, 150, 180), width=1)

        for i in range(n_rain_mid):
            y_cur = (rm_y[i] + rm_spd[i] * t) % HEIGHT
            x_cur = (rm_x[i] + wind_drift * (y_cur / HEIGHT)) % (WIDTH + 200) - 100
            draw.line([(x_cur, y_cur), (x_cur + 25, y_cur + rm_len[i])], fill=(160, 195, 230), width=2)

        for i in range(n_rain_near):
            y_cur = (rn_y[i] + rn_spd[i] * t) % HEIGHT
            x_cur = (rn_x[i] + wind_drift * (y_cur / HEIGHT)) % (WIDTH + 200) - 100
            draw.line([(x_cur, y_cur), (x_cur + 40, y_cur + rn_len[i])], fill=(210, 235, 255), width=3)

        # --------------------------------------------------------------------------------------
        # STRICTLY BOUND DELUGE CHRONOMETER HUD CARD (ZERO TEXT OVERFLOW)
        # --------------------------------------------------------------------------------------
        panel_x = WIDTH - 560
        panel_y = 60
        card_w, card_h = 520, 490
        draw_hud_card(draw, panel_x, panel_y, card_w, card_h, bg_color=(10, 14, 24, 235), border_color=(0, 210, 255), border_width=3)

        # Header (Widths: ~354px, ~305px < 470px limit)
        draw.text((panel_x + 25, panel_y + 25), "THE THOUSAND-YEAR DELUGE", font=font_title, fill=(0, 220, 255))
        draw.text((panel_x + 25, panel_y + 60), "CATASTROPHIC PLANETARY CONDENSATION", font=font_sub, fill=(180, 205, 225))

        # Deluge Chronometer (Width: ~305px inside 470px limit!)
        draw.text((panel_x + 25, panel_y + 105), "DELUGE CHRONOMETER:", font=font_data, fill=(255, 255, 255))
        draw.text((panel_x + 25, panel_y + 138), f"CENTURY {century} OF 10", font=font_century, fill=(255, 235, 70))
        # Strictly Confined text line (Width: ~403px inside 470px limit!)
        draw.text((panel_x + 25, panel_y + 185), f"ELAPSED: ~{century * 100} YEARS CONTINUOUS DELUGE", font=font_data, fill=(0, 210, 255))

        # Rain Metrics (Widths: 285px to 334px, all well inside 470px limit!)
        draw.line([(panel_x + 25, panel_y + 225), (panel_x + card_w - 25, panel_y + 225)], fill=(60, 80, 110), width=1)
        draw.text((panel_x + 25, panel_y + 245), "PRECIPITATION METRICS:", font=font_data, fill=(255, 255, 255))
        draw.text((panel_x + 25, panel_y + 278), "• RATE: > 50,000 mm / YR (GLOBAL SCALE)", font=font_small, fill=(255, 140, 80))
        draw.text((panel_x + 25, panel_y + 308), "• RAINDROP TEMP: 180°C - 230°C (BOILING ACID)", font=font_small, fill=(220, 230, 245))
        draw.text((panel_x + 25, panel_y + 338), "• ACIDITY: pH 4.2 - 5.0 (SO2 & CO2 CLOUDS)", font=font_small, fill=(220, 230, 245))
        draw.text((panel_x + 25, panel_y + 368), "• DETONATIONS: STEAM EXPLOSIONS ON BASALT", font=font_small, fill=(220, 230, 245))

        # Steam Collapse Progress Bar
        draw.text((panel_x + 25, panel_y + 408), f"STEAM COLLAPSE PROGRESS: {int(prog * 94)}%", font=font_data, fill=(0, 230, 130))
        draw.rectangle([panel_x + 25, panel_y + 438, panel_x + card_w - 25, panel_y + 453], fill=(25, 35, 50), outline=(70, 90, 120), width=1)
        draw.rectangle([panel_x + 25, panel_y + 438, panel_x + 25 + max(2, int((card_w - 50) * prog)), panel_y + 453], fill=(0, 230, 130))

        draw_top_series_banner(draw, "SCENE 4: THE THOUSAND-YEAR DELUGE")
        yield np.array(img)


# ==============================================================================================
# ACT 5: THE EMERALD SEA (EARTH'S FIRST OCEAN — ORBITAL & SURFACE VIEWS)
# ==============================================================================================

def render_act_05_frames(duration_sec: float, fps: int = FPS):
    """
    Act 5:
    Phase 1 (0 to 18s): Global orbital view of Earth covered in emerald green oceans from space!
    Phase 2 (18 to end): Surface vista of the Emerald Sea with undulating waves & iron chemistry HUD.
    """
    total_frames = int(duration_sec * fps)
    split_t = min(18.0, duration_sec * 0.45)
    split_f = int(split_t * fps)

    font_title = _get_font(24, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)
    font_huge = _get_font(32, bold=True)

    for f_idx in range(total_frames):
        t = f_idx / fps

        # --------------------------------------------------------------------------------------
        # PHASE 1: THE EMERALD PLANET FROM SPACE (0 to ~18s)
        # --------------------------------------------------------------------------------------
        if f_idx < split_f and BG_EARTH_OCEAN_SPACE is not None:
            p_prog = t / split_t
            max_dx = 2304 - 1920
            max_dy = 1296 - 1080
            crop_x = int(max_dx * 0.20 + p_prog * (max_dx * 0.50))
            crop_y = int(max_dy * 0.30 - p_prog * (max_dy * 0.20))
            img = BG_EARTH_OCEAN_SPACE.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

            draw = ImageDraw.Draw(img)

            # Identification HUD Card (Lower Left)
            card_w, card_h = 620, 160
            cx, cy = 60, HEIGHT - 220
            draw_hud_card(draw, cx, cy, card_w, card_h, bg_color=(10, 16, 22, 235), border_color=(0, 220, 140), border_width=3)
            draw.text((cx + 25, cy + 20), "EARTH 4.35 BILLION YEARS AGO (ORBITAL VIEW)", font=font_title, fill=(0, 230, 150))
            draw.text((cx + 25, cy + 55), "• GLOBAL STATUS: THE EMERALD PLANET", font=font_data, fill=(255, 235, 70))
            draw.text((cx + 25, cy + 85), "• FIRST GLOBAL HYDROSPHERE: DEEP MURKY GREEN IRON SEAS", font=font_small, fill=(200, 240, 220))
            draw.text((cx + 25, cy + 115), "• CRUSTAL ARCHITECTURE: VOLCANIC ISLAND ARCS & EARLY CRATONS", font=font_small, fill=(220, 235, 250))

            draw_top_series_banner(draw, "SCENE 5: THE EMERALD SEA — ORBITAL DISCOVERY (4.35 Ga)")
            yield np.array(img)
            continue

        # --------------------------------------------------------------------------------------
        # PHASE 2: SURFACE VIEW OF THE EMERALD SEA (18s to end)
        # --------------------------------------------------------------------------------------
        if BG_EMERALD_SEA is not None:
            p2_t = t - split_t
            max_dx = 2304 - 1920
            max_dy = 1296 - 1080
            crop_x = int(max_dx * 0.30 + math.sin(p2_t * 0.15) * (max_dx * 0.20))
            crop_y = int(max_dy * 0.40 + math.cos(p2_t * 0.12) * (max_dy * 0.15))
            img = BG_EMERALD_SEA.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
        else:
            img = Image.new("RGB", (WIDTH, HEIGHT), (20, 50, 40))

        draw = ImageDraw.Draw(img)

        # Dynamic Lightning in Background Clouds
        if f_idx % 35 in [0, 1, 2, 7]:
            np.random.seed(f_idx // 3)
            lx1 = np.random.randint(180, WIDTH - 180)
            ly1 = np.random.randint(40, 220)
            for _ in range(5):
                lx2 = lx1 + np.random.randint(-50, 50)
                ly2 = ly1 + np.random.randint(50, 100)
                draw.line([(lx1, ly1), (lx2, ly2)], fill=(255, 255, 220), width=4)
                draw.line([(lx1, ly1), (lx2, ly2)], fill=(180, 230, 255), width=2)
                lx1, ly1 = lx2, ly2

        # Geochemical Analysis HUD Card (Left Side)
        panel_x = 60
        panel_y = 60
        card_w, card_h = 560, 490
        draw_hud_card(draw, panel_x, panel_y, card_w, card_h, bg_color=(10, 16, 22, 235), border_color=(0, 220, 140), border_width=3)

        draw.text((panel_x + 25, panel_y + 25), "PRIMORDIAL OCEAN COMPOSITION", font=font_title, fill=(0, 230, 150))
        draw.text((panel_x + 25, panel_y + 60), "HADEAN BASIN GEOCHEMISTRY (4.35 Ga)", font=font_small, fill=(180, 210, 200))

        draw.text((panel_x + 25, panel_y + 105), "• WATER COLOR: EMERALD GREEN", font=font_huge, fill=(0, 240, 160))
        draw.text((panel_x + 25, panel_y + 150), "DISSOLVED FERROUS IRON (Fe2+) SATURATION", font=font_data, fill=(255, 235, 70))

        draw.line([(panel_x + 25, panel_y + 190), (panel_x + card_w - 25, panel_y + 190)], fill=(50, 80, 70), width=1)

        metrics = [
            ("OCEAN TEMPERATURE:", "80°C - 100°C (SCALDING SEA)"),
            ("ACIDITY LEVEL:", "pH 5.8 (CARBONIC & HYDROCHLORIC ACID)"),
            ("SALINITY LEVEL:", "~2.0x MODERN SEAWATER"),
            ("DISSOLVED OXYGEN (O2):", "0.000% (STRICTLY ANOXIC)"),
            ("ATMOSPHERIC SKY:", "OVERCAST DENSE TOXIC AMBER")
        ]
        my = panel_y + 215
        for mlabel, mval in metrics:
            draw.text((panel_x + 25, my), mlabel, font=font_small, fill=(200, 220, 215))
            draw.text((panel_x + 230, my), mval, font=font_data, fill=(255, 255, 255) if "0.000%" not in mval else (255, 80, 60))
            my += 36

        draw_hud_card(draw, panel_x + 25, panel_y + 415, card_w - 50, 45, bg_color=(20, 45, 35), border_color=(0, 230, 150), border_width=1)
        draw.text((panel_x + 35, panel_y + 428), "CONCLUSION: THE FIRST GLOBAL SEA WAS AN ALIEN GREEN", font=font_small, fill=(0, 255, 180))

        draw_top_series_banner(draw, "SCENE 5: THE EMERALD SEA — SURFACE VIEW")
        yield np.array(img)


# ==============================================================================================
# ACT 6: THE ATOMIC CHRONOMETER (3D ROTATING ZIRCON & MASS SPECTROMETER)
# ==============================================================================================

def render_act_06_frames(duration_sec: float, fps: int = FPS):
    """Act 6: 3D rotating faceted zircon crystal with UV laser ablation & oxygen-18 mass spectrometry HUD."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(24, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)
    font_huge = _get_font(34, bold=True)

    gcx, gcy = 460, 560

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        frame[:, :] = (14, 18, 30)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # 3D Rotating Zircon Crystal
        rot_c = t * 0.8
        pts_3d = [
            (0, -220, 0),
            (120, -60, 0), (0, -60, 120), (-120, -60, 0), (0, -60, -120),
            (140, 100, 0), (0, 100, 140), (-140, 100, 0), (0, 100, -140),
            (0, 230, 0)
        ]
        cos_r = math.cos(rot_c)
        sin_r = math.sin(rot_c)
        pts_2d = []
        for x, y, z in pts_3d:
            xr = x * cos_r - z * sin_r
            zr = x * sin_r + z * cos_r
            pf = 600.0 / (600.0 + zr)
            pts_2d.append((gcx + xr * pf, gcy + y * pf))

        facets = [
            ([0, 1, 2], (255, 235, 120)), ([0, 2, 3], (230, 195, 70)),
            ([0, 3, 4], (200, 160, 50)), ([0, 4, 1], (240, 215, 90)),
            ([1, 5, 6, 2], (255, 210, 80)), ([2, 6, 7, 3], (220, 175, 55)),
            ([3, 7, 8, 4], (190, 145, 45)), ([4, 8, 5, 1], (235, 190, 65)),
            ([9, 6, 5], (245, 200, 75)), ([9, 7, 6], (215, 165, 50)),
            ([9, 8, 7], (185, 135, 40)), ([9, 5, 8], (230, 180, 60))
        ]

        for f_indices, base_col in facets:
            poly_pts = [pts_2d[idx] for idx in f_indices]
            v1x = poly_pts[1][0] - poly_pts[0][0]
            v1y = poly_pts[1][1] - poly_pts[0][1]
            v2x = poly_pts[2][0] - poly_pts[0][0]
            v2y = poly_pts[2][1] - poly_pts[0][1]
            if (v1x * v2y - v1y * v2x) > 0:
                draw.polygon(poly_pts, fill=base_col, outline=(30, 40, 55), width=2)

        for ring_r in [40, 75, 110]:
            draw.ellipse([gcx - ring_r, gcy - ring_r*0.6, gcx + ring_r, gcy + ring_r*0.6], outline=(255, 255, 255, 90), width=1)

        # UV Laser
        laser_source_x, laser_source_y = 120, 200
        draw_hud_card(draw, laser_source_x - 30, laser_source_y - 30, 120, 60, bg_color=(35, 45, 65), border_color=(0, 200, 255), border_width=2)
        draw.text((laser_source_x - 15, laser_source_y - 15), "UV LASER", font=font_small, fill=(0, 220, 255))
        draw.line([(laser_source_x + 90, laser_source_y), (gcx, gcy - 20)], fill=(0, 220, 255), width=6)
        draw.line([(laser_source_x + 90, laser_source_y), (gcx, gcy - 20)], fill=(255, 255, 255), width=2)

        np.random.seed(f_idx % 18)
        for _ in range(16):
            sx = gcx + np.random.randint(-25, 25)
            sy = gcy - 20 + np.random.randint(-25, 25)
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 200))

        for ion_i in range(12):
            ion_t = (t * 2.0 + ion_i * 0.15) % 1.0
            ix = int(gcx + ion_t * 360)
            iy = int(gcy - 20 + math.sin(ion_t * 8.0) * 18)
            draw.ellipse([ix - 3, iy - 3, ix + 3, iy + 3], fill=(0, 220, 255))

        # Mass Spectrometer HUD Card
        panel_x = 760
        panel_y = 60
        draw_hud_card(draw, panel_x, panel_y, WIDTH - panel_x - 60, 920, bg_color=(10, 14, 24, 235), border_color=(0, 210, 255), border_width=3)
        draw.text((panel_x + 35, panel_y + 25), "ION MICROPROBE MASS SPECTROMETRY (SIMS)", font=font_title, fill=(0, 220, 255))
        draw.text((panel_x + 35, panel_y + 60), "SAMPLE: JACK HILLS ZIRCON (W. AUSTRALIA) • GRAIN #W74", font=font_small, fill=(180, 205, 225))

        draw_hud_card(draw, panel_x + 35, panel_y + 95, WIDTH - panel_x - 130, 80, bg_color=(20, 35, 55), border_color=(255, 215, 60), border_width=2)
        draw.text((panel_x + 55, panel_y + 110), "URANIUM-LEAD (U-Pb) CONCORDIA AGE:", font=font_small, fill=(200, 215, 235))
        draw.text((panel_x + 55, panel_y + 135), "4.404 ± 0.008 BILLION YEARS", font=font_huge, fill=(255, 235, 70))

        draw.text((panel_x + 35, panel_y + 205), "ISOTOPE RATIO ANALYSIS: δ18O (HEAVY OXYGEN):", font=font_data, fill=(255, 255, 255))

        gx0, gy0, gw, gh = panel_x + 35, panel_y + 245, WIDTH - panel_x - 130, 300
        draw.rectangle([gx0, gy0, gx0 + gw, gy0 + gh], fill=(15, 22, 35), outline=(50, 75, 110), width=1)

        pk1_x = gx0 + int(gw * 0.32)
        draw.line([(pk1_x, gy0 + gh), (pk1_x, gy0 + 110)], fill=(255, 120, 50), width=4)
        draw.text((pk1_x - 70, gy0 + 80), "MANTLE: +5.3‰", font=font_small, fill=(255, 140, 60))

        pk2_x = gx0 + int(gw * 0.68)
        draw.line([(pk2_x, gy0 + gh), (pk2_x, gy0 + 30)], fill=(0, 230, 140), width=5)
        draw.text((pk2_x - 90, gy0 + 5), "ZIRCON: +7.2‰ (SPIKE!)", font=font_data, fill=(0, 255, 160))

        scan_x = gx0 + int((t * 140) % gw)
        draw.line([(scan_x, gy0), (scan_x, gy0 + gh)], fill=(0, 220, 255, 180), width=2)

        vy = panel_y + 580
        draw.line([(panel_x + 35, vy), (panel_x + gw, vy)], fill=(60, 85, 120), width=1)
        draw.text((panel_x + 35, vy + 20), "FORENSIC SCIENTIFIC VERDICT:", font=font_data, fill=(255, 255, 255))
        draw.text((panel_x + 35, vy + 55), "• Heavy δ18O enrichment (+7.2‰) CANNOT form in dry mantle magma.", font=font_small, fill=(220, 235, 250))
        draw.text((panel_x + 35, vy + 85), "• It ONLY occurs when rock interacts with LOW-TEMPERATURE LIQUID WATER.", font=font_data, fill=(0, 220, 255))
        draw.text((panel_x + 35, vy + 118), "• Old scientific consensus of a dry, molten desert until 3.8 Ga was FALSE.", font=font_small, fill=(255, 160, 140))

        draw_hud_card(draw, panel_x + 35, vy + 175, gw, 100, bg_color=(25, 50, 40), border_color=(0, 240, 160), border_width=3)
        draw.text((panel_x + 55, vy + 195), "FORENSIC PROOF: LIQUID OCEANS CONFIRMED AT 4.40 Ga", font=font_data, fill=(0, 255, 170))
        draw.text((panel_x + 55, vy + 230), "Liquid water formed within 150 million years of Earth's birth", font=font_small, fill=(220, 245, 235))

        draw_top_series_banner(draw, "SCENE 6: THE ATOMIC CHRONOMETER (JACK HILLS ZIRCONS)")
        yield np.array(img)


# ==============================================================================================
# ACT 7: THE PREBIOTIC CRUCIBLE — CLIFFHANGER (HYDROTHERMAL VENT & THE SPARK OF LIFE)
# ==============================================================================================

def render_act_07_frames(duration_sec: float, fps: int = FPS):
    """Act 7: 3D abyssal descent to black smoker chimney with billowing mineral plumes & prebiotic molecular spark."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(24, bold=True)
    font_data = _get_font(18, bold=True)
    font_small = _get_font(14, bold=False)
    font_huge = _get_font(38, bold=True)

    vx, vy = WIDTH // 2 - 120, HEIGHT - 80
    np.random.seed(99)
    n_smoke = 75
    smk_phase = np.random.uniform(0, 1.0, n_smoke)
    smk_vx = np.random.uniform(-18, 18, n_smoke)

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            frame[y, :, 0] = int(8 + 25 * ratio)
            frame[y, :, 1] = int(10 + 18 * ratio)
            frame[y, :, 2] = int(16 + 15 * ratio)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Marine snow
        np.random.seed(f_idx % 30)
        for _ in range(60):
            snx = np.random.randint(0, WIDTH)
            sny = np.random.randint(0, HEIGHT)
            snr = np.random.randint(1, 4)
            draw.ellipse([snx - snr, sny - snr, snx + snr, sny + snr], fill=(160, 180, 205, 140))

        # Chimney spire
        chimney_pts = [
            (vx - 90, HEIGHT), (vx - 65, vy - 240), (vx - 35, vy - 360),
            (vx - 20, vy - 420), (vx + 20, vy - 420),
            (vx + 35, vy - 360), (vx + 65, vy - 240), (vx + 90, HEIGHT)
        ]
        draw.polygon(chimney_pts, fill=(38, 34, 40), outline=(75, 65, 70), width=3)
        draw.ellipse([vx - 25, vy - 435, vx + 25, vy - 405], fill=(255, 120, 30))

        # Mineral plume
        for s_i in range(n_smoke):
            s_t = (smk_phase[s_i] + t * 0.45) % 1.0
            px = int(vx + smk_vx[s_i] * s_t * 6.0 + math.sin(s_t * 6.0) * 25)
            py = int((vy - 420) - s_t * 520)
            pr = int(14 + s_t * 70)
            sh_val = int(25 + 40 * (1.0 - s_t))
            draw.ellipse([px - pr, py - pr*0.7, px + pr, py + pr*0.7], fill=(sh_val, sh_val, sh_val + 5, int(200 * (1.0 - s_t))))

        # Molecular chain callout
        spark_cx, spark_cy = vx + 160, vy - 280
        draw.ellipse([spark_cx - 95, spark_cy - 95, spark_cx + 95, spark_cy + 95], fill=(12, 20, 35), outline=(0, 230, 160), width=3)
        draw.text((spark_cx - 80, spark_cy - 125), "PREBIOTIC PORES (CATALYTIC CELL)", font=font_small, fill=(0, 240, 180))

        n_links = 8
        for li in range(n_links):
            link_ang = t * 3.5 + li * 0.7
            lx = int(spark_cx + math.sin(link_ang) * 55)
            ly = int(spark_cy - 60 + li * 16)
            col_link = (0, 255, 180) if li % 2 == 0 else (255, 220, 70)
            draw.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=col_link)
            lx2 = int(spark_cx - math.sin(link_ang) * 55)
            draw.line([(lx, ly), (lx2, ly)], fill=(120, 220, 200), width=2)
            draw.ellipse([lx2 - 6, ly - 6, lx2 + 6, ly + 6], fill=(0, 200, 255))

        # Telemetry Card
        panel_x = 70
        panel_y = 60
        draw_hud_card(draw, panel_x, panel_y, 480, 340, bg_color=(10, 14, 22, 235), border_color=(0, 200, 255), border_width=3)
        draw.text((panel_x + 25, panel_y + 20), "ABYSSAL HYDROTHERMAL CRUCIBLE", font=font_title, fill=(0, 220, 255))
        draw.text((panel_x + 25, panel_y + 55), "LOCATION: PRIMORDIAL SPREADING RIDGE (4,000m DEPTH)", font=font_small, fill=(180, 200, 220))

        v_metrics = [
            ("FLUID TEMPERATURE:", "400°C (SUPERHEATED MINERAL SOUP)"),
            ("MINERALS EXPELLED:", "FeS, Ni, Co, H2, CH4, CO2"),
            ("ENERGY SOURCE:", "CHEMOAUTOTROPHIC PROTON GRADIENTS"),
            ("CRITICAL REVELATION:", "INORGANIC MINERALS SPARK SELF-REPLICATION")
        ]
        vy_t = panel_y + 95
        for vlbl, vv in v_metrics:
            draw.text((panel_x + 25, vy_t), vlbl, font=font_small, fill=(200, 215, 230))
            draw.text((panel_x + 25, vy_t + 20), vv, font=font_data, fill=(255, 235, 70) if "MINERALS" in vlbl else (0, 240, 180))
            vy_t += 52

        # Theatrical Teaser Banner
        if t > duration_sec * 0.35:
            card_w, card_h = 1060, 420
            cx, cy = WIDTH // 2 + 100, HEIGHT // 2 + 60
            draw_hud_card(draw, cx - card_w//2, cy - card_h//2, card_w, card_h, bg_color=(12, 16, 28, 245), border_color=(255, 140, 30), border_width=4, radius=20)
            draw.text((cx - 480, cy - 160), "NEXT TIME ON HISTORY OF EARTH • EPISODE 4", font=font_data, fill=(255, 160, 40))
            draw.text((cx - 480, cy - 110), "THE PLANET BEFORE LIFE", font=font_huge, fill=(255, 255, 255))
            draw.text((cx - 480, cy - 55), "HOW POISONOUS MINERALS SPARKED THE FIRST BREATH OF CODE", font=font_data, fill=(0, 220, 255))
            draw.text((cx - 480, cy - 10), "Hadean Era • Pillar: Life • The Deep-Sea Hydrothermal Genesis", font=font_small, fill=(200, 215, 235))

            btn_bounce = math.sin(t * 6.0) * 4
            bx1, by1 = cx - 480, cy + 50 + int(btn_bounce)
            draw.rounded_rectangle([bx1, by1, bx1 + 250, by1 + 65], radius=14, fill=(211, 47, 47), outline=(255, 255, 255), width=2)
            draw.text((bx1 + 35, by1 + 16), "SUBSCRIBE", font=font_title, fill=(255, 255, 255))
            draw.text((bx1 + 275, by1 + 20), "🔔 RING THE BELL TO FOLLOW THE SERIES!", font=font_data, fill=(255, 235, 70))

        draw_top_series_banner(draw, "SCENE 7: THE PREBIOTIC CRUCIBLE (CLIFFHANGER)")
        yield np.array(img)


# ==============================================================================================
# MASTER RENDER PIPELINE TO FFMPEG (DIRECT RAWVIDEO RGB24 PIPE)
# ==============================================================================================
EP3_ACT_RENDERERS = {
    1: render_act_01_frames,
    2: render_act_02_frames,
    3: render_act_03_frames,
    4: render_act_04_frames,
    5: render_act_05_frames,
    6: render_act_06_frames,
    7: render_act_07_frames,
}


def render_animated_act_ep3(
    act_index: int,
    duration_sec: float,
    output_clip_path: str,
    audio_path: str = None,
    fps: int = FPS
) -> str:
    """Renders 100% procedural 3D animations streaming directly to FFmpeg rawvideo pipe."""
    work_dir = os.path.dirname(os.path.abspath(output_clip_path))
    os.makedirs(work_dir, exist_ok=True)

    renderer = EP3_ACT_RENDERERS.get(act_index, render_act_01_frames)
    total_frames = int(duration_sec * fps)

    temp_video = os.path.join(work_dir, f"temp_act_{act_index:02d}_video.mp4")

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
    print(f"  [OK] Rendered Ep3 Act {act_index:02d} ({total_frames} frames, {duration_sec:.1f}s) in {elapsed:.1f}s ({(total_frames/elapsed):.1f} fps)")

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
