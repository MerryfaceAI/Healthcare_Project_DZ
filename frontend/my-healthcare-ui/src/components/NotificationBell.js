import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect, useRef } from 'react';
import { Bell } from 'lucide-react';
export default function NotificationBell() {
    const [notifications, setNotifications] = useState([]);
    const [open, setOpen] = useState(false);
    const bellRef = useRef(null);
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
            }
            catch (err) {
                console.error('Fetch failed', err);
            }
        };
        fetchNotifications();
        const iv = setInterval(fetchNotifications, 30000);
        return () => clearInterval(iv);
    }, []);
    const unreadCount = notifications.filter(n => !n.is_read).length;
    const markAsRead = async (id) => {
        try {
            await fetch(`/patients/api/notifications/${id}/`, {
                method: 'PATCH',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_read: true }),
            });
            setNotifications(ns => ns.map(n => (n.id === id ? { ...n, is_read: true } : n)));
        }
        catch (err) {
            console.error('Mark as read failed', err);
        }
    };
    // Close on outside click
    useEffect(() => {
        const handler = (e) => {
            if (bellRef.current && !bellRef.current.contains(e.target)) {
                setOpen(false);
            }
        };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, []);
    return (_jsxs("div", { className: "relative inline-block", ref: bellRef, children: [_jsxs("button", { onClick: () => setOpen(o => !o), className: "p-2 hover:bg-gray-200 rounded-full relative", children: [_jsx(Bell, { className: "w-6 h-6" }), unreadCount > 0 && (_jsx("span", { className: "absolute top-0 right-0 -mt-1 -mr-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-600 rounded-full", children: unreadCount }))] }), open && (_jsx("div", { className: "absolute right-0 mt-2 w-64 bg-white border border-gray-200 rounded shadow-lg z-10", children: notifications.length > 0 ? (notifications.map(n => (_jsxs("div", { onClick: () => markAsRead(n.id), className: `p-2 border-b last:border-none cursor-pointer ${n.is_read ? 'bg-gray-50' : 'bg-white'} hover:bg-gray-100`, children: [_jsx("p", { className: "text-sm", children: n.message }), _jsx("time", { className: "text-xs text-gray-500", children: new Date(n.created_at).toLocaleString() })] }, n.id)))) : (_jsx("p", { className: "p-2 text-sm text-center text-gray-500", children: "No notifications." })) }))] }));
}
