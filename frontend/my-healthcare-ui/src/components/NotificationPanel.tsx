// src/components/NotificationPanel.tsx
import React, { useEffect, useState } from "react";
import type { Notification } from "../api/notifications";
import { getNotifications, markNotificationAsRead } from "../api/notifications";

const NotificationPanel: React.FC = () => {
  const [notes, setNotes] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getNotifications(false)   // <-- pass the boolean!
      .then((data) => setNotes(data))
      .catch((err) => console.error("Failed to fetch notifications", err))
      .finally(() => setLoading(false));
  }, []);

  // ...
  return <div>{loading ? "Loading..." : /* render notes */ null}</div>;
};

export default NotificationPanel;
