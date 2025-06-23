// src/api/users.ts
export interface CurrentUser {
  id: number;
  first_name: string;
  last_name: string;
  role: string;
  avatar_url?: string;
  // any other fields you need...
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const res = await fetch('/api/users/me/', {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) {
    throw new Error('Could not fetch current user');
  }
  return res.json();
}