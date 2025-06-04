import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAppointments } from "@/api/appointments";
import { getPatients } from "@/api/patients";
import { getProviders } from "@/api/providers";
import { getNotifications } from "@/api/notifications";

interface SummaryCounts {
  patientCount: number;
  appointmentCount: number;
  providerCount: number;
  unreadNotificationCount: number;
}

const Dashboard: React.FC = () => {
  const [counts, setCounts] = useState<SummaryCounts | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [patients, appointments, providers, notifications] = await Promise.all([
          getPatients(),
          getAppointments(),
          getProviders(),
          getNotifications(true),
        ]);

        setCounts({
          patientCount: patients.length,
          appointmentCount: appointments.length,
          providerCount: providers.length,
          unreadNotificationCount: notifications.length,
        });
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading || !counts) {
    return (
      <div className="flex justify-center items-center h-full text-gray-500">
        Loading dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <p className="text-gray-600">Welcome! Your summary:</p>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Patients</h2>
          <p className="text-3xl mt-2">{counts.patientCount}</p>
          <Link
            to="/patients"
            className="text-blue-600 hover:underline text-sm mt-1 block"
          >
            View All Patients
          </Link>
        </div>

        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Appointments</h2>
          <p className="text-3xl mt-2">{counts.appointmentCount}</p>
          <Link
            to="/appointments"
            className="text-blue-600 hover:underline text-sm mt-1 block"
          >
            View All Appointments
          </Link>
        </div>

        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Providers</h2>
          <p className="text-3xl mt-2">{counts.providerCount}</p>
          <Link
            to="/providers"
            className="text-blue-600 hover:underline text-sm mt-1 block"
          >
            View All Providers
          </Link>
        </div>

        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Unread Notifications</h2>
          <p className="text-3xl mt-2">{counts.unreadNotificationCount}</p>
          <Link
            to="/notifications"
            className="text-blue-600 hover:underline text-sm mt-1 block"
          >
            View Notifications
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
