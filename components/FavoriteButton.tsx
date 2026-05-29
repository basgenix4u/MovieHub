'use client';
import { useState } from 'react';
import { Heart } from 'lucide-react';
import { API_BASE_URL } from '@/lib/api';

interface FavoriteButtonProps {
  movieId: number;
  initialIsFavorite?: boolean;
}

export default function FavoriteButton({ movieId, initialIsFavorite = false }: FavoriteButtonProps) {
  const [isFavorite, setIsFavorite] = useState(initialIsFavorite);
  const [isLoading, setIsLoading] = useState(false);

  const toggleFavorite = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/favorites/${movieId}?user_id=1`, {
        method: 'POST',
      });
      if (res.ok) {
        setIsFavorite(!isFavorite);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button 
      onClick={toggleFavorite}
      disabled={isLoading}
      className="p-2 rounded-full bg-gray-900/50 hover:bg-gray-800 transition-colors border border-gray-700 group"
    >
      <Heart 
        className={`w-5 h-5 transition-colors ${isFavorite ? 'fill-red-600 text-red-600' : 'text-gray-400 group-hover:text-white'}`} 
      />
    </button>
  );
}
