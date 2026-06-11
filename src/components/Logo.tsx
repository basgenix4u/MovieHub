import React from 'react';

interface LogoProps {
  className?: string;
  showText?: boolean;
}

const Logo: React.FC<LogoProps> = ({ className = "", showText = true }) => {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <div className="relative w-10 h-10 group cursor-pointer">
        {/* Outer Glow / Glassmorphism Ring */}
        <div className="absolute inset-0 bg-gradient-to-tr from-red-600 to-red-400 rounded-full blur-sm opacity-50 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Main SVG Logo */}
        <svg 
          viewBox="0 0 100 100" 
          className="relative z-10 w-full h-full drop-shadow-lg"
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#EF4444" />
              <stop offset="100%" stopColor="#B91C1C" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          {/* Cinematic Circle Background */}
          <circle cx="50" cy="50" r="48" fill="url(#logoGradient)" filter="url(#glow)" />
          
          {/* Stylized Play Button / Film Strip Shape */}
          <path 
            d="M40 30L70 50L40 70V30Z" 
            fill="white" 
            className="transition-transform duration-300 group-hover:scale-110"
          />
          
          {/* Decorative Film Accents */}
          <rect x="10" y="45" width="5" height="10" rx="1" fill="white" opacity="0.6" />
          <rect x="10" y="55" width="5" height="10" rx="1" fill="white" opacity="0.6" />
          <rect x="85" y="45" width="5" height="10" rx="1" fill="white" opacity="0.6" />
          <rect x="85" y="55" width="5" height="10" rx="1" fill="white" opacity="0.6" />
        </svg>
      </div>

      {showText && (
        <span className="text-2xl font-black tracking-tighter text-white">
          MOVIE<span className="text-red-600">HUB</span>
        </span>
      )}
    </div>
  );
};

export default Logo;
