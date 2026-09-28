import React from 'react';
import { Shield, Brain, Search, Activity } from 'lucide-react';

const LoadingState = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <div className="glass-card p-10 flex flex-col items-center justify-center text-center">
        
        <div className="relative w-32 h-32 mb-8">
          {/* Base Shield */}
          <Shield className="w-full h-full text-primary/20 absolute inset-0" strokeWidth={1} />
          
          {/* Scanning line */}
          <div className="absolute inset-0 overflow-hidden rounded-full">
            <div className="w-full h-1 bg-accent shadow-[0_0_15px_rgba(139,92,246,0.8)] animate-scan"></div>
          </div>
          
          {/* Pulsing icons */}
          <div className="absolute inset-0 flex items-center justify-center">
            <Brain className="w-12 h-12 text-primary animate-pulse" />
          </div>
        </div>
        
        <h3 className="text-2xl font-bold text-white mb-6">Analyzing Threat Level...</h3>
        
        <div className="space-y-4 text-left w-full max-w-sm">
          <div className="flex items-center gap-3 text-gray-400 animate-pulse" style={{ animationDelay: '0ms' }}>
            <Activity className="w-5 h-5 text-accent" />
            <span>Scanning Email Content</span>
          </div>
          <div className="flex items-center gap-3 text-gray-400 animate-pulse" style={{ animationDelay: '500ms' }}>
            <Search className="w-5 h-5 text-primary" />
            <span>Analyzing Language Patterns (BERT)</span>
          </div>
          <div className="flex items-center gap-3 text-gray-400 animate-pulse" style={{ animationDelay: '1000ms' }}>
            <Shield className="w-5 h-5 text-green-400" />
            <span>Checking Suspicious Indicators</span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default LoadingState;
