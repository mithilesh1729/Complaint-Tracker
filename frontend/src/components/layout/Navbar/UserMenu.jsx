import { useState, useRef, useEffect } from "react";
import { FiChevronDown, FiUser, FiLogOut } from "react-icons/fi";
import { useNavigate } from "react-router-dom";

import useAuth from "../../../hooks/useAuth";

import "./UserMenu.css";

function UserMenu() {
  const navigate = useNavigate();

  const { user, logout } = useAuth();

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
    navigate("/student/profile");
  }

  function handleLogout() {
    setOpen(false);
    logout();
    navigate("/", {
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
