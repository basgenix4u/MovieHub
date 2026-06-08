import { notFound } from 'next/navigation';
import { API_BASE_URL } from '@/lib/api';
import MovieDetailsClient from '@/components/MovieDetailsClient';

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
    <MovieDetailsClient 
      movie={movie} 
      recommendations={recommendations} 
      sources={sources} 
      trailerUrl={trailerUrl} 
    />
  );
}
