import CalendarComp from "./Calendar";

function MainContent({ section }) {
  return (
    <div className="main-content">
      {section === "Bee's Video" && (
        <div>
          <CalendarComp />
        </div>
      )}
      {section === "Bird's Video" && <h2>Show Video</h2>}
      {section === "Data Analytics" && <h2>Data Analytics</h2>}
    </div>
  );
}

export default MainContent;
