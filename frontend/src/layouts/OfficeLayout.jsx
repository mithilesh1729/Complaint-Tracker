import { Outlet } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";

function OfficeLayout() {
  return (
    <AppLayout>
      <Outlet />
    </AppLayout>
  );
}

export default OfficeLayout;
