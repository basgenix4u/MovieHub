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

async function getSources(id: string, title: string) {
  const res = await fetch(`${API_BASE_URL}/movies/${id}/sources?title=${encodeURIComponent(title)}`, { next: { revalidate: 3600 } });
  if (!res.ok) return { sources: [] };
  return res.json();
}

export default async function MovieDetailsPage({ params }: { params: { id: string } }) {
  const movie = await getMovieDetails(params.id);
  if (!movie) return notFound();

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
          </div>

          <div className="flex flex-wrap gap-4">
            {trailerUrl && <TrailerPlayer url={trailerUrl} />}
            
            {sources.map((source: any, idx: number) => (
              <a 
                key={idx} 
                href={source.url} 
                target={source.type === 'download' ? '_blank' : '_self'}
                className="bg-red-600 hover:bg-red-700 text-white px-6 py-4 rounded-full font-bold transition-all transform hover:scale-105 shadow-lg shadow-red-600/30 flex items-center gap-2"
              >
                {source.type === 'download' ? '⬇️ Direct Download' : `📺 ${source.name}`}
              </a>
            ))}
          </div>
        </div>
      </div>
      
      <div className="max-w-6xl mx-auto px-8 py-12">
        <h2 className="text-3xl font-bold mb-4">Overview</h2>
        <p className="text-gray-400 text-lg leading-relaxed">{movie.overview}</p>
      </div>
    </main>
  );
}
