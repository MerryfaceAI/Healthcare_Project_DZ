import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  FaTachometerAlt,
  FaUserInjured,
  FaCalendarAlt,
  FaUserMd,
  FaBell,
  FaCog,
  FaSignOutAlt,
} from 'react-icons/fa';

const menu = [
  { label: 'Dashboard',   icon: <FaTachometerAlt />, to: '/dashboard' },
  { label: 'Patients',    icon: <FaUserInjured />,   to: '/patients' },
  { label: 'Appointments', icon: <FaCalendarAlt />,  to: '/appointments' },
  { label: 'Providers',   icon: <FaUserMd />,        to: '/providers' },
  { label: 'Notifications', icon: <FaBell />,        to: '/notifications' },
  { label: 'Settings',     icon: <FaCog />,          to: '/settings' },
  { label: 'Logout',       icon: <FaSignOutAlt />,   to: '/logout' },
];

const Sidebar: React.FC = () => (
  <aside
    className="
      fixed top-16 left-0 bottom-0
      w-16 hover:w-64
      bg-sidebar-bg text-sidebar-fg
      overflow-hidden
      transition-all duration-200
      z-20
    "
  >
    {/* Logo / Collapse handle */}
    <div className="h-16 flex items-center justify-center">
      <span className="text-2xl">🩺</span>
      <span className="ml-2 font-bold text-lg opacity-0 hover:opacity-100 transition-opacity duration-200">
        Healthcare
      </span>
    </div>

    {/* Navigation */}
    <nav className="mt-4 flex flex-col space-y-1">
      {menu.map(({ label, icon, to }) => (
        <NavLink
          key={label}
          to={to}
          className={({ isActive }) =>
            `flex items-center h-12 px-4 space-x-3 
             ${
               isActive
                 ? 'bg-sidebar-active text-sidebar-active-fg'
                 : 'hover:bg-sidebar-hover hover:text-sidebar-hover-fg'
             }
             transition-colors
            `
          }
        >
          <span className="text-lg">{icon}</span>
          <span className="opacity-0 hover:opacity-100 transition-opacity duration-200">
            {label}
          </span>
        </NavLink>
      ))}
    </nav>
  </aside>
);

export default Sidebar;
