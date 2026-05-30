'use client';
import { useState, useEffect } from 'react';
import { Bell, X } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';

export default function NotificationCenter() {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    if (!user) return;

    // Listen for real-time notifications in Supabase
    const channel = supabase
      .channel('realtime-notifications')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'notifications', filter: `user_id=eq.${user.id}` }, 
      (payload) => {
        setNotifications(prev => [payload.new, ...prev]);
        // Optional: Trigger a browser notification here
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [user]);

  return (
    <div className="fixed top-20 right-6 z-40">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="p-3 glass rounded-full text-white hover:text-red-500 transition-all relative"
      >
        <Bell className="w-6 h-6" />
        {notifications.length > 0 && (
          <span className="absolute top-0 right-0 w-3 h-3 bg-red-600 rounded-full border-2 border-black"></span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-4 w-80 glass rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
          <div className="p-4 border-b border-white/10 flex justify-between items-center bg-white/5">
            <h3 className="font-bold">Notifications</h3>
            <button onClick={() => setIsOpen(false)}><X className="w-4 h-4" /></button>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-8 text-center text-gray-500 text-sm">No new notifications</div>
            ) : (
              notifications.map((n, i) => (
                <div key={i} className="p-4 border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer">
                  <p className="text-sm text-gray-200">{n.message}</p>
                  <span className="text-[10px] text-gray-500">{n.created_at}</span>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
