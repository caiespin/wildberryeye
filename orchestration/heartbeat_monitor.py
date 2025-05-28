#!/usr/bin/env python3
import time
import logging
import requests
from datetime import datetime
import os
import sys

# Import utils from orchestration
sys.path.append(os.path.dirname(__file__))
from utils import start_service, wait_for_capture_api, start_remote_detection

# Config
OBJECT_HOST = "192.168.1.247"
MOTION_HOST = "192.168.1.216"
USER = "eye"
INTERVAL = 60  # seconds
MAX_FAILURES = 3
PORT = 5000

# Logging
log_path = os.path.expanduser("~/wildberryeye/logs/wildberryeye_heartbeat.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("=== Running Heartbeat Monitor ===")

failure_counts = {
    "object": 0,
    "motion": 0
}

def check_camera(host, label):
    try:
        response = requests.post(f"http://{host}:{PORT}/api/capture", timeout=10)
        if response.status_code == 200:
            fname = response.json().get("filename", "unknown")
            logging.info(f"[{label}] {host} OK — captured {fname}")
            failure_counts[label] = 0
            return True
        else:
            raise Exception(f"Bad status code: {response.status_code}")
    except Exception as e:
        failure_counts[label] += 1
        logging.warning(f"[{label}] {host} Failed (#{failure_counts[label]}): {e}")
        if failure_counts[label] >= MAX_FAILURES:
            logging.error(f"[{label}] Restarting service after {MAX_FAILURES} failures.")
            restart_and_recover(label, host)
            failure_counts[label] = 0
        return False

def restart_and_recover(label, host):
    # 1. Restart the remote camera service
    start_service(host, USER)
    # 2. Wait for Flask API to come up
    if wait_for_capture_api(host, timeout=180):
        # 3. Restart detection
        success = start_remote_detection(host, role=label)
        if success:
            logging.info(f"[{label}] Detection resumed successfully on {host}")
        else:
            logging.error(f"[{label}] Failed to resume detection on {host}")
    else:
        logging.error(f"[{label}] API did not become available after restart.")

# ──────────────────────────────────────────────
# Main Loop
# ──────────────────────────────────────────────
try:
    while True:
        check_camera(OBJECT_HOST, "object")
        check_camera(MOTION_HOST, "motion")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    logging.info("Heartbeat Monitor terminated by user.")
