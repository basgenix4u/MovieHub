'use client';

import { useState } from 'react';
import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import TrailerPlayer from '@/components/TrailerPlayer';
import Link from 'next/link';

export default function MovieDetailsClient({ movie, recommendations, sources, trailerUrl }: any) {
  const [ytMovies, setYtMovies] = useState<any[]>([]);
  const [isSearchingYt, setIsSearchingYt] = useState(false);

  const searchYouTube = async () => {
    setIsSearchingYt(true);
    try {
      // Access API_BASE_URL from a global or pass it as prop. 
      // For consistency, we'll use the same pattern as other components.
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${API_BASE_URL}/movies/youtube/search?title=${encodeURIComponent(movie.title)}`);
      const data = await res.json();
      setYtMovies(data.results || []);
    } catch (e) {
      console.error("YT Search Error", e);
    } finally {
      setIsSearchingYt(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      <div className="relative h-[70vh] w-full">
        <img 
          src={`https://image.tmdb.org/t/p/original${movie.backdrop_path}`} 
          alt={movie.title} 
          className="w-full h-full object-cover opacity-40"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
        
        <div className="absolute bottom-0 left-0 p-8 md:p-16 w-full max-w-6xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-black mb-4">{movie.title}</h1>
          <div className="flex items-center gap-4 text-lg text-gray-300 mb-8">
            <span className="text-yellow-400 font-bold">★ {movie.vote_average.toFixed(1)}</span>
            <span>{movie.release_date?.split('-')[0]}</span>
          </div>

          <div className="flex flex-wrap gap-4">
            {trailerUrl && <TrailerPlayer url={trailerUrl} />}
            
            {sources.map((source: any, idx: number) => (
              source.type === 'download' ? (
                <a 
                  key={idx} 
                  href={source.url} 
                  target="_blank"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-blue-600/30 flex items-center gap-2"
                >
                  ⬇️ Direct Download
                </a>
              ) : (
                <Link 
                  key={idx} 
                  href={`/watch?url=${encodeURIComponent(source.url)}`}
                  className="bg-red-600 hover:bg-red-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-red-600/30 flex items-center gap-2"
                >
                  📺 {source.name}
                </Link>
              )
            ))}

            <button 
              onClick={searchYouTube}
              disabled={isSearchingYt}
              className="bg-white text-black hover:bg-gray-200 px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg flex items-center gap-2 disabled:opacity-50"
            >
              {isSearchingYt ? 'Searching...' : '🔍 Find Full Movie on YT'}
            </button>
          </div>

          {ytMovies.length > 0 && (
            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
              {ytMovies.map((ytMovie: any) => (
                <div key={ytMovie.id} className="glass p-4 rounded-2xl border border-white/10 flex items-center gap-4">
                  <img src={ytMovie.thumbnail} className="w-24 h-14 object-cover rounded-lg" alt="thumb" />
                  <div className="flex-1 overflow-hidden">
                    <p className="text-sm font-bold truncate">{ytMovie.title}</p>
                    <p className="text-xs text-gray-400">{Math.floor(ytMovie.duration/60)}m {ytMovie.duration%60}s</p>
                  </div>
                  <a 
                    href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/movies/youtube/download/${ytMovie.id}?title=${encodeURIComponent(movie.title)}`}
                    className="bg-red-600 hover:bg-red-700 p-2 rounded-full transition"
                    title="Download to storage"
                  >
                    ⬇️
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      
      <div className="max-w-6xl mx-auto px-8 py-12">
        <h2 className="text-3xl font-bold mb-4">Overview</h2>
        <p className="text-gray-400 text-lg leading-relaxed">{movie.overview}</p>
      </div>

      {recommendations.length > 0 && (
        <section className="max-w-6xl mx-auto px-8 py-24 border-t border-white/10">
          <div className="flex items-center gap-4 mb-12">
            <h2 className="text-3xl font-black">Recommended For You</h2>
            <div className="h-px flex-1 bg-gray-800" />
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-8">
            {recommendations.map((rec: any) => (
              <MovieCard key={rec.id} movie={rec} />
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
