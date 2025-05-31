#!/usr/bin/env python3
import argparse
import datetime
import logging
import os
import zipfile
import subprocess
from utils import (
    stop_remote_detection,
    run_remote_zip,
    poll_for_zip_ready,
    rsync_zip_file,
    clean_images_by_date,
    delete_done_marker,
)

# ─── Logging Setup ─────────────────────────────────────────────────────────────
log_dir = os.path.expanduser("~/wildberryeye/logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "wildberryeye_stop_experiment.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

# ─── Stop Heartbeat Service Immediately ──────────────────────────────
subprocess.run(["systemctl", "--user", "stop", "wildberryeye_heartbeat.service"])
logging.info("Heartbeat service stopped.")

# ─── Constants ─────────────────────────────────────────────────────────────────
LOCAL_IMAGE_DIR = os.path.expanduser("~/wildberryeye/analysis/data")

def validate_zip(mode: str, date: str) -> bool:
    """Check if the downloaded ZIP is valid and non-empty."""
    zip_path = os.path.join(LOCAL_IMAGE_DIR, date, mode, f"{mode}_{date}.zip")
    if not os.path.exists(zip_path):
        logging.warning(f"[Local] ZIP not found at {zip_path}")
        return False
    if not zipfile.is_zipfile(zip_path):
        logging.warning(f"[Local] ZIP is not valid: {zip_path}")
        return False
    if os.path.getsize(zip_path) < 100:
        logging.warning(f"[Local] ZIP too small — possibly empty: {zip_path}")
        return False
    return True

# ─── Main Procedure ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Stop WildBerryEye experiment and archive data")
    parser.add_argument("--object-host", required=True)
    parser.add_argument("--object-user", required=True)
    parser.add_argument("--motion-host", required=True)
    parser.add_argument("--motion-user", required=True)
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    args = parser.parse_args()

    logging.info("===== WildBerryEye STOP EXPERIMENT =====")
    logging.info(f"Target date: {args.date}")

    # Step 1: Stop detection remotely
    stop_remote_detection(args.object_host)
    stop_remote_detection(args.motion_host)

    # Step 2: Zip and retrieve data from object detection camera
    run_remote_zip(args.object_host, args.object_user, "object", args.date)
    object_ok = False
    if poll_for_zip_ready(args.object_host, args.object_user, "object", args.date):
        if rsync_zip_file(args.object_host, args.object_user, "object", args.date) and validate_zip("object", args.date):
            logging.info(f"[{args.object_host}] ZIP retrieved and verified. Proceeding with cleanup.")
            clean_images_by_date(args.object_host, args.object_user, args.date)
            delete_done_marker(args.object_host, args.object_user, "object", args.date)
            object_ok = True
        else:
            logging.warning(f"[{args.object_host}] ZIP verification failed. Skipping cleanup.")

    # Step 3: Zip and retrieve data from motion detection camera
    run_remote_zip(args.motion_host, args.motion_user, "motion", args.date)
    motion_ok = False
    if poll_for_zip_ready(args.motion_host, args.motion_user, "motion", args.date):
        if rsync_zip_file(args.motion_host, args.motion_user, "motion", args.date) and validate_zip("motion", args.date):
            logging.info(f"[{args.motion_host}] ZIP retrieved and verified. Proceeding with cleanup.")
            clean_images_by_date(args.motion_host, args.motion_user, args.date)
            delete_done_marker(args.motion_host, args.motion_user, "motion", args.date)
            motion_ok = True
        else:
            logging.warning(f"[{args.motion_host}] ZIP verification failed. Skipping cleanup.")

    logging.info("Experiment stop completed.")

if __name__ == "__main__":
    main()
