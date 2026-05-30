'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Heart, Search, User } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import AuthModal from './AuthModal';

export default function Navbar() {
  const [searchQuery, setSearchQuery] = useState('');
  const { user, isAuthOpen, setAuthOpen } = useAuth();
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-3 glass rounded-full">
        <Link href="/" className="text-2xl font-black tracking-tighter text-red-600 hover:text-red-500 transition-colors">
          MOVIEHUB
        </Link>
        
        <div className="hidden md:flex gap-8 items-center text-sm font-medium text-gray-400">
          <Link href="/trending" className="hover:text-white transition-colors">Trending</Link>
          <Link href="/watchlist" className="hover:text-white transition-colors flex items-center gap-2">
            <Heart className="w-4 h-4" /> Watchlist
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <form onSubmit={handleSearch} className="relative hidden sm:block">
            <input 
              type="text" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search movies..." 
              className="bg-white/10 border border-white/10 rounded-full px-4 py-1.5 pl-10 text-sm focus:outline-none focus:ring-2 focus:ring-red-600 w-40 md:w-64 transition-all focus:bg-white/20"
            />
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-red-500 transition-colors" />
          </form>

          <button 
            onClick={() => setAuthOpen(true)}
            className="p-2 glass rounded-full text-white hover:text-red-500 transition-all relative flex items-center justify-center"
          >
            {user ? (
              <div className="relative">
                <User className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full border-2 border-black"></span>
              </div>
            ) : (
              <User className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
      <AuthModal isOpen={isAuthOpen} onClose={() => setAuthOpen(false)} />
    </nav>
  );
}
