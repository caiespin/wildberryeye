function MainContent({ section }) {
  return (
    <div className="main-content">
      {section === "Home" && <h2>Welcome to the Home page</h2>}
      {section === "About" && <h2>About us content</h2>}
      {section === "Contact" && <h2>Contact information</h2>}
    </div>
  );
}

export default MainContent;
