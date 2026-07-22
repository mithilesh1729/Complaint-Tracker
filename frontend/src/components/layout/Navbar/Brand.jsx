import logo from "../../../assets/logo/nitp_logo.png";

import "./Brand.css";

import { FaBars } from "react-icons/fa";

function Brand({ toggleCollapse }) {
  return (
    <div className="navbar-brand">
      <button 
        className="sidebar-toggle-btn" 
        onClick={toggleCollapse}
        style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', marginRight: '16px', color: 'var(--text-primary)' }}
      >
        <FaBars />
      </button>

      <img src={logo} alt="NIT Patna Logo" className="navbar-brand-logo" />

      <div className="navbar-brand-content">
        <h1>Hostel Complaint Tracker</h1>

        <span>National Institute of Technology Patna</span>
      </div>
    </div>
  );
}

export default Brand;
