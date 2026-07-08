import { Navigate, Outlet } from "react-router-dom";

import useAuth from "../hooks/useAuth";

function ProtectedRoute() {
  const { loading, isAuthenticated } = useAuth();

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
