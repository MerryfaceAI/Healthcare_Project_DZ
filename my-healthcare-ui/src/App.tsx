// src/App.tsx
import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import NotificationBell from './components/NotificationBell';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

// small helper to pull Django's CSRF token from cookies
function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : null;
}

const App: React.FC = () => {
  // null = checking, false = logged out, true = logged in
  const [loggedIn, setLoggedIn] = useState<boolean | null>(null);

  // on mount, ping a protected endpoint
  useEffect(() => {
    fetch('/patients/api/notifications/', {
      credentials: 'include',
    })
      .then(res => setLoggedIn(res.status === 200))
      .catch(() => setLoggedIn(false));
  }, []);

  // logout handler
  const handleLogout = async () => {
    await fetch('/api-auth/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCookie('csrftoken') || ''
      }
    });
    setLoggedIn(false);
  };

  // still checking?
  if (loggedIn === null) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-gray-500">Checking login…</p>
      </div>
    );
  }

  // not logged in?
  if (!loggedIn) {
    return <Login onSuccess={() => setLoggedIn(true)} />;
  }

  // logged in!
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="flex items-center justify-between p-4 bg-white shadow">
        <div className="flex items-center space-x-4">
          <img src={viteLogo} alt="Vite logo" className="h-8" />
          <img src={reactLogo} alt="React logo" className="h-8" />
          <h1 className="text-xl font-semibold">Healthcare App</h1>
        </div>
        <div className="flex items-center space-x-4">
          <NotificationBell />
          <button
            onClick={handleLogout}
            className="px-3 py-1 border rounded hover:bg-gray-100"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="p-6">
        <h2 className="text-lg font-medium mb-4">Welcome to your dashboard</h2>
        {/* …your other dashboard content… */}
      </main>
    </div>
  );
};

export default App;
