#!/usr/bin/env bash
#
# Clean out all image files from the frontend images folder.
# Usage: ./clean_images.sh [path-to-images-dir]
#

# Use first arg as images directory, or default relative to this script.
IMG_DIR="${1:-$(dirname "$0")/../frontend/images}"

if [ ! -d "$IMG_DIR" ]; then
  echo "Error: directory '$IMG_DIR' not found."
  exit 1
fi

echo "Removing all files in $IMG_DIR …"
rm -f "${IMG_DIR:?}/"* 

echo "Done."
