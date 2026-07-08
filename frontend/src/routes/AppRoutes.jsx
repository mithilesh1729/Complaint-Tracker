import { Routes, Route } from "react-router-dom";

import Login from "../pages/auth/Login";

import Dashboard from "../pages/student/Dashboard";

import ProtectedRoute from "./ProtectedRoute";
import RoleBasedRoute from "./RoleBasedRoute";

import StudentLayout from "../layouts/StudentLayout";
import OfficeLayout from "../layouts/OfficeLayout";
import AdminLayout from "../layouts/AdminLayout";
import WardenLayout from "../layouts/WardenLayout";
import HMCLayout from "../layouts/HMCLayout";

import { ROLES } from "../constants/roles";

import MyComplaints from "../pages/student/MyComplaints";

import ComplaintDetails from "../pages/student/ComplaintDetails/ComplaintDetails";
import RaiseComplaint from "../pages/student/RaiseComplaint";

import MyProfile from "../pages/student/Profile/MyProfile";

function Dummy({ title }) {
  return <h2 style={{ padding: 30 }}>{title}</h2>;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Login */}
      <Route path="/" element={<Login />} />

      {/* Protected */}
      <Route element={<ProtectedRoute />}>
        {/* Student */}
        <Route element={<RoleBasedRoute roles={[ROLES.STUDENT]} />}>
          <Route element={<StudentLayout />}>
            <Route path="/student" element={<Dashboard />} />

            <Route path="/student/complaints" element={<MyComplaints />} />

            <Route
              path="/student/complaints/new"
              element={<RaiseComplaint />}
            />

            <Route
              path="/student/complaints/:complaintId"
              element={<ComplaintDetails />}
            />

            <Route path="/student/profile" element={<MyProfile />} />
          </Route>
        </Route>

        {/* Hostel Office */}
        <Route element={<RoleBasedRoute roles={[ROLES.HOSTEL_OFFICE]} />}>
          <Route element={<OfficeLayout />}>
            <Route
              path="/office"
              element={<Dummy title="Office Dashboard" />}
            />

            <Route path="/office/queue" element={<Dummy title="Queue" />} />

            <Route
              path="/office/assigned"
              element={<Dummy title="Assigned Complaints" />}
            />
          </Route>
        </Route>

        {/* Warden */}
        <Route element={<RoleBasedRoute roles={[ROLES.WARDEN]} />}>
          <Route element={<WardenLayout />}>
            <Route
              path="/warden"
              element={<Dummy title="Warden Dashboard" />}
            />
          </Route>
        </Route>

        {/* HMC */}
        <Route element={<RoleBasedRoute roles={[ROLES.HMC]} />}>
          <Route element={<HMCLayout />}>
            <Route path="/hmc" element={<Dummy title="HMC Dashboard" />} />
          </Route>
        </Route>

        {/* Admin */}
        <Route element={<RoleBasedRoute roles={[ROLES.ADMIN]} />}>
          <Route element={<AdminLayout />}>
            <Route path="/admin" element={<Dummy title="Admin Dashboard" />} />
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}

export default AppRoutes;
