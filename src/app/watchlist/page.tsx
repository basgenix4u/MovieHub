'use client';
import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import { API_BASE_URL } from '@/lib/api';
import { supabase } from '@/lib/supabase';

export default function WatchlistPage() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    async function loadWatchlist() {
      try {
        const { data: { user } } = await supabase.auth.getUser();
        setUser(user);

        if (user) {
          const res = await fetch(`${API_BASE_URL}/favorites/${user.id}`);
          if (res.ok) {
            const data = await res.json();
            setMovies(data);
          }
        }
      } catch (error) {
        console.error('Error loading watchlist:', error);
      } finally {
        setLoading(false);
      }
    }
    loadWatchlist();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-600"></div>
          <p className="text-gray-500 animate-pulse">Loading your cinema...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      <section className="px-8 py-16 max-w-7xl mx-auto">
        <div className="mb-12">
          <h1 className="text-4xl font-black mb-2">My Watchlist</h1>
          <p className="text-gray-400">Your personal collection of must-watch cinema.</p>
        </div>

        {!user ? (
          <div className="text-center py-20 glass rounded-3xl p-12 border border-white/10">
            <h2 className="text-2xl font-semibold text-gray-500 mb-4">You aren't signed in</h2>
            <p className="text-gray-600 mb-8">Sign in to create your own personal movie collection!</p>
            <button 
              onClick={() => window.location.reload()}
              className="bg-red-600 text-white px-8 py-3 rounded-full font-bold hover:bg-red-700 transition"
            >
              Sign In Now
            </button>
          </div>
        ) : movies.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-8">
            {movies.map((movie: any) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <h2 className="text-2xl font-semibold text-gray-500">Your watchlist is empty.</h2>
            <p className="text-gray-600 mb-8">Start exploring movies and add some to your list!</p>
            <a href="/" className="inline-block bg-red-600 text-white px-8 py-3 rounded-full font-bold hover:bg-red-700 transition">
              Browse Movies
            </a>
          </div>
        )}
      </section>
    </main>
  );
}
