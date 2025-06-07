// src/components/PrivateRoute.tsx
import React, { useState } from 'react';
import Login from '../pages/Login';
import LoginModal from './LoginModal';

const PrivateRoute: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const token = localStorage.getItem('token');
  const [ok, setOk] = useState(!!token);
  if (!ok) {
    return <LoginModal onSuccess={() => setOk(true)} />;
  }
  return <>{children}</>;
};

export default PrivateRoute;
