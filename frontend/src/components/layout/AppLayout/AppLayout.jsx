import "./AppLayout.css";

import Navbar from "../Navbar";
import Sidebar from "../Sidebar";

function AppLayout({ children }) {
  return (
    <>
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main>{children}</main>
      </div>
    </>
  );
}

export default AppLayout;
