import logo from "../../../assets/logo/nitp_logo.png";

import "./Brand.css";

function Brand() {
  return (
    <div className="navbar-brand">
      <img src={logo} alt="NIT Patna Logo" className="navbar-brand-logo" />

      <div className="navbar-brand-content">
        <h1>Hostel Complaint Tracker</h1>

        <span>National Institute of Technology Patna</span>
      </div>
    </div>
  );
}

export default Brand;
