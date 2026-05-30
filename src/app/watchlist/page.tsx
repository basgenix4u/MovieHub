import Navbar from '@/components/Navbar';
import MovieCard from '@/components/MovieCard';
import { API_BASE_URL } from '@/lib/api';

async function getWatchlist() {
  // Using user_id=1 for the demo as per current backend setup
  const res = await fetch(`${API_BASE_URL}/favorites/1`, { next: { revalidate: 0 } });
  if (!res.ok) return [];
  return res.json();
}

export default async function WatchlistPage() {
  const movies = await getWatchlist();

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      <section className="px-8 py-16">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">My Watchlist</h1>
          <p className="text-gray-400">Your personal collection of must-watch cinema.</p>
        </div>

        {movies.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            {movies.map((movie: any) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <h2 className="text-2xl font-semibold text-gray-500">Your watchlist is empty.</h2>
            <p className="text-gray-600">Start exploring movies and add some to your list!</p>
            <a href="/" className="inline-block mt-6 bg-red-600 text-white px-6 py-2 rounded-full font-bold hover:bg-red-700 transition">
              Browse Movies
            </a>
          </div>
        )}
      </section>
    </main>
  );
}
