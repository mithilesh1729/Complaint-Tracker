import { Outlet } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";

function WardenLayout() {
  return (
    <AppLayout>
      <Outlet />
    </AppLayout>
  );
}

export default WardenLayout;
