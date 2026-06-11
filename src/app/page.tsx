import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import Logo from '@/components/Logo';
import { API_BASE_URL } from '@/lib/api';

async function getTrendingMovies() {
  const res = await fetch(`${API_BASE_URL}/movies/trending`, { next: { revalidate: 3600 } });
  if (!res.ok) return { results: [] };
  return res.json();
}

async function getLatestMovies() {
  // In a real scenario, we'd have a /movies/latest endpoint
  // For now, we can use the /movies/universal-search with a generic query or a specific 'latest' flag
  const res = await fetch(`${API_BASE_URL}/movies/universal-search?q=2026`, { next: { revalidate: 3600 } });
  if (!res.ok) return { results: [] };
  return res.json();
}

export default async function Home() {
  const trendingData = await getTrendingMovies();
  const trendingMovies = trendingData.results || [];

  const latestData = await getLatestMovies();
  const latestMovies = latestData.results || [];

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative h-[85vh] w-full flex items-center px-8 md:px-16 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070&auto=format&fit=crop" 
            alt="Cinema" 
            className="w-full h-full object-cover opacity-40 scale-105 transition-transform duration-1000"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-[#0a0a0a] via-transparent to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0a] via-transparent to-transparent" />
        </div>

        <div className="relative z-10 max-w-3xl">
          <div className="mb-6 animate-fade-in">
            <Logo showText={false} className="w-20 h-20 mb-4" />
          </div>
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-[0.9] mb-6 text-gradient">
            UNLIMITED <br /> <span className="text-red-600">CINEMA</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-xl mb-10 leading-relaxed">
            Dive into the world's most acclaimed films. Explore trending hits, 
            hidden gems, and the latest trailers in one premium experience.
          </p>
          <div className="flex gap-4">
            <button className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-red-600/30">
              Start Exploring
            </button>
          </div>
        </div>
      </section>

      {/* Trending Section */}
      <section className="px-8 md:px-16 py-24 max-w-7xl mx-auto">
        <div className="flex items-end justify-between mb-12">
          <div>
            <h2 className="text-sm font-bold text-red-600 uppercase tracking-widest mb-2">Now Trending</h2>
            <h3 className="text-4xl font-black tracking-tight">Top Picks For You</h3>
          </div>
          <div className="h-px flex-1 bg-gray-800 mx-8 mb-3 hidden md:block" />
        </div>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-8">
          {trendingMovies.length > 0 ? (
            trendingMovies.map((movie: any) => (
              <MovieCard key={movie.id} movie={movie} />
            ))
          ) : (
            <div className="col-span-full text-center py-20 text-gray-500">
              No trending movies found.
            </div>
          )}
        </div>
      </section>

      {/* Latest Releases Section */}
      <section className="px-8 md:px-16 py-24 max-w-7xl mx-auto">
        <div className="flex items-end justify-between mb-12">
          <div>
            <h2 className="text-sm font-bold text-blue-600 uppercase tracking-widest mb-2">Latest Releases</h2>
            <h3 className="text-4xl font-black tracking-tight">Freshly Added</h3>
          </div>
          <div className="h-px flex-1 bg-gray-800 mx-8 mb-3 hidden md:block" />
        </div>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-8">
          {latestMovies.length > 0 ? (
            latestMovies.map((movie: any, idx: number) => (
              <MovieCard key={movie.id || idx} movie={movie} />
            ))
          ) : (
            <div className="col-span-full text-center py-20 text-gray-500">
              No latest releases found.
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
