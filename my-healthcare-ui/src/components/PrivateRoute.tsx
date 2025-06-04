import React from "react";
import { Navigate } from "react-router-dom";

/**
 * Checks for “token” in localStorage.
 * If missing, redirect to /login.
 * Otherwise, render children (the Layout + nested routes).
 */
const PrivateRoute: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const token = localStorage.getItem("token");
  if (!token) {
    return <Navigate to="/login" />;
  }
  return <>{children}</>;
};

export default PrivateRoute;
