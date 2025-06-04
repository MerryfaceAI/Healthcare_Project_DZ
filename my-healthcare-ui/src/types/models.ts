// src/types/models.ts

export interface Patient {
  id: number;
  medical_record_number: string;
  first_name: string;
  last_name: string;
  date_of_birth: string; // ISO date string
  gender: string;
  contact?: {
    phone?: string;
    email?: string;
  };
  address?: {
    line1?: string;
    line2?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
  };
  emergency_contact?: {
    name?: string;
    relationship?: string;
    phone?: string;
  };
}

export interface Appointment {
  id: number;
  patient: number; // patient ID
  provider: number; // user ID
  appointment_date: string; // ISO datetime
  reason: string;
  status: string;
}

export interface Notification {
  id: number;
  recipient: number; // user ID
  appointment: number; // appointment ID
  message: string;
  is_read: boolean;
  created_at: string; // ISO datetime
}
