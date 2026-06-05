import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import { API_BASE_URL } from '@/lib/api';

async function getTrendingMovies() {
  const res = await fetch(`${API_BASE_URL}/movies/trending`, { next: { revalidate: 3600 } });
  if (!res.ok) return { results: [] };
  return res.json();
}

export default async function TrendingPage() {
  const data = await getTrendingMovies();
  const movies = data.results || [];

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white">
      <Navbar />
      
      <section className="px-8 md:px-16 py-24 max-w-7xl mx-auto">
        <div className="mb-12">
          <h1 className="text-sm font-bold text-red-600 uppercase tracking-widest mb-2">Trending</h1>
          <h2 className="text-5xl font-black tracking-tight">Global Hits</h2>
          <p className="text-gray-400 mt-4 text-lg">The most watched movies across the globe right now.</p>
        </div>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-8">
          {movies.length > 0 ? (
            movies.map((movie: any) => (
              <MovieCard key={movie.id} movie={movie} />
            ))
          ) : (
            <div className="col-span-full text-center py-20 text-gray-500">
              No trending movies found.
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
