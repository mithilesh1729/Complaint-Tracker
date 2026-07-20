import { useState, useRef, useEffect } from "react";
import { FiChevronDown, FiUser, FiLogOut } from "react-icons/fi";
import { useNavigate } from "react-router-dom";

import useAuth from "../../../hooks/useAuth";

import { ROLES } from "../../../constants/roles";
import { ROUTES } from "../../../constants/routes";

import "./Usermenu.css";

function UserMenu() {
  const navigate = useNavigate();

  const { user, logout } = useAuth();

  const PROFILE_ROUTES = {
    [ROLES.STUDENT]: ROUTES.STUDENT_PROFILE,

    [ROLES.HOSTEL_OFFICE]: ROUTES.OFFICE_PROFILE,

    [ROLES.WARDEN]: ROUTES.WARDEN_PROFILE,

    [ROLES.HMC]: ROUTES.HMC_PROFILE,

    [ROLES.ADMIN]: ROUTES.ADMIN_PROFILE,
  };

  const [open, setOpen] = useState(false);

  const menuRef = useRef(null);

  const initials =
    user?.name
      ?.split(" ")
      .map((word) => word[0])
      .join("")
      .substring(0, 2)
      .toUpperCase() || "U";

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);

    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  function handleProfile() {
    setOpen(false);

    navigate(PROFILE_ROUTES[user.role] || ROUTES.LOGIN);
  }

  function handleLogout() {
    setOpen(false);

    logout();

    navigate(ROUTES.LOGIN, {
      replace: true,
    });
  }

  return (
    <div className="user-menu" ref={menuRef}>
      <button
        type="button"
        className="user-menu-trigger"
        onClick={() => setOpen((prev) => !prev)}
      >
        <div className="user-avatar">{initials}</div>

        <div className="user-info">
          <h4>{user?.name}</h4>

          <span>{user?.roll_no}</span>
        </div>

        <FiChevronDown className={`chevron ${open ? "rotate" : ""}`} />
      </button>

      {open && (
        <div className="user-dropdown">
          <button type="button" onClick={handleProfile}>
            <FiUser />
            <span>My Profile</span>
          </button>

          <hr />

          <button type="button" className="logout-item" onClick={handleLogout}>
            <FiLogOut />
            <span>Logout</span>
          </button>
        </div>
      )}
    </div>
  );
}

export default UserMenu;
