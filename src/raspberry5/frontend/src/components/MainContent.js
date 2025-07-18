import CalendarComp from "./Calendar";
import CameraCapture from "./CameraCapture";

function MainContent({ section }) {
  return (
    <div className="main-content">
      {section === "Get Image" && (
        <div>
          <CameraCapture />
        </div>
      )}
      {section === "Get Video" && (
        <div>
          <CalendarComp />
        </div>
      )}
      {section === "Get Video by on selected time" && (
        <div>
          <CalendarComp />
        </div>
      )}
    </div>
  );
}

export default MainContent;
