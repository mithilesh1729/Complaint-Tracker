import { Navigate, Outlet } from "react-router-dom";

import useAuth from "../hooks/useAuth";

function RoleBasedRoute({ roles }) {
  const { user } = useAuth();

  if (!roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}

export default RoleBasedRoute;
