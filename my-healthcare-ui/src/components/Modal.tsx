// src/components/Modal.tsx
import React from 'react';

interface ModalProps {
  children: React.ReactNode;
  onClose?: () => void;
}

const Modal: React.FC<ModalProps> = ({ children, onClose }) => (
  <div className="modal">
    <div
      className="modal-backdrop"
      onClick={onClose}
    />
    <div className="modal-content">
      {children}
    </div>
  </div>
);

export default Modal;
