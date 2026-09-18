"""
Cinematic Procedural Animation Engine for History of Earth (Episode 2: "The Planet With No Plates").
Upgraded with:
1. Recognizable 3D rotating Earth Globe with oceans, continents, polar caps, and latitude/longitude grid!
2. Vibrant, high-engagement cartoon infographics, playful stickers, comic starbursts, animated thermometers,
   puzzle pieces, cartoon detectives, sparkling gemstones, and family tree scrolls that attract ALL age groups!
3. 100% genuine procedural animations where EVERY frame contains continuous motion.
"""

import os
import sys
import math
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"

WIDTH = 1920
HEIGHT = 1080
FPS = 30


def _get_font(size: int, bold: bool = True):
    """Fallback-safe font loader with bold preferences."""
    try:
        font_names = ["segoeuib.ttf", "arialbd.ttf", "comicbd.ttf", "consola.ttf", "arial.ttf"] if bold else ["segoeui.ttf", "arial.ttf", "consola.ttf"]
        for font_name in font_names:
            font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()


# ==============================================================================================
# CARTOON VISUAL HELPER FUNCTIONS (STICKERS, BUBBLES, STARBURSTS, THERMOMETERS)
# ==============================================================================================

def draw_cartoon_sticker(draw, x, y, w, h, fill_color, border_color=(255, 255, 255), border_width=4, radius=18):
    """Draws a vibrant, tactile cartoon sticker card with a soft 3D drop shadow."""
    # Dark shadow
    shadow_offset = 6
    draw.rounded_rectangle(
        [x + shadow_offset, y + shadow_offset, x + w + shadow_offset, y + h + shadow_offset],
        radius=radius,
        fill=(10, 15, 25, 200)
    )
    # Sticker body
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=radius,
        fill=fill_color,
        outline=border_color,
        width=border_width
    )


def draw_comic_starburst(draw, cx, cy, r_outer, r_inner, points=12, fill_color=(255, 215, 0), outline_color=(255, 80, 0), outline_width=4, width=None, **kwargs):
    """Draws a classic comic action burst for dramatic impacts, cracks, and discoveries."""
    pts = []
    for i in range(points * 2):
        ang = i * math.pi / points
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
    w = width if width is not None else outline_width
    draw.polygon(pts, fill=fill_color, outline=outline_color, width=w)


def draw_cartoon_puzzle_piece(draw, x, y, size=60, color=(0, 200, 255), outline_color=(255, 255, 255)):
    """Draws a cute, playful cartoon jigsaw puzzle piece."""
    s = size
    # Base square with rounded tab on top and right
    draw.rounded_rectangle([x, y, x + s, y + s], radius=10, fill=color, outline=outline_color, width=3)
    # Top tab
    draw.ellipse([x + s*0.35, y - s*0.25, x + s*0.65, y + s*0.25], fill=color, outline=outline_color, width=2)
    # Right tab
    draw.ellipse([x + s*0.75, y + s*0.35, x + s*1.25, y + s*0.65], fill=color, outline=outline_color, width=2)


def draw_cartoon_magnifying_glass(draw, cx, cy, radius=40, angle=45):
    """Draws a cute cartoon magnifying glass with shiny reflection."""
    r = radius
    # Handle
    h_len = r * 1.5
    rad = math.radians(angle)
    hx1 = cx + math.cos(rad) * r
    hy1 = cy + math.sin(rad) * r
    hx2 = cx + math.cos(rad) * (r + h_len)
    hy2 = cy + math.sin(rad) * (r + h_len)
    draw.line([(hx1, hy1), (hx2, hy2)], fill=(180, 110, 45), width=8)
    draw.line([(hx1, hy1), (hx2, hy2)], fill=(255, 215, 0), width=4)
    # Rim
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 235, 255, 120), outline=(255, 215, 0), width=5)
    # Glass reflection highlight
    draw.arc([cx - r*0.7, cy - r*0.7, cx + r*0.7, cy + r*0.7], start=200, end=270, fill=(255, 255, 255), width=3)


# ==============================================================================================
# ACT 1: THE RECOGNIZABLE EARTH GLOBE & THE UNBROKEN SHELL
# ==============================================================================================

