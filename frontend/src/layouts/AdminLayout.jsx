import { Outlet } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";

function AdminLayout() {
  return (
    <AppLayout>
      <Outlet />
    </AppLayout>
  );
}

export default AdminLayout;
