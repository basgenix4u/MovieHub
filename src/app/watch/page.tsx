'use client';

import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';
import Navbar from '@/components/Navbar';
import { API_BASE_URL } from '@/lib/api';

function WatchPlayer() {
  const searchParams = useSearchParams();
  const targetUrl = searchParams.get('url');

  if (!targetUrl) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <p className="text-2xl">No movie URL provided.</p>
      </div>
    );
  }

  const isYouTube = targetUrl.includes('youtube.com/embed/');
  const finalUrl = isYouTube 
    ? targetUrl 
    : `${API_BASE_URL}/proxy/?url=${encodeURIComponent(targetUrl)}`;

  return (
    <div className="fixed inset-0 bg-black flex flex-col">
      {/* Navbar height adjustment */}
      <div className="h-16 w-full" /> 
      
      <div className="flex-1 relative w-full h-full">
        <iframe 
          src={finalUrl}
          className="absolute inset-0 w-full h-full border-none"
          allowFullScreen
          allow="autoplay; encrypted-media; fullscreen"
          title="Movie Player"
        />
        
        {/* Overlay fallback for Age Restricted / Blocked Content */}
        <div className="absolute bottom-8 right-8 flex flex-col gap-3">
          <p className="text-xs text-gray-500 bg-black/50 px-2 py-1 rounded">
            If the video doesn't load, it may be age-restricted by YouTube.
          </p>
          <a 
            href={targetUrl.replace('/embed/', '/watch?v=')} 
            target="_blank" 
            className="text-xs bg-white/10 hover:bg-white/20 text-white px-3 py-2 rounded-full transition-all backdrop-blur-sm border border-white/10"
          >
            Watch on YouTube ↗
          </a>
        </div>
      </div>
    </div>
  );
}

export default function WatchPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <Navbar />
      <Suspense fallback={
        <div className="min-h-screen bg-black text-white flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-600"></div>
        </div>
      }>
        <WatchPlayer />
      </Suspense>
    </main>
  );
}
