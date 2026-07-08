import {
  FaHome,
  FaPlusCircle,
  FaClipboardList,
  FaUser,
  FaTasks,
  FaUsers,
  FaBuilding,
  FaChartBar,
} from "react-icons/fa";

import { ROUTES } from "../constants/routes";
import { ROLES } from "../constants/roles";

export const NAVIGATION = {
  [ROLES.STUDENT]: [
    {
      title: "Dashboard",
      icon: FaHome,
      path: ROUTES.STUDENT_DASHBOARD,
    },

    {
      title: "Raise Complaint",
      icon: FaPlusCircle,
      path: ROUTES.CREATE_COMPLAINT,
    },

    {
      title: "My Complaints",
      icon: FaClipboardList,
      path: ROUTES.MY_COMPLAINTS,
    },

    {
      title: "Profile",
      icon: FaUser,
      path: ROUTES.STUDENT_PROFILE,
    },
  ],

  [ROLES.HOSTEL_OFFICE]: [
    {
      title: "Queue",
      icon: FaTasks,
      path: ROUTES.OFFICE_QUEUE,
    },

    {
      title: "Assigned",
      icon: FaClipboardList,
      path: ROUTES.OFFICE_ASSIGNED,
    },

    {
      title: "Profile",
      icon: FaUser,
      path: ROUTES.OFFICE_PROFILE,
    },
  ],

  [ROLES.ADMIN]: [
    {
      title: "Students",
      icon: FaUsers,
      path: ROUTES.ADMIN_STUDENTS,
    },

    {
      title: "Staff",
      icon: FaUsers,
      path: ROUTES.ADMIN_STAFF,
    },

    {
      title: "Hostels",
      icon: FaBuilding,
      path: ROUTES.ADMIN_HOSTELS,
    },

    {
      title: "Analytics",
      icon: FaChartBar,
      path: ROUTES.ADMIN_ANALYTICS,
    },
  ],
};
