'use client';
import { useState, useEffect } from 'react';
import { Heart } from 'lucide-react';
import { API_BASE_URL } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';

interface FavoriteButtonProps {
  movieId: number;
  initialIsFavorite?: boolean;
}

export default function FavoriteButton({ movieId, initialIsFavorite = false }: FavoriteButtonProps) {
  const { user, setAuthOpen } = useAuth();
  const [isFavorite, setIsFavorite] = useState(initialIsFavorite);

  const toggleFavorite = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!user) {
      setAuthOpen(true); // OPEN MODAL INSTEAD OF ALERT
      return;
    }

    const previousState = isFavorite;
    setIsFavorite(!isFavorite);

    try {
      const res = await fetch(`${API_BASE_URL}/favorites/${movieId}?user_id=${user.id}`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to sync');
    } catch (error) {
      setIsFavorite(previousState);
    }
  };

  return (
    <button 
      onClick={toggleFavorite}
      className="p-2 rounded-full bg-gray-900/50 hover:bg-gray-800 transition-all duration-200 border border-gray-700 group active:scale-90"
    >
      <Heart 
        className={`w-5 h-5 transition-colors duration-200 ${isFavorite ? 'fill-red-600 text-red-600' : 'text-gray-400 group-hover:text-white'}`} 
      />
    </button>
  );
}
