import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Appointment,
  getAppointments,
  deleteAppointment,
} from "@/api/appointments";

const AppointmentList: React.FC = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getAppointments();
        setAppointments(data);
      } catch (err) {
        console.error("Failed to load appointments:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this appointment?")) return;
    try {
      await deleteAppointment(id);
      setAppointments((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full text-gray-500">
        Loading appointments...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Appointment List</h1>
        <button
          onClick={() => navigate("/appointments/new")}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          + New Appointment
        </button>
      </div>

      <div className="bg-white shadow rounded overflow-x-auto">
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
            {appointments.map((a) => (
              <tr key={a.id} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2">
                  {a.patient.first_name} {a.patient.last_name}
                </td>
                <td className="px-4 py-2">{a.provider.name}</td>
                <td className="px-4 py-2">
                  {new Date(a.appointment_date).toLocaleDateString()}
                </td>
                <td className="px-4 py-2">{a.reason}</td>
                <td className="px-4 py-2">{a.status}</td>
                <td className="px-4 py-2 space-x-2">
                  <Link
                    to={`/appointments/${a.id}/edit`}
                    className="text-blue-600 hover:underline"
                  >
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
            {appointments.length === 0 && (
              <tr>
                <td
                  colSpan={6}
                  className="px-4 py-4 text-center text-gray-500"
                >
                  No appointments found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AppointmentList;
