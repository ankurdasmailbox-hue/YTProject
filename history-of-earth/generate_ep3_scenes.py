"""
Generates cinematic high-resolution (1920x1080) atmospheric background scene plates
for Episode 3: "Hadean: The Sky Was Poison and the Rain Never Stopped".
Adheres strictly to style_bible.json (Hadean color palette, moody gradients, scientific depth).
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "scenes")
os.makedirs(ASSETS_DIR, exist_ok=True)


def create_supercritical_steam_vault():
    """Scene 1: 100-200 atm crushing steam & amber sulfur vault."""
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), color=(35, 20, 10))
    draw = ImageDraw.Draw(im)

    # 1. Sky Gradient (Toxic Amber-Brown to Burning Sulfur)
    for y in range(h):
        r_f = y / h
        r = int(55 + 160 * r_f)
        g = int(30 + 90 * r_f)
        b = int(10 + 25 * r_f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # 2. Supercritical steam clouds / turbulent layers
    for cx, cy, rx, ry in [(400, 250, 600, 200), (1200, 180, 800, 240), (800, 380, 700, 180)]:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 100, 40, 120))

    # 3. Jagged volcanic basalt peaks in the background
    pts_bg = [(0, 750)]
    for x in range(0, w + 100, 160):
        pts_bg.append((x, 620 + int(math.sin(x * 0.015) * 80 + math.cos(x * 0.03) * 50)))
    pts_bg.extend([(w, h), (0, h)])
    draw.polygon(pts_bg, fill=(45, 30, 25))

    # 4. Foreground volcanic crags with molten fissures
    pts_fg = [(0, 880)]
    for x in range(0, w + 100, 120):
        pts_fg.append((x, 820 + int(math.sin(x * 0.02) * 60)))
    pts_fg.extend([(w, h), (0, h)])
    draw.polygon(pts_fg, fill=(20, 18, 22))

    # Molten lava cracks
    for x in range(200, w - 200, 350):
        draw.line([(x, 860), (x + 80, 940), (x + 160, 1080)], fill=(255, 100, 20), width=6)
        draw.line([(x, 860), (x + 80, 940), (x + 160, 1080)], fill=(255, 220, 100), width=2)

    im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
    out_path = os.path.join(ASSETS_DIR, "supercritical_steam_vault.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_faint_young_sun_haze():
    """Scene 2: Faint Young Sun burning through thick orange greenhouse smog."""
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), color=(30, 15, 10))
    draw = ImageDraw.Draw(im)

    # Gradient: Upper cosmic darkness into thick orange smog
    for y in range(h):
        r_f = y / h
        r = int(25 + 180 * r_f)
        g = int(15 + 85 * r_f)
        b = int(10 + 15 * r_f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Faint Young Sun (25% fainter, pale diffuse disc behind smog)
    sun_x, sun_y = 960, 360
    # Corona / atmospheric halo
    for rad, col in [(380, (180, 80, 20)), (280, (210, 110, 30)), (180, (240, 160, 60)), (100, (255, 230, 180))]:
        draw.ellipse([sun_x - rad, sun_y - rad, sun_x + rad, sun_y + rad], fill=col)

    # Dense horizontal smog bands drifting across the Sun
    for y in range(200, 520, 40):
        draw.line([(200, y), (1720, y)], fill=(120, 50, 15), width=18)

    # Basalt Horizon
    pts = [(0, 820), (480, 780), (960, 840), (1440, 790), (w, 830), (w, h), (0, h)]
    draw.polygon(pts, fill=(25, 20, 22))

    im = im.filter(ImageFilter.GaussianBlur(radius=2.0))
    out_path = os.path.join(ASSETS_DIR, "faint_young_sun_haze.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_atmospheric_condensation_shatter():
    """Scene 3: Condensation tipping point with lightning and falling deluge."""
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), color=(20, 25, 30))
    draw = ImageDraw.Draw(im)

    # Dark storm gradient
    for y in range(h):
        r_f = y / h
        r = int(20 + 40 * r_f)
        g = int(25 + 50 * r_f)
        b = int(35 + 70 * r_f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Giant storm clouds
    for cx in [300, 800, 1400, 1900]:
        draw.ellipse([cx - 400, -100, cx + 400, 500], fill=(40, 55, 65))

    # Lightning strikes
    for lx in [650, 1280]:
        curr_x, curr_y = lx, 100
        while curr_y < 780:
            next_x = curr_x + random.randint(-40, 40)
            next_y = curr_y + random.randint(40, 90)
            draw.line([(curr_x, curr_y), (next_x, next_y)], fill=(255, 255, 240), width=5)
            draw.line([(curr_x, curr_y), (next_x, next_y)], fill=(120, 200, 255), width=10)
            curr_x, curr_y = next_x, next_y

    # Rain streaks
    for _ in range(800):
        rx = random.randint(0, w)
        ry = random.randint(300, h)
        rlen = random.randint(40, 120)
        draw.line([(rx, ry), (rx - 15, ry + rlen)], fill=(180, 220, 255, 140), width=2)

    # Dark basalt ocean basin below
    draw.polygon([(0, 820), (w, 820), (w, h), (0, h)], fill=(15, 18, 22))

    im = im.filter(ImageFilter.GaussianBlur(radius=1.2))
    out_path = os.path.join(ASSETS_DIR, "atmospheric_condensation_shatter.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_emerald_ocean_iron():
    """Scene 5: Scalding, emerald-green iron-rich global ocean."""
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), color=(30, 25, 20))
    draw = ImageDraw.Draw(im)

    # Sky: Toxic overcast amber-green
    for y in range(540):
        r_f = y / 540
        r = int(120 - 40 * r_f)
        g = int(80 + 30 * r_f)
        b = int(30 + 10 * r_f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Sea Horizon at y=540
    # Emerald-green sea gradient with dissolved iron depth
    for y in range(540, h):
        r_f = (y - 540) / 540
        r = int(20 + 20 * r_f)
        g = int(115 - 55 * r_f)   # Rich emerald green
        b = int(75 - 45 * r_f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Rolling turbulent boiling waves & foam lines
    for y in range(560, h, 28):
        amp = 8 + (y - 540) * 0.04
        pts = [(0, y)]
        for x in range(0, w + 60, 40):
            pts.append((x, y + int(math.sin(x * 0.02 + y) * amp)))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(60, 180, 130), width=3)
            # Emerald-gold highlights
            if i % 3 == 0:
                draw.line([pts[i], pts[i+1]], fill=(140, 220, 170), width=1)

    # Distant volcanic basalt archipelagos
    draw.polygon([(200, 540), (320, 480), (450, 540)], fill=(25, 30, 28))
    draw.polygon([(1350, 540), (1500, 460), (1680, 540)], fill=(25, 30, 28))

    im = im.filter(ImageFilter.GaussianBlur(radius=1.0))
    out_path = os.path.join(ASSETS_DIR, "emerald_ocean_iron.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


if __name__ == "__main__":
    create_supercritical_steam_vault()
    create_faint_young_sun_haze()
    create_atmospheric_condensation_shatter()
    create_emerald_ocean_iron()
    print("All Episode 3 background scene assets successfully generated.")
