// src/ui-kit/Button.tsx
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'danger';
}

export function Button({ variant = 'primary', className = '', ...rest }: ButtonProps) {
  const base = 'px-4 py-2 rounded font-medium';
  const styles = variant === 'primary'
    ? 'bg-blue-600 text-white hover:bg-blue-700'
    : 'bg-red-600 text-white hover:bg-red-700';
  return <button className={`${base} ${styles} ${className}`} {...rest} />;
}
