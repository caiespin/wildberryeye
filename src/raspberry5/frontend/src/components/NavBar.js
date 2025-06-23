import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

const NavBar = () => {
  return (
    <div className="navbar">
      <p>WildberryEye</p>
      <div className="linkstyle">
        <Link to="/" className="linktext">
          Home
        </Link>
        <Link to="/dashboard" className="linktext">
          Dashboard
        </Link>
      </div>
    </div>
  );
};

export default NavBar;
