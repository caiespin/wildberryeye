#!/bin/bash

# Check if a service name was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <service-name> <path-to-app>"
  exit 1
fi

SERVICE_NAME=$1
APP_PATH=$2

# Create the systemd service file
echo "Creating systemd service file for $SERVICE_NAME..."

cat <<EOF | sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null
[Unit]
Description=Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=$APP_PATH
ExecStart=/usr/bin/python3 $APP_PATH/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start at boot
echo "Enabling $SERVICE_NAME service..."
sudo systemctl enable $SERVICE_NAME

# Start the service
echo "Starting $SERVICE_NAME service..."
sudo systemctl start $SERVICE_NAME

# Display the status of the service
echo "Displaying the status of $SERVICE_NAME..."
sudo systemctl status $SERVICE_NAME
