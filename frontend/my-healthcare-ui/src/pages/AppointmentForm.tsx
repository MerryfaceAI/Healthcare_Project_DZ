import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Appointment,
  getAppointmentById,
  createAppointment,
  updateAppointment,
} from "@/api/appointments";
import { getPatients, Patient } from "@/api/patients";
import { getProviders, Provider } from "@/api/providers";

interface AppointmentFormProps {
  editMode?: boolean;
}

const AppointmentForm: React.FC<AppointmentFormProps> = ({ editMode = false }) => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

  const [patients, setPatients] = useState<Patient[]>([]);
  const [providers, setProviders] = useState<Provider[]>([]);

  const [formValues, setFormValues] = useState<Partial<Appointment>>({
    patient: undefined,
    provider: undefined,
    appointment_date: "",
    reason: "",
    status: "scheduled",
  });
  const [loading, setLoading] = useState(editMode);

  useEffect(() => {
    // Load dropdown data
    async function loadDropdowns() {
      try {
        const [pList, provList] = await Promise.all([
          getPatients(),
          getProviders(),
        ]);
        setPatients(pList);
        setProviders(provList);
      } catch (err) {
        console.error("Dropdown fetch error:", err);
      }
    }
    loadDropdowns();

    if (editMode && id) {
      getAppointmentById(Number(id))
        .then((appt) => {
          setFormValues({
            patient: appt.patient,
            provider: appt.provider,
            appointment_date: appt.appointment_date.slice(0, 16), // yyyy-MM-DDThh:mm
            reason: appt.reason,
            status: appt.status,
          });
        })
        .catch((err) => console.error("Fetch appointment failed:", err))
        .finally(() => setLoading(false));
    }
  }, [editMode, id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormValues({
      ...formValues,
      [name]:
        name === "patient" || name === "provider"
          ? Number(value)
          : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editMode && id) {
        await updateAppointment(Number(id), formValues as Appointment);
      } else {
        await createAppointment(formValues as Appointment);
      }
      navigate("/appointments");
    } catch (err) {
      console.error("Submit failed:", err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full text-gray-500">
        Loading form...
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-2xl font-semibold mb-4">
        {editMode ? "Edit Appointment" : "New Appointment"}
      </h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Patient dropdown */}
        <div>
          <label className="block text-sm font-medium">Patient</label>
          <select
            name="patient"
            value={typeof formValues.patient === "object" && formValues.patient !== null ? formValues.patient.id : formValues.patient ?? ""}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          >
            <option value="" disabled>
              — Select a patient —
            </option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.first_name} {p.last_name}
              </option>
            ))}
          </select>
        </div>

        {/* Provider dropdown */}
        <div>
          <label className="block text-sm font-medium">Provider</label>
          <select
            name="provider"
            value={typeof formValues.provider === "object" && formValues.provider !== null ? formValues.provider.id : formValues.provider ?? ""}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          >
            <option value="" disabled>
              — Select a provider —
            </option>
            {providers.map((pr) => (
              <option key={pr.id} value={pr.id}>
                {pr.name} ({pr.specialty})
              </option>
            ))}
          </select>
        </div>

        {/* Date & time */}
        <div>
          <label className="block text-sm font-medium">Date & Time</label>
          <input
            type="datetime-local"
            name="appointment_date"
            value={formValues.appointment_date ?? ""}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          />
        </div>

        {/* Reason */}
        <div>
          <label className="block text-sm font-medium">Reason</label>
          <input
            type="text"
            name="reason"
            value={formValues.reason ?? ""}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          />
        </div>

        {/* Status */}
        <div>
          <label className="block text-sm font-medium">Status</label>
          <select
            name="status"
            value={formValues.status ?? "scheduled"}
            onChange={handleChange}
            className="mt-1 w-full border px-3 py-2 rounded"
          >
            <option value="scheduled">Scheduled</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
            <option value="no_show">No Show</option>
          </select>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          {editMode ? "Update Appointment" : "Create Appointment"}
        </button>
      </form>
    </div>
  );
};

export default AppointmentForm;
