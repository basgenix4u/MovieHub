import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import { API_BASE_URL } from '@/lib/api';

async function getTrendingMovies() {
  const res = await fetch(`${API_BASE_URL}/movies/trending`, { next: { revalidate: 3600 } });
  if (!res.ok) return { results: [] };
  return res.json();
}

export default async function Home() {
  const data = await getTrendingMovies();
  const movies = data.results || [];

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      <section className="relative h-[70vh] w-full flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-black via-transparent to-black z-10" />
        <img 
          src="https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070&auto=format&fit=crop" 
          alt="Hero" 
          className="absolute inset-0 w-full h-full object-cover opacity-50"
        />
        <div className="relative z-20 text-center px-4">
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter mb-4">
            DISCOVER <span className="text-red-600">CINEMA</span>
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8">
            Explore the latest trending movies, deep-dive into details, and stream trailers all in one place.
          </p>
          <button className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-full font-bold transition-all transform hover:scale-105">
            Start Exploring
          </button>
        </div>
      </section>

      <section className="px-8 py-16">
        <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
          <span className="w-2 h-8 bg-red-600 rounded-full" />
          Trending Now
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {movies.length > 0 ? (
            movies.map((movie: any) => (
              <MovieCard key={movie.id} movie={movie} />
            ))
          ) : (
            <div className="col-span-full text-center py-20 text-gray-500">
              No movies found. Please make sure the backend is running.
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
