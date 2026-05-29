import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-black text-white border-b border-gray-800 sticky top-0 z-50">
      <Link href="/" className="text-2xl font-bold tracking-tighter text-red-600">
        MOVIEHUB
      </Link>
      <div className="flex gap-6 items-center">
        <Link href="/trending" className="hover:text-red-500 transition">Trending</Link>
        <Link href="/movies" className="hover:text-red-500 transition">Movies</Link>
        <div className="relative">
          <input 
            type="text" 
            placeholder="Search movies..." 
            className="bg-gray-900 border border-gray-700 rounded-full px-4 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-red-600 w-64"
          />
        </div>
      </div>
    </nav>
  );
}
