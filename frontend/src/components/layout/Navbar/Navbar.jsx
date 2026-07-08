import "./Navbar.css";

import Brand from "./Brand";
import UserMenu from "./UserMenu";

function Navbar() {
  return (
    <header className="navbar">
      <Brand />

      <UserMenu />
    </header>
  );
}

export default Navbar;
