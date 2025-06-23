// my-healthcare-ui/src/pages/Login.tsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "@/api/apiClient";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      // You must obtain a CSRF token first, so include the default Django login route:
      // Here we assume apiFetch will include credentials, so that set-cookie can set CSRF.
      await fetch("/api-auth/login/", {
        credentials: "include",
      });

      // Now POST credentials to /api/token-auth/
      const res = await fetch("/api/token-auth/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          // You must include the Django CSRF token in the header. 
          // Use a helper to read cookie “csrftoken”:
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setErrorMsg("Invalid credentials");
        return;
      }

      const data = await res.json();
      localStorage.setItem("token", data.token);
      navigate("/dashboard");
    } catch (err) {
      console.error("Login error:", err);
      setErrorMsg("Login failed");
    }
  };

  // Helper to read CSRF cookie by name:
  function getCookie(name: string): string | null {
    const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
    return match ? decodeURIComponent(match[2]) : null;
  }

  return (
    <div className="flex items-center justify-center h-full bg-gray-50">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold mb-4">Login</h1>
        {errorMsg && (
          <p className="text-red-600 mb-4">{errorMsg}</p>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="mt-1 w-full border px-3 py-2 rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 w-full border px-3 py-2 rounded"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
