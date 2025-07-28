import CalendarComp from "./Calendar";
import ImageCapture from "./ImageCapture";
import VideoCapture from "./VideoCapture";

function MainContent({ section }) {
  return (
    <div className="main-content">
      {section === "Get Image" && (
        <div>
          <ImageCapture />
        </div>
      )}
      {section === "Get Video" && (
        <div>
          <VideoCapture />
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
