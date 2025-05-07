#!/usr/bin/env python3
import os
import subprocess
import datetime
import argparse
import logging
import socket

# ─── CLI Arguments ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="WildBerryEye Orchestration Script")
parser.add_argument("--object-host", required=True, help="Hostname or IP of object detection camera")
parser.add_argument("--object-user", required=True, help="SSH username for object detection camera")
parser.add_argument("--motion-host", required=True, help="Hostname or IP of motion detection camera")
parser.add_argument("--motion-user", required=True, help="SSH username for motion detection camera")
parser.add_argument("--date", default=datetime.date.today().isoformat(),
                    help="Date to collect images for (YYYY-MM-DD), defaults to today")
args = parser.parse_args()

# ─── Paths & Config ─────────────────────────────────────────────────────────────
NAS_BASE = "/mnt/nas/WildBerryData/detections"
REPO_HOME = "/home/{user}/wildberryeye"
ZIP_SCRIPT = "scripts/zip_images_by_date.py"
LOG_FILE = "/var/log/wildberryeye_orchestrator.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def check_ping(host):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", host])
        return True
    except subprocess.CalledProcessError:
        return False

def check_ntp_sync():
    try:
        timedatectl = subprocess.check_output(["timedatectl", "show", "-p", "NTPSynchronized", "--value"]).decode().strip()
        ntp_status = subprocess.check_output(["systemctl", "is-active", "systemd-timesyncd"]).decode().strip()
        return timedatectl == "yes", ntp_status
    except Exception:
        return False, "unknown"

def collect_zip(camera_name, host, user, mode):
    logging.info(f"Connecting to {host} ({camera_name}) to zip {args.date} {mode} data...")
    ssh_cmd = (
        f"ssh {user}@{host} "
        f"'python3 {REPO_HOME.format(user=user)}/{ZIP_SCRIPT} "
        f"--mode {mode} --date {args.date}'"
    )
    result = subprocess.run(ssh_cmd, shell=True)
    if result.returncode != 0:
        logging.error(f"Zipping failed on {host} ({mode})")
        return False

    # Rsync ZIP file from camera to NAS
    remote_zip = f"{REPO_HOME.format(user=user)}/{mode}_{args.date}.zip"
    local_dir = os.path.join(NAS_BASE, args.date, mode)
    os.makedirs(local_dir, exist_ok=True)
    rsync_cmd = f"rsync -avz {user}@{host}:{remote_zip} {local_dir}/"
    result = subprocess.run(rsync_cmd, shell=True)
    if result.returncode != 0:
        logging.error(f"Rsync failed from {host} ({mode})")
        return False

    # Unzip it
    zip_path = os.path.join(local_dir, f"{mode}_{args.date}.zip")
    subprocess.run(["unzip", "-o", zip_path, "-d", local_dir])
    os.remove(zip_path)

    logging.info(f"{mode.capitalize()} images from {host} collected and extracted to {local_dir}")
    return True

# ─── MAIN ───────────────────────────────────────────────────────────────────────
logging.info("Starting WildBerryEye orchestration with --date=%s", args.date)

# Step 1: Reachability & Clock Check
for name, host in [("object", args.object_host), ("motion", args.motion_host)]:
    reachable = check_ping(host)
    if reachable:
        logging.info(f"{name.capitalize()} Detection camera ({host}) is reachable.")
    else:
        logging.warning(f"{name.capitalize()} Detection camera ({host}) is NOT reachable!")

synced, ntp_status = check_ntp_sync()
logging.info(f"System clock synchronized: {'yes' if synced else 'no'}")
logging.info(f"NTP service: {ntp_status}")

# Step 2: Collect & Extract ZIPs
collect_zip("object", args.object_host, args.object_user, "object")
collect_zip("motion", args.motion_host, args.motion_user, "motion")
