#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
import zipfile

parser = argparse.ArgumentParser(description="Zip WildBerryEye images by date.")
parser.add_argument("--mode", choices=["object", "motion"], required=True, help="Mode: object or motion")
parser.add_argument("--date", required=False, help="Date in YYYY-MM-DD format. Default: today")
args = parser.parse_args()

# Defaults
if not args.date:
    args.date = datetime.now().strftime("%Y-%m-%d")

repo_base = os.path.expanduser("~/wildberryeye")
image_dir = os.path.join(repo_base, "src", "wildberryeyezero", "frontend", "images")
output_dir = image_dir

prefix = args.mode
zip_filename = f"{prefix}_{args.date}.zip"
zip_path = os.path.join(output_dir, zip_filename)

# Clean up existing zip and marker if they exist
if os.path.exists(zip_path):
    os.remove(zip_path)

done_marker = os.path.join(output_dir, f"{prefix}_{args.date}.DONE")
if os.path.exists(done_marker):
    os.remove(done_marker)

# Collect files to zip
files_to_zip = [
    f for f in os.listdir(image_dir)
    if f.startswith(f"{prefix}_") and args.date.replace("-", "") in f
]

# Zip them
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for fname in files_to_zip:
        fpath = os.path.join(image_dir, fname)
        arcname = os.path.basename(fpath)
        zipf.write(fpath, arcname=arcname)

# Create .DONE marker
with open(done_marker, "w") as f:
    f.write("done\n")

print(f"Zipped {args.mode} detections for {args.date} to: {zip_path}")
print(f"Wrote done marker to: {done_marker}")

