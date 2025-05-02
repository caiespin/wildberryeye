#!/usr/bin/env python3
import os
import time
import psutil
from datetime import datetime

# Directory for per-boot logs
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs', 'wildberry_logs')
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


if __name__ == '__main__':
    # Prepare log file
    boot_iso = get_boot_time_iso()
    logfile = os.path.join(LOG_DIR, f"wildberry_{boot_iso}.txt")
    with open(logfile, 'w') as f:
        f.write(f"# Boot time: {boot_iso}\n")
        f.write("Timestamp\tBoot\tTemp\tCPU%\tLoad1m\n")

    # Prime CPU percent
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