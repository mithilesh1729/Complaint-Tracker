import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";


const ProtectedRoute = ({ children, adminOnly = false }) => {
  const token = localStorage.getItem("access");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  try {
    const decoded = jwtDecode(token);
    // adminOnly route protection
    if (adminOnly && !decoded.is_admin) {
      return <Navigate to="/dashboard" replace />;
    }

    return children;
  } catch {
    return <Navigate to="/" replace />;
  }
};

export default ProtectedRoute;
