import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import LoginModal from './components/LoginModal';
import ChatbotWidget from './components/ChatbotWidget';
import ErrorBoundary from './components/ErrorBoundary';

import Dashboard from './pages/Dashboard';
import PatientList from './pages/PatientList';
// …other pages…
import NotFound from './pages/NotFound';

const App: React.FC = () => {
  const [showLogin, setShowLogin] = useState(!localStorage.getItem('token'));

  if (showLogin) {
    return <LoginModal onSuccess={() => setShowLogin(false)} />;
  }

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<ErrorBoundary><Dashboard/></ErrorBoundary>} />
          <Route path="patients" element={<ErrorBoundary><PatientList/></ErrorBoundary>} />
          {/* …other routes… */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
      <ChatbotWidget />
    </BrowserRouter>
  );
};

export default App;
