import csv
import os
import re

def audit_file(path):
    print(f"\nAUDITING: {path}")
    if not os.path.exists(path):
        print("  File does not exist!")
        return

    with open(path, "rb") as f:
        raw_bytes = f.read()

    # Detect if opened with cp1252 / latin1 / utf-8
    try:
        utf8_text = raw_bytes.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        utf8_text = raw_bytes.decode("latin1")
        encoding = "latin1"

    # Search for suspicious characters:
    # 1. \ufffd (replacement character)
    # 2. mojibake sequences like â, Ã, Â
    # 3. special unicode quotation marks or dashes that might render as question marks in some tools
    
    issues = []
    lines = utf8_text.splitlines()
    for line_no, line in enumerate(lines, 1):
        # Check for \ufffd
        if "\ufffd" in line:
            issues.append((line_no, "Replacement Character (\\ufffd)", line))
        # Check for Windows-1252 to UTF-8 mojibake
        if re.search(r"â[€\x80-\x9f]", line) or "Ã" in line or "Â" in line:
            issues.append((line_no, "Mojibake sequence (â/Ã/Â)", line))
        # Check for curly quotes or em-dashes that might cause issues if viewed in raw ASCII/cp1252
        non_ascii_chars = set(c for c in line if ord(c) > 127)
        if non_ascii_chars:
            # Let's inspect which non-ascii characters are present
            pass

    print(f"  Encoding: {encoding}, Total lines: {len(lines)}")
    if issues:
        print(f"  FOUND {len(issues)} ISSUES:")
        for lno, itype, ltext in issues[:15]:
            print(f"    Line {lno} [{itype}]: {ltext[:100]}")
    else:
        print("  No mojibake or replacement characters found.")

    # Show all non-ascii characters in the file
    all_non_ascii = set(c for c in utf8_text if ord(c) > 127)
    if all_non_ascii:
        print("  Non-ASCII characters present in file:")
        for c in sorted(all_non_ascii):
            print(f"    '{c}' (U+{ord(c):04X}) - {c.encode('unicode_escape').decode()}")

audit_file("content_map.csv")
audit_file("output/hadean_air_ocean_03/metadata.json")
audit_file("review/gate_b_review_ep3.html")
