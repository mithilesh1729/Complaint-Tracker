import { Outlet } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";

function HMCLayout() {
  return (
    <AppLayout>
      <Outlet />
    </AppLayout>
  );
}

export default HMCLayout;
