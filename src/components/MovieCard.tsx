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
    <div className="group relative overflow-hidden rounded-lg transition-transform duration-300 hover:scale-105">
      <Link href={`/movie/${movie.id}`}>
        <img src={posterUrl} alt={movie.title} className="w-full h-auto object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
          <h3 className="text-white font-semibold text-sm">{movie.title}</h3>
          <div className="flex items-center gap-2">
            <span className="text-yellow-400 text-xs">★ {movie.vote_average.toFixed(1)}</span>
          </div>
        </div>
      </Link>
      <div className="absolute top-2 right-2 z-10">
        <FavoriteButton movieId={movie.id} />
      </div>
    </div>
  );
}
