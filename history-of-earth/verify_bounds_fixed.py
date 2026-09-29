from PIL import Image, ImageDraw, ImageFont
import os

def get_font(size, bold=True):
    for f in ['segoeuib.ttf', 'arialbd.ttf']:
        p = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', f)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

im = Image.new('RGB', (1920, 1080))
draw = ImageDraw.Draw(im)

# Proposed font sizes
font_title = get_font(24, bold=True)
font_sub = get_font(14, bold=False)
font_pres_val = get_font(26, bold=True)
font_data = get_font(18, bold=True)
font_small = get_font(14, bold=False)

print("=== VERIFYING SCENE 1 (Card width: 500, margin 25 -> max text width: 450px) ===")
s1_items = [
    "ATMOSPHERIC TELEMETRY",
    "EPOCH: 4.40 Ga • POST-MAGMA OCEAN",
    "SURFACE PRESSURE: 190 ATM",
    "FORCE: 19.2 MPa (HYDRAULIC CRUSH)",
    "ATMOSPHERIC COMPOSITION (VOLUMETRIC):",
    "H2O (Supercritical Steam Vapor)",
    "CO2 (Carbon Dioxide)",
    "SO2 / H2S (Sulfur Dioxides)",
    "N2 (Molecular Nitrogen)",
    "CRITICAL: SUPERCRITICAL FLUID REGIME"
]
fonts_s1 = [font_title, font_sub, font_pres_val, font_data, font_data, font_small, font_small, font_small, font_small, font_small]

for txt, fnt in zip(s1_items, fonts_s1):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    w = bb[2] - bb[0]
    print(f"'{txt:40s}' -> {w:3d}px / 450px [PASS: {w <= 450}]")

print("\n=== VERIFYING SCENE 4 (Card width: 520, margin 25 -> max text width: 470px) ===")
s4_items = [
    "THE THOUSAND-YEAR DELUGE",
    "CATASTROPHIC PLANETARY CONDENSATION",
    "DELUGE CHRONOMETER:",
    "CENTURY 10 OF 10",
    "ELAPSED: ~1,000 YEARS CONTINUOUS DELUGE",
    "PRECIPITATION METRICS:",
    "• RATE: > 50,000 mm / YR (GLOBAL SCALE)",
    "• RAINDROP TEMP: 180°C - 230°C (BOILING ACID)",
    "• ACIDITY: pH 4.2 - 5.0 (SO2 & CO2 CLOUDS)",
    "• DETONATIONS: STEAM EXPLOSIONS ON BASALT",
    "STEAM COLLAPSE PROGRESS: 94%"
]
font_century = get_font(34, bold=True)
fonts_s4 = [font_title, font_sub, font_data, font_century, font_data, font_data, font_small, font_small, font_small, font_small, font_data]

for txt, fnt in zip(s4_items, fonts_s4):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    w = bb[2] - bb[0]
    print(f"'{txt:42s}' -> {w:3d}px / 470px [PASS: {w <= 470}]")
