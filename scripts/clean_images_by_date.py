#!/usr/bin/env python3
import os
import re
import argparse
import psutil
from datetime import datetime

DEFAULT_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'wildberryeyezero', 'frontend', 'images')
TS_PATTERN = re.compile(r"_(\d{8})-(\d{6})")

def parse_timestamp(filename):
    match = TS_PATTERN.search(filename)
    if not match:
        return None
    try:
        return datetime.strptime(f"{match.group(1)}-{match.group(2)}", "%Y%m%d-%H%M%S")
    except ValueError:
        return None

def main():
    parser = argparse.ArgumentParser(description="Quietly delete images by date, boot time, or all.")
    parser.add_argument('--all', action='store_true', help='Delete all images (overrides other options).')
    parser.add_argument('--old', action='store_true', help='Delete images older than boot time.')
    parser.add_argument('--date', type=str, help='Delete images from this date (YYYY-MM-DD).')
    parser.add_argument('img_dir', nargs='?', default=DEFAULT_DIR, help='Path to images folder')

    args = parser.parse_args()
    img_dir = os.path.abspath(args.img_dir)

    if not os.path.isdir(img_dir):
        return

    boot_dt = datetime.fromtimestamp(psutil.boot_time()) if args.old else None
    date_filter = None
    if args.date:
        try:
            date_filter = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            return

    for fname in os.listdir(img_dir):
        path = os.path.join(img_dir, fname)
        if not os.path.isfile(path):
            continue

        if args.all:
            try:
                os.remove(path)
            except Exception:
                pass
            continue

        ts = parse_timestamp(fname)
        if ts is None:
            continue
        if args.old and ts >= boot_dt:
            continue
        if date_filter and ts.date() != date_filter:
            continue
        try:
            os.remove(path)
        except Exception:
            pass

if __name__ == '__main__':
    main()
