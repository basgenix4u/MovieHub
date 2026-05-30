'use client';
import { X } from 'lucide-react';

interface TrailerModalProps {
  url: string;
  isOpen: boolean;
  onClose: () => void;
}

export default function TrailerModal({ url, isOpen, onClose }: TrailerModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm">
      <div className="relative w-full max-w-5xl aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl border border-gray-800">
        <button 
          onClick={onClose} 
          className="absolute top-4 right-4 z-10 p-2 bg-black/50 hover:bg-black/80 text-white rounded-full transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
        <iframe 
          src={url} 
          className="w-full h-full" 
          allow="autoplay; encrypted-media; gyroscope; picture-in-picture" 
          allowFullScreen
        />
      </div>
      <div className="absolute inset-0 -z-10" onClick={onClose} />
    </div>
  );
}
