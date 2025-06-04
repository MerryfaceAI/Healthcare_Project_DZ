import { apiFetch } from "@/api/apiClient";

export interface Appointment {
  id: number;
  patient: { id: number; first_name: string; last_name: string };
  provider: { id: number; name: string };
  appointment_date: string;
  reason: string;
  status: string;
}

export async function getAppointments(): Promise<Appointment[]> {
  const res = await apiFetch("/appointments/");
  const data = await res.json();
  return data.results ?? data;
}

export async function getAppointmentById(id: number): Promise<Appointment> {
  const res = await apiFetch(`/appointments/${id}/`);
  return res.json();
}

export async function createAppointment(
  payload: Partial<Appointment>
): Promise<Appointment> {
  const res = await apiFetch("/appointments/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function updateAppointment(
  id: number,
  payload: Partial<Appointment>
): Promise<Appointment> {
  const res = await apiFetch(`/appointments/${id}/`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function deleteAppointment(id: number): Promise<void> {
  const res = await apiFetch(`/appointments/${id}/`, { method: "DELETE" });
  if (res.status !== 204 && res.status !== 200) {
    throw new Error(`Failed to delete appointment ${id}`);
  }
}
