#!/usr/bin/env python3
import os
import zipfile
import argparse
from datetime import datetime

# ─── Parse CLI Arguments ─────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Zip WildBerryEye detection images by date")
parser.add_argument("--mode", choices=["object", "motion"], required=True, help="Detection type to archive")
parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
args = parser.parse_args()

MODE = args.mode
DATE = args.date
DATE_COMPACT = DATE.replace("-", "")  # e.g., "20250507"

# ─── Paths ───────────────────────────────────────────────────────────
IMAGES_DIR = os.path.expanduser("~/wildberryeye/src/wildberryeyezero/frontend/images")
os.makedirs(IMAGES_DIR, exist_ok=True)

zip_filename = f"{MODE}_{DATE}.zip"
zip_path = os.path.join(IMAGES_DIR, zip_filename)
done_path = os.path.join(IMAGES_DIR, f"{MODE}_{DATE}.DONE")

# ─── Zip Matching Images ─────────────────────────────────────────────
count = 0
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for fname in os.listdir(IMAGES_DIR):
        if not fname.endswith(".jpg"):
            continue
        if not fname.startswith(f"{MODE}_"):
            continue
        if DATE_COMPACT in fname:  # Matches timestamps like motion_20250507-...
            fpath = os.path.join(IMAGES_DIR, fname)
            zf.write(fpath, arcname=fname)
            count += 1

# ─── Completion Marker ───────────────────────────────────────────────
if count > 0:
    with open(done_path, "w") as f:
        f.write(f"{datetime.now().isoformat()}\n")
    print(f"✅ Zipped {count} {MODE} images for {DATE} to: {zip_path}")
else:
    # Remove zip if nothing was added
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print(f"⚠️ No matching {MODE} images found for {DATE} in {IMAGES_DIR}")
