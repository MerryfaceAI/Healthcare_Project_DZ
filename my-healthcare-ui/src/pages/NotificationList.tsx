// src/pages/NotificationList.tsx
import React, { useEffect, useState } from "react";
import type { Notification } from "../api/notifications";
import {
  getNotifications,
  markNotificationAsRead,
  deleteNotification,
} from "../api/notifications";
import { format, parseISO, isValid } from "date-fns";

const NotificationList: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // pass false to get both read+unread; pass true to get only unread
    getNotifications(false)
      .then((data) => setNotifications(data))
      .catch(() => setError("Failed to load notifications."))
      .finally(() => setLoading(false));
  }, []);

  const handleMarkAsRead = (id: number) => {
    markNotificationAsRead(id).then((updated) => {
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? updated : n))
      );
    });
  };

  const handleDelete = (id: number) => {
    if (!window.confirm("Delete this notification?")) return;
    deleteNotification(id).then(() =>
      setNotifications((prev) => prev.filter((n) => n.id !== id))
    );
  };

  if (loading) return <p className="p-4">Loading…</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;

  return (
    <main className="main-content p-6">
      <div className="dashboard-card">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-semibold">Notifications</h1>
          <button className="btn-primary" onClick={() => getNotifications(false).then(setNotifications)}>
            Mark All Read
          </button>
        </div>
        {notifications.length === 0 ? (
          <p>No notifications found.</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {notifications.map((n) => (
              <li
                key={n.id}
                className={`py-3 flex justify-between items-center ${
                  n.is_read ? "" : "bg-gray-50"
                }`}
              >
                <div>
                  <p>{n.message}</p>
                  {n.appointment &&
                    isValid(parseISO(n.appointment.appointment_date)) && (
                      <p className="text-sm text-gray-500">
                        Appointment:{" "}
                        {format(
                          parseISO(n.appointment.appointment_date),
                          "yyyy-MM-dd HH:mm"
                        )}
                      </p>
                    )}
                  <p className="text-xs text-gray-400">
                    {isValid(parseISO(n.created_at))
                      ? format(parseISO(n.created_at), "yyyy-MM-dd HH:mm")
                      : "—"}
                  </p>
                </div>
                <div className="space-x-2">
                  {!n.is_read && (
                    <button
                      onClick={() => handleMarkAsRead(n.id)}
                      className="text-blue-600 hover:underline text-sm"
                    >
                      Mark Read
                    </button>
                  )}
                  <button
                    onClick={() => handleDelete(n.id)}
                    className="text-red-600 hover:underline text-sm"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
};

export default NotificationList;
