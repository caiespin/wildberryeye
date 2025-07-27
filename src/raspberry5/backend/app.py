from flask import Flask, Response, jsonify, request, abort, send_from_directory
from flask_cors import CORS
from picamera2 import Picamera2
import io
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
picam2 = Picamera2()


# Configure camera preview mode
config = picam2.create_still_configuration(main={"size": (1280, 720)})
picam2.configure(config)
picam2.start()

SAVE_FOLDER = "captured"
os.makedirs(SAVE_FOLDER, exist_ok=True)


@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/capture")
def capture_image():
    timestamp = request.args.get("t")
    print(f"Received timestamp: {timestamp}")  # For debugging/logging

    filename = f"{timestamp}.jpg"
    filepath = os.path.join(SAVE_FOLDER, filename)

    try:
        # Save file to disk
        picam2.capture_file(filepath, format="jpeg")

        # Also load file content to return
        with open(filepath, "rb") as f:
            img_bytes = f.read()

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
    
if __name__ == '__main__':
    app.run(host="10.0.0.146", port=5000, debug=False)