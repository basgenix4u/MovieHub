import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import { API_BASE_URL } from '@/lib/api';

async function searchMovies(query: string) {
  // FIX: Changed endpoint to /universal-search and parameter to q
  const res = await fetch(`${API_BASE_URL}/movies/universal-search?q=${encodeURIComponent(query)}`, { 
    next: { revalidate: 3600 } 
  });
  if (!res.ok) return { results: [] };
  const data = await res.json();
  return { results: data.results || [] };
}

export default async function SearchPage({ searchParams }: { searchParams: { q: string } }) {
  const query = searchParams.q || '';
  const data = await searchMovies(query);
  const movies = data.results || [];

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white">
      <Navbar />
      
      <section className="px-8 py-24 max-w-7xl mx-auto">
        <div className="mb-12">
          <h1 className="text-sm font-bold text-red-600 uppercase tracking-widest mb-2">Search Results</h1>
          <h2 className="text-4xl font-black tracking-tight mb-4">Results for "{query}"</h2>
          <p className="text-gray-400 text-lg">We found {movies.length} cinematic matches for your query.</p>
        </div>

        {movies.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-8">
            {movies.map((movie: any, idx: number) => (
              <MovieCard key={movie.id || idx} movie={movie} />
            ))}
          </div>
        ) : (
          <div className="text-center py-32 glass rounded-3xl border border-white/10">
            <h2 className="text-2xl font-semibold text-gray-500 mb-4">No movies found.</h2>
            <p className="text-gray-600 mb-8">We couldn't find anything matching "{query}". Try different keywords!</p>
            <a href="/" className="inline-block bg-red-600 text-white px-8 py-3 rounded-full font-bold hover:bg-red-700 transition">
              Back to Discovery
            </a>
          </div>
        )}
      </section>
    </main>
  );
}
