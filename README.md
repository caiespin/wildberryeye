# WildBerryEye

## About
WildBerryEye is a cost-effective ecological monitoring system designed to capture images of pollinators using embedded AI and motion detection. Built around the Raspberry Pi Zero 2 W and the Sony IMX500 AI camera, the system operates autonomously in the field, enabling researchers to track wildlife activity without constant human supervision. It integrates object detection with YOLOv11 and motion detection through frame differencing, saving metadata-rich images with accurate timestamps.

## Usage
The system supports two modes:
- **AI Detection Mode**: Runs a quantized YOLOv11 model on the IMX500 for species-specific detection.
- **Motion Detection Mode**: Uses frame differencing on the Pi Camera to detect movement and capture images.

Users can access the system through a responsive web interface hosted on the device, which provides:
- Live image preview
- Manual and automatic image capture
- REST API for remote control
- Gallery with batch download and deletion tools

All images are stored with filenames that embed detection labels, timestamps, and capture mode information.

## Test and Deployment
For detailed instructions look at the setup README

### Testing
1. Run the server
```bash
cd wildberryeye/backend
python3 app.py --mode object
```
- Open your browser to `http://<PI_IP>:5000`
- Click Start Detection and verify the live overlay
- Click Capture Now and confirm a new image appears in the gallery
- Navigate to Gallery and test download / delete functionality

### Deployment
1. Install as a systemd service
```bash
cd wildberryeye
chmod +x setup/setup_flask_service.sh
./setup/setup_flask_service.sh wildberryeye backend object
sudo systemctl daemon-reload
sudo systemctl enable wildberryeye
sudo systemctl start wildberryeye
```
2. Verify service status
```bash
sudo systemctl status wildberryeye
```
Once the service is running, the web interface will be available at `http://<PI_IP>:5000` on every boot.

## Support
For issues or questions, contact the authors or open an issue in the project repository.

## Roadmap
- Outdoor hummingbird detection and classification
- Integration with cloud data storage
- Improved thermal management and battery logging

## Project Status
The system has been tested in a controlled lab environment and supports both object and motion detection modes. Software reliability, power usage, and inference behavior have been evaluated using simulated workloads and scheduled image capture. Field deployment is planned as a next phase.

## Authors and Acknowledgment
Isaac Espinosa, Sage Silberman, Teodor Langan  
With thanks to Rossana Maguiña for the original dataset and inspiration

## How to Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the **MIT License**.