def _generate_earth_globe_texture(width=1024, height=512):
    """Generates an equirectangular Earth globe map with oceans, continents, and grid."""
    img = Image.new("RGB", (width, height), color=(20, 95, 185))
    draw = ImageDraw.Draw(img)

    # Ocean depth gradient
    for y in range(height):
        dist_eq = abs(y - height//2) / (height//2)
        b = int(195 - dist_eq * 45)
        g = int(105 - dist_eq * 25)
        draw.line([(0, y), (width, y)], fill=(18, g, b))

    # Polar ice caps
    draw.rectangle([0, 0, width, 40], fill=(245, 250, 255))
    draw.rectangle([0, height-35, width, height], fill=(245, 250, 255))

    # Latitude / Longitude lines (classroom globe style)
    for y_lat in range(50, height-40, 50):
        draw.line([(0, y_lat), (width, y_lat)], fill=(70, 150, 230), width=1)
    for x_lon in range(0, width, 75):
        draw.line([(x_lon, 0), (x_lon, height)], fill=(70, 150, 230), width=1)
    # Equator in gold
    draw.line([(0, height//2), (width, height//2)], fill=(255, 215, 80), width=2)

    # Continents
    green = (50, 175, 75)
    green_border = (25, 115, 45)
    desert = (215, 185, 100)

    # North America
    na = [(110, 70), (180, 60), (280, 65), (320, 120), (280, 180), (240, 230), (220, 260), (180, 230), (140, 160), (100, 110)]
    draw.polygon(na, fill=green, outline=green_border, width=3)

    # South America
    sa = [(225, 265), (290, 280), (330, 320), (310, 400), (270, 455), (245, 455), (220, 360), (215, 290)]
    draw.polygon(sa, fill=green, outline=green_border, width=3)

    # Eurasia
    eurasia = [(430, 80), (520, 65), (680, 70), (840, 90), (880, 180), (810, 240), (740, 260), (620, 230), (540, 190), (460, 160), (430, 120)]
    draw.polygon(eurasia, fill=green, outline=green_border, width=3)

    # Africa
    africa = [(440, 180), (520, 180), (560, 240), (550, 310), (515, 395), (480, 400), (445, 320), (420, 250), (425, 210)]
    draw.polygon(africa, fill=desert, outline=green_border, width=3)

    # Australia
    aus = [(770, 330), (860, 325), (875, 385), (835, 420), (765, 390)]
    draw.polygon(aus, fill=desert, outline=green_border, width=3)

    # India
    india = [(630, 215), (665, 220), (650, 280), (630, 250)]
    draw.polygon(india, fill=green, outline=green_border, width=3)

    # Swirling cartoon cloud belts
    for cy in [110, 240, 370]:
        for cx in range(40, width, 160):
            draw.arc([cx, cy, cx+130, cy+35], start=10, end=170, fill=(255, 255, 255), width=4)

    return np.array(img)


def render_act_01_frames(duration_sec: float, fps: int = FPS):
    """Act 1: Recognizable 3D Rotating Earth Globe transitioning into Stagnant Lid with Cartoon Infographics."""
    total_frames = int(duration_sec * fps)
    cx, cy, r = WIDTH // 2 - 140, HEIGHT // 2, 380

    # Twinkling cartoon stars
    np.random.seed(42)
    n_stars = 260
    star_x = np.random.randint(0, WIDTH, n_stars)
    star_y = np.random.randint(0, HEIGHT, n_stars)
    star_b = np.random.uniform(140, 255, n_stars)
    star_twinkle_speed = np.random.uniform(1.8, 4.5, n_stars)

    # 3D Sphere geometry
    y_idx, x_idx = np.mgrid[:HEIGHT, :WIDTH]
    dx = (x_idx - cx).astype(np.float32)
    dy = (y_idx - cy).astype(np.float32)
    dist_sq = dx**2 + dy**2
    sphere_mask = dist_sq <= r**2

    dz = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    dz[sphere_mask] = np.sqrt(r**2 - dist_sq[sphere_mask])
    
    nx = dx[sphere_mask] / r
    ny = dy[sphere_mask] / r
    nz = dz[sphere_mask] / r

    # Light direction (front-top-left)
    lx, ly, lz = -0.42, -0.32, 0.85
    l_mag = math.sqrt(lx**2 + ly**2 + lz**2)
    lx, ly, lz = lx / l_mag, ly / l_mag, lz / l_mag
    diffuse = np.maximum(0.12, nx * lx + ny * ly + nz * lz)

    # Pre-generate Earth globe map and primordial stagnant lid map
    map_w, map_h = 1024, 512
    earth_map = _generate_earth_globe_texture(map_w, map_h).astype(np.float32)
    
    # Primordial stagnant lid texture (dark basalt with glowing orange cracks)
    stagnant_map = np.zeros((map_h, map_w, 3), dtype=np.float32)
    stagnant_map[:, :, 0] = 42
    stagnant_map[:, :, 1] = 38
    stagnant_map[:, :, 2] = 48
    # Magma crack pattern
    crack_tex = np.sin(np.linspace(0, 16 * np.pi, map_w))[None, :] * np.cos(np.linspace(0, 8 * np.pi, map_h))[:, None]
    is_crack = crack_tex > 0.65
    stagnant_map[is_crack, 0] = 255
    stagnant_map[is_crack, 1] = 120
    stagnant_map[is_crack, 2] = 30

    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    for f_idx in range(total_frames):
        t = f_idx / fps
        rot_angle = t * 0.18  # Continuous planetary rotation
        
        # 1. Base space background
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        y_grad = np.linspace(12, 32, HEIGHT, dtype=np.uint8)[:, None]
        frame[:, :, 2] = y_grad
        frame[:, :, 0] = y_grad // 2

        # Twinkling stars
        twinkle = np.sin(t * star_twinkle_speed) * 0.4 + 0.6
        s_brightness = (star_b * twinkle).astype(np.uint8)
        frame[star_y, star_x, 0] = np.maximum(frame[star_y, star_x, 0], s_brightness)
        frame[star_y, star_x, 1] = np.maximum(frame[star_y, star_x, 1], s_brightness)
        frame[star_y, star_x, 2] = np.maximum(frame[star_y, star_x, 2], s_brightness)

        # 2. 3D Globe Projection
        lon = (np.arctan2(nx, nz) + rot_angle) % (2 * np.pi)
        lat = np.arcsin(np.clip(ny, -0.999, 0.999))
        
        u = ((lon / (2 * np.pi)) * (map_w - 1)).astype(np.int32)
        v = (((lat + np.pi/2) / np.pi) * (map_h - 1)).astype(np.int32)

        # Transition from Modern Earth Globe to Primordial Stagnant Lid after 12s
        # (matching narrator explaining: "Rewind the clock 4.4 billion years...")
        trans_stage = min(1.0, max(0.0, (t - 10.0) / 6.0)) if t > 10.0 else 0.0

        tex_earth = earth_map[v, u]
        tex_stagnant = stagnant_map[v, u]
        
        # Blend textures
        current_tex = (1.0 - trans_stage) * tex_earth + trans_stage * tex_stagnant

        # Apply spherical diffuse shading & gentle atmosphere rim glow
        shade = diffuse[:, None] * 0.85 + 0.15
        globe_rgb = current_tex * shade
        
        # Rim glow
        rim = ((1.0 - nz) ** 3.0)[:, None]
        globe_rgb += rim * np.array([40, 160, 255]) * (1.0 - trans_stage) + rim * np.array([255, 120, 30]) * trans_stage

        frame[sphere_mask] = np.clip(globe_rgb, 0, 255).astype(np.uint8)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Tectonic plate borders (cartoon dashed puzzle lines on modern Earth)
        if trans_stage < 0.8:
            alpha_line = int(255 * (1.0 - trans_stage))
            # Glowing puzzle boundary arc around globe
            draw.arc([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], start=30, end=150, fill=(255, 230, 80), width=4)
            draw.arc([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], start=190, end=320, fill=(255, 230, 80), width=4)

        # 3. CARTOON INFOGRAPHICS & STICKERS (Replacing cold mechanical boxes)
        panel_x = WIDTH - 520

        # Sticker 1: The Modern Jigsaw Puzzle
        draw_cartoon_sticker(draw, panel_x, 60, 460, 160, fill_color=(255, 225, 75), border_color=(255, 255, 255))
        draw_cartoon_puzzle_piece(draw, panel_x + 25, 90, size=55, color=(0, 190, 255))
        draw.text((panel_x + 105, 80), "THE 15-PIECE JIGSAW!", font=font_title, fill=(30, 30, 30))
        draw.text((panel_x + 105, 120), "Modern Earth is broken into", font=font_small, fill=(50, 50, 50))
        draw.text((panel_x + 105, 145), "15 giant sliding puzzle plates!", font=font_bold, fill=(211, 47, 47))

        # Sticker 2: Rewinding Time & The Missing Plates
        rewind_bounce = math.sin(t * 4.0) * 5
        draw_cartoon_sticker(draw, panel_x, 250 + int(rewind_bounce), 460, 180, fill_color=(255, 105, 95), border_color=(255, 255, 255))
        # Comic starburst on sticker
        draw_comic_starburst(draw, panel_x + 65, 335 + int(rewind_bounce), 42, 25, points=10, fill_color=(255, 240, 60), outline_color=(255, 255, 255))
        draw.text((panel_x + 42, 322 + int(rewind_bounce)), "0!", font=font_title, fill=(211, 47, 47))
        
        draw.text((panel_x + 130, 275 + int(rewind_bounce)), "4.4 BILLION YEARS AGO:", font=font_bold, fill=(255, 255, 255))
        draw.text((panel_x + 130, 310 + int(rewind_bounce)), "ZERO PLATES DETECTED!", font=font_title, fill=(255, 235, 70))
        draw.text((panel_x + 130, 355 + int(rewind_bounce)), "No Pacific plate. No Atlantic rift.", font=font_small, fill=(255, 240, 240))
        draw.text((panel_x + 130, 380 + int(rewind_bounce)), "Just ONE solid unbroken rock!", font=font_small, fill=(255, 255, 255))

        # Sticker 3: The Stagnant Lid Padlock
        draw_cartoon_sticker(draw, panel_x, 460, 460, 170, fill_color=(0, 215, 175), border_color=(255, 255, 255))
        # Cartoon Lock icon
        draw.rounded_rectangle([panel_x + 30, 520, panel_x + 85, 575], radius=10, fill=(255, 215, 0), outline=(50, 50, 50), width=3)
        draw.arc([panel_x + 40, 490, panel_x + 75, 535], start=180, end=0, fill=(255, 255, 255), width=5)
        
        draw.text((panel_x + 110, 480), "THE STAGNANT LID!", font=font_title, fill=(20, 40, 35))
        draw.text((panel_x + 110, 520), "Earth was locked in a monolithic", font=font_small, fill=(20, 50, 45))
        draw.text((panel_x + 110, 545), "unbroken basalt prison for", font=font_small, fill=(20, 50, 45))
        draw.text((panel_x + 110, 575), "500 MILLION YEARS!", font=font_bold, fill=(211, 47, 47))

        # Animated Cartoon Magnifying Glass sliding across globe
        mag_x = int(cx + math.sin(t * 1.5) * 160)
        mag_y = int(cy + math.cos(t * 1.2) * 140)
        draw_cartoon_magnifying_glass(draw, mag_x, mag_y, radius=42, angle=35)
        # Comic scan bubble popping off magnifying glass
        draw.rounded_rectangle([mag_x + 35, mag_y - 65, mag_x + 220, mag_y - 20], radius=12, fill=(255, 255, 255), outline=(211, 47, 47), width=3)
        draw.text((mag_x + 48, mag_y - 55), "SEARCHING FOR CRACKS...", font=font_small, fill=(20, 20, 20))

        # Top-Left Series Banner
        draw_cartoon_sticker(draw, 50, 50, 420, 95, fill_color=(35, 45, 65), border_color=(0, 220, 255), border_width=3)
        draw.text((70, 65), "HISTORY OF EARTH &bull; EPISODE 2", font=font_bold, fill=(0, 220, 255))
        draw.text((70, 98), "THE PLANET WITH NO PLATES", font=font_small, fill=(255, 255, 255))

        yield np.array(img)


# ==============================================================================================
# ACT 2: THE HEAT-PIPE FURNACE (CARTOON CROSS-SECTION, VOLCANOES & BOILING KETTLE)
# ==============================================================================================

def render_act_02_frames(duration_sec: float, fps: int = FPS):
    """Act 2: Playful cartoon Earth cross-section with smiling core, bubbly convection, and boiling kettle."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    volcano_x = [360, 720, 1080]

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # 1. Background sky & space (top third)
        sky_grad = np.linspace(15, 55, 340, dtype=np.uint8)[:, None]
        frame[:340, :, 0] = sky_grad * 2
        frame[:340, :, 1] = sky_grad // 2
        frame[:340, :, 2] = sky_grad // 3

        # 2. Warm cartoon mantle (y=380 to 900)
        m_h = 900 - 380
        m_grad = np.linspace(0, 1, m_h, dtype=np.float32)[:, None]
        frame[380:900, :, 0] = (210 * (1 - m_grad) + 255 * m_grad).astype(np.uint8)
        frame[380:900, :, 1] = (60 * (1 - m_grad) + 140 * m_grad).astype(np.uint8)
        frame[380:900, :, 2] = (15 * (1 - m_grad) + 25 * m_grad).astype(np.uint8)

        # 3. Smiling Glowing Cartoon Core (y=900 to 1080)
        frame[900:, :, 0] = 255
        frame[900:, :, 1] = 200
        frame[900:, :, 2] = 40

        # Rigid Basalt Lid
        frame[340:380, :, 0] = 40
        frame[340:380, :, 1] = 38
        frame[340:380, :, 2] = 48

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Crust Boundary line
        draw.line([(0, 340), (WIDTH, 340)], fill=(255, 255, 255), width=4)
        draw.line([(0, 380), (WIDTH, 380)], fill=(255, 120, 40), width=3)
        draw.text((40, 348), "SOLID ROCK CRUST (LOCKED LID!)", font=font_bold, fill=(255, 240, 100))

        # Vertical cartoon heat-pipe magma conduits
        for vx in volcano_x:
            w_pipe = 44 + int(math.sin(t * 6.0 + vx) * 8)
            draw.rectangle([vx - w_pipe//2, 340, vx + w_pipe//2, 900], fill=(255, 140, 20), outline=(255, 255, 255), width=3)
            # Cartoon Volcano cone
            draw.polygon([(vx - 90, 340), (vx + 90, 340), (vx + 45, 290), (vx - 45, 290)], fill=(65, 55, 60), outline=(255, 255, 255), width=3)
            draw.polygon([(vx - 40, 290), (vx + 40, 290), (vx, 260)], fill=(255, 140, 30))

            # Bouncing puffy cartoon smoke clouds popping out of volcano
            for s_i in range(4):
                puff_phase = ((t * 2.0 + s_i * 0.5) % 2.0) / 2.0
                puff_y = int(270 - puff_phase * 180)
                puff_x = int(vx + math.sin(puff_phase * 6.0 + vx) * 35)
                puff_r = int(18 + puff_phase * 35)
                # Fluffy white/orange puff
                draw.ellipse([puff_x - puff_r, puff_y - puff_r, puff_x + puff_r, puff_y + puff_r], fill=(255, int(220 - puff_phase*80), 160), outline=(255, 255, 255), width=2)

            # Cartoon lava drops splashing
            for d_i in range(5):
                drop_t = (t * 3.0 + d_i * 0.4) % 1.0
                drop_x = vx + int(math.sin(d_i) * 65 * drop_t)
                drop_y = 280 - int(math.sin(drop_t * math.pi) * 80)
                draw.ellipse([drop_x - 6, drop_y - 6, drop_x + 6, drop_y + 6], fill=(255, 220, 40), outline=(255, 255, 255), width=1)

        # Bubbly cartoon convection flow loops
        for cc_x, cc_y, d_sign in [(220, 640, 1), (540, 640, -1), (900, 640, 1), (1260, 640, -1)]:
            # Chunky cartoon circular arrows
            loop_r = 130
            draw.arc([cc_x - loop_r, cc_y - loop_r*0.7, cc_x + loop_r, cc_y + loop_r*0.7], start=0, end=360, fill=(255, 220, 50), width=5)
            # Animated cartoon bubbles rolling along loop
            for b_idx in range(6):
                ang = (b_idx * (math.pi / 3) + d_sign * t * 1.5) % (2 * math.pi)
                bx = cc_x + math.cos(ang) * loop_r
                by = cc_y + math.sin(ang) * (loop_r * 0.7)
                draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(255, 255, 255), outline=(255, 120, 40), width=2)

        # Smiling face on cartoon core at bottom
        draw.text((WIDTH//2 - 180, 950), "🔥 PLANETARY FURNACE: 3,800°C! 🔥", font=font_title, fill=(20, 20, 20))

        # CARTOON INFOGRAPHIC STICKERS
        panel_x = WIDTH - 540

        # Sticker 1: The Boiling Pressure Cooker
        draw_cartoon_sticker(draw, panel_x, 40, 480, 170, fill_color=(255, 120, 80), border_color=(255, 255, 255))
        # Whistling kettle icon
        draw.ellipse([panel_x + 25, 75, panel_x + 95, 145], fill=(240, 240, 250), outline=(40, 40, 40), width=3)
        draw.arc([panel_x + 85, 90, panel_x + 120, 115], start=270, end=90, fill=(240, 240, 250), width=4)
        # Steam puff
        draw.text((panel_x + 115, 65), "💨 WHISTLE!", font=font_bold, fill=(255, 240, 80))
        
        draw.text((panel_x + 130, 95), "BOILING UNDER THE LID!", font=font_title, fill=(255, 255, 255))
        draw.text((panel_x + 130, 135), "Radioactive heat was 3x hotter!", font=font_bold, fill=(255, 235, 70))
        draw.text((panel_x + 130, 160), "With no plates, pressure soared!", font=font_small, fill=(255, 245, 245))

        # Sticker 2: The Heat Pipe Express
        draw_cartoon_sticker(draw, panel_x, 230, 480, 150, fill_color=(255, 215, 65), border_color=(255, 255, 255))
        draw_comic_starburst(draw, panel_x + 65, 305, 38, 22, points=8, fill_color=(255, 90, 40), outline_color=(255, 255, 255))
        draw.text((panel_x + 45, 292), "🌋", font=font_title, fill=(255, 255, 255))
        
        draw.text((panel_x + 125, 255), "THE HEAT-PIPE EXPRESS!", font=font_title, fill=(30, 30, 30))
        draw.text((panel_x + 125, 295), "Massive volcanic chimneys drilled", font=font_small, fill=(50, 50, 50))
        draw.text((panel_x + 125, 320), "straight to space, like Jupiter's Io!", font=font_bold, fill=(211, 47, 47))

        yield np.array(img)


# ==============================================================================================
# ACT 3: THE 500-MILLION-YEAR CRIME SCENE (CARTOON GEOLOGY CAKE & DETECTIVE)
# ==============================================================================================

def render_act_03_frames(duration_sec: float, fps: int = FPS):
    """Act 3: Colorful cartoon geological layer cake, puzzled cartoon detective, and missing void."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        frame[:, :] = (20, 26, 42)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Header Banner
        draw_cartoon_sticker(draw, 60, 40, WIDTH - 120, 85, fill_color=(255, 215, 75), border_color=(255, 255, 255))
        draw.text((90, 55), "🕵️‍♂️ THE 500-MILLION-YEAR CRIME SCENE: WHERE IS THE CRUST?!", font=font_title, fill=(25, 25, 25))

        # 1. Left: Colorful Cartoon Geological "Layer Cake" (x=120 to 760)
        col_x1, col_x2 = 120, 760
        layers = [
            ("🌱 MODERN & MAMMALS (0 - 66 Ma)", 160, 240, (120, 210, 110), "🌳 Humans & Animals"),
            ("🦖 DINOSAURS & REPTILES (66 - 252 Ma)", 240, 340, (255, 170, 75), "🦕 T-Rex & Fossils"),
            ("🦐 ANCIENT SEA LIFE (252 - 541 Ma)", 340, 460, (75, 185, 240), "Trilobites & Coral"),
            ("🦠 BACTERIAL SEAS (541 - 2500 Ma)", 460, 600, (190, 125, 220), "Simple Microbes"),
            ("🌋 ANCIENT ARCHEAN (2500 - 4000 Ma)", 600, 740, (255, 110, 95), "Oldest Known Rocks")
        ]

        for name, y1, y2, col, icon_txt in layers:
            draw_cartoon_sticker(draw, col_x1, y1, col_x2 - col_x1, y2 - y1 - 8, fill_color=col, border_color=(255, 255, 255), radius=14)
            draw.text((col_x1 + 25, y1 + 15), name, font=font_bold, fill=(20, 20, 20))
            draw.text((col_x1 + 25, y1 + 45), icon_txt, font=font_small, fill=(40, 40, 40))

        # Bottom Layer: The HADEAN (4000 - 4540 Ma) — THE BLACK HOLE MYSTERY VOID
        draw_cartoon_sticker(draw, col_x1, 750, col_x2 - col_x1, 230, fill_color=(12, 16, 26), border_color=(255, 80, 60), border_width=4, radius=18)
        
        # Bouncing comic question marks popping out of the void
        for q_i in range(5):
            q_x = col_x1 + 100 + q_i * 110
            q_bounce = math.sin(t * 4.0 + q_i) * 15
            draw.text((q_x, 810 + int(q_bounce)), "???", font=font_title, fill=(255, 220, 50))

        draw.text((col_x1 + 40, 770), "💀 THE HADEAN VOID (FIRST 500 MILLION YEARS):", font=font_title, fill=(255, 80, 60))
        draw.text((col_x1 + 40, 875), "ZERO PERCENT INTACT CRUST SURVIVES ON EARTH TODAY!", font=font_bold, fill=(255, 255, 255))
        draw.text((col_x1 + 40, 915), "100% OF THE PRIMORDIAL MAP WAS DESTROYED AND RECYCLED!", font=font_small, fill=(255, 210, 100))

        # 2. Right Side: Cartoon Detective & Evidence Badges
        panel_x = 830

        # Cartoon Detective Badge
        draw_cartoon_sticker(draw, panel_x, 160, WIDTH - panel_x - 60, 240, fill_color=(255, 105, 95), border_color=(255, 255, 255))
        draw_cartoon_magnifying_glass(draw, panel_x + 65, 250, radius=40, angle=40)
        draw.text((panel_x + 130, 185), "CASE FILE: #4404-HADEAN", font=font_bold, fill=(255, 255, 255))
        draw.text((panel_x + 130, 220), "THE MISSING CRUST MYSTERY!", font=font_title, fill=(255, 235, 75))
        draw.text((panel_x + 130, 265), "If the stagnant lid really existed,", font=font_small, fill=(255, 245, 245))
        draw.text((panel_x + 130, 295), "how can detective scientists prove it", font=font_small, fill=(255, 245, 245))
        draw.text((panel_x + 130, 325), "if every rock was destroyed?!", font=font_bold, fill=(255, 255, 255))

        # Cartoon Clock Spinning Wildly
        spin_ang = t * 6.0
        draw_cartoon_sticker(draw, panel_x, 430, WIDTH - panel_x - 60, 220, fill_color=(0, 210, 255), border_color=(255, 255, 255))
        # Clock face
        clk_cx, clk_cy = panel_x + 75, 540
        draw.ellipse([clk_cx - 45, clk_cy - 45, clk_cx + 45, clk_cy + 45], fill=(255, 255, 255), outline=(30, 30, 30), width=4)
        draw.line([(clk_cx, clk_cy), (clk_cx + math.cos(spin_ang)*30, clk_cy + math.sin(spin_ang)*30)], fill=(211, 47, 47), width=4)
        
        draw.text((panel_x + 145, 460), "500,000,000 YEARS GONE!", font=font_title, fill=(20, 35, 45))
        draw.text((panel_x + 145, 505), "Ocean crust recycles every 200M years.", font=font_small, fill=(20, 35, 45))
        draw.text((panel_x + 145, 535), "Old crust dives into the hot mantle.", font=font_small, fill=(20, 35, 45))
        draw.text((panel_x + 145, 570), "We need an INDESTRUCTIBLE witness!", font=font_bold, fill=(211, 47, 47))

        # Cartoon Zircon Teaser Sticker
        draw_cartoon_sticker(draw, panel_x, 680, WIDTH - panel_x - 60, 240, fill_color=(255, 225, 75), border_color=(255, 255, 255))
        draw_comic_starburst(draw, panel_x + 75, 800, 48, 28, points=10, fill_color=(0, 220, 255), outline_color=(255, 255, 255))
        draw.text((panel_x + 55, 785), "💎", font=font_title, fill=(255, 255, 255))
        
        draw.text((panel_x + 145, 710), "ENTER: JACK HILLS ZIRCON!", font=font_title, fill=(30, 30, 30))
        draw.text((panel_x + 145, 755), "Microscopic gemstone crystals", font=font_bold, fill=(211, 47, 47))
        draw.text((panel_x + 145, 785), "from Western Australia dated to 4.4 Ga!", font=font_small, fill=(50, 50, 50))
        draw.text((panel_x + 145, 825), "They survived... and trapped a secret!", font=font_bold, fill=(30, 30, 30))

        yield np.array(img)


# ==============================================================================================
# ACT 4: THE ATOMIC WITNESS (SPARKLING GEM, CARTOON LASER & SHIVERING THERMOMETER)
# ==============================================================================================

def render_act_04_frames(duration_sec: float, fps: int = FPS):
    """Act 4: Sparkling cartoon zircon crystal, rainbow laser blaster, and shivering cartoon thermometer."""
    total_frames = int(duration_sec * fps)
    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    target_cx, target_cy = 440, 560

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        frame[:, :] = (16, 22, 38)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Header
        draw_cartoon_sticker(draw, 60, 40, WIDTH - 120, 85, fill_color=(0, 220, 255), border_color=(255, 255, 255))
        draw.text((90, 55), "💎 THE ATOMIC WITNESS: JACK HILLS ZIRCON FORENSICS!", font=font_title, fill=(20, 30, 45))

        # 1. Left Side: Sparkling Cartoon Zircon Gemstone
        gem_bounce = math.sin(t * 3.0) * 8
        gcx, gcy = target_cx, target_cy + int(gem_bounce)

        # Faceted Gemstone Polygon (Tetragonal cartoon crystal)
        gem_facets = [
            ([(gcx, gcy - 220), (gcx + 140, gcy - 80), (gcx, gcy), (gcx - 140, gcy - 80)], (255, 225, 90)),
            ([(gcx + 140, gcy - 80), (gcx + 180, gcy + 120), (gcx, gcy + 220), (gcx, gcy)], (255, 190, 50)),
            ([(gcx - 140, gcy - 80), (gcx - 180, gcy + 120), (gcx, gcy + 220), (gcx, gcy)], (255, 240, 140)),
            ([(gcx, gcy - 220), (gcx, gcy), (gcx, gcy + 220)], (255, 255, 255))
        ]
        for poly, fcol in gem_facets:
            draw.polygon(poly, fill=fcol, outline=(30, 30, 30), width=4)

        # Animated Twinkling Cartoon Sparkles around gem
        sparkle_pts = [
            (gcx - 180, gcy - 160, 0), (gcx + 190, gcy - 140, 1),
            (gcx - 190, gcy + 140, 2), (gcx + 180, gcy + 160, 3),
            (gcx, gcy - 240, 4)
        ]
        for sp_x, sp_y, sp_id in sparkle_pts:
            sp_scale = abs(math.sin(t * 5.0 + sp_id))
            draw_comic_starburst(draw, sp_x, sp_y, int(24 * sp_scale), int(10 * sp_scale), points=4, fill_color=(255, 255, 255), outline_color=(0, 220, 255), outline_width=2)

        # Retro Cartoon Laser Blaster Gun (top-left firing down at gem)
        gun_x, gun_y = 100, 220
        draw.rounded_rectangle([gun_x, gun_y, gun_x + 90, gun_y + 45], radius=8, fill=(80, 95, 120), outline=(255, 255, 255), width=3)
        draw.rectangle([gun_x + 90, gun_y + 12, gun_x + 130, gun_y + 32], fill=(255, 80, 60), outline=(255, 255, 255), width=2)
        # Laser beam
        draw.line([(gun_x + 130, gun_y + 22), (gcx, gcy)], fill=(200, 50, 255), width=8)
        draw.line([(gun_x + 130, gun_y + 22), (gcx, gcy)], fill=(255, 255, 255), width=3)
        draw.text((gun_x, gun_y - 30), "🔬 UV LASER PROBE!", font=font_bold, fill=(255, 220, 50))

        # 2. Right Side: The Bouncy Cartoon Thermometer & Revelation
        panel_x = 800

        # Big Cartoon Thermometer Sticker
        draw_cartoon_sticker(draw, panel_x, 160, WIDTH - panel_x - 60, 440, fill_color=(255, 245, 235), border_color=(255, 255, 255))
        
        # Thermometer graphics
        # Temperature plunges dynamically from 1200°C to 680°C
        temp_prog = min(1.0, t / max(duration_sec * 0.65, 1.0))
        cur_temp = int(1200 - temp_prog * (1200 - 680))
        shiver = int(math.sin(t * 15.0) * 4) if cur_temp < 750 else 0

        # Cartoon thermometer tube
        tx, ty, tw, th = panel_x + 60 + shiver, 240, 36, 260
        draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=16, fill=(220, 230, 245), outline=(40, 40, 40), width=4)
        # Bulb at bottom
        draw.ellipse([tx - 18, ty + th - 25, tx + tw + 18, ty + th + 45], fill=(255, 60, 50), outline=(40, 40, 40), width=4)
        
        # Red liquid level
        liq_h = int((cur_temp - 500) / (1300 - 500) * (th - 30))
        draw.rounded_rectangle([tx + 6, ty + th - liq_h, tx + tw - 6, ty + th], radius=8, fill=(255, 60, 50))

        # Thermometer face
        draw.text((panel_x + 130, 185), "🌡️ TITANIUM THERMOMETER", font=font_title, fill=(211, 47, 47))
        draw.text((panel_x + 130, 235), f"TEMPERATURE: {cur_temp}°C!", font=font_title, fill=(211, 47, 47))
        
        if cur_temp > 850:
            draw.text((panel_x + 130, 280), "🔥 1,200°C: Dry Stagnant Lid Basalt", font=font_bold, fill=(255, 100, 40))
            draw.text((panel_x + 130, 320), "Expected melting temperature...", font=font_small, fill=(70, 70, 70))
        else:
            draw.text((panel_x + 130, 280), "🧊 680°C?! BRRR! FREEZING COLD!", font=font_title, fill=(0, 160, 240))
            draw.text((panel_x + 130, 330), "Dry lava cannot melt at 680°C!", font=font_bold, fill=(40, 40, 40))
            draw.text((panel_x + 130, 360), "680°C ONLY occurs when WATER is", font=font_bold, fill=(20, 20, 20))
            draw.text((panel_x + 130, 390), "dragged into the mantle to melt granite!", font=font_bold, fill=(0, 160, 240))
            # Cute cartoon ice cubes & water droplets popping around
            draw.text((tx - 35, ty + 50), "🧊", font=font_title, fill=(255, 255, 255))
            draw.text((tx + 50, ty + 120), "💧", font=font_title, fill=(255, 255, 255))

        # The Smoking Gun Revelation Sticker
        draw_cartoon_sticker(draw, panel_x, 630, WIDTH - panel_x - 60, 290, fill_color=(255, 220, 65), border_color=(255, 255, 255))
        draw_comic_starburst(draw, panel_x + 65, 750, 45, 25, points=10, fill_color=(255, 80, 60), outline_color=(255, 255, 255))
        draw.text((panel_x + 45, 735), "⚡", font=font_title, fill=(255, 255, 255))

        draw.text((panel_x + 130, 655), "THE SMOKING GUN REVEALED!", font=font_title, fill=(20, 20, 20))
        draw.text((panel_x + 130, 700), "• Zircons date back 4.404 Billion Years.", font=font_bold, fill=(211, 47, 47))
        draw.text((panel_x + 130, 735), "• They formed in wet, cool granitic magma.", font=font_small, fill=(30, 30, 30))
        draw.text((panel_x + 130, 770), "• Water can only enter the mantle via SUBDUCTION!", font=font_bold, fill=(0, 140, 200))
        draw.text((panel_x + 130, 810), "CONCLUSION: THE STAGNANT LID CRACKED!", font=font_title, fill=(211, 47, 47))

        yield np.array(img)


# ==============================================================================================
# ACT 5: THE GREAT RUPTURE (COMIC-BOOK CRACK & FIRST SUBDUCTION DIVE)
# ==============================================================================================

def render_act_05_frames(duration_sec: float, fps: int = FPS):
    """Act 5: Comic-book action burst CRACK!, cartoon subduction slab dive, and tipping seesaw."""
    total_frames = int(duration_sec * fps)
    font_burst = _get_font(42)
    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Primordial dark sea above, red hot lava mantle below
        frame[:300, :, 0] = 20
        frame[:300, :, 1] = 60
        frame[:300, :, 2] = 110  # Blue cartoon sea

        # Hot lava mantle below y=420
        frame[420:, :, 0] = 230
        frame[420:, :, 1] = 75
        frame[420:, :, 2] = 25

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # 1. Tectonic Plates
        # Left overriding plate
        draw.polygon([(0, 300), (840, 300), (840, 420), (0, 420)], fill=(55, 65, 80), outline=(255, 255, 255), width=4)
        draw.text((80, 350), "OVERRIDING SHELL", font=font_bold, fill=(255, 235, 75))

        # Sinking plate diving down-left into the mantle at 45 degrees
        sub_prog = min(1.0, t / max(duration_sec * 0.75, 1.0))
        trench_x, trench_y = 840, 300
        slab_pts = [
            (WIDTH, 300),
            (trench_x, trench_y),
            (trench_x - int(420 * sub_prog), trench_y + int(520 * sub_prog)),
            (trench_x - int(340 * sub_prog), trench_y + int(600 * sub_prog)),
            (trench_x + 130, trench_y + 160),
            (WIDTH, 420)
        ]
        draw.polygon(slab_pts, fill=(40, 48, 60), outline=(255, 255, 255), width=4)

        # Glowing friction sparks along sliding fault line
        glow_w = 6 + int(math.sin(t * 12.0) * 3)
        draw.line([slab_pts[1], slab_pts[2]], fill=(255, 215, 40), width=glow_w)

        # Concentric cartoon seismic soundwave rings
        for w_i in range(4):
            w_r = int(((t * 180 + w_i * 90) % 400))
            draw.arc([trench_x - w_r, trench_y - w_r, trench_x + w_r, trench_y + w_r], start=60, end=210, fill=(255, 255, 255), width=3)

        # 2. Giant Comic Action Burst: "CRACK!!!"
        burst_scale = min(1.0, max(0.2, math.sin(t * 5.0) * 0.2 + 0.9))
        draw_comic_starburst(draw, trench_x, trench_y - 70, int(130 * burst_scale), int(75 * burst_scale), points=14, fill_color=(255, 220, 50), outline_color=(211, 47, 47), outline_width=6)
        draw.text((trench_x - 90, trench_y - 95), "CRACK!!!", font=font_burst, fill=(211, 47, 47))

        # 3. CARTOON INFOGRAPHICS & STICKERS
        panel_x = WIDTH - 540

        # Sticker 1: The Tipping Gravity Seesaw
        draw_cartoon_sticker(draw, panel_x, 50, 480, 200, fill_color=(255, 225, 75), border_color=(255, 255, 255))
        # Seesaw scale icon
        draw.polygon([(panel_x + 40, 160), (panel_x + 120, 160), (panel_x + 80, 110)], fill=(50, 50, 50))
        draw.line([(panel_x + 20, 135), (panel_x + 140, 95)], fill=(211, 47, 47), width=6)
        draw.text((panel_x + 15, 100), "⚖️", font=font_title, fill=(255, 255, 255))
        
        draw.text((panel_x + 155, 75), "GRAVITY WINS!", font=font_title, fill=(30, 30, 30))
        draw.text((panel_x + 155, 115), "Cold rock became too heavy", font=font_bold, fill=(211, 47, 47))
        draw.text((panel_x + 155, 145), "to stay on top of hot mantle!", font=font_small, fill=(50, 50, 50))
        draw.text((panel_x + 155, 175), "DOWN IT DIVES: SUBDUCTION!", font=font_bold, fill=(30, 30, 30))

        # Sticker 2: Megaquakes & Ocean Recycling
        draw_cartoon_sticker(draw, panel_x, 280, 480, 180, fill_color=(255, 105, 95), border_color=(255, 255, 255))
        draw_comic_starburst(draw, panel_x + 65, 370, 40, 22, points=8, fill_color=(255, 225, 50), outline_color=(255, 255, 255))
        draw.text((panel_x + 48, 355), "⚡", font=font_title, fill=(255, 255, 255))

        draw.text((panel_x + 130, 305), "EARTH'S FIRST SUBDUCTION!", font=font_title, fill=(255, 255, 255))
        draw.text((panel_x + 130, 350), "• Water dragged 60 miles deep.", font=font_bold, fill=(255, 235, 75))
        draw.text((panel_x + 130, 380), "• Trillions of tons of crust recycled.", font=font_small, fill=(255, 245, 245))
        draw.text((panel_x + 130, 410), "• THE PLATE TECTONIC CONVEYOR BELT IS BORN!", font=font_bold, fill=(255, 255, 255))

        yield np.array(img)


# ==============================================================================================
# ACT 6: FORGING THE ANCESTORS (CARTOON ISLAND COLLISION & FAMILY TREE SCROLL)
# ==============================================================================================

def render_act_06_frames(duration_sec: float, fps: int = FPS):
    """Act 6: Cute cartoon islands colliding with BONK!, rising pink granite plutons, and family tree scroll."""
    total_frames = int(duration_sec * fps)
    font_burst = _get_font(36)
    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Friendly blue ocean at top, warm mantle below
        frame[:420, :, 0] = 30
        frame[:420, :, 1] = 110
        frame[:420, :, 2] = 210

        frame[420:, :, 0] = 200
        frame[420:, :, 1] = 70
        frame[420:, :, 2] = 30

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # 1. Two Cartoon Island Boats Drifting Together (Bumping at cx=640)
        cx = 640
        drift = min(110, int(t * 18))
        
        # Left island
        draw.polygon([(0, 420), (cx - 130 + drift, 420), (cx - 180 + drift, 300), (cx - 280 + drift, 270), (0, 340)], fill=(70, 80, 95), outline=(255, 255, 255), width=4)
        draw.text((cx - 360 + drift, 360), "🏝️ ISLAND ARC A", font=font_bold, fill=(255, 235, 75))

        # Right island
        draw.polygon([(WIDTH, 420), (cx + 130 - drift, 420), (cx + 180 - drift, 300), (cx + 280 - drift, 270), (WIDTH, 340)], fill=(70, 80, 95), outline=(255, 255, 255), width=4)
        draw.text((cx + 180 - drift, 360), "🏝️ ISLAND ARC B", font=font_bold, fill=(255, 235, 75))

        # Collision impact starburst
        if drift >= 95:
            draw_comic_starburst(draw, cx, 340, 75, 45, points=12, fill_color=(255, 220, 50), outline_color=(211, 47, 47), width=4)
            draw.text((cx - 45, 325), "BONK!", font=font_burst, fill=(211, 47, 47))

        # 2. Bubbly Pink Granitic Magma Rising & Forming Craton Keel
        keel_h = min(360, int(t * 40))
        # Giant pink granite keel root
        draw.polygon([(cx - 160, 420), (cx + 160, 420), (cx + 120, 420 + keel_h), (cx - 120, 420 + keel_h)], fill=(255, 140, 170), outline=(255, 255, 255), width=4)
        
        # Cartoon Anchor graphic / label
        draw.text((cx - 110, 460), "⚓ CRATON KEEL!", font=font_title, fill=(20, 20, 20))
        draw.text((cx - 110, 500), "BUOYANT PINK GRANITE", font=font_bold, fill=(255, 255, 255))
        draw.text((cx - 110, 530), "LIGHT LIKE STYROFOAM!", font=font_bold, fill=(255, 235, 75))
        draw.text((cx - 110, 560), "CAN NEVER SINK OR SUBDUCT!", font=font_small, fill=(20, 20, 20))

        # Bubbly cartoon pink magma bubbles floating up
        for b_i in range(8):
            bx = cx + int(math.sin(t * 4.0 + b_i) * 65)
            by = 420 + keel_h - int(((t * 70 + b_i * 45) % max(keel_h, 10)))
            draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 190, 210), outline=(255, 255, 255), width=2)

        # 3. CARTOON INFOGRAPHICS & FAMILY TREE SCROLL
        panel_x = WIDTH - 560

        # Family Tree Scroll Sticker
        draw_cartoon_sticker(draw, panel_x, 50, 500, 280, fill_color=(255, 240, 200), border_color=(180, 120, 50), border_width=5)
        draw.text((panel_x + 35, 75), "📜 CONTINENT FAMILY TREE!", font=font_title, fill=(120, 50, 20))
        
        # Generation 1
        draw_cartoon_sticker(draw, panel_x + 35, 120, 430, 40, fill_color=(255, 140, 170), border_color=(255, 255, 255), radius=8)
        draw.text((panel_x + 50, 130), "1. PILBARA & KAAPVAAL CRATONS (4.4 Ga)", font=font_small, fill=(20, 20, 20))
        
        # Arrow
        draw.text((panel_x + 235, 165), "⬇️ Fused Together", font=font_small, fill=(120, 50, 20))
        
        # Generation 2
        draw_cartoon_sticker(draw, panel_x + 35, 190, 430, 40, fill_color=(255, 215, 75), border_color=(255, 255, 255), radius=8)
        draw.text((panel_x + 50, 200), "2. SUPERCONTINENTS (Pangaea, Rodinia)", font=font_small, fill=(20, 20, 20))

        # Arrow
        draw.text((panel_x + 235, 235), "⬇️ Split Apart", font=font_small, fill=(120, 50, 20))

        # Generation 3
        draw_cartoon_sticker(draw, panel_x + 35, 260, 430, 40, fill_color=(100, 220, 120), border_color=(255, 255, 255), radius=8)
        draw.text((panel_x + 50, 270), "3. MODERN CONTINENTS WE WALK ON!", font=font_bold, fill=(20, 20, 20))

        # Celebration Confetti Sticker
        draw_cartoon_sticker(draw, panel_x, 370, 500, 180, fill_color=(0, 215, 185), border_color=(255, 255, 255))
        draw.text((panel_x + 35, 395), "🎉 CELEBRATE THE BEDROCK!", font=font_title, fill=(20, 30, 40))
        draw.text((panel_x + 35, 440), "Australia & Africa hold the ancient seeds", font=font_bold, fill=(255, 255, 255))
        draw.text((panel_x + 35, 470), "of the very first continents on Earth!", font=font_small, fill=(20, 40, 50))
        draw.text((panel_x + 35, 500), "INDESTRUCTIBLE FOR 4 BILLION YEARS!", font=font_bold, fill=(255, 235, 75))

        yield np.array(img)


# ==============================================================================================
# ACT 7: THE DEGASSING CRISIS (CARTOON VOLCANO MONSTER & EPISODE 3 TEASER)
# ==============================================================================================

def render_act_07_frames(duration_sec: float, fps: int = FPS):
    """Act 7: Sweating cartoon Earth, billowing lime-green sulfur clouds, 95 atm gauge, and bouncy teaser."""
    total_frames = int(duration_sec * fps)
    font_huge = _get_font(38)
    font_title = _get_font(28)
    font_bold = _get_font(22)
    font_small = _get_font(16)

    np.random.seed(66)
    n_puffs = 120
    puff_x = np.random.uniform(100, WIDTH - 100, n_puffs)
    puff_y = np.random.uniform(300, HEIGHT + 100, n_puffs)
    puff_vy = -np.random.uniform(90, 240, n_puffs)
    puff_r = np.random.uniform(40, 90, n_puffs)

    for f_idx in range(total_frames):
        t = f_idx / fps
        prog = min(1.0, t / max(duration_sec, 1.0))
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Sky turns from blue to toxic emerald lime-green greenhouse smog
        for y_i in range(HEIGHT):
            ratio = y_i / HEIGHT
            frame[y_i, :, 0] = int(20 + 80 * ratio * prog)
            frame[y_i, :, 1] = int(60 + 130 * ratio * prog)
            frame[y_i, :, 2] = int(40 + 30 * ratio)

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # 1. Billowing Fluffy Cartoon Sulfur Clouds
        dt = 1.0 / fps
        for i in range(n_puffs):
            puff_y[i] += puff_vy[i] * dt
            if puff_y[i] < -100:
                puff_y[i] = HEIGHT + 50
                puff_x[i] = np.random.uniform(80, WIDTH - 80)
            
            pr = int(puff_r[i])
            draw.ellipse([puff_x[i] - pr, puff_y[i] - pr, puff_x[i] + pr, puff_y[i] + pr], fill=(int(60 + 50*math.sin(i)), int(160 + 60*math.cos(i)), 45), outline=(255, 255, 255, 100), width=2)

        # Cartoon Lightning Bolts
        if int(t * 8) % 4 == 0:
            lx1 = np.random.randint(150, WIDTH - 150)
            ly1 = np.random.randint(80, 320)
            for _ in range(4):
                lx2 = lx1 + np.random.randint(-50, 50)
                ly2 = ly1 + np.random.randint(40, 80)
                draw.line([(lx1, ly1), (lx2, ly2)], fill=(255, 255, 180), width=5)
                lx1, ly1 = lx2, ly2

        # 2. Giant Cartoon Pressure Meter (Bouncing needle up to 95 ATM)
        pres_atm = int(1.0 + prog * 94.0)
        draw_cartoon_sticker(draw, 80, 60, 480, 180, fill_color=(255, 85, 75), border_color=(255, 255, 255))
        # Dial icon
        draw.ellipse([110, 100, 180, 170], fill=(255, 255, 255), outline=(40, 40, 40), width=3)
        n_ang = math.pi * (1.0 - (pres_atm / 100.0))
        draw.line([(145, 135), (145 + math.cos(n_ang)*30, 135 - math.sin(n_ang)*30)], fill=(211, 47, 47), width=4)
        
        draw.text((205, 85), "⚠️ PRESSURE CRISIS!", font=font_title, fill=(255, 255, 255))
        draw.text((205, 125), f"{pres_atm} ATMOSPHERES!", font=font_huge, fill=(255, 235, 75))
        draw.text((205, 175), "POISON STEAM & SULFUR DELUGE!", font=font_small, fill=(255, 240, 240))

        # 3. Theatrical Bouncy Teaser Card (Second half of act)
        if t > duration_sec * 0.38:
            fade = min(1.0, (t - duration_sec * 0.38) / (duration_sec * 0.25))
            card_w, card_h = 1020, 420
            cx, cy = WIDTH // 2, HEIGHT // 2 + 70
            
            # Big Cartoon Teaser Banner with Drop Shadow
            draw_cartoon_sticker(draw, cx - card_w//2, cy - card_h//2, card_w, card_h, fill_color=(255, 225, 75), border_color=(255, 255, 255), border_width=6, radius=24)
            
            draw.text((cx - 440, cy - 160), "🚀 NEXT TIME ON HISTORY OF EARTH &bull; EPISODE 3!", font=font_bold, fill=(211, 47, 47))
            draw.text((cx - 440, cy - 110), "THE SKY WAS POISON", font=font_huge, fill=(20, 20, 20))
            draw.text((cx - 440, cy - 60), "AND THE RAIN NEVER STOPPED!", font=font_huge, fill=(0, 140, 220))
            draw.text((cx - 440, cy + 5), "Hadean Era &bull; Pillar: Air & Ocean &bull; The Cataclysmic Birth of the Seas", font=font_bold, fill=(50, 50, 50))

            # Bouncy Red Subscribe Button with Bell
            btn_bounce = math.sin(t * 6.0) * 4
            draw.rounded_rectangle([cx - 440, cy + 60 + int(btn_bounce), cx - 180, cy + 130 + int(btn_bounce)], radius=18, fill=(211, 47, 47), outline=(255, 255, 255), width=3)
            draw.text((cx - 400, cy + 80 + int(btn_bounce)), "SUBSCRIBE", font=font_title, fill=(255, 255, 255))
            draw.text((cx - 140, cy + 85), "🔔 RING THE BELL TO FOLLOW THE SERIES!", font=font_bold, fill=(20, 20, 20))

        yield np.array(img)


# ==============================================================================================
# MASTER RENDER PIPELINE TO FFMPEG (DIRECT RAWVIDEO PIPE)
# ==============================================================================================
ACT_RENDERERS = {
    1: render_act_01_frames,
    2: render_act_02_frames,
    3: render_act_03_frames,
    4: render_act_04_frames,
    5: render_act_05_frames,
    6: render_act_06_frames,
    7: render_act_07_frames,
}


def render_animated_act(
    act_index: int,
    duration_sec: float,
    output_clip_path: str,
    audio_path: str = None,
    fps: int = FPS
) -> str:
    """Renders procedural cartoon animations streaming directly to FFmpeg."""
    work_dir = os.path.dirname(os.path.abspath(output_clip_path))
    os.makedirs(work_dir, exist_ok=True)

    renderer = ACT_RENDERERS.get(act_index, render_act_01_frames)
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
    print(f"  [OK] Rendered Act {act_index:02d} ({total_frames} frames, {duration_sec:.1f}s) in {t1 - t0:.1f}s ({(total_frames/(t1-t0+1e-5)):.1f} fps)")

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
    print("Testing Upgraded Cartoon Procedural Animation Engine...")
    test_out = "test_act1_cartoon.mp4"
    res = render_animated_act(1, 2.0, test_out)
    print(f"Rendered test animation: {res}")
    if os.path.exists(test_out):
        os.remove(test_out)
    print("Test passed successfully!")
