from flask import Flask, Response, jsonify, request, abort, send_from_directory
from flask_cors import CORS
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, MJPEGEncoder
from picamera2.outputs import FileOutput
import threading
import os
import io
from datetime import datetime
from PIL import Image
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
picam2 = Picamera2()


SAVE_FOLDER = "captured"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Track current video recording state
recording = {
    "is_recording": False,
    "filename": None
}

# For MJPEG live streaming
stream = io.BytesIO()
live_encoder = MJPEGEncoder(bitrate=1000000)
live_output = FileOutput(stream)
live_encoder.output = live_output

# helper function to convert h264 to mp4
def convert_to_mp4(input_path, output_path, resolution="1920x1080", framerate=30):
    command = [
        "ffmpeg",
        "-framerate", str(framerate),
        # "-video_size", resolution,
        "-i", input_path,
        "-c", "copy",
        output_path
    ]
    subprocess.run(command, check=True)


# Image Recording Endpoints
@app.route("/capture")
def capture_image():
    timestamp = request.args.get("t")
    print(f"Received timestamp: {timestamp}")  # For debugging/logging

    filename = f"{timestamp}.jpg"
    filepath = os.path.join(SAVE_FOLDER, filename)

    # Configure camera preview mode
    config = picam2.create_still_configuration(main={"size": (1280, 720)})
    picam2.configure(config)
    picam2.start()

    try:
        # Save file to disk
        picam2.capture_file(filepath, format="jpeg")

        # Also load file content to return
        with open(filepath, "rb") as f:
            img_bytes = f.read()

        # Stop the camera after capturing the image
        picam2.stop()
        return Response(img_bytes, mimetype="image/jpeg")

    except Exception as e:
        return {"error": f"Failed to capture image: {e}"}, 500


@app.route("/download/<filename>")
def download_image(filename):
    try:
        # Security check: prevent directory traversal attacks
        if ".." in filename or filename.startswith("/"):
            abort(400, "Invalid filename")

        # Send the file as an attachment to force download
        return send_from_directory(
            SAVE_FOLDER,
            filename,
            as_attachment=True,
            mimetype="image/jpeg"
        )
    except FileNotFoundError:
        abort(404, "File not found")


# Video Recording Endpoints
# start recording
@app.route("/start_record", methods=["POST"])
def start_record():
    if recording["is_recording"]:
        return jsonify({"message": "Already recording"}), 400

    timestamp = request.args.get("t") or datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"video_{timestamp}.h264"
    filepath = os.path.join(SAVE_FOLDER, filename)

    try:
        # video_config = picam2.create_video_configuration()
        # picam2.configure(video_config)
        # picam2.start()

        encoder = H264Encoder(bitrate=1000000)
        output = FileOutput(filepath)
        picam2.start_recording(encoder, output)

        recording["is_recording"] = True
        recording["filename"] = filename
        
        return jsonify({"message": f"Started recording: {filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# stop recording
@app.route("/stop_record", methods=["POST"])
def stop_record():
    if not recording["is_recording"]:
        return jsonify({"message": "Not recording"}), 400

    try:
        picam2.stop_recording()
        recording["is_recording"] = False

        h264_path = os.path.join(SAVE_FOLDER, recording["filename"])
        mp4_path = h264_path.replace(".h264", ".mp4")
        convert_to_mp4(h264_path, mp4_path, resolution="1280x720", framerate=30)
        recording["filename"] = mp4_path

        picam2.stop()

        return jsonify({
            "message": f"Recording stopped. MP4 available.",
            "video": os.path.basename(mp4_path)
        })
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"ffmpeg failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# generate video feed
def generate():
    while True:
        try:
            request = picam2.capture_request()
            image = request.make_image("main")  # returns a PIL.Image
            request.release()

            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            jpeg_bytes = buffer.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n')

        except Exception as e:
            print(f"Streaming error: {e}")
            break

    
@app.route("/video_feed")
def video_feed():
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()
    
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host="10.0.0.146", port=5000, debug=False)