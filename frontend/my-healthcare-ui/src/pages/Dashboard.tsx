// src/pages/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import { format, parseISO } from 'date-fns';

import { getPatients, Patient } from '../api/patients';
import { getProviders, Provider } from '../api/providers';
import { getAppointments, Appointment } from '../api/appointments';
import { getNotifications, Notification } from '../api/notifications';
import UserProfileCard from '../components/UserProfileCard';
import { CurrentUser } from '../api/users';
import './Dashboard.css';

type ApiResponse<T> = T[] | { results: T[] };

export default function Dashboard() {
  // pull user passed down from Layout
  const user = useOutletContext<CurrentUser>();

  const [totalToday, setTotalToday]             = useState(0);
  const [pendingDischarge, setPendingDischarge] = useState(0);
  const [providersCount, setProvidersCount]     = useState(0);
  const [appointments, setAppointments]         = useState<Appointment[]>([]);
  const [notifications, setNotifications]       = useState<Notification[]>([]);
  const [loading, setLoading]                   = useState(true);

  // simple chart placeholders
  const ChartBox: React.FC<{ label: string }> = ({ label }) => (
    <div className="dashboard-card">
      <p className="text-center text-gray-500">{label} Chart</p>
    </div>
  );

  useEffect(() => {
    async function loadAll() {
      try {
        // Patients
        const patRes = (await getPatients()) as ApiResponse<Patient>;
        const patArr = Array.isArray(patRes) ? patRes : patRes.results;
        setTotalToday(patArr.length);
        setPendingDischarge(patArr.filter(p => p.pending_discharge).length);

        // Providers
        const provRes = (await getProviders()) as ApiResponse<Provider>;
        const provArr = Array.isArray(provRes) ? provRes : provRes.results;
        setProvidersCount(provArr.length);

        // Appointments
        const apptRes = (await getAppointments()) as ApiResponse<Appointment>;
        const apptArr = Array.isArray(apptRes) ? apptRes : apptRes.results;
        setAppointments(apptArr.slice(0, 3));

        // Notifications
        const notRes = (await getNotifications(true)) as ApiResponse<Notification>;
        const notArr = Array.isArray(notRes) ? notRes : notRes.results;
        setNotifications(notArr.slice(0, 3));
      } catch (err) {
        console.error('Dashboard load error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAll();
  }, []);

  if (loading) {
    return (
      <div className="content">
        <p className="text-gray-500">Loading dashboard…</p>
      </div>
    );
  }

  return (
    <div className="content space-y-6">
      {/* Metrics Row */}
      <div className="dashboard-grid">
        {[
          ['Total Patients', totalToday],
          ['Pending Discharge', pendingDischarge],
          ['Total Staff', providersCount],
          ['Unread Notifications', notifications.length],
        ].map(([label, value], i) => (
          <div key={i} className="dashboard-card">
            <p className="text-gray-600">{label}</p>
            <p className="text-2xl font-bold">{value}</p>
          </div>
        ))}
      </div>

      {/* Profile & Calendar */}
      <div className="dashboard-grid">
        <div className="dashboard-card">
          {/* full card shows avatar + name + role */}
          {user && (
            <UserProfileCard
              mode="full"
              user={user}
            />
          )}
        </div>
        <div className="dashboard-card">
          <h2 className="text-lg font-semibold mb-2">May 2025</h2>
          <div className="grid grid-cols-7 gap-1 text-center text-gray-500 text-sm">
            {['Mo','Tu','We','Th','Fr','Sa','Su'].map(d => (
              <div key={d} className="font-medium">{d}</div>
            ))}
            {Array.from({ length: 34 }).map((_, i) => (
              <div key={i} className="p-1 rounded-full hover:bg-blue-100">
                {i >= 3 && i < 34 ? i - 2 : ''}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="dashboard-grid">
        <ChartBox label="Line" />
        <ChartBox label="Donut" />
      </div>

      {/* Upcoming Appointments */}
      <div className="dashboard-card">
        <h2 className="text-lg font-semibold mb-2">Upcoming Appointments</h2>
        <ul className="divide-y">
          {appointments.map(a => (
            <li key={a.id} className="py-2 flex justify-between">
              <div>
                <p className="font-medium">
                  {format(parseISO(a.appointment_date), 'HH:mm')} –{' '}
                  {a.patient.first_name} {a.patient.last_name}
                </p>
                <p className="text-sm text-gray-500">Dr. {a.provider.name}</p>
              </div>
              <span className={`px-2 py-0.5 rounded-full text-xs ${
                a.status === 'cancelled'
                  ? 'bg-red-100 text-red-600'
                  : 'bg-green-100 text-green-600'
              }`}>
                {a.status.charAt(0).toUpperCase() + a.status.slice(1)}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
