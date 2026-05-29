import Navbar from '@/components/Navbar';
import { notFound } from 'next/navigation';

async function getMovieDetails(id: string) {
  const res = await fetch(`http://localhost:8000/movies/${id}`, { next: { revalidate: 3600 } });
  if (!res.ok) return null;
  return res.json();
}

export default async function MovieDetailsPage({ params }: { params: { id: string } }) {
  const movie = await getMovieDetails(params.id);

  if (!movie) return notFound();

  const trailer = movie.videos?.results?.find((v: any) => v.type === 'Trailer' && v.site === 'YouTube');
  const trailerUrl = trailer ? `https://www.youtube.com/embed/${trailer.key}` : null;

  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      
      {/* Backdrop Section */}
      <div className="relative h-[60vh] w-full">
        <img 
          src={`https://image.tmdb.org/t/p/original${movie.backdrop_path}`} 
          alt={movie.title} 
          className="w-full h-full object-cover opacity-40"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
        
        <div className="absolute bottom-0 left-0 p-8 md:p-16 w-full max-w-6xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-black mb-4">{movie.title}</h1>
          <div className="flex items-center gap-4 text-lg text-gray-300">
            <span className="text-yellow-400 font-bold">★ {movie.vote_average.toFixed(1)}</span>
            <span>{movie.release_date?.split('-')[0]}</span>
            <span className="px-2 py-1 bg-gray-800 rounded text-xs uppercase font-bold">{movie.runtime} min</span>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="max-w-6xl mx-auto px-8 py-12 grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Left Column: Poster & Details */}
        <div className="lg:col-span-1">
          <img 
            src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} 
            alt={movie.title} 
            className="w-full rounded-2xl shadow-2xl border border-gray-800"
          />
          <div className="mt-8 space-y-4">
            <h3 className="text-xl font-bold">Genres</h3>
            <div className="flex flex-wrap gap-2">
              {movie.genres?.map((g: any) => (
                <span key={g.id} className="px-3 py-1 bg-red-600/20 text-red-500 rounded-full text-sm border border-red-600/30">
                  {g.name}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Overview & Trailer */}
        <div className="lg:col-span-2 space-y-8">
          <div>
            <h2 className="text-3xl font-bold mb-4">Overview</h2>
            <p className="text-gray-400 text-lg leading-relaxed">{movie.overview}</p>
          </div>

          <div>
            <h2 className="text-3xl font-bold mb-4">Official Trailer</h2>
            {trailerUrl ? (
              <div className="aspect-video w-full rounded-2xl overflow-hidden border border-gray-800 shadow-2xl">
                <iframe 
                  src={trailerUrl} 
                  className="w-full h-full" 
                  allowFullScreen
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                />
              </div>
            ) : (
              <div className="aspect-video w-full bg-gray-900 rounded-2xl flex items-center justify-center text-gray-500 border border-gray-800">
                No trailer available for this movie.
              </div>
            )}
          </div>

          <div>
            <h2 className="text-3xl font-bold mb-4">Top Cast</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {movie.credits?.cast?.slice(0, 8).map((person: any) => (
                <div key={person.id} className="text-center group">
                  <img 
                    src={person.profile_path ? `https://image.tmdb.org/t/p/w185${person.profile_path}` : 'https://via.placeholder.com/185x278?text=No+Image'} 
                    className="w-full rounded-lg mb-2 group-hover:scale-105 transition-transform duration-300"
                  />
                  <p className="text-sm font-semibold truncate">{person.name}</p>
                  <p className="text-xs text-gray-500 truncate">{person.character}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
