#!/usr/bin/env bash
LOG_DIR="$(dirname "$0")/../logs/wildberry_logs"
THRESHOLD="$1"

if [[ -z "$THRESHOLD" ]]; then
  echo "Usage: $0 <min_minutes>"
  exit 1
fi

for f in "$LOG_DIR"/wildberry_*.txt; do
  [[ -e "$f" ]] || break
  t0=$(sed -n '3p' "$f" | awk '{print $1}' | cut -d '.' -f1)
  t1=$(tail -n1 "$f" | awk '{print $1}' | cut -d '.' -f1)
  dur=$(( ( $(date -d "$t1" +%s) - $(date -d "$t0" +%s) ) / 60 ))
  if (( dur < THRESHOLD )); then
    echo "Deleting $(basename "$f") (duration ${dur} min)"
    rm "$f"
  fi
done