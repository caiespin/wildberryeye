#!/usr/bin/env python3
import os
import time
import psutil
import socket
from datetime import datetime

# Directory for per-boot logs
LOG_DIR = os.path.join(os.path.dirname(__file__),
                       '..', 'logs', 'wildberry_logs')
os.makedirs(LOG_DIR, exist_ok=True)


def get_boot_time_iso():
    """Return last boot timestamp as ISO string without colons."""
    bt = datetime.fromtimestamp(psutil.boot_time())
    return bt.isoformat().replace(':', '-').split('.')[0]


def get_cpu_temp():
    """Read CPU temperature via psutil or sysfs fallback."""
    temps = psutil.sensors_temperatures()
    if 'cpu-thermal' in temps:
        entry = temps['cpu-thermal'][0]
        return f"{entry.current:.2f}°C"
    if 'coretemp' in temps:
        entry = temps['coretemp'][0]
        return f"{entry.current:.2f}°C"
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            return f"{int(f.read().strip())/1000:.2f}°C"
    except:
        return "N/A"


def has_internet(host="8.8.8.8", port=53, timeout=2):
    """Check for internet connectivity by attempting a socket connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


if __name__ == '__main__':
    boot_iso = get_boot_time_iso()

    # Wait for clock sync and internet connectivity (up to 5 minutes)
    max_wait = 300  # seconds
    waited = 0
    sync_ok = False

    while waited < max_wait:
        now_ts = datetime.utcnow().timestamp()
        if now_ts >= psutil.boot_time() and has_internet():
            sync_ok = True
            break
        time.sleep(1)
        waited += 1

    # Choose filename suffix if sync failed
    suffix = '' if sync_ok else '_NOSYNC'
    logfile = os.path.join(LOG_DIR, f"wildberry_{boot_iso}{suffix}.txt")

    # Write header (with warning if needed)
    with open(logfile, 'w') as f:
        f.write(f"# Boot time: {boot_iso}\n")
        if not sync_ok:
            f.write(f"# WARNING: clock not synchronized or no internet after {max_wait} seconds\n")
        f.write("Timestamp\tBoot\tTemp\tCPU%\tLoad1m\n")

    # Prime CPU percent measurement
    psutil.cpu_percent(interval=None)

    # Logging loop
    while True:
        now   = datetime.utcnow().isoformat()
        temp  = get_cpu_temp()
        cpu   = psutil.cpu_percent(interval=None)
        load1 = os.getloadavg()[0]
        with open(logfile, 'a') as f:
            f.write(f"{now}\t{boot_iso}\t{temp}\t{cpu:.1f}%\t{load1:.2f}\n")
        time.sleep(60)
