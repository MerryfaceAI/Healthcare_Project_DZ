// src/pages/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { getPatients } from '../api/patients';
import { getProviders } from '../api/providers';
import { getAppointments } from '../api/appointments';
import { getNotifications } from '../api/notifications';
import UserProfileCard from '../components/UserProfileCard';
import { format, parseISO } from 'date-fns';

// Placeholder chart components
const LineChartPlaceholder = () => (
  <div className="w-full h-40 flex items-center justify-center text-muted">
    [Line Chart]
  </div>
);
const DonutChartPlaceholder = () => (
  <div className="w-full h-40 flex items-center justify-center text-muted">
    [Donut Chart]
  </div>
);

interface PatientMetric {
  totalToday: number;
  pendingDischarge: number;
}
interface Appointment {
  id: number;
  appointment_date: string;
  patient: { first_name: string; last_name: string };
  provider: { name: string };
  status: string;
}
interface Notification {
  id: number;
  message: string;
  appointment?: { id: number; appointment_date: string };
  is_read: boolean;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<PatientMetric>({ totalToday: 0, pendingDischarge: 0 });
  const [providersCount, setProvidersCount] = useState<number>(0);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  const today = new Date().toISOString().split('T')[0];

  useEffect(() => {
    async function fetchAll() {
      try {
        // 1) Patients admitted today
        const patientsData = await getPatients();
        const patientsArray = Array.isArray(patientsData)
          ? patientsData
          : (patientsData as any).results ?? [];
        const totalToday = patientsArray.length;
        const pendingDischarge = patientsArray.filter((p: any) => p.pending_discharge).length;
        setMetrics({ totalToday, pendingDischarge });

        // 2) Total providers
        const providersData = await getProviders();
        const providersArray = Array.isArray(providersData)
          ? providersData
          : (providersData as any).results ?? [];
        setProvidersCount(providersArray.length);

        // 3) Today’s appointments (limit 3)
        const apptsRaw = await getAppointments();
        const apptsArray = Array.isArray(apptsRaw)
          ? apptsRaw
          : (apptsRaw as any).results ?? [];
        setAppointments(apptsArray.slice(0, 3));

        // 4) Unread notifications (limit 3)
        const notifsRaw = await getNotifications(true);
        const notifsArray = Array.isArray(notifsRaw)
          ? notifsRaw
          : (notifsRaw as any).results ?? [];
        setNotifications(
          notifsArray
            .map((n: any) => ({
              id: n.id,
              message: n.message,
              appointment:
                typeof n.appointment === 'object'
                  ? n.appointment
                  : n.appointment
                  ? { id: n.appointment, appointment_date: '' }
                  : undefined,
              is_read: n.is_read,
              created_at: n.created_at,
            }))
            .slice(0, 3)
        );
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchAll();
  }, [today]);

  if (loading) {
    return (
      <div className="dashboard-grid">
        {/* each .dashboard-card as shown earlier */}
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col overflow-auto bg-app-bg">
      {/* ─── Top Header ─── */}
      <header className="flex items-center justify-between h-16 px-6 bg-card-bg shadow">
        <h1 className="text-2xl font-semibold text-card-fg">Dashboard</h1>
        <UserProfileCard inTopBar />
      </header>

      {/* ─── Metrics Row ─── */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 p-6">
        {/* Total Patients */}
        <div className="dashboard-card flex items-center space-x-3">
          <div className="p-3 bg-card-bg rounded-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-btn-primary"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                d="M3 4a4 4 0 014-4h10a4 4 0 014 4v16l-7-3-7 3V4z"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
              />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-muted">Total Patients</p>
            <p className="mt-1 text-2xl font-bold text-card-fg">{metrics.totalToday}</p>
          </div>
        </div>

        {/* Total Staff */}
        <div className="dashboard-card flex items-center space-x-3">
          <div className="p-3 bg-card-bg rounded-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-green-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                d="M17 20h5v-2a2 2 0 00-2-2H4a2 2 0 00-2 2v2h5m5-10a4 4 0 100-8 4 4 0 000 8z"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
              />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-muted">Total Staff</p>
            <p className="mt-1 text-2xl font-bold text-card-fg">{providersCount}</p>
          </div>
        </div>

        {/* Pending Discharge */}
        <div className="dashboard-card flex items-center space-x-3">
          <div className="p-3 bg-card-bg rounded-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-yellow-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                d="M3 7h18M3 7l3 13h12l3-13m-3 0a9 9 0 11-18 0 9 9 0 0118 0z"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
              />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-muted">Pending Discharge</p>
            <p className="mt-1 text-2xl font-bold text-card-fg">{metrics.pendingDischarge}</p>
          </div>
        </div>

        {/* Total Doctors (Placeholder) */}
        <div className="dashboard-card flex items-center space-x-3">
          <div className="p-3 bg-card-bg rounded-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-red-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                d="M12 7v6m0 4h.01M20.49 20.49l-6.07-6.07M3.51 3.51l6.07 6.07M12 3a9 9 0 019 9h-2a7 7 0 00-7-7V3z"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
              />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-muted">Total Doctors</p>
            <p className="mt-1 text-2xl font-bold text-card-fg">{/* fill as needed */}</p>
          </div>
        </div>
      </section>

      {/* ─── Profile & Calendar ─── */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4 px-6 mb-6">
        <UserProfileCard />

        <div className="dashboard-card p-4">
          <h2 className="text-lg font-semibold text-card-fg mb-2">May 2025</h2>
          <div className="grid grid-cols-7 gap-1 text-center text-muted text-sm">
            {['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'].map(day => (
              <div key={day} className="font-medium">{day}</div>
            ))}
            {/* blank slots until the 1st… */}
            <div /><div /><div />
            {Array.from({ length: 31 }, (_, i) => (
              <div
                key={i + 1}
                className={`p-1 rounded-full cursor-pointer ${
                  i + 1 === new Date().getDate()
                    ? 'bg-btn-primary text-btn-primary-fg font-semibold'
                    : 'bg-card-bg'
                }`}
              >
                {i + 1}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Analytics Row ─── */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4 px-6 mb-6">
        <div className="dashboard-card p-4">
          <h2 className="text-lg font-semibold text-card-fg mb-2">Total Admitted (7 Days)</h2>
          <LineChartPlaceholder />
        </div>

        <div className="dashboard-card p-4">
          <h2 className="text-lg font-semibold text-card-fg mb-2">Patients by Gender</h2>
          <DonutChartPlaceholder />
          <div className="flex justify-center space-x-4 mt-2 text-muted">
            <div className="flex items-center space-x-1 text-sm">
              <span className="w-2 h-2 bg-btn-primary rounded-full" />
              <span>Male</span>
            </div>
            <div className="flex items-center space-x-1 text-sm">
              <span className="w-2 h-2 bg-pink-600 rounded-full" />
              <span>Female</span>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Upcoming Appointments ─── */}
      <section className="px-6 mb-6">
        <div className="dashboard-card p-4">
          <h2 className="text-lg font-semibold text-card-fg mb-2">Upcoming Appointments</h2>
          <ul className="divide-y divide-gray-200">
            {appointments.length > 0 ? (
              appointments.map(appt => (
                <li key={appt.id} className="py-2 flex justify-between items-center">
                  <div>
                    <p className="text-card-fg">
                      {format(parseISO(appt.appointment_date), 'HH:mm')}
                      {' – '}{appt.patient.first_name} {appt.patient.last_name}
                    </p>
                    <p className="text-sm text-muted">Dr. {appt.provider.name}</p>
                  </div>
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs ${
                      appt.status === 'cancelled'
                        ? 'bg-red-100 text-red-600'
                        : 'bg-green-100 text-green-600'
                    }`}
                  >
                    {appt.status.charAt(0).toUpperCase() + appt.status.slice(1)}
                  </span>
                </li>
              ))
            ) : (
              <li className="py-2 text-muted">No upcoming appointments.</li>
            )}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
