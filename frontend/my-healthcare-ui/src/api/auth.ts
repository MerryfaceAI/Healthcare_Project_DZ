// frontend/my-healthcare-ui/src/api/auth.ts

export interface TokenResponse {
  token: string;
}

/**
 * Calls DRF's token-auth endpoint and stores the token.
 * @throws {Error} if credentials are invalid or request fails.
 */
export async function login(username: string, password: string): Promise<void> {
  const res = await fetch('/api/token-auth/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    // DRF returns {"detail": "..."} on 400
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Login failed');
  }

  const { token }: TokenResponse = await res.json();
  // Persist the token for later API calls / auth checks
  localStorage.setItem('token', token);
}

/** Clears stored token */
export function logout(): void {
  localStorage.removeItem('token');
}

/** Simple auth check: do we have a token? */
export function isAuthenticated(): boolean {
  return !!localStorage.getItem('token');
}
