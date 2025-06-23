// my-healthcare-ui/src/components/NotificationBell.tsx
import React, { useEffect, useState } from 'react';
import type { Notification } from '@/types/models';
import { apiFetch } from '@/api/apiClient';

const NotificationBell: React.FC = () => {
  const [count, setCount] = useState<number>(0);
  const [list, setList] = useState<Notification[]>([]);
  const [open, setOpen] = useState(false);

  const apiUrl = '/api/notifications/';

  const fetchNotifications = async () => {
    const res = await apiFetch(`${apiUrl}?is_read=false`);
    if (!res || !res.ok) return;
    const json = await res.json();
    setCount(json.count);
    setList(json.results);
  };

  const markRead = async (id: number) => {
    const res = await apiFetch(`${apiUrl}${id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ is_read: true }),
    });
    if (res && res.ok) {
      setList(prev => prev.filter(n => n.id !== id));
      setCount(prev => prev - 1);
    }
  };

  useEffect(() => {
    fetchNotifications();
    const iv = setInterval(fetchNotifications, 60000);
    return () => clearInterval(iv);
  }, []);

  return (
    <div className="relative inline-block">
      <button
        onClick={() => setOpen(o => !o)}
        className="relative focus:outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg"
             className="h-6 w-6 text-gray-700"
             fill="none"
             viewBox="0 0 24 24"
             stroke="currentColor">
          <path strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 
                   6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 
                   3 0 11-6 0v-1m6 0H9" />
        </svg>
        {count > 0 && (
          <span className="absolute -top-1 -right-1 inline-flex items-center justify-center
                           px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-600 rounded-full">
            {count}
          </span>
        )}
      </button>
      {open && (
        <div className="absolute right-0 mt-2 w-64 bg-white shadow-lg rounded-lg overflow-hidden z-50">
          <ul className="divide-y divide-gray-200 max-h-72 overflow-auto">
            {list.length > 0 ? (
              list.map(n => (
                <li
                  key={n.id}
                  onClick={() => markRead(n.id)}
                  className="p-2 hover:bg-gray-100 cursor-pointer"
                >
                  {n.message}
                </li>
              ))
            ) : (
              <li className="p-2 text-gray-500 text-sm">No notifications</li>
            )}
          </ul>
          <div className="p-2 text-center text-sm text-gray-500">
            <a href="http://localhost:8000/patients/" className="hover:underline">
              Go to Patient List
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
