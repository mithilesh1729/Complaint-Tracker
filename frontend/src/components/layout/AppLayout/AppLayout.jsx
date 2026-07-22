import { useState } from "react";
import "./AppLayout.css";

import Navbar from "../Navbar";
import Sidebar from "../Sidebar";

function AppLayout({ children }) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <>
      <Navbar toggleCollapse={toggleCollapse} />

      <div className={`layout ${isCollapsed ? 'collapsed' : ''}`}>
        <Sidebar isCollapsed={isCollapsed} />

        <main>{children}</main>
      </div>
    </>
  );
}

export default AppLayout;
