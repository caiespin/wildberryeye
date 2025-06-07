import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <nav
      style={{
        background: "#282c34",
        padding: "1rem",
        color: "white",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <h2 style={{ margin: 0 }}>My Website</h2>
      <div>
        <Link to="/" style={linkStyle}>
          Home
        </Link>
        <Link to="/dashboard" style={linkStyle}>
          Dashboard
        </Link>
      </div>
    </nav>
  );
};

const linkStyle = {
  marginLeft: "1rem",
  color: "white",
  textDecoration: "none",
  fontSize: "1.1rem",
};

export default NavBar;
