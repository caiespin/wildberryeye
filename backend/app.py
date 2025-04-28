#!/usr/bin/env python3
import os
import threading
import time

from flask import Flask, render_template, request, url_for, send_from_directory
from picamera2 import Picamera2

# ─── Configuration ─────────────────────────────────────────────────────────────

# Base directory of this script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Frontend lives alongside backend in ../frontend
FRONTEND = os.path.join(BASE_DIR, '..', 'frontend')

# Flask will serve static files (CSS, JS, images) from FRONTEND
# and look for index.html there as its template
app = Flask(
    __name__,
    static_folder=FRONTEND,
    template_folder=FRONTEND
)

# Where captured images will be written
save_path = os.path.join(FRONTEND, 'images')

# Default capture interval (seconds)
capture_frequency = 60

# ─── Camera Setup ──────────────────────────────────────────────────────────────

camera = Picamera2()
camera.start()

lock = threading.Lock()

def capture_images():
    """Continuously capture and save images."""
    while True:
        # snapshot shared state
        lock.acquire()
        path = save_path
        frequency = capture_frequency
        lock.release()

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}.jpg"
        file_path = os.path.join(path, filename)

        # capture & save
        camera.capture_file(file_path)
        time.sleep(frequency)

# start capture thread
thread = threading.Thread(target=capture_images, daemon=True)
thread.start()

# ─── Utility ───────────────────────────────────────────────────────────────────

def find_latest_image(path):
    """Return the filename of the newest .jpg in `path`, or None."""
    try:
        files = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.endswith('.jpg')
        ]
        if not files:
            return None
        latest = max(files, key=os.path.getctime)
        return os.path.basename(latest)
    except Exception as e:
        print(f"Error finding latest image: {e}")
        return None

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def index():
    global save_path, capture_frequency

    if request.method == 'POST':
        lock.acquire()
        save_path = request.form['path']
        capture_frequency = int(request.form['frequency'])
        lock.release()

    latest = find_latest_image(save_path)
    return render_template(
        'index.html',
        path=save_path,
        frequency=capture_frequency,
        image_file=latest
    )

@app.route('/latest-image')
def latest_image():
    """Return the URL (via Flask static) of the newest image, or a placeholder."""
    latest = find_latest_image(save_path)
    if latest:
        return url_for('static', filename='images/' + latest)
    return url_for('static', filename='images/no-image.png')

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # ensure the images folder exists
    os.makedirs(save_path, exist_ok=True)

    # run on port 5000 (matches new structure)
    app.run(host='0.0.0.0', port=5000)
