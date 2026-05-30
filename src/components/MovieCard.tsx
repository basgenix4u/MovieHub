import Link from 'next/link';
import FavoriteButton from './FavoriteButton';

interface MovieProps {
  movie: {
    id: number;
    title: string;
    poster_path: string;
    vote_average: number;
  };
}

export default function MovieCard({ movie }: MovieProps) {
  const posterUrl = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
  
  return (
    <div className="group relative aspect-[2/3] overflow-hidden rounded-xl bg-gray-900 transition-all duration-500 hover:scale-105 hover:shadow-[0_0_30px_rgba(229,9,20,0.3)]">
      <Link href={`/movie/${movie.id}`} className="block w-full h-full">
        <img 
          src={posterUrl} 
          alt={movie.title} 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" 
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
          <h3 className="text-white font-bold text-sm leading-tight mb-1">{movie.title}</h3>
          <div className="flex items-center gap-2">
            <span className="text-yellow-400 text-xs font-bold">★ {movie.vote_average.toFixed(1)}</span>
          </div>
        </div>
      </Link>
      <div className="absolute top-2 right-2 z-10">
        <FavoriteButton movieId={movie.id} />
      </div>
    </div>
  );
}
