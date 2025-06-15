import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <nav
      style={{
        background: "#F4F0F0",
        padding: "1rem",
        color: "black",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <h2 style={{ margin: 0 }}>WildberryEye</h2>
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
  color: "black",
  textDecoration: "none",
  fontSize: "1.1rem",
};

export default NavBar;
