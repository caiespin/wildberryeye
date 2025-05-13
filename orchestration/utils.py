#!/usr/bin/env python3
import subprocess
import logging
import socket
import os
import zipfile
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

# ───────────────────────────────
# Trigger Remote Zipping
# ───────────────────────────────
def zip_images_by_date(host, user, role, date):
    """Remotely invoke zipping on a WildBerry for the given date and role (object or motion)."""
    logging.info(f"[{host}] Zipping {role} images for {date}...")
    cmd = f"ssh {user}@{host} 'nohup python3 ~/wildberryeye/scripts/zip_images_by_date.py --mode {role} --date {date} > /dev/null 2>&1 &'"
    subprocess.run(cmd, shell=True, check=False)

# ───────────────────────────────
# Remote Zipping and Polling
# ───────────────────────────────

LOCAL_IMAGE_DIR = "/mnt/nas/WildBerryData/detections"
REMOTE_IMAGE_DIR = "/home/eye/wildberryeye/src/wildberryeyezero/frontend/images"
ZIP_SCRIPT_PATH = "/home/eye/wildberryeye/scripts/zip_images_by_date.py"
POLL_INTERVAL = 10
POLL_TIMEOUT = 10800  # 3 hours

def run_remote_zip(host, user, mode, date):
    zip_name = f"{mode}_{date}.zip"
    done_marker = f"{mode}_{date}.DONE"
    logging.info(f"[{host}] Zipping {mode} images for {date}...")

    cmd = (
        f"cd {REMOTE_IMAGE_DIR} && "
        f"rm -f {zip_name} {done_marker} && "
        f"nohup python3 {ZIP_SCRIPT_PATH} --mode {mode} --date {date} > /dev/null 2>&1 &"
    )
    ssh_run(host, user, cmd)

def poll_for_zip_ready(host, user, mode, date):
    """Poll for .DONE marker and parse its content to determine zip result."""
    marker_path = f"/home/{user}/wildberryeye/src/wildberryeyezero/frontend/images/{mode}_{date}.DONE"
    logging.info(f"[{host}] Polling for completion marker: {marker_path}")
    elapsed = 0

    while elapsed < POLL_TIMEOUT:
        result = ssh_run(host, user, f"cat {marker_path}")
        if result.returncode == 0:
            lines = result.stdout.strip().splitlines()
            status = "unknown"
            for line in lines:
                if line.startswith("status:"):
                    status = line.split(":", 1)[1].strip()
                    break
            if status == "ok":
                logging.info(f"[{host}] DONE marker found. Status: ok")
                return True
            elif status == "empty":
                logging.warning(f"[{host}] DONE marker found. No images to zip (status: empty).")
                return False
            else:
                logging.warning(f"[{host}] DONE marker found but status unknown:\n{result.stdout.strip()}")
                return False
        else:
            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL

    logging.error(f"[{host}] Timeout while waiting for {marker_path}")
    return False


def rsync_zip_file(host, user, mode, date):
    remote_zip = f"{REMOTE_IMAGE_DIR}/{mode}_{date}.zip"
    local_dir = os.path.join(LOCAL_IMAGE_DIR, date, mode)
    os.makedirs(local_dir, exist_ok=True)
    logging.info(f"[{host}] Downloading ZIP: {remote_zip} -> {local_dir}")
    result = subprocess.run([
        "rsync", "-avz", f"{user}@{host}:{remote_zip}", local_dir
    ])
    return result.returncode == 0

def verify_nas_archive(mode, date):
    path = os.path.join(LOCAL_IMAGE_DIR, date, mode)
    zip_file = f"{mode}_{date}.zip"
    full_path = os.path.join(path, zip_file)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
        logging.info(f"[NAS] Archive confirmed at {full_path}")
        return True
    else:
        logging.warning(f"[NAS] ZIP not found or empty at {full_path}")
        return False

# ───────────────────────────────
# Transfer ZIP to NAS and Store
# ───────────────────────────────
def transfer_and_store_zip(host, user, role, date, local_dir="/mnt/nas/WildBerryData/detections"):
    """Transfer the ZIP file from a remote WildBerry and store it in the NAS directory."""
    zipname = f"{role}_{date}.zip"
    remote_path = f"/home/{user}/wildberryeye/src/wildberryeyezero/frontend/images/{zipname}"
    local_path = os.path.join(local_dir, date, role)
    os.makedirs(local_path, exist_ok=True)

    logging.info(f"[{host}] Downloading {zipname} to {local_path}")
    result = subprocess.run(
        ["rsync", "-avz", f"{user}@{host}:{remote_path}", local_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        logging.error(f"[{host}] Rsync failed: {result.stderr.strip()}")
        return False

    zip_path = os.path.join(local_path, zipname)
    if not zipfile.is_zipfile(zip_path):
        logging.warning(f"[{host}] {zipname} failed verification -- update discarded.")
        os.remove(zip_path)
        return False

    logging.info(f"[{host}] ZIP saved to: {zip_path}")
    return True

def stop_remote_detection(host: str):
    """Stops detection via Flask API."""
    logging.info(f"[{host}] Stopping detection via /api/stop...")
    try:
        r = requests.post(f"http://{host}:5000/api/stop", timeout=5)
        if r.status_code == 200:
            logging.info(f"[{host}] Detection stopped.")
            return True
        else:
            logging.warning(f"[{host}] Failed to stop detection. Status code: {r.status_code}")
    except requests.RequestException as e:
        logging.error(f"[{host}] Error while stopping detection: {e}")
    return False

def delete_done_marker(host, user, mode, date):
    """Delete the .DONE file after processing to avoid stale state."""
    done_path = f"/home/{user}/wildberryeye/src/wildberryeyezero/frontend/images/{mode}_{date}.DONE"
    logging.info(f"[{host}] Removing stale marker: {done_path}")
    ssh_run(host, user, f"rm -f {done_path}")
