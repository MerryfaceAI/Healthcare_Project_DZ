// src/main.tsx (or index.tsx)
import { StrictMode } from 'react';
import { createRoot }   from 'react-dom/client';
import './index.css';
import App              from './App';   // ← no “.tsx”

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
