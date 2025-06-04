/**
 * Minimal fetch wrapper that automatically:
 *  • Prepends “/api” if you don’t include it
 *  • Sends credentials so Django’s session/CSRF tokens work
 *  • Throws an error on non‐OK responses
 */
export interface ApiFetchOptions extends RequestInit {
  // method, body, headers, etc.
}

export async function apiFetch(
  path: string,
  options: ApiFetchOptions = {}
): Promise<Response> {
  const fetchOpts: RequestInit = {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    method: options.method || "GET",
    body: options.body,
  };

  const url = path.startsWith("/api") ? path : `/api${path}`;
  const res = await fetch(url, fetchOpts);
  if (!res.ok) {
    throw new Error(`API request failed: [${res.status}] ${res.statusText} at ${url}`);
  }
  return res;
}
