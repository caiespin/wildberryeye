#!/usr/bin/env python3
import os
import argparse
import datetime
import time
import logging
import requests
import subprocess
from utils import (
    ssh_run,
    stop_service,
    start_service,
    clean_images_by_date,
    wait_for_capture_api,
    start_remote_detection
)

# ─── Logging Setup ─────────────────────────────────────────────────────────────
LOG_DIR = os.path.expanduser("~/wildberryeye/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "wildberryeye_start_experiment.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

def main():
    parser = argparse.ArgumentParser(description="Start WildBerryEye experiment")
    parser.add_argument("--object-host", required=True, help="Hostname or IP of object detection camera")
    parser.add_argument("--object-user", required=True, help="SSH user for object detection camera")
    parser.add_argument("--motion-host", required=True, help="Hostname or IP of motion detection camera")
    parser.add_argument("--motion-user", required=True, help="SSH user for motion detection camera")
    parser.add_argument("--date", default=datetime.date.today().isoformat(), help="Experiment date (default: today)")
    args = parser.parse_args()

    logging.info("===== WildBerryEye START EXPERIMENT =====")
    logging.info(f"Target date: {args.date}")

    # Step 1: Stop services
    stop_service(args.object_host, args.object_user)
    stop_service(args.motion_host, args.motion_user)

    # Step 2: Clean images from specified date
    clean_images_by_date(args.object_host, args.object_user, args.date)
    clean_images_by_date(args.motion_host, args.motion_user, args.date)

    # Step 3: Start services
    start_service(args.object_host, args.object_user)
    start_service(args.motion_host, args.motion_user)

    # Step 5: Poll /api/capture to ensure it's available
    wait_for_capture_api(args.object_host)
    wait_for_capture_api(args.motion_host)

    # Step 6: Start detections
    success_object = start_remote_detection(args.object_host, "object")
    success_motion = start_remote_detection(args.motion_host, "motion")

    if success_object and success_motion:
        logging.info("Experiment started successfully.")
    else:
        logging.error("Experiment startup failed — one or both cameras did not respond.")
        if not success_object:
            logging.error(f"[{args.object_host}] API failed.")
        if not success_motion:
            logging.error(f"[{args.motion_host}] API failed.")

    # Start heartbeat monitor service
    subprocess.run(["systemctl", "--user", "start", "wildberryeye_heartbeat.service"])
    logging.info("Heartbeat monitor started.")

if __name__ == "__main__":
    main()
