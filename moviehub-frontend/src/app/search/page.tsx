import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import { API_BASE_URL } from '@/lib/api';

async function searchMovies(query: string) {
  const res = await fetch(`${API_BASE_URL}/movies/search?query=${query}`, { 
    next: { revalidate: 3600 } 
  });
  if (!res.ok) return { results: [] };
  return res.json();
}

export default async function SearchPage({ searchParams }: { searchParams: { q: string } }) {
  const query = searchParams.q || '';
  const data = await searchMovies(query);
  const movies = data.results || [];

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      <section className="px-8 py-16">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Search Results</h1>
          <p className="text-gray-400">Showing results for <span className="text-red-600 font-semibold">"{query}"</span></p>
        </div>

        {movies.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            {movies.map((movie: any) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <h2 className="text-2xl font-semibold text-gray-500">No movies found for your search.</h2>
            <p className="text-gray-600">Try using different keywords.</p>
          </div>
        )}
      </section>
    </main>
  );
}
