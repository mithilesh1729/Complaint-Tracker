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
import OfficeDashboard from "../pages/office/Dashboard/officeDashboard";
import IncomingComplaints from "../pages/office/IncomingComplaints/IncomingComplaints";
import AssignedComplaints from "../pages/office/AssignedComplaints/AssignedComplaints";
import OfficeComplaintDetails from "../pages/office/ComplaintDetails/OfficeComplaintDetails";
import OfficeProfile from "../pages/office/officeProfile/officeProfile";
import AdminDashboard from "../pages/admin/AdminDashboard";
import AdminStudents from "../pages/admin/AdminStudents";
import AdminStaff from "../pages/admin/AdminStaff";
import AdminCategories from "../pages/admin/AdminCategories";
import AdminReports from "../pages/admin/AdminReports";
import AdminProfile from "../pages/admin/AdminProfile";
import AdminHostels from "../pages/admin/AdminHostels";
import AdminDepartments from "../pages/admin/AdminDepartments";

import WardenDashboard from "../pages/warden/WardenDashboard";
import WardenQueue from "../pages/warden/WardenQueue";
import WardenComplaintDetails from "../pages/warden/WardenComplaintDetails";
import StaffPerformance from "../pages/warden/StaffPerformance";
import WardenProfile from "../pages/warden/WardenProfile";

import HMCDashboard from "../pages/hmc/HMCDashboard";
import HMCQueue from "../pages/hmc/HMCQueue";
import HMCComplaintDetails from "../pages/hmc/HMCComplaintDetails";
import HostelPerformance from "../pages/hmc/HostelPerformance";
import HMCProfile from "../pages/hmc/HMCProfile";


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
            <Route path="/office" element={<OfficeDashboard />} />

            <Route path="/office/queue" element={<IncomingComplaints />} />

            <Route path="/office/assigned" element={<AssignedComplaints />} />

            <Route path="/office/profile" element={<OfficeProfile />} />

            <Route
              path="/office/complaints/:complaintId"
              element={<OfficeComplaintDetails />}
            />
          </Route>
        </Route>

        {/* Warden */}
        <Route element={<RoleBasedRoute roles={[ROLES.WARDEN]} />}>
          <Route element={<WardenLayout />}>
            <Route path="/warden" element={<WardenDashboard />} />
            <Route path="/warden/queue" element={<WardenQueue />} />
            <Route path="/warden/complaints/:complaintId" element={<WardenComplaintDetails />} />
            <Route path="/warden/performance" element={<StaffPerformance />} />
            <Route path="/warden/profile" element={<WardenProfile />} />
          </Route>
        </Route>

        {/* HMC */}
        <Route element={<RoleBasedRoute roles={[ROLES.HMC]} />}>
          <Route element={<HMCLayout />}>
            <Route path="/hmc" element={<HMCDashboard />} />
            <Route path="/hmc/queue" element={<HMCQueue />} />
            <Route path="/hmc/complaints/:complaintId" element={<HMCComplaintDetails />} />
            <Route path="/hmc/performance" element={<HostelPerformance />} />
            <Route path="/hmc/profile" element={<HMCProfile />} />
          </Route>
        </Route>

        {/* Admin */}
        <Route element={<RoleBasedRoute roles={[ROLES.ADMIN]} />}>
          <Route element={<AdminLayout />}>
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/students" element={<AdminStudents />} />
            <Route path="/admin/staff" element={<AdminStaff />} />
            <Route path="/admin/hostels" element={<AdminHostels />} />
            <Route path="/admin/departments" element={<AdminDepartments />} />
            <Route path="/admin/categories" element={<AdminCategories />} />
            <Route path="/admin/reports" element={<AdminReports />} />
            <Route path="/admin/profile" element={<AdminProfile />} />
            <Route path="/admin/emails" element={<AdminEmails />} />
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}

export default AppRoutes;
