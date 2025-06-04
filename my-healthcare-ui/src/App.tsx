import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "@/pages/Login";
import Dashboard from "@/pages/Dashboard";
import PatientList from "@/pages/PatientList";
import PatientForm from "@/pages/PatientForm";
import AppointmentList from "@/pages/AppointmentList";
import AppointmentForm from "@/pages/AppointmentForm";
import NotFound from "@/pages/NotFound";
import Layout from "@/components/Layout";
import PrivateRoute from "@/components/PrivateRoute";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public route: Login */}
        <Route path="/login" element={<Login />} />

        {/*
          All authenticated routes sit under Layout. We wrap Layout in PrivateRoute,
          which checks for a valid token in localStorage. If no token, redirect → /login.
        */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          {/* When user goes to "/" → redirect to "/dashboard" */}
          <Route index element={<Navigate to="dashboard" replace />} />

          {/* Dashboard */}
          <Route path="dashboard" element={<Dashboard />} />

          {/* Patients: Listing and Create/Edit */}
          <Route path="patients">
            <Route index element={<PatientList />} />
            <Route path="new" element={<PatientForm />} />
            <Route
              path=":id/edit"
              element={<PatientForm editMode={true} />}
            />
          </Route>

          {/* Appointments: Listing and Create/Edit */}
          <Route path="appointments">
            <Route index element={<AppointmentList />} />
            <Route path="new" element={<AppointmentForm />} />
            <Route
              path=":id/edit"
              element={<AppointmentForm editMode={true} />}
            />
          </Route>

          {/* Providers (you can create a page if you like) */}
          <Route
            path="providers"
            element={
              <div className="text-center text-gray-600">
                {/* Eventually replace this with a ProviderList page */}
                <h2 className="text-xl font-semibold">Providers</h2>
                <p className="mt-2">Coming soon: provider management</p>
              </div>
            }
          />

          {/* Notifications (you can create a page if you like) */}
          <Route
            path="notifications"
            element={
              <div className="text-center text-gray-600">
                <h2 className="text-xl font-semibold">Notifications</h2>
                <p className="mt-2">Coming soon: your notifications</p>
              </div>
            }
          />

          {/* Catch-all → 404 */}
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
