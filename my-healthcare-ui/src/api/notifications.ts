import { apiFetch } from "@/api/apiClient";

export interface Notification {
  id: number;
  recipient: number;
  appointment: number;
  message: string;
  is_read: boolean;
  created_at: string;
}

export async function getNotifications(
  unreadOnly = false
): Promise<Notification[]> {
  let url = "/notifications/";
  if (unreadOnly) url += "?is_read=false";
  const res = await apiFetch(url);
  const data = await res.json();
  return data.results ?? data;
}

export async function markNotificationAsRead(
  id: number
): Promise<Notification> {
  const res = await apiFetch(`/notifications/${id}/`, {
    method: "PATCH",
    body: JSON.stringify({ is_read: true }),
  });
  return res.json();
}
