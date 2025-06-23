// src/pages/AppointmentList.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate, Link }            from 'react-router-dom';
import {
  Appointment,
  getAppointments,
  deleteAppointment
} from '@/api/appointments';

export default function AppointmentList() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading]           = useState(true);
  const nav = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const data = await getAppointments();
        // guard both array and { results: [] }
        const list = Array.isArray(data)
          ? data
          : (data && typeof data === 'object' && 'results' in data && Array.isArray((data as any).results))
            ? (data as any).results
            : [];
        setAppointments(list);
      } catch (err) {
        console.error('Failed to load appointments:', err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this appointment?')) return;
    try {
      await deleteAppointment(id);
      setAppointments(prev => prev.filter(a => a.id !== id));
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="content">
        <p className="text-gray-500">Loading appointments…</p>
      </div>
    );
  }

  return (
    <div className="content space-y-4">
      {/* header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Appointment List</h1>
        <button
          className="btn-primary"
          onClick={() => nav('/appointments/new')}
        >
          + New Appointment
        </button>
      </div>

      {/* card + table */}
      <div className="dashboard-card overflow-auto">
        <table className="min-w-full table-auto">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">Patient</th>
              <th className="px-4 py-2 text-left">Provider</th>
              <th className="px-4 py-2 text-left">Date</th>
              <th className="px-4 py-2 text-left">Reason</th>
              <th className="px-4 py-2 text-left">Status</th>
              <th className="px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {appointments.length === 0 && (
              <tr>
                <td colSpan={6} className="px-4 py-4 text-center text-gray-500">
                  No appointments found.
                </td>
              </tr>
            )}
            {appointments.map(a => (
              <tr key={a.id} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2">
                  {a.patient.first_name} {a.patient.last_name}
                </td>
                <td className="px-4 py-2">{a.provider.name}</td>
                <td className="px-4 py-2">
                  {new Date(a.appointment_date).toLocaleDateString()}
                </td>
                <td className="px-4 py-2">{a.reason}</td>
                <td className="px-4 py-2 capitalize">{a.status}</td>
                <td className="px-4 py-2 space-x-2">
                  <Link to={`/appointments/${a.id}/edit`} className="text-blue-600 hover:underline">
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(a.id)}
                    className="bg-red-600 text-white px-2 py-1 rounded hover:bg-red-700"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
