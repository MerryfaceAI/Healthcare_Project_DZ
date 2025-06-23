// src/ui-kit/Card.tsx
import React from 'react';

export function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`dashboard-card ${className}`}>
      {children}
    </div>
  );
}
