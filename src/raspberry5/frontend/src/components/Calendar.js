import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../";

function CalendarComp() {
  const [date, setDate] = useState(new Date());

  return (
    <div className="calendar">
      <h2 className="text-xl font-bold mb-4">Pick a Date</h2>
      <Calendar onChange={setDate} value={date} />
      <p className="mt-4">Selected Date: {date.toDateString()}</p>
      <button className="download-button">Submit</button>
    </div>
  );
}

export default CalendarComp;
