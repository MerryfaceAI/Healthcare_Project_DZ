// frontend/my-healthcare-ui/src/components/PrivateRoute.tsx

import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { isAuthenticated } from '@/api/auth';

/**
 * Wrap protected routes in <Route element={<PrivateRoute />}>.
 * If no token is present, redirect to /login.
 */
const PrivateRoute: React.FC = () => {
  return isAuthenticated() ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
