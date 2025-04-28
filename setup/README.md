# Setup Instructions for WildberryEyeZero

Follow these steps to get WildberryEyeZero up and running on your Raspberry Pi.

---

## 1. Clone & enter the repo
```bash
git clone https://github.com/caiespin/wildberryeyezero.git
cd wildberryeyezero
```
# 2. Install OS-level dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip libcamera-apps libcamera-dev
```

# 3. Install Picamera2 from source
```bash
git clone https://github.com/raspberrypi/picamera2
cd picamera2
pip3 install -e . --break-system-packages
cd ..
```

# 4. Install Python requirements
```bash
pip3 install --upgrade pip
pip3 install -r backend/requirements.txt
```
# 5. Install & start the WildberryEyeZero service
```bash
chmod +x setup/setup_flask_service.sh
./setup/setup_flask_service.sh wildberryeyezero "$(pwd)/backend"
```

# 5. Verify service status
```bash
sudo systemctl status wildberryeyezero
```