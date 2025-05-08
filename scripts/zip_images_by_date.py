#!/usr/bin/env python3
import os
import sys
import zipfile
import argparse
from datetime import datetime

# ─── Argument Parsing ───────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Zip WildBerryEye images for a given date")
parser.add_argument("--mode", choices=["object", "motion"], required=True, help="Detection type")
parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
args = parser.parse_args()

mode = args.mode
date_str = args.date

# ─── Paths ──────────────────────────────────────────────────────────────────────
HOME_DIR = os.path.expanduser("~")
REPO_ROOT = os.path.join(HOME_DIR, "wildberryeye")
IMAGES_DIR = os.path.join(REPO_ROOT, "src", "wildberryeyezero", "frontend", "images")
zip_name = f"{mode}_{date_str}.zip"
zip_path = os.path.join(IMAGES_DIR, zip_name)

# ─── Collect Matching Files ─────────────────────────────────────────────────────
files_to_zip = []
for filename in os.listdir(IMAGES_DIR):
    if not filename.endswith(".jpg"):
        continue
    if not filename.startswith(f"{mode}_"):
        continue
    if date_str.replace("-", "") in filename:
        files_to_zip.append(filename)

if not files_to_zip:
    print(f"[WARN] No {mode} images found for {date_str} in flat directory.")
    sys.exit(0)

# ─── Create Zip File ────────────────────────────────────────────────────────────
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for fname in files_to_zip:
        abs_path = os.path.join(IMAGES_DIR, fname)
        zipf.write(abs_path, arcname=fname)

print(f"Zipped {mode} detections for {date_str} to: {zip_path}")

# ─── Optional Marker File ───────────────────────────────────────────────────────
done_marker = os.path.join(IMAGES_DIR, f"{mode}_{date_str}.DONE")
with open(done_marker, "w") as f:
    f.write("done\n")
