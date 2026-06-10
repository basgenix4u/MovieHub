'use client';

import { useState } from 'react';
import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import TrailerPlayer from '@/components/TrailerPlayer';
import Link from 'next/link';

export default function MovieDetailsClient({ movie, recommendations, sources, trailerUrl }: any) {
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
            <span className="text-yellow-400 font-bold">{movie.vote_average.toFixed(1)}</span>
            <span>{movie.release_date?.split('-')[0]}</span>
          </div>

          <div className="flex flex-wrap gap-4">
            {trailerUrl && <TrailerPlayer url={trailerUrl} />}
            
            {sources && sources.length > 0 ? (
              sources.map((source: any, idx: number) => {
                // Handle YouTube vs other sources
                if (source.type === 'youtube') {
                  const watchUrl = `https://www.youtube.com/watch?v=${source.url}`;
                  const downloadUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/movies/youtube/download/${source.url}?title=${encodeURIComponent(movie.title)}`;
                  
                  return (
                    <div key={idx} className="flex gap-2">
                      <Link 
                        href={`/watch?url=${encodeURIComponent(watchUrl)}`}
                        className="bg-red-600 hover:bg-red-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-red-600/30 flex items-center gap-2"
                      >
                        Watch HD Movie
                      </Link>
                      <a 
                        href={downloadUrl} 
                        target="_blank"
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-blue-600/30 flex items-center gap-2"
                      >
                        Download HD Movie
                      </a>
                    </div>
                  );
                }

                // Handle other sources
                const finalUrl = source.url.startsWith('http') 
                  ? source.url 
                  : `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${source.url}`;

                return source.type === 'download' ? (
                  <a 
                    key={idx} 
                    href={finalUrl} 
                    target="_blank"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-blue-600/30 flex items-center gap-2"
                  >
                    Download Direct
                  </a>
                ) : (
                  <Link 
                    key={idx} 
                    href={`/watch?url=${encodeURIComponent(source.url)}`}
                    className="bg-red-600 hover:bg-red-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-red-600/30 flex items-center gap-2"
                  >
                    Watch {source.name}
                  </Link>
                );
              })
            ) : (
              <div className="text-gray-500 italic text-sm">
                Searching for high-quality sources...
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="max-w-6xl mx-auto px-8 py-12">
        <h2 className="text-3xl font-bold mb-4">Overview</h2>
        <p className="text-gray-400 text-lg leading-relaxed">{movie.overview}</p>
      </div>

      {recommendations && recommendations.length > 0 && (
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
