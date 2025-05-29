# WildBerryEye Orchestrator Setup

This guide explains how to set up and run the orchestration scripts for coordinating object and motion detection cameras in the WildBerryEye system.

## Requirements

- A central orchestrator device (e.g., Raspberry Pi 5)
- Two detection devices running the WildBerryEye Flask service
- SSH access to both devices (key-based or password-less preferred)
- Python 3 installed on the orchestrator

## File Structure
```bash
wildberryeye/
├── orchestration/
│   ├── start_experiment.py      
│   ├── stop_experiment.py        
│   ├── heartbeat_monitor.py      
│   └── utils.py                   
```

## Overview of Scripts

### start_experiment.py
- Stops any running services
- Cleans images for the target date
- Starts detection services via systemctl
- Waits for /api/capture to become responsive
- Sends a start command to both cameras
- Launches the heartbeat monitor as a systemd user service

### stop_experiment.py
- Stops remote detection on both cameras
- Triggers image zipping remotely
- Downloads ZIP files via rsync
- Validates and cleans up images on the remote devices
- Stops the local heartbeat monitor service

### heartbeat_monitor.py
- Periodically checks if each camera responds to /api/capture
- Automatically restarts remote services and detection if either fails

### utils.py
- Shared helper functions (SSH, rsync, API)

## One-Time Setup for Heartbeat Monitoring

Create the heartbeat systemd service on the orchestrator Pi 
```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/wildberryeye_heartbeat.service
```
With the contents: 
```bash
[Unit]
Description=WildBerryEye Heartbeat Monitor
After=network.target

[Service]
ExecStart=/usr/bin/env python3 /home/decim/wildberryeye/orchestration/heartbeat_monitor.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```
Reload systemd:
```bash
systemctl --user daemon-reexec
systemctl --user daemon-reload
```
Note: No need to enable this service it is started and stopped dynamically from the orchestration scripts.

## Manual Experiment Workflow

### Start an Experiment
```bash
python3 orchestration/start_experiment.py \
  --object-host <IP address> --object-user eye \
  --motion-host <IP address> --motion-user eye

```

### Stop an Experiment
```bash
python3 orchestration/stop_experiment.py \
  --object-host <IP address> --object-user eye \
  --motion-host <IP address> --motion-user eye

```

## Automation via systemd Timers
We'll create two files in ~/.config/systemd/user/:

- wildberryeye_start_experiment.timer → starts the experiment daily
- wildberryeye_stop_experiment.timer → stops the experiment daily

### 1. Create the Start Service and Timer

Start Service:
```bash
nano ~/.config/systemd/user/wildberryeye_start_experiment.service
```
```ini
[Unit]
Description=Start WildBerryEye Experiment

[Service]
ExecStart=/usr/bin/env python3 /home/decim/wildberryeye/orchestration/start_experiment.py \
  --object-host <IP address> --object-user eye \
  --motion-host <IP address> --motion-user eye

```
Start Timer:
```bash
nano ~/.config/systemd/user/wildberryeye_start_experiment.timer
```
```ini
[Unit]
Description=Daily start of WildBerryEye experiment

[Timer]
OnCalendar=*-*-* 07:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

### 2. Create the Stop Service and Timer

Stop Service:
```bash
nano ~/.config/systemd/user/wildberryeye_stop_experiment.service
```
```ini
[Unit]
Description=Stop WildBerryEye Experiment

[Service]
ExecStart=/usr/bin/env python3 /home/decim/wildberryeye/orchestration/stop_experiment.py \
  --object-host <IP address> --object-user eye \
  --motion-host <IP address> --motion-user eye
```
Stop Timer:
```bash
nano ~/.config/systemd/user/wildberryeye_stop_experiment.timer
```
```ini
[Unit]
Description=Daily stop of WildBerryEye experiment

[Timer]
OnCalendar=*-*-* 01:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## Reload and Enable Timers
```bash
systemctl --user daemon-reload
systemctl --user enable wildberryeye_start_experiment.timer
systemctl --user enable wildberryeye_stop_experiment.timer

systemctl --user start wildberryeye_start_experiment.timer
systemctl --user start wildberryeye_stop_experiment.timer
```

### Verify
```bash
systemctl --user list-timers
journalctl --user -u wildberryeye_start_experiment.service
journalctl --user -u wildberryeye_stop_experiment.service
```