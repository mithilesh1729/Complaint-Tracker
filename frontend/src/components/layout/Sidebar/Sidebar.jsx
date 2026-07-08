import "./Sidebar.css";

import { NavLink } from "react-router-dom";

import { NAVIGATION } from "../../../config/navigation";

import logo from "../../../assets/logo/nitp_logo.png";
import student_logo from "../../../assets/logo/student_logo.png";

function Sidebar() {
  const menu = NAVIGATION.student;

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <img src={student_logo} alt="NIT Patna" className="sidebar-logo" />

        <div>
          <h3>Student Portal</h3>
        </div>
      </div>

      <nav className="sidebar-menu">
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/student/complaints"}
              className={({ isActive }) =>
                isActive ? "sidebar-link active" : "sidebar-link"
              }
            >
              <Icon className="sidebar-icon" />
              <span>{item.title}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
