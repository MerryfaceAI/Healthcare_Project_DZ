// src/api/notifications.ts
import { apiFetch } from "@/api/apiClient";

export interface Notification {
  id: number;
  message: string;
  appointment?: { id: number; appointment_date: string } | null;
  is_read: boolean;
  created_at: string;
}

/**
 * @param unreadOnly  if true, only unread; otherwise both read+unread
 */
export async function getNotifications(
  unreadOnly: boolean = false
): Promise<Notification[]> {
  let url = "/api/notifications/";
  if (unreadOnly) {
    url += "?is_read=false";
  }
  const res = await apiFetch(url);
  const data = await res.json();
  return data.results ?? data;
}

export async function markNotificationAsRead(
  id: number
): Promise<Notification> {
  const res = await apiFetch(`/api/notifications/${id}/`, {
    method: "PATCH",
    body: JSON.stringify({ is_read: true }),
    headers: { "Content-Type": "application/json" },
  });
  return res.json();
}

export async function deleteNotification(id: number): Promise<void> {
  await apiFetch(`/api/notifications/${id}/`, {
    method: "DELETE",
  });
}
