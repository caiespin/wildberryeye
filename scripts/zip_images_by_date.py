#!/usr/bin/env python3
import os
import zipfile
import argparse
from datetime import datetime

# ─── Argument Parsing ─────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Zip WildBerryEye images for a given date")
parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"),
                    help="Date in YYYY-MM-DD format (default: today)")
parser.add_argument("--mode", choices=["object", "motion"], required=True,
                    help="Detection mode (object or motion)")
args = parser.parse_args()

DATE = args.date
MODE = args.mode

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_HOME = os.path.expanduser("~/wildberryeye")
FRONTEND_IMAGES = os.path.join(REPO_HOME, "src", "wildberryeyezero", "frontend", "images")
DAILY_DIR = os.path.join(FRONTEND_IMAGES, DATE)
ZIP_NAME = f"{MODE}_{DATE}.zip"
ZIP_PATH = os.path.join(FRONTEND_IMAGES, ZIP_NAME)

# ─── Ensure Directory Exists ──────────────────────────────────────────────────
os.makedirs(DAILY_DIR, exist_ok=True)

# ─── Collect Matching Files ───────────────────────────────────────────────────
prefix = "detection_" if MODE == "object" else "motion_"
for fname in os.listdir(FRONTEND_IMAGES):
    if fname.startswith(prefix) and DATE.replace("-", "") in fname:
        src = os.path.join(FRONTEND_IMAGES, fname)
        dst = os.path.join(DAILY_DIR, fname)
        os.rename(src, dst)

# ─── Zip the Folder ───────────────────────────────────────────────────────────
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(DAILY_DIR):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, FRONTEND_IMAGES)
            zipf.write(abs_path, arcname=rel_path)

print(f"Zipped {MODE} detections for {DATE} to: {ZIP_PATH}")
