import React from 'react';
import { Shield, Brain, Zap, Lock } from 'lucide-react';

const HeroSection = () => {
  return (
    <div className="relative pt-32 pb-20 sm:pt-40 sm:pb-24 overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-1/4 -left-1/4 w-1/2 h-1/2 bg-primary/20 blur-[120px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-accent/20 blur-[120px] rounded-full pointer-events-none"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Left Text */}
          <div className="text-left">
            <div className="flex flex-wrap gap-3 mb-6">
              <span className="px-3 py-1 text-xs font-medium bg-white/5 border border-white/10 rounded-full text-gray-300 flex items-center gap-1.5">
                <Brain className="w-3 h-3 text-primary" /> BERT Powered
              </span>
              <span className="px-3 py-1 text-xs font-medium bg-white/5 border border-white/10 rounded-full text-gray-300 flex items-center gap-1.5">
                <Zap className="w-3 h-3 text-accent" /> Real-Time Analysis
              </span>
            </div>
            
            <h1 className="text-5xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight mb-6">
              AI-Powered <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                Email Phishing Detection
              </span>
            </h1>
            
            <p className="text-xl text-gray-400 mb-8 max-w-2xl leading-relaxed">
              Detect suspicious emails using state-of-the-art BERT Natural Language Processing and intelligent URL analysis. Defend against modern threats with military-grade precision.
            </p>
            
            <div className="flex flex-wrap gap-4">
              <a href="#analyzer" className="btn-primary">
                Analyze an Email
              </a>
              <a href="#how-it-works" className="px-6 py-3 rounded-xl border border-white/10 hover:bg-white/5 text-white font-medium transition-colors flex items-center gap-2">
                How It Works
              </a>
            </div>
          </div>
          
          {/* Right Visual */}
          <div className="relative hidden lg:block">
            <div className="glass-card p-6 relative z-10 transform rotate-2 hover:rotate-0 transition-transform duration-500 shadow-2xl shadow-primary/20">
              <div className="flex items-center gap-4 border-b border-white/10 pb-4 mb-4">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Threat Detected</h3>
                  <p className="text-sm text-gray-400">Suspicious language patterns found</p>
                </div>
              </div>
              <div className="space-y-3">
                <div className="h-2 bg-white/10 rounded w-3/4"></div>
                <div className="h-2 bg-white/10 rounded w-full"></div>
                <div className="h-2 bg-white/10 rounded w-5/6"></div>
              </div>
            </div>
            
            {/* Floating elements */}
            <div className="absolute -top-6 -right-6 glass-card p-4 animate-bounce z-20" style={{ animationDuration: '3s' }}>
              <Lock className="w-6 h-6 text-accent" />
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
