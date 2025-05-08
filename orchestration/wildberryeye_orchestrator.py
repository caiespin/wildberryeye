#!/usr/bin/env python3
import os
import subprocess
import datetime
import argparse
import logging
import socket
import time

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
LOG_FILE = os.path.expanduser("~/wildberryeye/logs/wildberryeye_orchestrator.log")
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

    try:
        zip_base = f"{mode}_{args.date}"
        remote_dir = f"/home/{user}/wildberryeye/src/wildberryeyezero/frontend/images"
        remote_zip = f"{remote_dir}/{zip_base}.zip"
        remote_done = f"{remote_dir}/{zip_base}.DONE"

        # Step 1: Trigger zip script in background
        zip_cmd = (
            f"nohup python3 /home/{user}/wildberryeye/scripts/zip_images_by_date.py "
            f"--mode {mode} --date {args.date} > /dev/null 2>&1 &"
        )
        subprocess.run(f"ssh {user}@{host} '{zip_cmd}'", shell=True, check=True)

        # Step 2: Poll for .DONE marker file
        logging.info(f"[{camera_name}] Polling for completion marker: {remote_done}")
        for attempt in range(60):  # 10 minutes max
            result = subprocess.run(
                f"ssh {user}@{host} 'test -f {remote_done}'",
                shell=True
            )
            if result.returncode == 0:
                logging.info(f"[{camera_name}] DONE marker found.")
                break
            time.sleep(10)
        else:
            raise TimeoutError(f"[{camera_name}] Timeout: .DONE marker not found after 10 minutes.")

        # Step 3: Rsync zip file to NAS
        local_dir = os.path.join(NAS_BASE, args.date, mode)
        os.makedirs(local_dir, exist_ok=True)
        rsync_cmd = f"rsync -avz {user}@{host}:{remote_zip} {local_dir}/"
        subprocess.run(rsync_cmd, shell=True, check=True)

        # Step 4: Unzip and preserve the zip
        zip_path = os.path.join(local_dir, f"{zip_base}.zip")
        subprocess.run(["unzip", "-oq", zip_path, "-d", local_dir], check=True)

        logging.info(f"[{camera_name}] Images collected and extracted to {local_dir}")

    except TimeoutError as e:
        logging.error(str(e))
    except subprocess.CalledProcessError as e:
        logging.error(f"[{camera_name}] Subprocess failed: {e}")


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
