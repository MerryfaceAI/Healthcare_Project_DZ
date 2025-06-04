// my-healthcare-ui/src/main.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from '@/App';
import './index.css'; // global styles

const rootEl = document.getElementById('react-bar-root');
if (rootEl) {
  const root = createRoot(rootEl);
  root.render(<App />);
}
