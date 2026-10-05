import os, sys
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    for f in ['segoeuib.ttf', 'arialbd.ttf']:
        p = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', f)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

im = Image.new('RGB', (1920, 1080))
draw = ImageDraw.Draw(im)

font_title = get_font(24, bold=True)
font_sub = get_font(14, bold=False)
font_data = get_font(18, bold=True)
font_small = get_font(14, bold=False)
font_huge = get_font(28, bold=True)

test_cards = {
    'Act 1': [
        ('PLANETARY RECONNAISSANCE', font_title),
        ('EPOCH: 4.20 Ga • THE DEAD WORLD', font_sub),
        ('GLOBAL BIOMASS: 0.000 kg', font_huge),
        ('STATUS: 100% STERILE GRAVEYARD', font_data),
        ('• ATMOSPHERE: CH4 / CO2 / H2O (NO O2)', font_small),
        ('• SOLAR UV: LETHAL (NO OZONE LAYER)', font_small),
        ('• SURFACE STATUS: PRE-BIOTIC VOID', font_small),
    ],
    'Act 2': [
        ('ABYSSAL BATHYMETRY', font_title),
        ('4,000 METERS BELOW SURFACE', font_sub),
        ('DEPTH PRESSURE: 400 ATM', font_huge),
        ('PRESSURE FORCE: 40.5 MPa (DEEP SHIELD)', font_data),
        ('• WATER TEMP: 65°C - 85°C (STABLE)', font_small),
        ('• AMBIENT LIGHT: 0.00 LUX (PITCH BLACK)', font_small),
        ('• UV EXPOSURE: ZERO (SAFE HARBOR)', font_small),
        ('• STATUS: RADIATION-FREE CRADLE', font_small),
    ],
    'Act 3': [
        ('ALKALINE VENT FIELD', font_title),
        ('LOST CITY-TYPE SERPENTINITE MONOLITH', font_sub),
        ('SPIRE HEIGHT: 50 METERS', font_huge),
        ('SERPENTINIZATION REACTION ACTIVE', font_data),
        ('• FLUID TEMP: 70°C - 90°C (ALKALINE FLOW)', font_small),
        ('• FLUID pH: 9.5 - 11.0 (HYDROXIDE RICH)', font_small),
        ('• DISSOLVED GASES: ENRICHED H2 & CH4', font_small),
        ('• MINERALS: ARAGONITE, BRUCITE & FeS', font_small),
    ],
    'Act 4': [
        ('GEOCHEMICAL PROTON ENGINE', font_title),
        ('ABIOTIC CHEMIOSMOSIS MATRIX', font_sub),
        ('ELECTRICAL POTENTIAL: 200 mV', font_huge),
        ('NATURAL VOLTAGE: 0.20 VOLTS ACROSS ROCK', font_data),
        ('• OCEAN ACIDITY: pH 5.5 (H+ ENRICHED)', font_small),
        ('• VENT FLUIDITY: pH 10.0 (OH- ENRICHED)', font_small),
        ('• NATURAL GRADIENT: Delta-pH = 4.5 UNITS', font_small),
        ('• MODERN EQUIVALENT: MITOCHONDRIA', font_small),
    ],
    'Act 5': [
        ('MINERAL NANO-CHAMBER', font_title),
        ('MACKINAWITE [FeS] CATALYTIC CRUCIBLE', font_sub),
        ('PORE SCALE: 20 MICROMETERS', font_huge),
        ('INORGANIC HARDWARE FOR RNA CODE', font_data),
        ('• CATALYST: FeS & NiS MINERAL CLUSTERS', font_small),
        ('• CONCENTRATION: > 1,000x THERMOPHORESIS', font_small),
        ('• SYNTHESIS: PEPTIDES & RIBONUCLEOTIDES', font_small),
        ('• ROLE: ANCESTRAL STONE CELL WALLS', font_small),
    ],
    'Act 6': [
        ('FIRST AUTONOMOUS PROTOCELL', font_title),
        ('PRE-LUCA BIOENERGETIC THRESHOLD', font_sub),
        ('LIPID BILAYER DETACHMENT', font_huge),
        ('AUTONOMOUS PROTO-ORGANISM FORMED', font_data),
        ('• MEMBRANE: SELF-ASSEMBLED LIPIDS', font_small),
        ('• GENETIC CORE: CATALYTIC RNA RIBOZYMES', font_small),
        ('• POWER: TRAPPED PROTON MOTIVE FORCE', font_small),
        ('• STATUS: INDEPENDENT LIVING CODE', font_small),
    ],
    'Act 7': [
        ('THE COMING EXTINCTION THREAT', font_title),
        ('LATE HEAVY BOMBARDMENT (4.1 Ga)', font_sub),
        ('ASTEROID FLUX: 10,000x', font_huge),
        ('PLANETARY STERILIZATION HAZARD', font_data),
        ('• IMPACT ENERGY: > 10^28 JOULES', font_small),
        ('• BIOSPHERE STAKES: SUB-CRUST SURVIVAL', font_small),
        ('• NEXT: WHEN ROCKS LEARNED TO COOL', font_small),
        ('• EVIDENCE: THE 4.4B YEAR ZIRCON CODE', font_small),
    ]
}

max_allowed = 460
print(f'Checking all text elements against max width {max_allowed}px:')
all_ok = True
for act_name, lines in test_cards.items():
    for txt, fnt in lines:
        bb = draw.textbbox((0, 0), txt, font=fnt)
        w = bb[2] - bb[0]
        if w > max_allowed:
            print(f'  [FAIL] {act_name}: "{txt}" -> {w}px > {max_allowed}px')
            all_ok = False
        else:
            print(f'  [PASS] {act_name}: "{txt}" -> {w}px')

if all_ok:
    print('\nALL ACT TEXT STRINGS FIT PERFECTLY WITHIN HUD CARD BOUNDS!')
else:
    print('\nSOME TEXT STRINGS EXCEEDED BOUNDS!')
