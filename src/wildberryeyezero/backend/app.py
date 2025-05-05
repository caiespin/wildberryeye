#!/usr/bin/env python3
import os
import threading
import time
import zipfile
import argparse
import io
import socket
import getpass
from datetime import datetime

from flask import Flask, render_template, jsonify, send_file, request
from picamera2 import Picamera2, MappedArray
from picamera2.devices import IMX500
from picamera2.devices.imx500 import NetworkIntrinsics, postprocess_nanodet_detection
import cv2
import numpy as np

# ─── CLI Arguments ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="WildberryEyeZero Detector")
parser.add_argument("--save-raw", action="store_true", help="Save raw frames (no bounding boxes). Default saves annotated frames.")
parser.add_argument("--mode", choices=["object", "motion"], default="object", help="Operation mode: 'object' for AI-camera object detection; 'motion' for motion detection on any camera.")
args = parser.parse_args()
SAVE_RAW = args.save_raw
MODE = args.mode

# ─── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND = os.path.join(BASE_DIR, '..', 'frontend')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_imx_model.rpk')
OUTPUT_DIR = os.path.join(FRONTEND, 'images')

THRESHOLD = 0.55
IOU = 0.65
MAX_DETECTIONS = 10
MOTION_THRESH = 25
MIN_AREA = 500

# Metadata
HOSTNAME = socket.gethostname()
USERNAME = getpass.getuser()

# ─── Flask App Setup ───────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=FRONTEND, template_folder=FRONTEND)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Camera & Model Initialization ─────────────────────────────────────────────
imx500 = None
intrinsics = None
if MODE == "object":
    imx500 = IMX500(MODEL_PATH)
    intrinsics = imx500.network_intrinsics or NetworkIntrinsics()
    intrinsics.task = "object detection"
    intrinsics.update_with_defaults()
    labels_file = os.path.join(MODELS_DIR, 'labels.txt')
    if os.path.exists(labels_file):
        with open(labels_file, 'r') as f:
            intrinsics.labels = [line.strip() for line in f if line.strip() != '-']
    else:
        raise FileNotFoundError("labels.txt not found in models folder")

camera_index = imx500.camera_num if imx500 else 0
picam2 = Picamera2(camera_index)
config = picam2.create_preview_configuration(
    main={"format": "RGB888"},
    controls={"FrameRate": intrinsics.inference_rate if intrinsics else 30},
    buffer_count=12
)

def camera_init():
    picam2.start(config, show_preview=False)
    if MODE == "object" and intrinsics.preserve_aspect_ratio:
        imx500.set_auto_aspect_ratio()

threading.Thread(target=camera_init, daemon=True).start()

# ─── Shared State ───────────────────────────────────────────────────────────────
running = False
lock = threading.Lock()
_last_detections = []
_last_file = None
prev_gray = None
baseline_set = False

# ─── Object-Detection Helper ────────────────────────────────────────────────────
def parse_detections(metadata):
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
            dets.append((int(x), int(y), int(w), int(h), intrinsics.labels[int(cat)], float(score)))
    return dets

# ─── Detection Worker ───────────────────────────────────────────────────────────
def detection_worker():
    global running, _last_detections, _last_file, prev_gray, baseline_set
    while True:
        if not running:
            time.sleep(0.1)
            continue

        metadata = picam2.capture_metadata() if MODE == "object" else None

        if MODE == "object":
            dets = parse_detections(metadata)
            settings = f"CONF{int(THRESHOLD*100)}_IOU{int(IOU*100)}"
        else:
            if not baseline_set:
                time.sleep(0.5)
                continue
            frame = picam2.capture_array()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            diff = cv2.absdiff(gray, prev_gray)
            _, thresh = cv2.threshold(diff, MOTION_THRESH, 255, cv2.THRESH_BINARY)
            cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hits = [cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) > MIN_AREA]
            dets = [(x, y, w, h, "motion", 1.0) for (x, y, w, h) in hits]
            prev_gray = gray
            settings = f"THRESH{MOTION_THRESH}_AREA{MIN_AREA}"

        if dets:
            req = picam2.capture_request()
            with MappedArray(req, "main") as m:
                img = m.array.copy()
            req.release()

            if not SAVE_RAW:
                for x, y, w, h, label, score in dets:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, f"{label} {score:.2f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            prefix = "motion" if MODE == "motion" else "detection"
            fname = f"{prefix}_{ts}_{HOSTNAME}_{USERNAME}_{settings}.jpg"
            path = os.path.join(OUTPUT_DIR, fname)
            cv2.imwrite(path, img)

            _last_detections = dets
            _last_file = fname

threading.Thread(target=detection_worker, daemon=True).start()

# ─── Flask Routes ───────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', newest=_last_file)

@app.route('/gallery')
def gallery():
    files = sorted(
        [f for f in os.listdir(OUTPUT_DIR) if f.startswith(("detection_", "motion_", "manual_"))],
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

@app.route('/api/capture', methods=['POST'])
def api_capture():
    global _last_file, _last_detections
    req = picam2.capture_request()
    with MappedArray(req, "main") as m:
        img = m.array.copy()
    req.release()
    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    fname = f"manual_{ts}_{HOSTNAME}_{USERNAME}.jpg"
    path = os.path.join(OUTPUT_DIR, fname)
    cv2.imwrite(path, img)
    _last_file = fname
    _last_detections = []
    return jsonify(filename=fname)

@app.route('/api/set-baseline', methods=['POST'])
def api_set_baseline():
    global prev_gray, baseline_set
    frame = picam2.capture_array()
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    baseline_set = True
    return jsonify(baseline=True)

@app.route('/api/delete-images', methods=['POST'])
def api_delete_images():
    data = request.get_json(force=True)
    names = data.get('filenames', [])
    success, failed = [], []
    for fname in names:
        path = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(path):
            try:
                os.remove(path)
                success.append(fname)
            except:
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
    return send_file(buf, mimetype='application/zip', as_attachment=True, download_name='detections.zip')

@app.route('/latest-image')
def latest_image():
    if not _last_file:
        return ('', 204)
    path = os.path.join(OUTPUT_DIR, _last_file)
    img = cv2.imread(path)
    for x, y, w, h, label, score in _last_detections:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, f"{label} {score:.2f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    _, buf = cv2.imencode('.jpg', img)
    return send_file(io.BytesIO(buf.tobytes()), mimetype='image/jpeg', download_name='latest_detection.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
