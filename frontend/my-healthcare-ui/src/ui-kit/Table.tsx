// src/ui-kit/Table.tsx
import React from 'react';

export function Table({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <table className={`min-w-full table-auto ${className}`}>
      {children}
    </table>
  );
}
