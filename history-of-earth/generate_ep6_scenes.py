"""
Generates cinematic high-resolution (2304x1296) atmospheric background scene plates
for Episode 6: "Hadean: The Bombardment That Almost Reset the Clock".
Adheres strictly to style_bible.json (Hadean color palette, orbital mechanics, planetary impact, geochronology).
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "scenes")
os.makedirs(ASSETS_DIR, exist_ok=True)

W, H = 2304, 1296


def create_solar_system_resonance():
    """Act 1: Outer solar system gas giants, resonant orbital rings, and perturbed asteroid streams."""
    im = Image.new("RGB", (W, H), color=(4, 6, 14))
    draw = ImageDraw.Draw(im)

    # Cosmic starfield
    random.seed(3900)
    for _ in range(800):
        sx = random.randint(0, W)
        sy = random.randint(0, H)
        sb = random.randint(140, 255)
        sz = random.choice([1, 1, 1, 2, 2, 3])
        draw.ellipse([sx, sy, sx + sz, sy + sz], fill=(sb, sb, int(sb * 0.9)))

    # Distant Sun (faint early sun in distance)
    sun_x, sun_y = int(W * 0.12), int(H * 0.35)
    for rad, col in [(180, (255, 180, 50, 40)), (90, (255, 210, 100)), (40, (255, 250, 220))]:
        draw.ellipse([sun_x - rad, sun_y - rad, sun_x + rad, sun_y + rad], fill=col)

    # Jupiter (massive banded gas giant at upper right)
    jx, jy = int(W * 0.78), int(H * 0.32)
    jr = 240
    # Jupiter atmosphere base
    draw.ellipse([jx - jr, jy - jr, jx + jr, jy + jr], fill=(160, 100, 60))
    # Atmospheric storm bands
    for band_y in range(jy - jr + 15, jy + jr - 15, 14):
        col_band = (200, 140, 90) if (band_y // 14) % 2 == 0 else (120, 70, 40)
        draw.line([(jx - int(math.sqrt(max(0, jr*jr - (band_y - jy)**2))), band_y),
                   (jx + int(math.sqrt(max(0, jr*jr - (band_y - jy)**2))), band_y)],
                  fill=col_band, width=9)
    # Great Red Spot / storm vortex
    draw.ellipse([jx - 90, jy + 35, jx - 10, jy + 85], fill=(225, 75, 40))

    # Saturn in midground (left-center) with ring system
    sx, sy = int(W * 0.42), int(H * 0.65)
    sr = 110
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(190, 165, 110))
    for r_w, r_h, r_col in [(320, 75, (170, 150, 105)), (280, 65, (220, 195, 140)), (240, 55, (140, 120, 80))]:
        draw.ellipse([sx - r_w, sy - r_h, sx + r_w, sy + r_h], outline=r_col, width=6)

    # Resonant orbital gravitational field lines (cyan/gold arcs)
    for res_r in [450, 650, 880, 1150]:
        draw.arc([sun_x - res_r, sun_y - res_r, sun_x + res_r, sun_y + res_r],
                 start=310, end=90, fill=(56, 189, 248), width=2)

    # Swarms of perturbed asteroids (flying inwards from outer belts)
    for _ in range(250):
        ax = random.randint(int(W * 0.3), W)
        ay = random.randint(int(H * 0.4), H)
        rad = random.randint(2, 7)
        draw.ellipse([ax, ay, ax + rad, ay + rad], fill=(180, 175, 165))
        # Motion blur velocity trail towards inner solar system
        draw.line([(ax, ay), (ax - random.randint(15, 45), ay - random.randint(8, 25))],
                  fill=(120, 115, 110), width=1)

    im = im.filter(ImageFilter.GaussianBlur(radius=0.8))
    out_path = os.path.join(ASSETS_DIR, "solar_system_resonance_instability.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_lunar_crater_basin():
    """Act 2: The scarred face of the Moon — Apollo 14/17 impact melt basins and breccia plains."""
    im = Image.new("RGB", (W, H), color=(8, 10, 16))
    draw = ImageDraw.Draw(im)

    # Lunar surface horizon gradient (stark black space to chalky gray regolith)
    for y in range(int(H * 0.45), H):
        y_frac = (y - int(H * 0.45)) / (H * 0.55)
        gray = int(45 + 55 * y_frac)
        draw.line([(0, y), (W, y)], fill=(gray, gray, int(gray * 1.05)))

    # Distant Earth hanging in lunar sky (half illuminated, green ocean and orange volcanic clouds)
    ex, ey, er = int(W * 0.8), int(H * 0.22), 110
    draw.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(15, 35, 60))
    # Illuminated crescent of infant Earth
    draw.chord([ex - er, ey - er, ex + er, ey + er], start=270, end=90, fill=(35, 110, 80))
    # Molten volcanic hotspots on Earth nightside
    for vx, vy in [(ex - 30, ey - 20), (ex - 50, ey + 30), (ex - 10, ey + 40)]:
        draw.ellipse([vx, vy, vx + 8, vy + 8], fill=(255, 120, 30))

    # Giant Imbrium multi-ring crater basin in foreground
    cx, cy = int(W * 0.38), int(H * 0.72)
    # Outer crater rim ridge
    for r, col, w in [(480, (110, 110, 120), 12), (380, (90, 90, 100), 8), (280, (70, 70, 80), 6)]:
        draw.ellipse([cx - r, cy - int(r * 0.45), cx + r, cy + int(r * 0.45)], outline=col, width=w)

    # Central impact melt floor (dark basaltic mare filled with thermal breccia)
    draw.ellipse([cx - 200, cy - 90, cx + 200, cy + 90], fill=(40, 42, 48))

    # Glowing orange thermal shock fractures in the impact melt rock (dated by Apollo to 3.9 Ga)
    for deg in range(0, 360, 25):
        rad = math.radians(deg)
        x1 = cx + int(math.cos(rad) * 60)
        y1 = cy + int(math.sin(rad) * 30)
        x2 = cx + int(math.cos(rad) * 220)
        y2 = cy + int(math.sin(rad) * 110)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 130, 40), width=3)

    # Lunar highland boulders (anorthositic impact breccia)
    random.seed(3902)
    for _ in range(60):
        bx = random.randint(40, W - 40)
        by = random.randint(int(H * 0.65), H - 30)
        bw = random.randint(25, 90)
        bh = random.randint(18, 55)
        draw.ellipse([bx - 6, by + bh - 10, bx + bw + 8, by + bh + 10], fill=(25, 25, 30))
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(125, 125, 135), outline=(170, 170, 185), width=2)

    im = im.filter(ImageFilter.GaussianBlur(radius=1.0))
    out_path = os.path.join(ASSETS_DIR, "lunar_crater_basin_apollo.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_crater_dating_spectrometer():
    """Act 4: High-tech geochronological comparison chamber: lunar crater curve vs. zircon record."""
    im = Image.new("RGB", (W, H), color=(10, 14, 24))
    draw = ImageDraw.Draw(im)

    # Background grid lines
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(18, 28, 48), width=1)
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(18, 28, 48), width=1)

    # Dual analytical display panels: Left = Apollo Basin Ages; Right = Nice Model Simulation
    # Left display frame
    draw.rounded_rectangle([120, 160, int(W * 0.48), int(H * 0.82)], radius=16, fill=(14, 22, 38), outline=(56, 189, 248), width=2)
    # Right display frame
    draw.rounded_rectangle([int(W * 0.52), 160, W - 120, int(H * 0.82)], radius=16, fill=(14, 22, 38), outline=(249, 115, 22), width=2)

    # Left Graph: 3.9 Ga Cataclysmic Spike (Classic Apollo view)
    gx0, gy0 = 180, int(H * 0.72)
    gw, gh = int(W * 0.48) - 240, int(H * 0.45)
    draw.line([(gx0, gy0), (gx0 + gw, gy0)], fill=(100, 130, 170), width=3)
    draw.line([(gx0, gy0), (gx0, gy0 - gh)], fill=(100, 130, 170), width=3)
    # Dramatic spike curve at 3.9 Ga
    curve_pts = []
    for step in range(gw):
        x = gx0 + step
        frac = step / gw
        # Peak at frac = 0.65 (3.9 Ga)
        val = math.exp(-((frac - 0.65) ** 2) / 0.008) * gh * 0.85 + 20
        curve_pts.append((x, gy0 - int(val)))
    for i in range(len(curve_pts) - 1):
        draw.line([curve_pts[i], curve_pts[i+1]], fill=(56, 189, 248), width=4)

    # Right Graph: Exponentially Decaying Tail (Boehnke & Harrison 2016 view)
    rx0, ry0 = int(W * 0.52) + 60, int(H * 0.72)
    rw, rh = gw, gh
    draw.line([(rx0, ry0), (rx0 + rw, ry0)], fill=(170, 130, 100), width=3)
    draw.line([(rx0, ry0), (rx0, ry0 - rh)], fill=(170, 130, 100), width=3)
    curve_pts_decay = []
    for step in range(rw):
        x = rx0 + step
        frac = step / rw
        # Exponential decay from early accretion
        val = math.exp(-frac * 3.2) * rh * 0.9 + 15
        curve_pts_decay.append((x, ry0 - int(val)))
    for i in range(len(curve_pts_decay) - 1):
        draw.line([curve_pts_decay[i], curve_pts_decay[i+1]], fill=(249, 115, 22), width=4)

    im = im.filter(ImageFilter.GaussianBlur(radius=0.8))
    out_path = os.path.join(ASSETS_DIR, "crater_dating_spectrometer.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_subterranean_sanctuary():
    """Act 5: Subsurface geothermal crust cross-section: boiling inferno surface above, sheltered hydrothermal fracture refuge below."""
    im = Image.new("RGB", (W, H), color=(25, 12, 10))
    draw = ImageDraw.Draw(im)

    # Top 25%: Blazing asteroid impact inferno on surface
    for y in range(int(H * 0.28)):
        y_f = y / (H * 0.28)
        draw.line([(0, y), (W, y)], fill=(int(220 - 60*y_f), int(70 + 30*y_f), int(20)))

    # Surface basalt crust barrier (dense dark basalt layer insulating depths)
    draw.polygon([(0, int(H * 0.26)), (W, int(H * 0.26)), (W, int(H * 0.40)), (0, int(H * 0.40))], fill=(30, 25, 35))

    # Deep lithosphere (H * 0.40 to H): deep cool basaltic rock cross section
    draw.polygon([(0, int(H * 0.40)), (W, int(H * 0.40)), (W, H), (0, H)], fill=(14, 20, 32))

    # Complex hydrothermal fracture network (cool clement aquifers, 50-80°C, glowing cyan/emerald)
    random.seed(3905)
    for _ in range(45):
        fx = random.randint(100, W - 100)
        fy = random.randint(int(H * 0.44), H - 100)
        # Branching fracture channels
        for b in range(5):
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(40, 160)
            ex = fx + int(math.cos(angle) * length)
            ey = fy + int(math.sin(angle) * length)
            draw.line([(fx, fy), (ex, ey)], fill=(56, 189, 248), width=5)
            draw.line([(fx, fy), (ex, ey)], fill=(74, 222, 128), width=2)
            # Microbial colonies in mineral cavities
            draw.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(16, 185, 129))

    im = im.filter(ImageFilter.GaussianBlur(radius=1.2))
    out_path = os.path.join(ASSETS_DIR, "subterranean_hydrothermal_sanctuary.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_carbonaceous_chondrite_delivery():
    """Act 6: Macro extraterrestrial meteorite cross section delivering water and organic molecules."""
    im = Image.new("RGB", (W, H), color=(8, 12, 20))
    draw = ImageDraw.Draw(im)

    # Deep ocean seafloor hydrothermal background
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=(int(10 + 20 * (y/H)), int(25 + 35 * (y/H)), int(45 + 50 * (y/H))))

    # Huge carbonaceous chondrite meteorite resting on seafloor (center stage)
    mx, my, mw, mh = int(W * 0.5), int(H * 0.55), 750, 420
    draw.ellipse([mx - mw//2 - 20, my - mh//2 - 20, mx + mw//2 + 20, my + mh//2 + 20], fill=(20, 25, 30))
    draw.ellipse([mx - mw//2, my - mh//2, mx + mw//2, my + mh//2], fill=(45, 48, 55), outline=(130, 135, 145), width=5)

    # Chondrules: spherical silicate granules inside meteorite
    random.seed(3906)
    for _ in range(80):
        cx = random.randint(mx - mw//2 + 60, mx + mw//2 - 60)
        cy = random.randint(my - mh//2 + 40, my + mh//2 - 40)
        cr = random.randint(14, 38)
        col = random.choice([(180, 160, 120), (140, 150, 160), (210, 190, 150), (95, 105, 115)])
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=col, outline=(220, 220, 230), width=2)

    # Chemical organic vapor streams & water molecules diffusing into hydrothermal fluid
    for sx in range(mx - 280, mx + 300, 70):
        sy = my - mh//2 + 30
        draw.line([(sx, sy), (sx - 40, sy - 180), (sx + 30, sy - 340)], fill=(56, 189, 248), width=4)
        draw.line([(sx, sy), (sx - 40, sy - 180), (sx + 30, sy - 340)], fill=(255, 255, 255), width=1)
        # Phosphorus & amino acid molecular nodes
        draw.ellipse([sx + 20, sy - 350, sx + 40, sy - 330], fill=(250, 204, 21))

    im = im.filter(ImageFilter.GaussianBlur(radius=1.1))
    out_path = os.path.join(ASSETS_DIR, "carbonaceous_chondrite_delivery.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_acasta_gneiss_first_rock():
    """Act 7: The dawn of the Archean eon (4.0 Ga): The banded Acasta Gneiss cratonic shield."""
    im = Image.new("RGB", (W, H), color=(20, 25, 40))
    draw = ImageDraw.Draw(im)

    # Sky: The very first clear dawn sky as post-bombardment clouds part (Deep gold and pale twilight blue)
    for y in range(int(H * 0.52)):
        y_f = y / (H * 0.52)
        r = int(25 + 185 * y_f)
        g = int(35 + 120 * y_f)
        b = int(75 + 30 * y_f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Rising early sun on horizon
    sun_x, sun_y = int(W * 0.5), int(H * 0.48)
    for rad, col in [(280, (255, 170, 60)), (180, (255, 210, 110)), (90, (255, 245, 200))]:
        draw.ellipse([sun_x - rad, sun_y - rad, sun_x + rad, sun_y + rad], fill=col)

    # Distant calm ocean horizon (greenish-blue primeval sea at H * 0.50)
    for y in range(int(H * 0.50), int(H * 0.62)):
        draw.line([(0, y), (W, y)], fill=(30, 80, 75))

    # Midground & Foreground: Massive banded Acasta Gneiss craton outcrop (TTG metamorphic rock)
    pts_rock = [
        (0, int(H * 0.58)),
        (int(W * 0.25), int(H * 0.54)),
        (int(W * 0.55), int(H * 0.57)),
        (int(W * 0.78), int(H * 0.52)),
        (W, int(H * 0.56)),
        (W, H),
        (0, H)
    ]
    draw.polygon(pts_rock, fill=(90, 85, 95))

    # Tonalite-Trondhjemite-Granodiorite metamorphic gneissic foliation banding (wavy alternating dark amphibole & light feldspar/quartz bands)
    random.seed(4000)
    for by in range(int(H * 0.56), H, 16):
        wavy_pts = []
        for x in range(0, W + 40, 30):
            w_y = by + int(math.sin(x * 0.015) * 14 + math.cos(x * 0.03) * 8)
            wavy_pts.append((x, w_y))
        band_col = (175, 170, 185) if (by // 16) % 2 == 0 else (55, 52, 60)
        for i in range(len(wavy_pts) - 1):
            draw.line([wavy_pts[i], wavy_pts[i+1]], fill=band_col, width=7)

    im = im.filter(ImageFilter.GaussianBlur(radius=1.0))
    out_path = os.path.join(ASSETS_DIR, "acasta_gneiss_first_rock.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


if __name__ == "__main__":
    create_solar_system_resonance()
    create_lunar_crater_basin()
    create_crater_dating_spectrometer()
    create_subterranean_sanctuary()
    create_carbonaceous_chondrite_delivery()
    create_acasta_gneiss_first_rock()
    print("All Episode 6 background scene plates created successfully!")
