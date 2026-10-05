"""
Generates cinematic high-resolution (2304x1296) atmospheric background scene plates
for Episode 7: "The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss".
Pillar: Landscape // Era: Archean: Eoarchean
Adheres to deep-time geology, cratonic shield glaciology, and mineral physics.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "scenes")
os.makedirs(ASSETS_DIR, exist_ok=True)

W, H = 2304, 1296


def create_acasta_river_tundra():
    """Act 1: The remote Canadian sub-arctic tundra, winding dark Acasta River, and glacially carved Precambrian rock bluffs."""
    im = Image.new("RGB", (W, H), color=(25, 30, 42))
    draw = ImageDraw.Draw(im)

    # 1. Moody northern sub-arctic sky (pale indigo gradient with atmospheric cloud shelves)
    for y in range(int(H * 0.55)):
        ratio = y / (H * 0.55)
        r = int(35 + 45 * ratio)
        g = int(45 + 50 * ratio)
        b = int(65 + 65 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Low-hanging arctic cloud strata
    random.seed(4020)
    for c_i in range(12):
        cy = int(H * 0.12 + c_i * 35)
        cw = random.randint(700, 1600)
        cx = random.randint(-200, W - 400)
        ch = random.randint(40, 95)
        draw.ellipse([cx, cy, cx + cw, cy + ch], fill=(70, 80, 100, 60))

    # 2. Distant rugged cratonic hills on the horizon
    hills_pts = [(0, int(H * 0.48))]
    for hx in range(0, W + 100, 80):
        hy = int(H * 0.48 + 35 * math.sin(hx * 0.004) + 18 * math.cos(hx * 0.012) + random.randint(-6, 6))
        hills_pts.append((hx, hy))
    hills_pts.extend([(W, H), (0, H)])
    draw.polygon(hills_pts, fill=(38, 44, 52))

    # 3. Canadian Shield Precambrian bedrock plateau (dark granite-gneiss terraces)
    plateau_pts = [(0, int(H * 0.56))]
    for px in range(0, W + 100, 60):
        py = int(H * 0.56 + 25 * math.sin(px * 0.006) + random.randint(-8, 8))
        plateau_pts.append((px, py))
    plateau_pts.extend([(W, H), (0, H)])
    draw.polygon(plateau_pts, fill=(48, 52, 60))

    # Rugged tundra escarpments and lichen/permafrost patches
    for rx in range(0, W, 40):
        ry = int(H * 0.58 + random.randint(0, int(H * 0.38)))
        rw = random.randint(60, 200)
        rh = random.randint(20, 60)
        # Glacial striations / dark gneiss slabs
        draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=6, fill=(32, 35, 42), outline=(65, 75, 88), width=2)
        # Arctic moss & rust-red iron lichen
        if random.random() > 0.4:
            draw.ellipse([rx + 10, ry + 5, rx + rw - 15, ry + rh - 10], fill=(75, 55, 35))

    # 4. The Winding Acasta River (cold deep steel-blue reflecting pale sky)
    river_pts_top = []
    river_pts_bot = []
    for step in range(30):
        prog = step / 29.0
        y_pos = int(H * 0.54 + prog * (H * 0.46))
        # S-curve river
        curve = math.sin(prog * math.pi * 2.2) * (W * 0.22)
        x_center = int(W * 0.50 + curve)
        w_half = int(35 + prog * 240)
        river_pts_top.append((x_center - w_half, y_pos))
        river_pts_bot.append((x_center + w_half, y_pos))

    river_polygon = river_pts_top + river_pts_bot[::-1]
    draw.polygon(river_polygon, fill=(28, 48, 68), outline=(60, 95, 130), width=3)

    # Water shimmer highlights
    for s_i in range(15):
        s_y = int(H * 0.62 + s_i * 24)
        s_w = int(40 + s_i * 18)
        s_x = int(W * 0.45 + math.sin(s_i * 0.4) * 80)
        draw.line([(s_x, s_y), (s_x + s_w, s_y)], fill=(120, 165, 200), width=2)

    # Atmospheric vignette / cold mist
    out_im = im.filter(ImageFilter.GaussianBlur(radius=1.2))
    d_out = ImageDraw.Draw(out_im)
    # Frost riming along banks
    for fr in range(40):
        fx = random.randint(0, W)
        fy = random.randint(int(H * 0.6), H)
        draw.line([(fx, fy), (fx + random.randint(10, 30), fy)], fill=(180, 200, 220), width=1)

    target_path = os.path.join(ASSETS_DIR, "acasta_river_canadian_tundra.jpg")
    out_im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def create_acasta_outcrop_expedition():
    """Act 2: Close-up cratonic bedrock outcrop, geological fault foliation, hammer scale, and field markings."""
    im = Image.new("RGB", (W, H), color=(35, 38, 45))
    draw = ImageDraw.Draw(im)

    # Massive cratonic cliff face with 45-degree folded gneissic banding
    for y in range(H):
        ratio = y / H
        r = int(45 + 25 * ratio)
        g = int(48 + 25 * ratio)
        b = int(55 + 30 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Ancient metamorphic deformation folds (S-folds & Z-folds in the rock)
    random.seed(4021)
    for band_idx in range(-20, 50):
        base_y = band_idx * 32
        is_felsic = (band_idx % 2 == 0)
        col = (175, 160, 145) if is_felsic else (25, 28, 34)  # Light tonalite vs dark amphibolite
        pts = []
        for x in range(0, W + 40, 20):
            fold = 45 * math.sin(x * 0.005 + band_idx * 0.3) + 20 * math.sin(x * 0.015)
            y = int(base_y + x * 0.35 + fold)
            pts.append((x, y))
        draw.line(pts, fill=col, width=random.randint(8, 22))

    # Rock fracture joints / tectonic cleavage lines
    for f_i in range(18):
        fx1 = random.randint(100, W - 100)
        fy1 = random.randint(50, H - 200)
        fx2 = fx1 + random.randint(-120, 120)
        fy2 = fy1 + random.randint(180, 420)
        draw.line([(fx1, fy1), (fx2, fy2)], fill=(12, 14, 18), width=3)

    # Geological Expedition Survey Markers:
    # 1. Steel chisel / field rock hammer placed on outcrop for scale (lower center)
    hx, hy = int(W * 0.48), int(H * 0.72)
    # Steel handle (blue rubberized grip)
    draw.line([(hx - 90, hy + 45), (hx + 40, hy - 20)], fill=(30, 90, 180), width=14)
    draw.line([(hx - 90, hy + 45), (hx + 40, hy - 20)], fill=(20, 60, 140), width=10)
    # Chrome steel shaft
    draw.line([(hx + 40, hy - 20), (hx + 110, hy - 55)], fill=(210, 220, 230), width=10)
    # Pick head (pointed pick on left, square flat hammer face on right)
    draw.line([(hx + 85, hy - 85), (hx + 135, hy - 25)], fill=(180, 195, 210), width=18)
    draw.polygon([(hx + 70, hy - 95), (hx + 90, hy - 80), (hx + 100, hy - 65)], fill=(150, 165, 180))

    # 2. Fluorescent field sampling flag / tag pinned into bedrock
    fx, fy = int(W * 0.32), int(H * 0.52)
    draw.line([(fx, fy), (fx, fy - 110)], fill=(180, 190, 200), width=3)
    draw.polygon([(fx, fy - 110), (fx + 55, fy - 95), (fx, fy - 80)], fill=(255, 90, 20))
    # Survey sample ID tag
    draw.rectangle([fx + 8, fy - 50, fx + 85, fy - 22], fill=(245, 245, 240), outline=(20, 20, 20), width=1)

    target_path = os.path.join(ASSETS_DIR, "acasta_outcrop_geology_expedition.jpg")
    im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def create_acasta_ttg_macro():
    """Act 3: High-magnification petrographic slab of Tonalite-Trondhjemite-Granodiorite (TTG) showing quartz, feldspar, biotite."""
    im = Image.new("RGB", (W, H), color=(20, 22, 28))
    draw = ImageDraw.Draw(im)

    # Interlocking crystalline mosaic texture
    random.seed(4022)
    tile_size = 45
    for ty in range(0, H + tile_size, tile_size):
        for tx in range(0, W + tile_size, tile_size):
            # Mineral type based on TTG composition:
            # 60% Plagioclase feldspar (pearly white/grey)
            # 25% Quartz (smoky translucent grey/glassy)
            # 15% Biotite / Hornblende (black/deep greenish brown mafic laths)
            rand_val = random.random()
            poly_pts = [
                (tx + random.randint(-15, 15), ty + random.randint(-15, 15)),
                (tx + tile_size + random.randint(-15, 15), ty + random.randint(-15, 15)),
                (tx + tile_size + random.randint(-15, 15), ty + tile_size + random.randint(-15, 15)),
                (tx + random.randint(-15, 15), ty + tile_size + random.randint(-15, 15))
            ]

            if rand_val < 0.20:
                # Biotite / amphibole mafic band
                col = (random.randint(18, 28), random.randint(20, 32), random.randint(22, 34))
            elif rand_val < 0.50:
                # Smoky quartz crystal
                col = (random.randint(110, 135), random.randint(115, 140), random.randint(130, 155))
            elif rand_val < 0.85:
                # Plagioclase feldspar
                col = (random.randint(185, 215), random.randint(180, 210), random.randint(175, 205))
            else:
                # Trace potassium feldspar / accessory titanite
                col = (random.randint(190, 220), random.randint(135, 160), random.randint(130, 150))

            draw.polygon(poly_pts, fill=col, outline=(30, 32, 38), width=1)

    # Superimpose high-strain mylonitic foliation streaks (flowing ductile ribbons)
    for s_i in range(35):
        sy = int(s_i * 38 + random.randint(-10, 10))
        pts = [(0, sy)]
        for sx in range(100, W + 100, 120):
            sy_curv = sy + int(math.sin(sx * 0.003) * 25 + random.randint(-5, 5))
            pts.append((sx, sy_curv))
        draw.line(pts, fill=(15, 18, 24), width=random.randint(4, 14))

    # Microscopic mineral cleavage twinning lines on feldspars
    for c_i in range(120):
        cx = random.randint(50, W - 50)
        cy = random.randint(50, H - 50)
        draw.line([(cx, cy), (cx + 35, cy + 12)], fill=(240, 245, 255), width=1)

    target_path = os.path.join(ASSETS_DIR, "acasta_ttg_gneiss_macro.jpg")
    im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def create_shrimp_zircon_geochronology():
    """Act 4: Sensitive High Resolution Ion Microprobe (SHRIMP) cathodoluminescence (CL) zircon image with ion spot & decay ratios."""
    im = Image.new("RGB", (W, H), color=(8, 12, 18))
    draw = ImageDraw.Draw(im)

    # High-tech analytical vacuum chamber interface (dark blue glass grid background)
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(16, 24, 38), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(16, 24, 38), width=1)

    # Hero Centerpiece: Cathodoluminescence (CL) image of 4.02 Ga Acasta Zircon crystal
    zx, zy = int(W * 0.50), int(H * 0.50)
    # Zircon euhedral prismatic crystal outline (elongated doubly terminated prism)
    prism_pts = [
        (zx, zy - 380),             # Top pyramidal apex
        (zx + 210, zy - 220),       # Top right shoulder
        (zx + 210, zy + 220),       # Bottom right shoulder
        (zx, zy + 380),             # Bottom pyramidal apex
        (zx - 210, zy + 220),       # Bottom left shoulder
        (zx - 210, zy - 220)        # Top left shoulder
    ]
    draw.polygon(prism_pts, fill=(25, 35, 52), outline=(56, 189, 248), width=4)

    # Concentric magmatic oscillatory growth zoning rings (alternating dark/luminescent zones)
    for r_scale in np.linspace(0.12, 0.95, 24):
        ring_pts = [
            (zx, int(zy - 380 * r_scale)),
            (int(zx + 210 * r_scale), int(zy - 220 * r_scale)),
            (int(zx + 210 * r_scale), int(zy + 220 * r_scale)),
            (zx, int(zy + 380 * r_scale)),
            (int(zx - 210 * r_scale), int(zy + 220 * r_scale)),
            (int(zx - 210 * r_scale), int(zy - 220 * r_scale))
        ]
        ring_col = (110, 180, 240) if int(r_scale * 100) % 2 == 0 else (40, 65, 95)
        draw.polygon(ring_pts, outline=ring_col, width=3)

    # Primary SHRIMP Oxygen Ion Beam Target Spot (25-micrometer ablation pit in core)
    pit_x, pit_y = zx + 40, zy - 60
    # Outer targeting crosshairs
    draw.line([(pit_x - 70, pit_y), (pit_x + 70, pit_y)], fill=(255, 60, 60), width=2)
    draw.line([(pit_x, pit_y - 70), (pit_x, pit_y + 70)], fill=(255, 60, 60), width=2)
    # Laser / Ion crater glow
    draw.ellipse([pit_x - 30, pit_y - 30, pit_x + 30, pit_y + 30], fill=(255, 220, 80), outline=(255, 80, 20), width=3)
    draw.ellipse([pit_x - 12, pit_y - 12, pit_x + 12, pit_y + 12], fill=(255, 255, 255))

    # Analytical telemetry overlays (spectrum curves on left and right)
    # U-Pb Concordia Curve (Left)
    draw.line([(120, int(H * 0.75)), (520, int(H * 0.75))], fill=(100, 115, 135), width=2)
    draw.line([(120, int(H * 0.75)), (120, int(H * 0.25))], fill=(100, 115, 135), width=2)
    concordia_pts = []
    for px in range(120, 520, 10):
        t = (px - 120) / 400.0
        py = int(H * 0.75 - 280 * (t ** 0.65))
        concordia_pts.append((px, py))
    draw.line(concordia_pts, fill=(56, 189, 248), width=3)
    # Acasta datum point on concordia
    acasta_pt = concordia_pts[-8]
    draw.ellipse([acasta_pt[0] - 8, acasta_pt[1] - 8, acasta_pt[0] + 8, acasta_pt[1] + 8], fill=(74, 222, 128), outline=(255, 255, 255), width=2)

    target_path = os.path.join(ASSETS_DIR, "shrimp_zircon_acasta_geochronology.jpg")
    im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def create_iceland_protocontinent():
    """Act 5: The 4.02 Ga Iceland-like geodynamic model: thick oceanic basalt plateau, mantle plume, hydrothermal steam, and felsic magma generation."""
    im = Image.new("RGB", (W, H), color=(18, 12, 15))
    draw = ImageDraw.Draw(im)

    # 1. Dark Archean atmosphere with volcanic gas haze (sulfur gold & amber glow)
    for y in range(int(H * 0.52)):
        ratio = y / (H * 0.52)
        r = int(50 + 130 * ratio)
        g = int(30 + 70 * ratio)
        b = int(20 + 25 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Colossal mantle plume volcanic rift on horizon
    rift_x = int(W * 0.50)
    for glow_r in [380, 260, 150, 70]:
        draw.ellipse([rift_x - glow_r, int(H * 0.45 - glow_r * 0.4), rift_x + glow_r, int(H * 0.45 + glow_r * 0.4)], fill=(255, 100 + glow_r // 4, 30, 80))

    # Steaming volcanic rift chimneys & ash plumes
    for steam_i in range(16):
        sx = int(W * 0.20 + steam_i * 85 + random.randint(-20, 20))
        sy = int(H * 0.46)
        sw = random.randint(35, 90)
        sh = random.randint(140, 320)
        draw.ellipse([sx - sw, sy - sh, sx + sw, sy], fill=(120, 90, 80, 70))

    # 2. Vast oceanic basalt plateau (jagged, black, steaming vesicular basalt lava fields)
    plateau_pts = [(0, int(H * 0.48))]
    for px in range(0, W + 80, 40):
        py = int(H * 0.48 + 18 * math.sin(px * 0.008) + random.randint(-6, 6))
        plateau_pts.append((px, py))
    plateau_pts.extend([(W, H), (0, H)])
    draw.polygon(plateau_pts, fill=(28, 22, 24))

    # Glowing molten magma fissures cutting across the basalt crust
    fissure_pts = [(int(W * 0.50), int(H * 0.46))]
    for step in range(25):
        prog = step / 24.0
        fy = int(H * 0.46 + prog * (H * 0.54))
        fx = int(W * 0.50 + math.sin(prog * 8.0) * (W * 0.18) + (prog * 200))
        fissure_pts.append((fx, fy))

    draw.line(fissure_pts, fill=(255, 90, 20), width=16)
    draw.line(fissure_pts, fill=(255, 210, 80), width=6)
    draw.line(fissure_pts, fill=(255, 255, 230), width=2)

    # 3. Emerald green ocean washing against steaming black lava shores (lower left/right)
    sea_pts = [(0, int(H * 0.72)), (int(W * 0.35), int(H * 0.78)), (int(W * 0.42), H), (0, H)]
    draw.polygon(sea_pts, fill=(20, 75, 55))
    for wv in range(8):
        wy = int(H * 0.75 + wv * 28)
        draw.line([(0, wy), (int(W * 0.38 - wv * 30), wy + 15)], fill=(50, 160, 115), width=3)

    target_path = os.path.join(ASSETS_DIR, "eoarchean_iceland_protocontinent.jpg")
    im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def create_hafnium_crustal_recycling():
    """Act 6: Deep crustal geodynamic cross-section: mantle plume upwelling, partial melting of 4.2 Ga mafic proto-crust, and hafnium isotope tracking."""
    im = Image.new("RGB", (W, H), color=(15, 10, 20))
    draw = ImageDraw.Draw(im)

    # Cross-section layers:
    # 0 - 280px: Eoarchean Ocean & Upper Basalt Crust
    # 280 - 650px: 4.2 Ga Hydrated Mafic Lower Crust (Proto-crust melting zone)
    # 650 - 1296px: Churning Convective Asthenospheric Mantle Plume

    # Upper crust
    draw.rectangle([0, 0, W, 280], fill=(35, 42, 50))
    # Hydrated mafic proto-crust (thick greenstone / amphibolite slab)
    draw.rectangle([0, 280, W, 680], fill=(42, 55, 48))
    # Mantle furnace
    for my in range(680, H):
        ratio = (my - 680) / (H - 680)
        r = int(120 + 130 * ratio)
        g = int(35 + 45 * ratio)
        b = int(15 + 20 * ratio)
        draw.line([(0, my), (W, my)], fill=(r, g, b))

    # Mantle Plume (central upwelling column of hot rising peridotite)
    plume_cx = int(W * 0.50)
    for p_rad in [380, 280, 180, 90]:
        draw.ellipse([plume_cx - p_rad, 480, plume_cx + p_rad, H + 200], fill=(255, 80 + p_rad // 3, 25, 75))

    # Felsic Magma Chamber (The Acasta TTG Nursery at depth 20-30 km)
    magma_x, magma_y = plume_cx, 440
    draw.ellipse([magma_x - 260, magma_y - 120, magma_x + 260, magma_y + 120], fill=(255, 180, 60), outline=(255, 240, 160), width=4)
    draw.ellipse([magma_x - 180, magma_y - 75, magma_x + 180, magma_y + 75], fill=(255, 230, 140))

    # Ascending granitic diapirs punching upward toward surface
    for d_off in [-140, 0, 140]:
        dx = magma_x + d_off
        draw.line([(dx, magma_y - 80), (dx, 220)], fill=(255, 210, 120), width=18)
        draw.ellipse([dx - 35, 180, dx + 35, 250], fill=(240, 245, 255), outline=(255, 180, 60), width=3)

    # Isotopic flow arrows (white dashed curves showing crustal remelting)
    for arrow_x in range(plume_cx - 320, plume_cx + 340, 80):
        draw.line([(arrow_x, 620), (magma_x + (arrow_x - plume_cx) // 3, magma_y + 60)], fill=(56, 189, 248), width=3)

    target_path = os.path.join(ASSETS_DIR, "hafnium_isotope_crustal_recycling.jpg")
    im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def create_slave_craton_keel():
    """Act 7: Global tectonic cutaway: The buoyant Slave Craton with its 250-km-deep lithospheric mantle keel anchored in convective mantle."""
    im = Image.new("RGB", (W, H), color=(6, 8, 14))
    draw = ImageDraw.Draw(im)

    # Outer space stars (top portion)
    random.seed(4023)
    for _ in range(350):
        sx = random.randint(0, W)
        sy = random.randint(0, int(H * 0.28))
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 230, 255))

    # Planetary curvature (horizon arc at y ~ 320px)
    cx, cy = int(W * 0.50), int(H * 1.8)
    planet_r = int(H * 1.55)
    # Atmospheric halo
    draw.ellipse([cx - planet_r - 25, cy - planet_r - 25, cx + planet_r + 25, cy + planet_r + 25], outline=(56, 189, 248), width=18)

    # Global emerald ocean
    draw.ellipse([cx - planet_r, cy - planet_r, cx + planet_r, cy + planet_r], fill=(18, 55, 45))

    # The Slave Craton Proto-continent on the horizon (Center)
    craton_w = 480
    craton_pts = [
        (cx - craton_w // 2, int(H * 0.26)),
        (cx - craton_w // 4, int(H * 0.23)),
        (cx + craton_w // 4, int(H * 0.24)),
        (cx + craton_w // 2, int(H * 0.27)),
        (cx + craton_w // 2 - 20, int(H * 0.32)),
        (cx - craton_w // 2 + 20, int(H * 0.32))
    ]
    draw.polygon(craton_pts, fill=(160, 150, 140), outline=(230, 235, 245), width=3)

    # Sub-surface Lithospheric Keel (V-shaped deep triangular diamond/depleted peridotite root extending 250 km down)
    keel_pts = [
        (cx - craton_w // 2 + 30, int(H * 0.32)),
        (cx + craton_w // 2 - 30, int(H * 0.32)),
        (cx + 80, int(H * 0.75)),
        (cx, int(H * 0.82)),
        (cx - 80, int(H * 0.75))
    ]
    # Keel body (cold, rigid, buoyant depleted mantle)
    draw.polygon(keel_pts, fill=(35, 70, 95), outline=(56, 189, 248), width=3)

    # Mantle convection cells flowing harmlessly AROUND the keel (protecting it from destruction)
    # Left convection cell
    draw.arc([cx - 480, int(H * 0.40), cx - 120, int(H * 0.88)], start=90, end=270, fill=(255, 120, 40), width=6)
    # Right convection cell
    draw.arc([cx + 120, int(H * 0.40), cx + 480, int(H * 0.88)], start=270, end=90, fill=(255, 120, 40), width=6)

    # Telemetry text label on keel
    draw.line([(cx + 40, int(H * 0.60)), (cx + 280, int(H * 0.60))], fill=(56, 189, 248), width=2)
    draw.ellipse([cx + 36, int(H * 0.60) - 4, cx + 44, int(H * 0.60) + 4], fill=(255, 255, 255))

    target_path = os.path.join(ASSETS_DIR, "slave_craton_lithospheric_keel.jpg")
    im.save(target_path, quality=94)
    print(f"  [OK] Generated {target_path}")
    return target_path


def main():
    print("=" * 80)
    print("GENERATING EPISODE 7 CINEMATIC SCENE PLATES (2304x1296 QHD)")
    print("Episode: 'The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss'")
    print("=" * 80)

    p1 = create_acasta_river_tundra()
    p2 = create_acasta_outcrop_expedition()
    p3 = create_acasta_ttg_macro()
    p4 = create_shrimp_zircon_geochronology()
    p5 = create_iceland_protocontinent()
    p6 = create_hafnium_crustal_recycling()
    p7 = create_slave_craton_keel()

    print("\nALL 7 EPISODE 7 SCENE PLATES GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
