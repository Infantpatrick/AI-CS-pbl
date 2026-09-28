import React, { useState } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import EmailAnalyzer from './components/EmailAnalyzer';
import LoadingState from './components/LoadingState';
import ResultDashboard from './components/ResultDashboard';
import { api, analyzeEmail } from './services/api';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (subject, body) => {
    setIsAnalyzing(true);
    setError(null);
    setResult(null);
    
    // Smooth scroll to analyzer
    document.getElementById('analyzer')?.scrollIntoView({ behavior: 'smooth' });

    const response = await analyzeEmail(subject, body);
    
    // Add artificial delay for animation effect (1.5s)
    setTimeout(() => {
      setIsAnalyzing(false);
      if (response.success) {
        setResult(response.data);
      } else {
        setError(response.error);
      }
    }, 1500);
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <main>
        <HeroSection />
        
        <div className="relative">
          {/* Subtle background separator */}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-transparent pointer-events-none"></div>
          
          <EmailAnalyzer 
            onAnalyze={handleAnalyze} 
            isLoading={isAnalyzing} 
            error={error} 
          />
          
          {isAnalyzing && <LoadingState />}
          
          {!isAnalyzing && result && <ResultDashboard result={result} />}
        </div>
        
        {/* Project Stats Section */}
        <section id="how-it-works" className="max-w-7xl mx-auto px-4 sm:px-6 py-24 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Project Statistics & Performance</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              This system uses a fine-tuned BERT model evaluated on a dedicated test set. High recall ensures we catch most phishing attempts, while URL analysis provides additional context.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
            {[
              { label: 'Dataset Size', value: '87,886' },
              { label: 'Test Samples', value: '8,789' },
              { label: 'Recall (TP Rate)', value: '97.48%' },
              { label: 'F1 Score', value: '75.25%' }
            ].map((stat, i) => (
              <div key={i} className="glass-card p-6 text-center border-t-2 border-t-primary/50 hover:-translate-y-1 transition-transform">
                <p className="text-3xl font-bold text-white mb-2">{stat.value}</p>
                <p className="text-sm text-gray-400 font-medium">{stat.label}</p>
              </div>
            ))}
          </div>

          <div className="glass-card p-8 text-center max-w-3xl mx-auto">
            <h3 className="text-xl font-bold text-white mb-6">Test Set Performance</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-gray-400 text-sm">Accuracy</p>
                <p className="text-xl font-bold text-white">67.58%</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Precision</p>
                <p className="text-xl font-bold text-white">61.28%</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Recall</p>
                <p className="text-xl font-bold text-accent">97.48%</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">F1 Score</p>
                <p className="text-xl font-bold text-primary">75.25%</p>
              </div>
            </div>
            <p className="text-sm text-gray-500 italic border-t border-white/10 pt-4">
              "High recall helps minimize missed phishing emails, while the current model has a relatively high false-positive rate. This is balanced by static URL analysis for a comprehensive risk assessment."
            </p>
          </div>
        </section>

      </main>
      
      <footer id="about" className="bg-surface border-t border-white/10 py-12 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">AI-Based Email Phishing Detection</h2>
          <p className="text-gray-400 max-w-2xl mx-auto mb-8">
            This project uses a fine-tuned BERT model to classify email content as phishing or legitimate. It combines NLP-based classification with static URL analysis to provide an additional risk assessment.
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-500">
            <span>Built with:</span>
            <span className="text-gray-300">Python</span> •
            <span className="text-gray-300">BERT</span> •
            <span className="text-gray-300">PyTorch</span> •
            <span className="text-gray-300">FastAPI</span> •
            <span className="text-gray-300">React</span> •
            <span className="text-gray-300">Vite</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
