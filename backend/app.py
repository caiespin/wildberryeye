#!/usr/bin/env python3
import os
import threading
import time
import zipfile
import argparse
import io

from flask import Flask, render_template, jsonify, send_file
from flask import request, send_file
import zipfile
from picamera2 import Picamera2, MappedArray
from picamera2.devices import IMX500
from picamera2.devices.imx500 import NetworkIntrinsics, postprocess_nanodet_detection
import cv2
import numpy as np

# ─── CLI Arguments ──────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="WildberryEyeZero Detector")
parser.add_argument(
    "--save-raw",
    action="store_true",
    help="Save raw frames (no bounding boxes). Default saves annotated frames."
)
args = parser.parse_args()
SAVE_RAW = args.save_raw

# ─── Configuration ─────────────────────────────────────────────────────────────

BASE_DIR   = os.path.abspath(os.path.dirname(__file__))
FRONTEND   = os.path.join(BASE_DIR, '..', 'frontend')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_imx_model.rpk')
OUTPUT_DIR = os.path.join(FRONTEND, 'images')

# Detection thresholds
THRESHOLD      = 0.55
IOU            = 0.65
MAX_DETECTIONS = 10

# ─── Flask App Setup ───────────────────────────────────────────────────────────

app = Flask(
    __name__,
    static_folder=FRONTEND,
    template_folder=FRONTEND
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Model Extraction ──────────────────────────────────────────────────────────

if not os.path.exists(MODEL_PATH):
    zip_path = os.path.join(MODELS_DIR, 'best_imx_model.zip')
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(MODELS_DIR)
    else:
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

# ─── IMX500 + Picamera2 Initialization ────────────────────────────────────────

imx500 = IMX500(MODEL_PATH)
intrinsics = imx500.network_intrinsics
if intrinsics is None:
    intrinsics = NetworkIntrinsics()
    intrinsics.task = "object detection"
intrinsics.update_with_defaults()

# Load labels explicitly
labels_file = os.path.join(MODELS_DIR, 'labels.txt')
if os.path.exists(labels_file):
    with open(labels_file, 'r') as f:
        intrinsics.labels = [line.strip() for line in f if line.strip() != '-']
else:
    raise FileNotFoundError("labels.txt not found in models folder")

# Create Picamera2 instance & config—do not start yet
picam2 = Picamera2(imx500.camera_num)
config = picam2.create_preview_configuration(
    main={"format": "RGB888"},
    controls={"FrameRate": intrinsics.inference_rate},
    buffer_count=12
)

# ─── Camera Startup Thread ─────────────────────────────────────────────────────

def camera_init():
    """Load firmware and start the camera—may take several minutes."""
    picam2.start(config, show_preview=False)
    if intrinsics.preserve_aspect_ratio:
        imx500.set_auto_aspect_ratio()

threading.Thread(target=camera_init, daemon=True).start()

# ─── Shared State ───────────────────────────────────────────────────────────────

running = False
lock = threading.Lock()
_last_detections = []  # most recent detections
_last_file = None      # most recent saved filename

# ─── Detection Helpers ─────────────────────────────────────────────────────────

def parse_detections(metadata):
    """Run on-sensor inference and return detections list."""
    outputs = imx500.get_outputs(metadata, add_batch=True)
    if outputs is None:
        return []

    if intrinsics.postprocess == "nanodet":
        boxes, scores, classes = postprocess_nanodet_detection(
            outputs=outputs[0],
            conf=THRESHOLD,
            iou_thres=IOU,
            max_out_dets=MAX_DETECTIONS
        )[0]
        from picamera2.devices.imx500.postprocess import scale_boxes
        iw, ih = imx500.get_input_size()
        boxes = scale_boxes(boxes, 1, 1, ih, iw, False, False)
    else:
        iw, ih = imx500.get_input_size()
        boxes, scores, classes = outputs[0][0], outputs[1][0], outputs[2][0]
        mask = scores > THRESHOLD
        boxes, scores, classes = boxes[mask], scores[mask], classes[mask]
        parts = np.array_split(boxes, 4, axis=1)
        boxes = zip(*(p.flatten() for p in parts))

    dets = []
    for (x, y, w, h), score, cat in zip(boxes, scores, classes):
        if score > THRESHOLD:
            dets.append((int(x), int(y), int(w), int(h),
                         intrinsics.labels[int(cat)], float(score)))
    return dets

def detection_worker():
    """Background detection loop: cheap metadata-only, full capture on hits."""
    global running, _last_detections, _last_file
    while True:
        if not running:
            time.sleep(0.1)
            continue

        metadata = picam2.capture_metadata()
        dets = parse_detections(metadata)
        if dets:
            req = picam2.capture_request()
            with MappedArray(req, "main") as m:
                img = m.array.copy()
            req.release()

            if not SAVE_RAW:
                for x, y, w, h, label, score in dets:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(img, f"{label} {score:.2f}",
                                (x, y-5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            ts = time.strftime("%Y%m%d-%H%M%S")
            fname = f"detection_{ts}.jpg"
            path = os.path.join(OUTPUT_DIR, fname)
            cv2.imwrite(path, img)

            _last_detections = dets
            _last_file = fname

threading.Thread(target=detection_worker, daemon=True).start()

# ─── Flask Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', newest=_last_file)

@app.route('/gallery')
def gallery():
    files = sorted(
        [f for f in os.listdir(OUTPUT_DIR)
         if f.startswith("detection_") or f.startswith("manual_")],
        key=lambda fn: os.path.getmtime(os.path.join(OUTPUT_DIR, fn)),
        reverse=True
    )
    return render_template('gallery.html', images=files)

@app.route('/api/start', methods=['POST'])
def api_start():
    global running
    with lock:
        running = True
    return jsonify(running=True)

@app.route('/api/stop', methods=['POST'])
def api_stop():
    global running
    with lock:
        running = False
    return jsonify(running=False)

@app.route('/api/latest-filename')
def api_latest_filename():
    return jsonify(filename=_last_file)

@app.route('/api/capture', methods=['POST'])
def api_capture():
    """Force a raw capture (manual) and update the last-file."""
    global _last_file, _last_detections
    req = picam2.capture_request()
    with MappedArray(req, "main") as m:
        img = m.array.copy()
    req.release()

    ts = time.strftime("%Y%m%d-%H%M%S")
    fname = f"manual_{ts}.jpg"
    path = os.path.join(OUTPUT_DIR, fname)
    cv2.imwrite(path, img)

    _last_file = fname
    _last_detections = []
    return jsonify(filename=fname)

@app.route('/api/delete-images', methods=['POST'])
def api_delete_images():
    data = request.get_json(force=True)
    names = data.get('filenames', [])
    success = []
    failed = []
    for fname in names:
        path = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(path):
            try:
                os.remove(path)
                success.append(fname)
            except Exception:
                failed.append(fname)
        else:
            failed.append(fname)
    return jsonify(deleted=success, failed=failed)

@app.route('/api/download-images', methods=['POST'])
def api_download_images():
    data = request.get_json(force=True)
    names = data.get('filenames', [])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for fname in names:
            path = os.path.join(OUTPUT_DIR, fname)
            if os.path.exists(path):
                z.write(path, arcname=fname)
    buf.seek(0)
    return send_file(
        buf,
        mimetype='application/zip',
        as_attachment=True,
        download_name='detections.zip'
    )

@app.route('/latest-image')
def latest_image():
    """Stream the most recent frame with detection boxes drawn in red."""
    if not _last_file:
        return ('', 204)
    path = os.path.join(OUTPUT_DIR, _last_file)
    img = cv2.imread(path)
    for x, y, w, h, label, score in _last_detections:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
        cv2.putText(img, f"{label} {score:.2f}",
                    (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    _, buf = cv2.imencode('.jpg', img)
    return send_file(
        io.BytesIO(buf.tobytes()),
        mimetype='image/jpeg',
        download_name='latest_detection.jpg'
    )

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
