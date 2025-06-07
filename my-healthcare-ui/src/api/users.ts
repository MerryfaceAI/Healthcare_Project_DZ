// src/api/users.ts
import { apiFetch } from './apiClient';

export interface CurrentUser {
  first_name: string;
  last_name: string;
  role: string;
  avatar_url?: string;
  gender?: string;
  tags?: string[];
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const res = await apiFetch('/users/me/');
  return res.json();
}
