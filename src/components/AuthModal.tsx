'use client';
import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { X, Mail, Lock } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const router = useRouter();

  if (!isOpen) return null;

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    try {
      if (isSignUp) {
        const { data, error } = await supabase.auth.signUp({ email, password });
        if (error) throw error;
        setMessage({ 
          text: 'Success! Please check your email to confirm your account before signing in.', 
          type: 'success' 
        });
      } else {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        
        setMessage({ text: 'Signed in successfully! Redirecting...', type: 'success' });
        router.push('/');
        router.refresh();
      }
    } catch (error: any) {
      console.error('Auth Error:', error);
      setMessage({ 
        text: error.message || 'An unexpected error occurred. Please try again.', 
        type: 'error' 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="relative w-full max-w-md p-8 glass rounded-3xl border border-white/10 shadow-2xl">
        <button onClick={onClose} className="absolute top-4 right-4 p-2 text-gray-500 hover:text-white transition-colors">
          <X className="w-6 h-6" />
        </button>

        <div className="text-center mb-8">
          <h2 className="text-3xl font-black text-white mb-2">
            {isSignUp ? 'Create Account' : 'Welcome Back'}
          </h2>
          <p className="text-gray-400">Join the ultimate cinema community</p>
        </div>

        <form onSubmit={handleAuth} className="space-y-4">
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input 
              type="email" 
              placeholder="Email address" 
              className="w-full bg-white/5 border border-white/10 rounded-xl px-11 py-3 text-white focus:outline-none focus:ring-2 focus:ring-red-600 transition-all"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input 
              type="password" 
              placeholder="Password" 
              className="w-full bg-white/5 border border-white/10 rounded-xl px-11 py-3 text-white focus:outline-none focus:ring-2 focus:ring-red-600 transition-all"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {message.text && (
            <p className={`text-sm text-center p-2 rounded-lg ${message.type === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
              {message.text}
            </p>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-xl transition-all transform active:scale-95 disabled:opacity-50"
          >
            {loading ? 'Processing...' : isSignUp ? 'Sign Up' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button 
            onClick={() => setIsSignUp(!isSignUp)} 
            className="text-sm text-gray-400 hover:text-white transition-colors"
          >
            {isSignUp ? 'Already have an account? Sign In' : 'New here? Create an account'}
          </button>
        </div>
      </div>
    </div>
  );
}
