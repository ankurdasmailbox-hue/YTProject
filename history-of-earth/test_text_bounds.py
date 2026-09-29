from PIL import Image, ImageDraw, ImageFont
import os, sys

def get_font(size, bold=True):
    for f in ['segoeuib.ttf', 'arialbd.ttf']:
        p = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', f)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

im = Image.new('RGB', (1920, 1080))
draw = ImageDraw.Draw(im)

font_title = get_font(26, bold=True)
font_data = get_font(20, bold=True)
font_small = get_font(15, bold=False)
font_huge = get_font(42, bold=True)

print("=== SCENE 1 TEXT WIDTHS (Card limit: 480, margin 30 -> max text width: 420) ===")
s1_texts = [
    ("ATMOSPHERIC TELEMETRY", font_title),
    ("EPOCH: 4.40 Ga • POST-MAGMA OCEAN", font_small),
    ("SURFACE PRESSURE: 190 ATM", font_huge),
    ("FORCE: 19.2 MPa (HYDRAULIC CRUSH)", font_data),
    ("ATMOSPHERIC COMPOSITION (VOLUMETRIC):", font_data),
    ("H2O (Supercritical Steam Vapor)", font_small),
    ("CO2 (Carbon Dioxide)", font_small),
    ("SO2 / H2S (Sulfur Dioxides)", font_small),
    ("N2 (Molecular Nitrogen)", font_small),
    ("CRITICAL: SUPERCRITICAL FLUID REGIME", font_small)
]
for txt, fnt in s1_texts:
    bb = draw.textbbox((0, 0), txt, font=fnt)
    w = bb[2] - bb[0]
    print(f"Text: '{txt}' -> Width: {w}px (Max: 420px) -> Exceeds? {w > 420}")

# In Scene 1, check the gas value placements too:
# panel_x + 400 with card width 480. panel_x + 30 is left margin, panel_x + 480 is right edge.
# If gval is drawn at panel_x + 400:
bb = draw.textbbox((0, 0), "84.2%", font=font_data)
w_val = bb[2] - bb[0]
print(f"Gas val '84.2%' drawn at 400: 400 + {w_val} = {400 + w_val}px vs card width 480px. Right margin: {480 - (400 + w_val)}px")

# Also check gas mini bar:
# panel_x + 30 to panel_x + 440 -> width 410px.

print("\n=== SCENE 4 TEXT WIDTHS (Card limit: 500, margin 30 -> max text width: 440) ===")
s4_texts = [
    ("THE THOUSAND-YEAR DELUGE", font_title),
    ("CATASTROPHIC PLANETARY CONDENSATION", font_small),
    ("DELUGE CHRONOMETER:", font_data),
    ("CENTURY 10 OF 10", font_huge),
    ("ELAPSED TIME: ~1000 YEARS CONTINUOUS RAIN", font_data),
    ("PRECIPITATION METRICS:", font_data),
    ("• RATE: > 50,000 mm / YEAR (GLOBAL SCALE)", font_data),
    ("• RAINDROP TEMP: 180°C - 230°C (BOILING ACID)", font_small),
    ("• ACIDITY: pH 4.2 - 5.0 (DISSOLVED SO2 & CO2)", font_small),
    ("• SURFACE EXPLOSIONS: VAPOR DETONATIONS ON BASALT", font_small),
    ("STEAM COLLAPSE PROGRESS: 94%", font_data)
]
for txt, fnt in s4_texts:
    bb = draw.textbbox((0, 0), txt, font=fnt)
    w = bb[2] - bb[0]
    print(f"Text: '{txt}' -> Width: {w}px (Max: 440px) -> Exceeds? {w > 440}")
