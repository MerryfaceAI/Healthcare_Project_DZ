import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import LoginModal    from './components/LoginModal';
import ChatbotWidget from './components/ChatbotWidget';
import ErrorBoundary from './components/ErrorBoundary';
import Layout        from './components/Layout';

import Dashboard        from './pages/Dashboard';
import PatientList      from './pages/PatientList';
import PatientForm      from './pages/PatientForm';
import AppointmentList  from './pages/AppointmentList';
import AppointmentForm  from './pages/AppointmentForm';
import ProviderList     from './pages/ProviderList';
import NotificationList from './pages/NotificationList';
import Settings         from './pages/Settings';
import NotFound         from './pages/NotFound';

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'));

  if (!loggedIn) {
    return <LoginModal onSuccess={() => setLoggedIn(true)} />;
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* wrap all protected paths under Layout */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="dashboard" replace />} />

          <Route
            path="dashboard"
            element={
              <ErrorBoundary>
                <Dashboard />
              </ErrorBoundary>
            }
          />

          <Route
            path="patients"
            element={
              <ErrorBoundary>
                <PatientList />
              </ErrorBoundary>
            }
          />
          <Route
            path="patients/new"
            element={
              <ErrorBoundary>
                <PatientForm />
              </ErrorBoundary>
            }
          />

          <Route
            path="appointments"
            element={
              <ErrorBoundary>
                <AppointmentList />
              </ErrorBoundary>
            }
          />
          <Route
            path="appointments/new"
            element={
              <ErrorBoundary>
                <AppointmentForm />
              </ErrorBoundary>
            }
          />

          <Route
            path="providers"
            element={
              <ErrorBoundary>
                <ProviderList />
              </ErrorBoundary>
            }
          />

          <Route
            path="notifications"
            element={
              <ErrorBoundary>
                <NotificationList />
              </ErrorBoundary>
            }
          />

          <Route
            path="settings"
            element={
              <ErrorBoundary>
                <Settings />
              </ErrorBoundary>
            }
          />

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>

      <ChatbotWidget />
    </BrowserRouter>
  );
}
