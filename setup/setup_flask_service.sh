#!/bin/bash

# Usage:
#   ./setup_flask_service.sh <service-name> <path-to-backend> [mode] [--save-raw]
#   mode: "object" (default) or "motion"
#   --save-raw: include this flag to save unannotated frames

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <service-name> <path-to-backend> [mode] [--save-raw]"
  exit 1
fi

SERVICE_NAME=$1
APP_PATH=$2
MODE=${3:-object}
SAVE_RAW_FLAG=${4}

# Validate mode
if [[ "$MODE" != "object" && "$MODE" != "motion" ]]; then
  echo "Invalid mode: $MODE. Must be 'object' or 'motion'."
  exit 1
fi

# Build ExecStart command
EXEC_START="/usr/bin/python3 $APP_PATH/app.py --mode $MODE"
if [ "$SAVE_RAW_FLAG" == "--save-raw" ]; then
  EXEC_START+=" --save-raw"
fi

# Create systemd service file
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=WildBerryEyeZero Flask App ($MODE mode)
After=network.target

[Service]
User=root
WorkingDirectory=$APP_PATH
ExecStart=$EXEC_START
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload, enable, and start service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Show status
sudo systemctl status $SERVICE_NAME --no-pager