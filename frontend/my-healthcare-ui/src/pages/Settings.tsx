// src/pages/Settings.tsx
import React, { useState } from 'react';

const Settings: React.FC = () => {
  // Example: Dark Mode toggle (you can expand this as needed)
  const [darkMode, setDarkMode] = useState(false);

  const handleToggleDarkMode = () => {
    setDarkMode((prev) => !prev);
    // Optionally persist to backend/user preferences
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold text-gray-800 mb-4">Settings</h1>

      <section className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-medium text-gray-700 mb-2">Appearance</h2>
        <div className="flex items-center space-x-3">
          <label htmlFor="darkModeToggle" className="text-gray-600">
            Dark Mode
          </label>
          <input
            id="darkModeToggle"
            type="checkbox"
            checked={darkMode}
            onChange={handleToggleDarkMode}
            className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            aria-checked={darkMode}
          />
        </div>
      </section>

      <section className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-medium text-gray-700 mb-2">Account</h2>
        <p className="text-gray-600">No account settings implemented yet.</p>
        {/* Add more settings (e.g., password, email) as needed */}
      </section>
    </div>
  );
};

export default Settings;
