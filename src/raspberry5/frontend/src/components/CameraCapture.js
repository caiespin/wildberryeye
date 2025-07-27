import React, { useState } from "react";

const CameraCapture = () => {
  const [imageUrl, setImageUrl] = useState("");
  const [timestamp, setTimestamp] = useState();

  const handleCapture = () => {
    // Add timestamp to avoid caching
    const ts = new Date().getTime();
    setTimestamp(ts);
    setImageUrl(`http://10.0.0.146:5000/capture?t=${ts}`);
  };

  const handleDownload = () => {
    if (!timestamp) return;

    const filename = `${timestamp}.jpg`;
    const downloadUrl = `http://10.0.0.146:5000/download/${filename}`;

    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>Raspberry Pi Camera Capture</h1>
      <p>{timestamp}</p>
      {imageUrl && (
        <img
          src={imageUrl}
          alt="Captured"
          style={{ maxWidth: "100%", border: "1px solid #ccc" }}
        />
      )}
      <br />
      <button onClick={handleCapture} style={{ marginTop: "1em", padding: "0.5em 1em" }}>
        Capture Image
      </button>

      {imageUrl && (
        <button onClick={handleDownload} style={{ marginTop: "1em", padding: "0.5em 1em", marginLeft: "1em" }}>
          Download Image
        </button>
      )}
    </div>
  );
};

export default CameraCapture;
