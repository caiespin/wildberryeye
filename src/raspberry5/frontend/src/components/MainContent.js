import CalendarComp from "./Calendar";
import CameraCapture from "./CameraCapture";

function MainContent({ section }) {
  return (
    <div className="main-content">
      {section === "Bee's Video" && (
        <div>
          <CalendarComp />
        </div>
      )}
      {section === "Bird's Video" && <h2>Show Video</h2>}
      {section === "Data Analytics" && (
        <div>
          <CameraCapture />
        </div>
      )}
    </div>
  );
}

export default MainContent;
