```bash
#!/usr/bin/env bash
#
# Clean out image files from the frontend images folder.
# Usage:
#   ./clean_images.sh [--old] [path-to-images-dir]
#
#   --old    Delete only files older than current boot time.
#   path     Path to images directory (default: ../src/wildberryeyezero/frontend/images).

MODE="all"
IMG_DIR="$(dirname "$0")/../src/wildberryeyezero/frontend/images"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --old)
      MODE="old"
      shift
      ;;
    -*|--*)
      echo "Unknown option: $1"
      echo "Usage: $0 [--old] [path-to-images-dir]"
      exit 1
      ;;
    *)
      IMG_DIR="$1"
      shift
      ;;
  esac
done

# Verify directory exists
if [ ! -d "$IMG_DIR" ]; then
  echo "Error: directory '$IMG_DIR' not found."
  exit 1
fi

echo "Cleaning images in $IMG_DIR (mode=$MODE)…"

case "$MODE" in
  all)
    # Remove everything
    rm -f "${IMG_DIR:?}/"*
    ;;

  old)
    # Calculate boot epoch
    uptime_s=$(awk '{print int($1)}' /proc/uptime)
    boot_epoch=$(( $(date +%s) - uptime_s ))

    # Marker file at boot time
    marker=$(mktemp)
    touch -d "@$boot_epoch" "$marker"

    # Delete files older than boot time
    find "$IMG_DIR" -type f ! -newer "$marker" -exec rm -f {} +

    # Cleanup marker
    rm -f "$marker"
    ;;

  *)
    echo "Invalid mode: $MODE"
    echo "Usage: $0 [--old] [path-to-images-dir]"
    exit 1
    ;;
esac

echo "Done."
```
