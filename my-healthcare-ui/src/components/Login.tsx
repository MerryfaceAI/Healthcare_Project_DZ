// src/components/Login.tsx
import React, { useState, useEffect } from 'react';
import { getCookie } from '../utils/csrf';

interface LoginProps {
  onSuccess: () => void;
}

export default function Login({ onSuccess }: LoginProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // Prime the CSRF cookie (so Django will set it in document.cookie)
  useEffect(() => {
    fetch('/api-auth/login/', { credentials: 'include' }).catch(() => {});
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const csrfToken = getCookie('csrftoken') || '';

    const res = await fetch('/api-auth/login/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken':    csrfToken,
        'Referer':        window.location.origin,
      },
      body: new URLSearchParams({ username, password }).toString(),
    });

    if (res.ok) onSuccess();
    else      setError('Invalid credentials');
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-sm mx-auto mt-10 p-4 bg-white rounded shadow">
      <h2 className="text-lg font-semibold mb-4">Sign In</h2>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <label className="block mb-2">
        <span className="text-sm">Username</span>
        <input
          type="text"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="mt-1 block w-full border rounded p-2"
          required
        />
      </label>
      <label className="block mb-4">
        <span className="text-sm">Password</span>
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="mt-1 block w-full border rounded p-2"
          required
        />
      </label>
      <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Sign In
      </button>
    </form>
  );
}
