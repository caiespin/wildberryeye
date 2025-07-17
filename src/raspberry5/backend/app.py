from flask import Flask, Response, jsonify
from flask_cors import CORS
from picamera2 import Picamera2
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
picam2 = Picamera2()

# Configure camera preview mode
config = picam2.create_still_configuration(main={"size": (1280, 720)})
picam2.configure(config)
picam2.start()


@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/capture")
def capture_image():
    stream = io.BytesIO()
    picam2.capture_file(stream, format="jpeg")
    stream.seek(0)
    return Response(stream.read(), mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(host="10.0.0.145", port=5000, debug=True)