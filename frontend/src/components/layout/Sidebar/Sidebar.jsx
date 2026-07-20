import "./Sidebar.css";

import { NavLink } from "react-router-dom";

import { useContext } from "react";
import { AuthContext } from "../../../contexts/AuthContext";

import { NAVIGATION } from "../../../config/navigation";
import { PORTAL_TITLES } from "../../../config/portalTitles";

import student_logo from "../../../assets/logo/student_logo.png";
import nitp_logo from "../../../assets/logo/nitp_logo.png";

function Sidebar() {
  const { user } = useContext(AuthContext);
  
  const menu = NAVIGATION[user.role] || [];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <img src={student_logo} alt="Logo" className="sidebar-logo" />

        <div>
          <h3>{PORTAL_TITLES[user.role]}</h3>
        </div>
      </div>

      <nav className="sidebar-menu">
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "sidebar-link active" : "sidebar-link"
              }
            >
              <Icon className="sidebar-icon" />

              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
