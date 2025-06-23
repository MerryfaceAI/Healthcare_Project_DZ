// src/components/LoginModal.tsx
import React, { useState } from "react";
import { apiFetch } from "../api/apiClient";
import Modal from "./Modal";

interface LoginModalProps {
  onSuccess: () => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ onSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErrorMsg("");

    // POST to token-auth as JSON
    const res = await apiFetch("/api/token-auth/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      setErrorMsg("Invalid credentials");
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.token);
    onSuccess();
  }

  return (
    <div className="modal">
      <div className="modal-backdrop" />
      <div className="modal-content">
        <h2 className="text-xl font-semibold mb-4">Sign In</h2>
        {errorMsg && <p className="text-red-600 mb-2">{errorMsg}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm">Username</label>
            <input
              type="text"
              className="mt-1 w-full border px-3 py-2 rounded"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm">Password</label>
            <input
              type="password"
              className="mt-1 w-full border px-3 py-2 rounded"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex justify-end">
            <button type="submit" className="btn-primary">
              Sign In
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginModal;
