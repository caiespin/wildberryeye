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

# Setup Instructions for WildberryEyeZero Object Detection Mode

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
  python3-munkres \
  python3-dev \
  libatlas-base-dev \
  libjpeg-dev \
  libcamera-apps \
  libcamera-dev \
  libcap-dev \
  imx500-all \
  imx500-tools \
  build-essential \
  git
sudo reboot
```

## 2. Install Picamera2 from upstream
```bash
cd ~
git clone git@github.com:caiespin/picamera2.git
cd picamera2
pip3 install -e . --break-system-packages
cd ~
```

## 3. Clone & enter WildBerryEye repo
```bash
cd ~
git clone git@github.com:caiespin/wildberryeye.git
cd wildberryeye
git pull origin main
```

## 4. Verify model files are in place
```bash
cd ~
git clone git@github.com:caiespin/wildberryeye.git
cd wildberryeye
git pull origin main
```

## 5. Run the server manually in object‑detection mode
```bash
cd src/wildberryeyezero/backend
python3 app.py --mode object --save-raw
```
Without --save-raw: saves frames with bounding‑box annotations.

With --save-raw: saves raw (unannotated) frames.

Then browse to http://<pi‑ip>:5000 to confirm the live object‑detection UI.

## 6. Install as a systemd service
Make the install-script executable
```bash
cd ~/wildberryeye
chmod +x setup/setup_flask_service.sh
```
Run it
 ```bash
# Annotated object mode:
sudo setup/setup_flask_service.sh wildberry_object ~/wildberryeye/src/wildberryeyezero/backend object

# Raw (no boxes) object mode:
sudo setup/setup_flask_service.sh wildberry_object_raw ~/wildberryeye/src/wildberryeyezero/backend object --save-raw
```

## 7. Manage the service
```bash
sudo systemctl daemon-reload
sudo systemctl status wildberry_object_raw       # or wildberry_object
sudo journalctl -u wildberry_object_raw -f      # live logs
sudo systemctl restart wildberry_object_raw      # apply changes
sudo systemctl stop    wildberry_object_raw
```

# Setup Instructions for WildberryEyeZero Motion Detection Mode

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
  python3-munkres \
  python3-dev \
  libatlas-base-dev \
  libjpeg-dev \
  libcamera-apps \
  libcamera-dev \
  libcap-dev \
  imx500-all \
  imx500-tools \
  build-essential \
  git
sudo reboot
```
## 2. Install Picamera2 from upstream
```bash
cd ~
git clone git@github.com:caiespin/picamera2.git
cd picamera2
pip3 install -e . --break-system-packages
cd ~
```

## 3. Clone & enter WildBerryEye repo
```bash
cd ~
git clone https://github.com/caiespin/wildberryeye.git
cd wildberryeye
```

## 4. Test the app manually before making it a service
```bash
cd src/wildberryeyezero/backend

# Motion detection (works with V2 or IMX500 camera):
python3 app.py --mode motion --save-raw
```
Without --save-raw: saves frames with bounding‑box annotations.

With --save-raw: saves raw (unannotated) frames.

Then browse to http://<pi‑ip>:5000 to confirm the live object‑detection UI.

## 5. Install as a systemd service
Make the install-script executable
```bash
cd ~/wildberryeye
chmod +x setup/setup_flask_service.sh
```
Run it
 ```bash
# Annotated motion (with boxes):
sudo setup/setup_flask_service.sh wildberry_motion ~/wildberryeye/src/wildberryeyezero/backend motion

# Raw motion (no boxes):
sudo setup/setup_flask_service.sh wildberry_motion_raw ~/wildberryeye/src/wildberryeyezero/backend motion --save-raw
```

## 6. Manage the service
```bash
sudo systemctl daemon-reload
sudo systemctl status wildberry_motion_raw      # or wildberry_motion
sudo journalctl -u wildberry_motion_raw -f      # live logs
sudo systemctl restart wildberry_motion_raw     # apply changes
sudo systemctl stop    wildberry_motion_raw
```
