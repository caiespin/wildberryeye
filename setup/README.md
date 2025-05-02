# Setup Instructions for WildberryAiZero

Follow these steps to get WildberryAiZero up and running on your Raspberry Pi.

---

## 1. Clone & enter the repo
```bash
git clone https://github.com/caiespin/wildberryeyezero.git
cd wildberryeyezero
```
## 2. Copy your ZIP into backend/models/
```bash
mkdir -p backend/models
cd backend/models
wget https://github.com/caiespin/wildberryeyezero/releases/download/v1.0.0/best_imx_model.zip
unzip best_imx_model.zip \
  "content/runs/detect/train/weights/best_imx_model/*" \
  -d .
mv content/runs/detect/train/weights/best_imx_model/* ./
rm -rf content
```

## 3. Package into RPK if you have packerOut.zip
```bash
imx500-package -i packerOut.zip -o .
mv network.rpk best_imx_model.rpk
cd ../..
```

## 4. Install OS-level dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip libcamera-apps libcamera-dev python3-libcamera python3-kms++
sudo apt install imx500-all imx500-tools
sudo apt install python3-opencv python3-munkres
sudo apt install libcap-dev python3-dev
sudo reboot
```

## 5. Install Picamera2 from source
```bash
git clone https://github.com/raspberrypi/picamera2
cd picamera2
pip3 install -e . --break-system-packages
cd ..
```

## 6. Install Python requirements
```bash
pip3 install --upgrade pip
pip3 install -r backend/requirements.txt
```
or 
```bash
sudo apt install -y python3-pip python3-flask python3-numpy python3-pillow
```

## 7. Install & start the WildberryEyeZero service
```bash
chmod +x setup/setup_flask_service.sh
./setup/setup_flask_service.sh wildberryeyezero "$(pwd)/backend"
```

## 8. Verify service status
```bash
sudo systemctl status wildberryeyezero
```

# Setup Instructions for WildberryEyeZero

Follow these steps to get WildberryEyeZero up and running on your Raspberry Pi.

## 1. Update system and install core packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  python3-pip \
  python3-flask \
  python3-numpy \
  python3-opencv \
  python3-libcamera \
  python3-pil \
  python3-av \
  python3-v4l2 \
  python3-prctl \
  python3-piexif \
  python3-simplejpeg \
  python3-pidng \
  python3-jsonschema \
  python3-libarchive-c \
  python3-tqdm \
  libatlas-base-dev \
  libjpeg-dev \
  libcamera-apps \
  libcamera-dev \
  libcap-dev \
  build-essential \
  git
```
## 2. Install Picamera2 from upstream
```bash
cd ~
git clone https://github.com/raspberrypi/picamera2
cd picamera2
pip3 install -e . --break-system-packages
cd ..
```

## 3. Clone & enter WildBerryEye repo
```bash
git clone https://github.com/caiespin/wildberryeyezero.git
cd wildberryeyezero
```

## 4. Test the app manually before making it a service
```bash
cd backend

# Motion detection (works with V2 or IMX500 camera):
python3 app.py --mode motion
```

## 5. Install as a systemd service
Make the install-script executable
```bash
chmod +x setup/setup_flask_service.sh
```
Run it
 ```bash
sudo setup/setup_flask_service.sh wildberry_motion ~/wildberryeyezero/backend motion --save-raw
```

## 6. Manage the service
```bash
sudo systemctl daemon-reload
sudo systemctl status wildberry_motion
sudo journalctl -u wildberry_motion -f
sudo systemctl restart wildberry_motion
sudo systemctl stop wildberry_motion
```
