import {
  FaHome,
  FaPlusCircle,
  FaClipboardList,
  FaUser,
  FaTasks,
  FaUsers,
  FaBuilding,
  FaChartBar,
  FaTags,
  FaUserShield,
} from "react-icons/fa";

import { ROUTES } from "../constants/routes";
import { ROLES } from "../constants/roles";

export const NAVIGATION = {
  [ROLES.STUDENT]: [
    {
      label: "Dashboard",
      path: ROUTES.STUDENT_DASHBOARD,
      icon: FaHome,
    },
    {
      label: "Raise Complaint",
      path: ROUTES.CREATE_COMPLAINT,
      icon: FaPlusCircle,
    },
    {
      label: "My Complaints",
      path: ROUTES.MY_COMPLAINTS,
      icon: FaClipboardList,
    },
    {
      label: "Profile",
      path: ROUTES.STUDENT_PROFILE,
      icon: FaUser,
    },
  ],

  [ROLES.HOSTEL_OFFICE]: [
    {
      label: "Dashboard",
      path: ROUTES.OFFICE_DASHBOARD,
      icon: FaHome,
    },
    {
      label: "Incoming Complaints",
      path: ROUTES.OFFICE_QUEUE,
      icon: FaClipboardList,
    },
    {
      label: "My Assigned Work",
      path: ROUTES.OFFICE_ASSIGNED,
      icon: FaTasks,
    },
    {
      label: "Profile",
      path: ROUTES.OFFICE_PROFILE,
      icon: FaUser,
    },
  ],

  [ROLES.WARDEN]: [
    {
      label: "Dashboard",
      path: ROUTES.WARDEN_DASHBOARD,
      icon: FaHome,
    },
    {
      label: "Escalated Queue",
      path: ROUTES.WARDEN_QUEUE,
      icon: FaClipboardList,
    },
    {
      label: "Staff Performance",
      path: ROUTES.WARDEN_PERFORMANCE,
      icon: FaChartBar,
    },
    {
      label: "Profile",
      path: ROUTES.WARDEN_PROFILE,
      icon: FaUser,
    },
  ],

  [ROLES.HMC]: [
    {
      label: "Dashboard",
      path: ROUTES.HMC_DASHBOARD,
      icon: FaHome,
    },
    {
      label: "HMC Queue",
      path: ROUTES.HMC_QUEUE,
      icon: FaClipboardList,
    },
    {
      label: "Hostel Performance",
      path: ROUTES.HMC_PERFORMANCE,
      icon: FaBuilding,
    },
    {
      label: "Profile",
      path: ROUTES.HMC_PROFILE,
      icon: FaUser,
    },
  ],

  [ROLES.ADMIN]: [
    {
      label: "Dashboard",
      path: ROUTES.ADMIN_DASHBOARD,
      icon: FaHome,
    },
    {
      label: "Students",
      path: ROUTES.ADMIN_STUDENTS,
      icon: FaUsers,
    },
    {
      label: "Staff",
      path: ROUTES.ADMIN_STAFF,
      icon: FaUsers,
    },
    {
      label: "Hostels",
      path: ROUTES.ADMIN_HOSTELS,
      icon: FaBuilding,
    },
    {
      label: "Departments",
      path: "/admin/departments",
      icon: FaBuilding,
    },
    {
      label: "Categories",
      path: "/admin/categories",
      icon: FaTags,
    },
    {
      label: "Reports",
      path: ROUTES.ADMIN_ANALYTICS,
      icon: FaChartBar,
    },
    {
      label: "Profile",
      path: ROUTES.ADMIN_PROFILE,
      icon: FaUserShield,
    },
  ],
};
