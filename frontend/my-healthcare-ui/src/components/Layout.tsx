// src/components/Layout.tsx
import React, { useState, useEffect } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  FaTachometerAlt,
  FaUserInjured,
  FaCalendarAlt,
  FaUserMd,
  FaBell,
  FaCog,
  FaSignOutAlt,
} from 'react-icons/fa';
import UserProfileCard from './UserProfileCard';
import { getCurrentUser, CurrentUser } from '../api/users';
import './Layout.css';

const menu = [
  { to: 'dashboard',     icon: <FaTachometerAlt/>, label: 'Dashboard' },
  { to: 'patients',      icon: <FaUserInjured/>,   label: 'Patients'  },
  { to: 'appointments',  icon: <FaCalendarAlt/>,   label: 'Appointments' },
  { to: 'providers',     icon: <FaUserMd/>,        label: 'Providers' },
  { to: 'notifications', icon: <FaBell/>,          label: 'Notifications' },
  { to: 'settings',      icon: <FaCog/>,           label: 'Settings' },
];

export default function Layout() {
  const [user, setUser] = useState<CurrentUser|null>(null);
  const nav = useNavigate();

  useEffect(() => {
    getCurrentUser()
      .then(u => setUser(u))
      .catch(() => {
        // token invalid or missing: force login
        localStorage.removeItem('token');
        nav('/login');
      });
  }, [nav]);

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="logo">🩺</div>
        <nav>
          {menu.map(m => (
            <NavLink
              key={m.to}
              to={m.to}
              className={({ isActive }) => isActive ? 'active' : ''}
            >
              {m.icon}
              <span>{m.label}</span>
            </NavLink>
          ))}
        </nav>
        <button
          className="logout"
          onClick={() => {
            localStorage.removeItem('token');
            nav('/login');
          }}
        >
          <FaSignOutAlt/><span>Logout</span>
        </button>
      </aside>

      <div className="main">
        <header className="topbar">
          <h1>Your App Name</h1>
          {user && (
            <UserProfileCard
              mode="icon-only"
              user={user}
            />
          )}
        </header>

        {/* render child routes here, and make `user` available via context */}
        <Outlet context={user} />
      </div>
    </div>
  );
}
