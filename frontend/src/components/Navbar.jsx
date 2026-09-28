import React from 'react';
import { ShieldCheck, Activity } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="fixed w-full z-50 bg-background/80 backdrop-blur-lg border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <div className="flex-shrink-0 flex items-center gap-3">
            <div className="relative">
              <ShieldCheck className="w-8 h-8 text-primary" />
              <div className="absolute top-0 right-0 w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            </div>
            <span className="font-bold text-xl tracking-tight text-white hidden sm:block">
              AI Phishing Detector
            </span>
          </div>
          
          {/* Desktop Nav */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <a href="#" className="hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">Home</a>
              <a href="#analyzer" className="hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">Analyze Email</a>
              <a href="#how-it-works" className="hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">How It Works</a>
              <a href="#about" className="hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">About</a>
            </div>
          </div>
          
          {/* Status Badge */}
          <div className="flex items-center gap-2 bg-primary/10 border border-primary/20 px-3 py-1.5 rounded-full">
            <Activity className="w-4 h-4 text-primary animate-pulse" />
            <span className="text-xs font-semibold text-primary uppercase tracking-wider">AI Powered</span>
          </div>

        </div>
      </div>
    </nav>
  );
};

export default Navbar;
