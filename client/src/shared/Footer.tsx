import React from "react";
import "./footer.css";

const Footer = () => {
  return (
    <footer className="footer bg-dark">
      <div className="container-xl container-xxl bg-dark pl-md-0">
        <span className="text-white">
          © {new Date().getFullYear()} Adam Feinstein {"&"} Ian Kenley. All
          Rights Reserved
        </span>
      </div>
    </footer>
  );
};

export default Footer;
