"""
Generates Tri-Platform Packaging (YouTube, Facebook, Instagram) for all episodes
directly from content_map.csv using Python standard library.
"""

import os
import sys
import csv
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.tri_platform_packaging import generate_tri_platform_package

CONTENT_MAP = os.path.join(PROJECT_ROOT, "content_map.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


def batch_generate_packages(limit: int = 10):
    if not os.path.exists(CONTENT_MAP):
        print("content_map.csv not found")
        return

    with open(CONTENT_MAP, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            if idx > limit:
                break
            era = row["era"].strip()
            pillar = row["pillar"].strip()
            working_title = row["working_title"].strip()
            hook = row["hook"].strip()

            pillar_slug = pillar.lower().replace("&", "").replace("-", " ").replace(" ", "_").strip()
            pillar_slug = "_".join(p for p in pillar_slug.split("_") if p)
            era_slug = era.split(":")[0].lower().strip()
            ep_id = f"{era_slug}_{pillar_slug}_{idx:02d}"

            ep_dir = os.path.join(OUTPUT_DIR, ep_id)
            pkg = generate_tri_platform_package(
                episode_id=ep_id,
                era=era,
                pillar=pillar,
                working_title=working_title,
                hook=hook,
                approved_claims=[{"text": hook, "source_url": "https://nature.com"}],
                shot_list=[{"timestamp_start": "00:00", "scene_title": "OPENING HOOK"}],
                output_dir=ep_dir
            )
            print(f"Generated Tri-Platform Package for #{idx:02d} [{ep_id}]: {working_title}")


if __name__ == "__main__":
    batch_generate_packages(6)
