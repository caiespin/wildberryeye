#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./setup_flask_service.sh <service-name> <path-to-backend> [mode] [--save-raw]
# Examples:
#   ./setup_flask_service.sh wildberry_motion \
#     /home/eye/wildberryeye/src/wildberryeyezero/backend \
#     motion \
#     --save-raw

if [ $# -lt 2 ]; then
  echo "Usage: $0 <service-name> <path-to-backend> [mode] [--save-raw]"
  exit 1
fi

SERVICE_NAME=$1
RAW_PATH=$2
MODE=${3:-object}
SAVE_RAW_FLAG=${4:-}

# Validate mode
if [[ "$MODE" != "object" && "$MODE" != "motion" ]]; then
  echo "Error: mode must be 'object' or 'motion'"
  exit 1
fi

# Canonicalize backend path
if ! APP_BACKEND=$(cd "$RAW_PATH" 2>/dev/null && pwd); then
  echo "Error: '$RAW_PATH' is not a directory"
  exit 1
fi

# Determine real home (so PYTHONPATH works under sudo)
if [ -n "${SUDO_USER:-}" ]; then
  USER_HOME=$(eval echo "~$SUDO_USER")
else
  USER_HOME="$HOME"
fi

PICAMERA2_SRC="${USER_HOME}/picamera2"

# Make sure your fork lives there
if [ ! -d "$PICAMERA2_SRC" ]; then
  echo "Error: picamera2 source not found at $PICAMERA2_SRC"
  echo "Clone your fork there first, e.g.:"
  echo "  git clone git@github.com:caiespin/picamera2.git $PICAMERA2_SRC"
  exit 1
fi

# Build the ExecStart command
EXEC_START="/usr/bin/python3 $APP_BACKEND/app.py --mode $MODE"
if [[ "$SAVE_RAW_FLAG" == "--save-raw" ]]; then
  EXEC_START+=" --save-raw"
fi

# Write the systemd unit
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=WildBerryEyeZero Flask App (${MODE} mode)
After=network.target

[Service]
User=root
WorkingDirectory=${APP_BACKEND}
# Prepend your fork so python picks it before any system install
Environment=PYTHONPATH=${PICAMERA2_SRC}

ExecStart=${EXEC_START}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload, enable & start
sudo systemctl daemon-reload
sudo systemctl enable  ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}
sudo systemctl status  ${SERVICE_NAME} --no-pager
