import Link from 'next/link';
import { Github, Twitter, Instagram, Mail } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-black border-t border-white/10 py-12 px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="col-span-1 md:col-span-2">
          <Link href="/" className="text-2xl font-black tracking-tighter text-red-600 mb-6 block">
            MOVIEHUB
          </Link>
          <p className="text-gray-400 max-w-sm mb-6 leading-relaxed">
            The ultimate cinema aggregator. Bringing together the world's best movie 
            databases and streaming sources into one high-end experience.
          </p>
          <div className="flex gap-4">
            <a href="#" className="p-2 glass rounded-full text-gray-400 hover:text-white transition"><Github className="w-5 h-5" /></a>
            <a href="#" className="p-2 glass rounded-full text-gray-400 hover:text-white transition"><Twitter className="w-5 h-5" /></a>
            <a href="#" className="p-2 glass rounded-full text-gray-400 hover:text-white transition"><Instagram className="w-5 h-5" /></a>
            <a href="#" className="p-2 glass rounded-full text-gray-400 hover:text-white transition"><Mail className="w-5 h-5" /></a>
          </div>
        </div>
        
        <div>
          <h4 className="text-white font-bold mb-6">Platform</h4>
          <ul className="space-y-4 text-gray-400 text-sm">
            <li><Link href="/trending" className="hover:text-white transition">Trending</Link></li>
            <li><Link href="/watchlist" className="hover:text-white transition">My Watchlist</Link></li>
            <li><Link href="/profile" className="hover:text-white transition">Account Settings</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-bold mb-6">Support</h4>
          <ul className="space-y-4 text-gray-400 text-sm">
            <li><a href="#" className="hover:text-white transition">Help Center</a></li>
            <li><a href="#" className="hover:text-white transition">Terms of Service</a></li>
            <li><a href="#" className="hover:text-white transition">Privacy Policy</a></li>
          </ul>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto mt-12 pt-8 border-t border-white/5 text-center text-gray-500 text-xs">
        © {new Date().getFullYear()} MovieHub. All rights reserved. Designed for the ultimate cinema lover.
      </div>
    </footer>
  );
}
