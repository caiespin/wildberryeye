import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import "./App.css";

const Dashboard = () => {
  const [selectedSection, setSelectedSection] = useState("Get Image");
  return (
    <div className="container">
      <Sidebar onSelect={setSelectedSection} selected={selectedSection} />
      <MainContent section={selectedSection} />
    </div>
  );
};

export default Dashboard;
