import { Navigate, useLocation } from "react-router-dom";
import { getStoredUser } from "../services/fitnovaService";

function ProtectedRoute({ children, roles }) {
  const location = useLocation();
  const user = getStoredUser();
  if (!user) return <Navigate to="/" replace state={{ from: location }} />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/calls" replace />;
  return children;
}

export default ProtectedRoute;
