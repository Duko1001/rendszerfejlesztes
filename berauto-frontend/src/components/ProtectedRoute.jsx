import { Navigate } from 'react-router-dom';
import { getUser, hasRole } from '../utils/auth';

export default function ProtectedRoute({ roles, children }) {
  const user = getUser();
  if (!user?.token) return <Navigate to="/login" replace />;
  if (roles?.length && !hasRole(roles)) return <Navigate to="/" replace />;
  return children;
}
