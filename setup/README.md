# Setup Instructions for WildberryEyeZero

Follow these steps to get WildberryEyeZero up and running on your Raspberry Pi.

---

## 1. Clone & enter the repo
```bash
git clone https://github.com/caiespin/wildberryeyezero.git
cd wildberryeyezero
```
# 2. Copy your ZIP into backend/models/
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

# 3. Package into RPK if you have packerOut.zip
```bash
imx500-package -i packerOut.zip -o .
mv network.rpk best_imx_model.rpk
cd ../..
```

# 4. Install OS-level dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip libcamera-apps libcamera-dev python3-libcamera python3-kms++
sudo apt install imx500-all imx500-tools
sudo apt install python3-opencv python3-munkres
sudo apt install libcap-dev python3-dev
sudo reboot
```

# 5. Install Picamera2 from source
```bash
git clone https://github.com/raspberrypi/picamera2
cd picamera2
pip3 install -e . --break-system-packages
cd ..
```

# 6. Install Python requirements
```bash
pip3 install --upgrade pip
pip3 install -r backend/requirements.txt
```
or 
```bash
sudo apt install -y python3-pip python3-flask python3-numpy python3-pillow
```

# 7. Install & start the WildberryEyeZero service
```bash
chmod +x setup/setup_flask_service.sh
./setup/setup_flask_service.sh wildberryeyezero "$(pwd)/backend"
```

# 8. Verify service status
```bash
sudo systemctl status wildberryeyezero
```