'use client';
import { useState } from 'react';
import TrailerModal from './TrailerModal';

interface TrailerPlayerProps {
  url: string;
}

export default function TrailerPlayer({ url }: TrailerPlayerProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        onClick={() => setIsOpen(true)}
        className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-full font-bold transition-all transform hover:scale-105 inline-flex items-center gap-2 shadow-lg shadow-red-600/30"
      >
        <span>▶ Watch Trailer</span>
      </button>
      <TrailerModal url={url} isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
}
