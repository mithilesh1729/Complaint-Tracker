import { Outlet } from "react-router-dom";

import AppLayout from "../components/layout/AppLayout";

function StudentLayout() {
  return (
    <AppLayout>
      <Outlet />
    </AppLayout>
  );
}

export default StudentLayout;
