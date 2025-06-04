import { apiFetch } from "@/api/apiClient";

export interface Provider {
  id: number;
  name: string;
  specialty: string;
  email?: string;
  phone?: string;
}

export async function getProviders(): Promise<Provider[]> {
  const res = await apiFetch("/providers/");
  const data = await res.json();
  return data.results ?? data;
}
