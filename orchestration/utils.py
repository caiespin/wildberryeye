# utils.py
import subprocess
import logging
import socket
import os
from datetime import datetime
import requests
import time


# ───────────────────────────────
# Reachability Check
# ───────────────────────────────
def check_reachability(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False

# ───────────────────────────────
# Start/Stop Camera Service
# ───────────────────────────────
def stop_service(host, user, service_name="wildberryeye"):
    logging.info(f"[{host}] Stopping camera service...")
    cmd = f"ssh {user}@{host} 'sudo systemctl stop {service_name}.service'"
    subprocess.run(cmd, shell=True, check=False)

def start_service(host, user, service_name="wildberryeye"):
    logging.info(f"[{host}] Starting camera service...")
    cmd = f"ssh {user}@{host} 'sudo systemctl start {service_name}.service'"
    subprocess.run(cmd, shell=True, check=False)

# ───────────────────────────────
# Remote Image Cleanup
# ───────────────────────────────
def clean_images_by_date(host, user, date):
    logging.info(f"[{host}] Cleaning images for date: {date}")
    cmd = f"ssh {user}@{host} 'python3 ~/wildberryeye/scripts/clean_images_by_date.py --date {date}'"
    subprocess.run(cmd, shell=True, check=False)

# ───────────────────────────────
# SSH Utility
# ───────────────────────────────
def ssh_run(host, user, command):
    full_cmd = f"ssh {user}@{host} '{command}'"
    return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

# ───────────────────────────────
# Test Manual Capture
# ───────────────────────────────
def wait_for_capture_api(host, timeout=120, interval=5):
    """Wait for Flask API /api/capture to become available."""
    url = f"http://{host}:5000/api/capture"
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.post(url, timeout=5)
            if response.status_code == 200 and "filename" in response.json():
                logging.info(f"[{host}] API is up and responding.")
                return True
        except requests.exceptions.RequestException as e:
            logging.info(f"[{host}] API not ready: {e}")
        time.sleep(interval)
    logging.error(f"[{host}] Flask API not available after {timeout} seconds.")
    return False

# ───────────────────────────────
# Start Remote Detections
# ───────────────────────────────
def start_remote_detection(host: str, role: str, timeout: int = 60):
    """Starts detection via Flask API and optionally sets baseline for motion."""
    logging.info(f"[{host}] Starting detection via /api/start...")
    try:
        r = requests.post(f"http://{host}:5000/api/start", timeout=5)
        if r.status_code != 200:
            logging.warning(f"[{host}] Failed to start detection. Status code: {r.status_code}")
            return False
        logging.info(f"[{host}] Detection started.")
    except requests.RequestException as e:
        logging.error(f"[{host}] Error while starting detection: {e}")
        return False

    if role == "motion":
        # Give camera a moment to warm up
        time.sleep(2)
        logging.info(f"[{host}] Setting baseline via /api/set-baseline...")
        try:
            b = requests.post(f"http://{host}:5000/api/set-baseline", timeout=5)
            if b.status_code == 200:
                logging.info(f"[{host}] Baseline set successfully.")
            else:
                logging.warning(f"[{host}] Failed to set baseline. Status code: {b.status_code}")
        except requests.RequestException as e:
            logging.error(f"[{host}] Error while setting baseline: {e}")
            return False

    return True