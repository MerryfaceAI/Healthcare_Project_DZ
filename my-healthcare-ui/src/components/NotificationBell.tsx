import React, { useState, useEffect, useRef } from 'react';
import { Bell } from 'lucide-react';

interface Notification {
  id: number;
  message: string;
  is_read: boolean;
  created_at: string;
}

export default function NotificationBell() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [open, setOpen] = useState(false);
  const bellRef = useRef<HTMLDivElement>(null);

  // Poll every 30s
  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await fetch('/patients/api/notifications/', {
          credentials: 'include',
        });
        if (res.ok) {
          const data = await res.json();
          setNotifications(data.results);
        }
      } catch (err) {
        console.error('Fetch failed', err);
      }
    };
    fetchNotifications();
    const iv = setInterval(fetchNotifications, 30000);
    return () => clearInterval(iv);
  }, []);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const markAsRead = async (id: number) => {
    try {
      await fetch(`/patients/api/notifications/${id}/`, {
        method: 'PATCH',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_read: true }),
      });
      setNotifications(ns =>
        ns.map(n => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch (err) {
      console.error('Mark as read failed', err);
    }
  };

  // Close on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (bellRef.current && !bellRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div className="relative inline-block" ref={bellRef}>
      <button
        onClick={() => setOpen(o => !o)}
        className="p-2 hover:bg-gray-200 rounded-full relative"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 -mt-1 -mr-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-600 rounded-full">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-64 bg-white border border-gray-200 rounded shadow-lg z-10">
          {notifications.length > 0 ? (
            notifications.map(n => (
              <div
                key={n.id}
                onClick={() => markAsRead(n.id)}
                className={`p-2 border-b last:border-none cursor-pointer ${
                  n.is_read ? 'bg-gray-50' : 'bg-white'
                } hover:bg-gray-100`}
              >
                <p className="text-sm">{n.message}</p>
                <time className="text-xs text-gray-500">
                  {new Date(n.created_at).toLocaleString()}
                </time>
              </div>
            ))
          ) : (
            <p className="p-2 text-sm text-center text-gray-500">
              No notifications.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
