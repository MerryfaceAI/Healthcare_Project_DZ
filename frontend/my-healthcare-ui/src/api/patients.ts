import { apiFetch } from "@/api/apiClient";
import { ReactNode } from "react";

export interface Patient {
  dob: ReactNode;
  mrn: ReactNode;
  pending_discharge: unknown;
  id: number;
  medical_record_number: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  // Add any other fields your serializer produces
}

export async function getPatients(): Promise<Patient[]> {
  const res = await apiFetch("/api/patients/");
  const data = await res.json();
  return data.results ?? data;
}

export async function getPatient(id: number): Promise<Patient> {
  const res = await apiFetch(`/api/patients/${id}/`);
  return res.json();
}

export async function createPatient(payload: Partial<Patient>): Promise<Patient> {
  const res = await apiFetch("/api/patients/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function updatePatient(
  id: number,
  payload: Partial<Patient>
): Promise<Patient> {
  const res = await apiFetch(`/api/patients/${id}/`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function deletePatient(id: number): Promise<void> {
  const res = await apiFetch(`/api/patients/${id}/`, { method: "DELETE" });
  if (res.status !== 204 && res.status !== 200) {
    throw new Error(`Failed to delete patient ${id}`);
  }
}

export async function searchPatients(query: string): Promise<Patient[]> {
  const encoded = encodeURIComponent(query);
  const res = await apiFetch(`/api/patients/?search=${encoded}`);
  const data = await res.json();
  return data.results ?? data;
}
