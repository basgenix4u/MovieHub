'use client';

import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import { User, LogOut, Mail, Shield, Settings } from 'lucide-react';

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState('');
  const [updating, setUpdating] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function loadUser() {
      const { data: { user }, error } = await supabase.auth.getUser();
      if (error || !user) {
        router.push('/');
      } else {
        setUser(user);
        setEmail(user.email || '');
      }
      setLoading(false);
    }
    loadUser();
  }, [router]);

  const handleUpdateEmail = async () => {
    setUpdating(true);
    const { error } = await supabase.auth.updateUser({ email });
    if (error) {
      alert('Error updating email: ' + error.message);
    } else {
      alert('Email updated successfully!');
    }
    setUpdating(false);
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-8 py-24">
        <div className="flex flex-col items-center text-center mb-12">
          <div className="w-24 h-24 bg-red-600 rounded-full flex items-center justify-center mb-4 shadow-lg shadow-red-600/30">
            <User className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-4xl font-black mb-2">Account Settings</h1>
          <p className="text-gray-400">Manage your identity and preferences</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1 space-y-2">
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-white/10 text-white font-medium hover:bg-white/20 transition">
              <User className="w-5 h-5" /> Profile
            </button>
            <button 
              onClick={() => router.push('/watchlist')}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 font-medium hover:bg-white/10 hover:text-white transition"
            >
              <Shield className="w-5 h-5" /> Watchlist
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 font-medium hover:bg-white/10 hover:text-white transition">
              <Settings className="w-5 h-5" /> Preferences
            </button>
          </div>

          <div className="md:col-span-2 glass rounded-3xl p-8 border border-white/10">
            <h2 className="text-xl font-bold mb-6">Personal Information</h2>
            
            <div className="space-y-6">
              <div className="flex flex-col gap-2">
                <label className="text-sm text-gray-400 flex items-center gap-2">
                  <Mail className="w-4 h-4" /> Email Address
                </label>
                <div className="flex gap-2">
                  <input 
                    type="email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-white/5 border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-red-600 w-full"
                  />
                  <button 
                    onClick={handleUpdateEmail}
                    disabled={updating}
                    className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg font-bold transition disabled:opacity-50"
                  >
                    {updating ? '...' : 'Save'}
                  </button>
                </div>
              </div>

              <div className="pt-8 border-t border-white/10">
                <button 
                  onClick={handleSignOut}
                  className="w-full flex items-center justify-center gap-2 bg-white/5 hover:bg-red-600/20 text-gray-400 hover:text-red-500 px-4 py-3 rounded-xl font-bold transition-all"
                >
                  <LogOut className="w-5 h-5" /> Sign Out of Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
