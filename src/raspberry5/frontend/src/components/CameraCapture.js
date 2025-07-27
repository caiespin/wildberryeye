import React, { useState } from "react";

const CameraCapture = () => {
  const [imageUrl, setImageUrl] = useState("");

  const handleCapture = () => {
    // Add timestamp to avoid caching
    const timestamp = new Date().getTime();
    setImageUrl(`http://10.0.0.146:5000/capture?t=${timestamp}`);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>Raspberry Pi Camera Capture</h1>
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
    </div>
  );
};

export default CameraCapture;
