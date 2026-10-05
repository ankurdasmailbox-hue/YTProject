"""
Generates cinematic high-resolution (2304x1296) atmospheric background scene plates
for Episode 5: "When Rocks Learned to Cool — The Zircon Code".
Adheres strictly to style_bible.json (Hadean color palette, forensic geology, scientific instrumentation).
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "scenes")
os.makedirs(ASSETS_DIR, exist_ok=True)

W, H = 2304, 1296


def create_jack_hills_outback():
    """Act 2: Western Australian Outback — ancient Jack Hills red metaconglomerate ridge."""
    im = Image.new("RGB", (W, H), color=(40, 15, 10))
    draw = ImageDraw.Draw(im)

    # 1. Sky: Fiery Outback Sunset Gradient (Deep twilight purple to blazing desert orange)
    for y in range(int(H * 0.6)):
        r_f = y / (H * 0.6)
        r = int(50 + 195 * r_f)
        g = int(20 + 110 * r_f)
        b = int(60 - 30 * r_f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Low glaring desert sun
    sun_x, sun_y = int(W * 0.65), int(H * 0.42)
    for rad, col in [(320, (255, 140, 40)), (220, (255, 180, 70)), (130, (255, 220, 140)), (60, (255, 255, 220))]:
        draw.ellipse([sun_x - rad, sun_y - rad, sun_x + rad, sun_y + rad], fill=col)

    # 2. Distant Outback Ridges (Purplish red)
    pts_dist = [(0, int(H * 0.52))]
    for x in range(0, W + 100, 120):
        pts_dist.append((x, int(H * 0.50 + math.sin(x * 0.008) * 35 + math.cos(x * 0.015) * 20)))
    pts_dist.extend([(W, H), (0, H)])
    draw.polygon(pts_dist, fill=(110, 45, 35))

    # 3. Midground: The Jack Hills Metaconglomerate Escarpment (Deep Ochre / Terracotta)
    pts_mid = [(0, int(H * 0.62))]
    for x in range(0, W + 80, 80):
        elev = int(math.sin(x * 0.012) * 55 + math.sin(x * 0.025) * 30 + math.cos(x * 0.04) * 15)
        pts_mid.append((x, int(H * 0.60) + elev))
    pts_mid.extend([(W, H), (0, H)])
    draw.polygon(pts_mid, fill=(165, 55, 30))

    # Geological strata banding in the ridge
    for b_y in range(int(H * 0.63), int(H * 0.78), 24):
        for x in range(0, W, 40):
            if (x // 40) % 2 == 0:
                draw.line([(x, b_y + int(math.sin(x * 0.02) * 12)), (x + 35, b_y + int(math.sin((x + 35) * 0.02) * 12))], fill=(195, 80, 45), width=4)

    # 4. Foreground: Ancient Red Desert Plateau & Weathered Quartz Boulders
    pts_fg = [(0, int(H * 0.76))]
    for x in range(0, W + 60, 60):
        pts_fg.append((x, int(H * 0.74 + math.sin(x * 0.018) * 25)))
    pts_fg.extend([(W, H), (0, H)])
    draw.polygon(pts_fg, fill=(125, 35, 20))

    # Quartzite boulders holding detrital zircons
    random.seed(4404)
    for _ in range(35):
        bx = random.randint(50, W - 50)
        by = random.randint(int(H * 0.78), H - 40)
        bw = random.randint(40, 140)
        bh = random.randint(25, 75)
        # Boulder shadow
        draw.ellipse([bx - 10, by + bh - 15, bx + bw + 15, by + bh + 15], fill=(50, 15, 10))
        # Boulder body (Quartz-rich conglomerate)
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(185, 75, 45), outline=(220, 120, 80), width=2)
        # Quartz pebble inclusions
        for _ in range(4):
            px = random.randint(bx + 8, bx + bw - 15)
            py = random.randint(by + 6, by + bh - 12)
            draw.ellipse([px, py, px + random.randint(6, 16), py + random.randint(5, 12)], fill=(240, 220, 200))

    im = im.filter(ImageFilter.GaussianBlur(radius=1.2))
    out_path = os.path.join(ASSETS_DIR, "jack_hills_outback_red.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_zircon_mass_spectrometer():
    """Act 4: SHRIMP Secondary Ion Mass Spectrometer & Atom Probe Laser Chamber."""
    im = Image.new("RGB", (W, H), color=(8, 12, 22))
    draw = ImageDraw.Draw(im)

    # High-tech analytical laboratory background: deep moody slate and cyan grid
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(15, 25, 42), width=1)
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(15, 25, 42), width=1)

    # Central Vacuum Analysis Chamber (circular steel flange with viewport)
    cx, cy = int(W * 0.5), int(H * 0.5)
    for rad, col in [(520, (25, 38, 58)), (460, (40, 58, 85)), (400, (18, 28, 45)), (360, (10, 16, 28))]:
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col, outline=(56, 189, 248), width=3)

    # Flange bolts
    for deg in range(0, 360, 20):
        rad = math.radians(deg)
        bx = cx + int(math.cos(rad) * 490)
        by = cy + int(math.sin(rad) * 490)
        draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(180, 210, 240), outline=(20, 30, 45), width=2)

    # Inside Viewport: Polished Zircon Mount W74/2-36
    # Gold-coated circular specimen disk
    draw.ellipse([cx - 240, cy - 240, cx + 240, cy + 240], fill=(60, 48, 20), outline=(245, 200, 60), width=4)

    # Zircon crystal grain in the center
    z_pts = [
        (cx - 70, cy - 110),
        (cx + 70, cy - 110),
        (cx + 120, cy),
        (cx + 60, cy + 120),
        (cx - 60, cy + 120),
        (cx - 120, cy)
    ]
    draw.polygon(z_pts, fill=(180, 80, 40), outline=(255, 220, 150), width=3)

    # Concentric cathodoluminescence growth rings inside zircon
    for scale in [0.8, 0.6, 0.4, 0.2]:
        ring_pts = [(cx + int((px - cx) * scale), cy + int((py - cy) * scale)) for px, py in z_pts]
        draw.polygon(ring_pts, outline=(255, 180, 90), width=2)

    # Focused Primary Ion Beam (O2- / Cs+ or UV Laser Ablation Beam)
    # Intense electric cyan beam focusing onto a 20-micrometer spot on the zircon
    beam_source_x, beam_source_y = cx - 750, cy - 420
    draw.line([(beam_source_x, beam_source_y), (cx, cy)], fill=(0, 240, 255), width=6)
    draw.line([(beam_source_x, beam_source_y), (cx, cy)], fill=(255, 255, 255), width=2)

    # Ionization impact spark & secondary ion plume
    draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=(255, 255, 255))
    draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline=(56, 189, 248), width=3)

    # Secondary Ion extraction flight tube (heading toward mass spectrometer detector at upper right)
    spec_dest_x, spec_dest_y = cx + 750, cy - 380
    for offset in [-25, 0, 25]:
        draw.line([(cx, cy), (spec_dest_x + offset, spec_dest_y)], fill=(168, 85, 247), width=3)

    im = im.filter(ImageFilter.GaussianBlur(radius=0.8))
    out_path = os.path.join(ASSETS_DIR, "zircon_mass_spectrometer.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


def create_granite_protocontinent():
    """Act 6: Earth's very first granitic craton & continental crust emerging at 680°C."""
    im = Image.new("RGB", (W, H), color=(25, 20, 18))
    draw = ImageDraw.Draw(im)

    # 1. Moody Hadean Sky (Amber haze with volcanic steam clouds)
    for y in range(int(H * 0.55)):
        r_f = y / (H * 0.55)
        r = int(75 + 110 * r_f)
        g = int(45 + 75 * r_f)
        b = int(25 + 35 * r_f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Giant volcanic steam plume rising into amber clouds
    for plume_x, plume_y, prx, pry in [(W * 0.35, H * 0.3, 180, 260), (W * 0.42, H * 0.22, 240, 220)]:
        draw.ellipse([plume_x - prx, plume_y - pry, plume_x + prx, plume_y + pry], fill=(130, 95, 65, 160))

    # 2. Scalding Emerald-Green Iron Ocean Horizon
    for y in range(int(H * 0.52), H):
        r_f = (y - H * 0.52) / (H * 0.48)
        r = int(18 + 15 * r_f)
        g = int(95 - 40 * r_f)  # Emerald ocean
        b = int(60 - 30 * r_f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 3. Rising Granitic Proto-Continental Shield (TTG: Tonalite-Trondhjemite-Granodiorite)
    # Distinct pink-gray granitic massif rising buoyantly above the dark oceanic basalt
    pts_craton = [
        (int(W * 0.15), int(H * 0.72)),
        (int(W * 0.25), int(H * 0.55)),
        (int(W * 0.36), int(H * 0.46)),  # High granitic peak
        (int(W * 0.45), int(H * 0.52)),
        (int(W * 0.58), int(H * 0.44)),  # Second granitic massif
        (int(W * 0.72), int(H * 0.58)),
        (int(W * 0.85), int(H * 0.74)),
        (W, int(H * 0.82)),
        (W, H),
        (0, H),
        (0, int(H * 0.78))
    ]
    # Granitic pink-gray plutonic bedrock
    draw.polygon(pts_craton, fill=(105, 82, 85))

    # Volcanic and hydrothermal vents on the granite shield
    for vx, vy in [(int(W * 0.36), int(H * 0.46)), (int(W * 0.58), int(H * 0.44))]:
        # Molten geothermal fissure
        draw.line([(vx, vy), (vx - 15, vy + 60)], fill=(255, 120, 30), width=5)
        draw.line([(vx, vy), (vx - 15, vy + 60)], fill=(255, 230, 120), width=2)
        # Steam vent
        draw.ellipse([vx - 30, vy - 80, vx + 30, vy], fill=(220, 200, 180, 140))

    # Granite intrusive veins & felsic quartz bands
    for vy in range(int(H * 0.58), int(H * 0.85), 32):
        for vx in range(int(W * 0.2), int(W * 0.8), 60):
            draw.line([(vx, vy), (vx + 45, vy - 12)], fill=(160, 135, 140), width=3)
            if vx % 120 == 0:
                draw.line([(vx, vy), (vx + 35, vy + 18)], fill=(225, 200, 205), width=2)

    # Ocean surf crashing against the cratonic coast with green-white foam
    for sy in range(int(H * 0.70), int(H * 0.88), 18):
        draw.line([(0, sy), (W, sy)], fill=(52, 199, 115), width=2)

    im = im.filter(ImageFilter.GaussianBlur(radius=1.2))
    out_path = os.path.join(ASSETS_DIR, "granite_protocontinent.jpg")
    im.save(out_path, "JPEG", quality=95)
    print("Created:", out_path)


if __name__ == "__main__":
    create_jack_hills_outback()
    create_zircon_mass_spectrometer()
    create_granite_protocontinent()
    print("All Episode 5 background scene assets generated successfully!")
