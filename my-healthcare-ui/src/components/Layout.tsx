import React from "react";
import { NavLink, Outlet } from "react-router-dom";

/**
 * Layout wraps the entire app once the user is authenticated.
 * It renders a fixed sidebar on the left with navigation links,
 * and an <Outlet /> on the right where child routes are displayed.
 */
const Layout: React.FC = () => {
  return (
    <div className="min-h-screen flex">
      {/* ===== Sidebar ===== */}
      <aside className="w-64 bg-gray-800 text-white flex flex-col">
        <div className="p-6 text-2xl font-bold">
          Healthcare App
        </div>

        <nav className="flex-1 px-4 space-y-2">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive
                ? "block px-4 py-2 bg-gray-700 rounded"
                : "block px-4 py-2 hover:bg-gray-700 rounded"
            }
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/patients"
            className={({ isActive }) =>
              isActive
                ? "block px-4 py-2 bg-gray-700 rounded"
                : "block px-4 py-2 hover:bg-gray-700 rounded"
            }
          >
            Patients
          </NavLink>

          <NavLink
            to="/appointments"
            className={({ isActive }) =>
              isActive
                ? "block px-4 py-2 bg-gray-700 rounded"
                : "block px-4 py-2 hover:bg-gray-700 rounded"
            }
          >
            Appointments
          </NavLink>

          <NavLink
            to="/providers"
            className={({ isActive }) =>
              isActive
                ? "block px-4 py-2 bg-gray-700 rounded"
                : "block px-4 py-2 hover:bg-gray-700 rounded"
            }
          >
            Providers
          </NavLink>

          <NavLink
            to="/notifications"
            className={({ isActive }) =>
              isActive
                ? "block px-4 py-2 bg-gray-700 rounded"
                : "block px-4 py-2 hover:bg-gray-700 rounded"
            }
          >
            Notifications
          </NavLink>
        </nav>

        <div className="p-4">
          <button
            className="w-full bg-red-600 px-4 py-2 rounded hover:bg-red-700"
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/login";
            }}
          >
            Logout
          </button>
        </div>
      </aside>

      {/* ===== Main Content Area ===== */}
      <main className="flex-1 bg-gray-100 p-6 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
