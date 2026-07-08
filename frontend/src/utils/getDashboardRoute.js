import { ROLES } from "../constants/roles";

export default function getDashboardRoute(role) {
  switch (role) {
    case ROLES.STUDENT:
      return "/student";

    case ROLES.HOSTEL_OFFICE:
      return "/office";

    case ROLES.WARDEN:
      return "/warden";

    case ROLES.HMC:
      return "/hmc";

    case ROLES.ADMIN:
      return "/admin";

    default:
      return "/";
  }
}
