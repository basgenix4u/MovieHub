import Navbar from '@/components/Navbar';
import { notFound } from 'next/navigation';
import { API_BASE_URL } from '@/lib/api';
import MovieCard from '@/components/MovieCard';
import TrailerPlayer from '@/components/TrailerPlayer';

async function getMovieDetails(id: string) {
  const res = await fetch(`${API_BASE_URL}/movies/${id}`, { next: { revalidate: 3600 } });
  if (!res.ok) return null;
  return res.json();
}

async function getRecommendations(id: string) {
  const res = await fetch(`${API_BASE_URL}/movies/${id}/recommendations`, { next: { revalidate: 3600 } });
  if (!res.ok) return { results: [] };
  return res.json();
}

async function getSources(id: string, title: string) {
  const res = await fetch(`${API_BASE_URL}/movies/${id}/sources?title=${encodeURIComponent(title)}`, { next: { revalidate: 3600 } });
  if (!res.ok) return { sources: [] };
  return res.json();
}

export default async function MovieDetailsPage({ params }: { params: { id: string } }) {
  const movie = await getMovieDetails(params.id);
  if (!movie) return notFound();

  const recs = await getRecommendations(params.id);
  const recommendations = recs.results || [];

  const sourcesData = await getSources(params.id, movie.title);
  const sources = sourcesData.sources || [];

  const trailer = movie.videos?.results?.find((v: any) => v.type === 'Trailer' && v.site === 'YouTube');
  const trailerUrl = trailer ? `https://www.youtube.com/embed/${trailer.key}?autoplay=1` : null;

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
            <span className="px-2 py-1 bg-gray-800 rounded text-xs uppercase font-bold">{movie.runtime} min</span>
          </div>

          <div className="flex flex-wrap gap-4">
            {trailerUrl && (
              <TrailerPlayer url={trailerUrl} />
            )}
            
            {sources.map((source: any, idx: number) => (
              <a 
                key={idx} 
                href={source.url} 
                target="_blank" 
                className="bg-white/10 hover:bg-white/20 text-white px-6 py-4 rounded-full font-bold transition-all backdrop-blur-md border border-white/10 flex items-center gap-2"
              >
                {source.type === 'download' ? '⬇️ Direct Download' : `📺 Watch on ${source.name}`}
              </a>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-8 py-12 grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-1">
          <img 
            src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} 
            alt={// a placeholder if no poster exists
            movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 'https://via.placeholder.com/500x750'} 
            className="w-full rounded-2xl shadow-2xl border border-gray-800"
          />
        </div>

        <div className="lg:col-span-2 space-y-8">
          <div>
            <h2 className="text-3xl font-bold mb-4">Overview</h2>
            <p className="text-gray-400 text-lg leading-relaxed">{movie.overview}</p>
          </div>

          <div>
            <h2 className="text-3xl font-bold mb-6">Recommended For You</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {recommendations.length > 0 ? (
                recommendations.slice(0, 8).map((rec: any) => (
                  <MovieCard key={rec.id} movie={rec} />
                ))
              ) : (
                <p className="text-gray-500">No recommendations available.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
