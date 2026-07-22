import "./Navbar.css";

import Brand from "./Brand";
import UserMenu from "./UserMenu";

function Navbar({ toggleCollapse }) {
  return (
    <header className="navbar">
      <Brand toggleCollapse={toggleCollapse} />

      <UserMenu />
    </header>
  );
}

export default Navbar;
