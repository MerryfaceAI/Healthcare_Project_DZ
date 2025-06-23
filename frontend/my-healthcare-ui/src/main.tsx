// src/main.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import { ConfigProvider } from 'antd';
import App from './App';
import 'antd/dist/reset.css'; // or 'antd/dist/antd.css' for v4

// this is the one file that contains
// your .app-container, .sidebar, .topbar, .main, .dashboard-card, etc.
import './index.css';

const container = document.getElementById('root');
if (!container) throw new Error('Root container missing');
createRoot(container).render(
  <ConfigProvider>
    <App />
  </ConfigProvider>
);
