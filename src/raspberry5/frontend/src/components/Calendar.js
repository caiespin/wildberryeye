import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../";

function CalendarComp() {
  const [date, setDate] = useState(new Date());

  const [recording, setRecording] = useState(false);

  const startRecording = async () => {
    try {
      await fetch("http://10.0.0.146:5000/start_recording");
      setRecording(true);
    } catch (err) {
      console.error("Failed to start recording", err);
    }
  };

  const stopRecording = async () => {
    try {
      await fetch("http://10.0.0.146:5000/stop_recording");
      setRecording(false);
    } catch (err) {
      console.error("Failed to stop recording", err);
    }
  };


  return (
    <div className="calendar">
      <h2 className="text-xl font-bold mb-4">Pick a Date</h2>
      <Calendar onChange={setDate} value={date} />
      <p className="mt-4">Selected Date: {date.toDateString()}</p>
      <button className="download-button">Submit</button>

      <h2>Raspberry Pi Camera Stream</h2>
      <img
        src="http://10.0.0.146:5000/video_feed"
        alt="Live Stream"
        style={{ width: "640px", height: "auto", border: "1px solid #ccc" }}
      />
      <div style={{ marginTop: "1rem" }}>
        <button onClick={startRecording} disabled={recording}>
          Start Recording
        </button>
        <button onClick={stopRecording} disabled={!recording} style={{ marginLeft: "10px" }}>
          Stop Recording
        </button>
      </div>
    </div>
  );
}

export default CalendarComp;
