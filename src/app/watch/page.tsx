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

  // The proxy URL
  const proxyUrl = `${API_BASE_URL}/proxy/?url=${encodeURIComponent(targetUrl)}`;

  return (
    <div className="fixed inset-0 pt-16 bg-black">
      <iframe 
        src={proxyUrl}
        className="w-full h-full border-none"
        allowFullScreen
        allow="autoplay; encrypted-media; fullscreen"
      />
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
