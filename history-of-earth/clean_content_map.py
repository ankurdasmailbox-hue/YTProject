"""
Cleans content_map.csv and generate_full_content_map.py of all non-ASCII / mojibake-prone characters:
- Replaces em-dashes (—) and en-dashes (–) with clean standard hyphens (' - ' / '-')
- Replaces smart curly apostrophes (’) with standard single quotes (')
- Replaces smart quotes (“ ”) with standard quotes (")
- Replaces degree signs (°) with ' deg ' (e.g., '350 deg C', '-50 deg C')
- Replaces diacritics (ț -> t, ñ -> n, ó -> o) so names like Hateg, Canadon, and Cerrejon render cleanly on all platforms.
"""

import csv
import os
import unicodedata

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(PROJECT_ROOT, "content_map.csv")
PY_PATH = os.path.join(PROJECT_ROOT, "generate_full_content_map.py")


def clean_text(text: str) -> str:
    """Replaces all non-ASCII characters with clean, platform-universal ASCII equivalents."""
    replacements = {
        "—": " - ",     # Em-dash
        "–": "-",        # En-dash
        "’": "'",        # Right single curly quote
        "‘": "'",        # Left single curly quote
        "“": '"',        # Left double curly quote
        "”": '"',        # Right double curly quote
        "°": " deg ",    # Degree sign
        "ț": "t",        # Romanian t with comma (Hateg)
        "Ț": "T",
        "ñ": "n",        # Spanish n with tilde (Canadon)
        "Ñ": "N",
        "ó": "o",        # Spanish o with acute (Cerrejon)
        "Ó": "O",
        "é": "e",
        "É": "E",
        "á": "a",
        "Á": "A",
        "…": "...",      # Ellipsis
    }

    for char, repl in replacements.items():
        text = text.replace(char, repl)

    # Normalize any multiple spaces created by replacements
    while "  " in text:
        text = text.replace("  ", " ")

    # Fallback: if any non-ASCII characters remain, normalize via NFKD
    cleaned_chars = []
    for c in text:
        if ord(c) > 127:
            # Try to decompose
            decomposed = unicodedata.normalize("NFKD", c)
            ascii_equiv = "".join([d for d in decomposed if ord(d) <= 127])
            cleaned_chars.append(ascii_equiv if ascii_equiv else "?")
        else:
            cleaned_chars.append(c)

    return "".join(cleaned_chars)


def clean_content_map_csv():
    print(f"Cleaning {CSV_PATH}...")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    cleaned_rows = []
    changes_count = 0
    for row in rows:
        cleaned_row = {}
        for k, v in row.items():
            cleaned_v = clean_text(v)
            if cleaned_v != v:
                changes_count += 1
            cleaned_row[k] = cleaned_v
        cleaned_rows.append(cleaned_row)

    # Write out cleanly
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"  [SUCCESS] Cleaned {changes_count} field values in content_map.csv!")


def clean_generator_script():
    print(f"Cleaning {PY_PATH}...")
    with open(PY_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned_content = clean_text(content)
    with open(PY_PATH, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    print(f"  [SUCCESS] Cleaned {PY_PATH}!")


def verify_pure_ascii(path):
    with open(path, "rb") as f:
        data = f.read()
    non_ascii = [(idx, b) for idx, b in enumerate(data) if b > 127]
    if non_ascii:
        print(f"  [WARN] {path} still has {len(non_ascii)} non-ASCII bytes: {non_ascii[:5]}")
    else:
        print(f"  [VERIFIED] {path} is 100% PURE CLEAN ASCII! Zero garbage characters possible on any platform.")


if __name__ == "__main__":
    clean_content_map_csv()
    clean_generator_script()
    verify_pure_ascii(CSV_PATH)
    verify_pure_ascii(PY_PATH)
