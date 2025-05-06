#!/usr/bin/env python3
import os
import re
import argparse
import psutil
from datetime import datetime

# Directory for frontend images by default
DEFAULT_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'wildberryeyezero', 'frontend', 'images')

# Regex to extract timestamp from filenames: detection_YYYYMMDD-HHMMSS or manual_YYYYMMDD-HHMMSS
TS_PATTERN = re.compile(r"_(?P<ts>\d{8}-\d{6})")


def parse_timestamp(filename):
    m = TS_PATTERN.search(filename)
    if not m:
        return None
    try:
        return datetime.strptime(m.group('ts'), "%Y%m%d-%H%M%S")
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Clean images by age based on embedded timestamp in filename"
    )
    parser.add_argument(
        '--old', action='store_true',
        help='Delete only files older than current boot time.'
    )
    parser.add_argument(
        'img_dir', nargs='?', default=DEFAULT_DIR,
        help='Path to frontend images directory'
    )
    args = parser.parse_args()

    img_dir = os.path.abspath(args.img_dir)
    if not os.path.isdir(img_dir):
        print(f"Error: directory '{img_dir}' not found.")
        return

    boot_dt = datetime.fromtimestamp(psutil.boot_time())
    print(f"Boot time: {boot_dt.isoformat()}")
    print(f"Cleaning images in '{img_dir}' (mode={'old' if args.old else 'all'})")

    for fname in os.listdir(img_dir):
        path = os.path.join(img_dir, fname)
        if not os.path.isfile(path):
            continue
        if not args.old:
            # delete all
            os.remove(path)
            print(f"Deleted: {fname}")
        else:
            ts = parse_timestamp(fname)
            if ts and ts < boot_dt:
                os.remove(path)
                print(f"Deleted old: {fname} (timestamp {ts.isoformat()})")
            else:
                print(f"Keep: {fname}")

if __name__ == '__main__':
    main()
