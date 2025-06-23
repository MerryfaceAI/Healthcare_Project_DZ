// src/components/Modal.tsx
import React from 'react';
import './Modal.css';

interface ModalProps {
  children: React.ReactNode;
  onClose?: () => void;
}
export default function Modal({ children, onClose }: ModalProps) {
  return (
    <>
      <div className="modal-backdrop" />
      <div className="modal-content">
        {children}
      </div>
    </>
  );
}
