import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

const NavBar = () => {
  return (
    <div className="navbar">
      <p>WildberryEye</p>
      <div className="linkstyle">
        <Link to="/">
          <button className="linktext">Home</button>
        </Link>
        <Link to="/dashboard">
          <button className="linktext">Dashboard</button>
        </Link>
      </div>
    </div>
  );
};

export default NavBar;
