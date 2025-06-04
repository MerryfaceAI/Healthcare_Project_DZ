// my-healthcare-ui/src/api/auth.ts
export interface TokenResponse {
  token: string;
}

export async function login(username: string, password: string): Promise<void> {
  const res = await fetch('/api/token-auth/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Login failed');
  }
  const data: TokenResponse = await res.json();
  localStorage.setItem('token', data.token);
}

export function logout(): void {
  localStorage.removeItem('token');
}
export function isAuthenticated(): boolean {
  return !!localStorage.getItem('token');
}