import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  FaTachometerAlt,
  FaUserInjured,
  FaCalendarAlt,
  FaUserMd,
  FaBell,
  FaCog,
  FaSignOutAlt
} from 'react-icons/fa';
import UserProfileCard from './UserProfileCard';

const items = [
  { to: 'dashboard', icon: <FaTachometerAlt/>, label: 'Dashboard' },
  { to: 'patients',  icon: <FaUserInjured/>,    label: 'Patients'  },
  { to: 'appointments', icon: <FaCalendarAlt/>, label: 'Appointments' },
  { to: 'providers', icon: <FaUserMd/>,        label: 'Providers' },
  { to: 'notifications', icon: <FaBell/>,      label: 'Notifications' },
  { to: 'settings',    icon: <FaCog/>,         label: 'Settings' },
];

const Layout: React.FC = () => {
  const nav = useNavigate();
  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="logo">🩺</div>
        <nav>
          {items.map(({to,icon,label})=>(
            <NavLink
              key={to}
              to={to}
              className={({isActive})=> isActive?'active':''}
            >
              {icon}<span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <button
          className="btn-danger"
          onClick={() => { localStorage.removeItem('token'); nav('/'); }}
        >
          <FaSignOutAlt/> Logout
        </button>
      </aside>

      <div className="main">
        <header className="topbar">
          <h1>Your App Name</h1>
          <UserProfileCard mode="icon-only" />
        </header>
        <div style={{ padding: '1rem' }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
