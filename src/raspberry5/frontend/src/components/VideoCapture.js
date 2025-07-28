import React, { useState } from "react";

const VideoCapture = () => {
    const [recording, setRecording] = useState(false);
    const [timestamp, setTimestamp] = useState("");

    const startRecording = async () => {
        const ts = Date.now();
        setTimestamp(ts);

        const res = await fetch(`http://10.0.0.146:5000/start_record?t=${ts}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
        setRecording(true);
        console.log(data.message);
        } else {
        alert(data.error || data.message);
        }
    };

    const stopRecording = async () => {
        const res = await fetch("http://10.0.0.146:5000/stop_record", { method: "POST" });
        const data = await res.json();
        if (res.ok) {
        setRecording(false);
        console.log(data.message);
        } else {
        alert(data.error || data.message);
        }
    };

    return (
        <div style={{ textAlign: "center" }}>
            <h1>Raspberry Pi Camera Video</h1>
            <img
                src="http://10.0.0.146:5000/video_feed"
                alt="Live Stream"
                style={{ width: "640px", height: "auto", border: "1px solid #ccc" }}
            />
            <p>{timestamp ? `Recording Timestamp: ${new Date(timestamp).toLocaleString()}` : "No recording in progress"}</p>

            <button
                onClick={startRecording}
                style={{ marginTop: "1em", padding: "0.5em 1em" }}
                disabled={recording}
            >
                Start Recording
            </button>

            <button
                onClick={stopRecording}
                style={{ marginTop: "1em", padding: "0.5em 1em", marginLeft: "1em" }}
                disabled={!recording}
            >
                Stop Recording
            </button>

            {/* <button
                onClick={downloadVideo}
                style={{ marginTop: "1em", padding: "0.5em 1em", marginLeft: "1em" }}
                disabled={!timestamp}
            >
                Download Video
            </button> */}
        </div>
    )
}

export default VideoCapture;
