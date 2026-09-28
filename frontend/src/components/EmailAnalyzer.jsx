import React, { useState } from 'react';
import { Search, Eraser, AlertCircle } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

const EmailAnalyzer = ({ onAnalyze, isLoading, error }) => {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');

  const handleAnalyze = () => {
    if (!subject.trim() && !body.trim()) return;
    onAnalyze(subject, body);
  };

  const handleClear = () => {
    setSubject('');
    setBody('');
  };

  const isFormEmpty = !subject.trim() && !body.trim();

  return (
    <div id="analyzer" className="max-w-4xl mx-auto px-4 sm:px-6 py-12 relative z-10">
      <div className="glass-card p-6 sm:p-10">
        
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Analyze Your Email</h2>
          <p className="text-gray-400">Paste an email below to detect potential phishing threats.</p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        )}

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2 ml-1">Email Subject</label>
            <input 
              type="text" 
              className="glass-input" 
              placeholder="e.g. URGENT: Account Verification Required"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              disabled={isLoading}
            />
          </div>

          <div>
            <div className="flex justify-between items-end mb-2 ml-1 mr-1">
              <label className="block text-sm font-medium text-gray-300">Email Body</label>
              <span className="text-xs text-gray-500">{body.length} characters</span>
            </div>
            <textarea 
              className="glass-input min-h-[200px] resize-y" 
              placeholder="Paste the full email body here..."
              value={body}
              onChange={(e) => setBody(e.target.value)}
              disabled={isLoading}
            ></textarea>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 pt-4 border-t border-white/10">
            <button 
              onClick={handleClear}
              disabled={isLoading || isFormEmpty}
              className="px-6 py-3 rounded-xl border border-white/10 hover:bg-white/5 text-gray-300 font-medium transition-colors flex items-center justify-center gap-2 flex-1 sm:flex-none disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Eraser className="w-4 h-4" /> Clear
            </button>
            
            <button 
              onClick={handleAnalyze}
              disabled={isLoading || isFormEmpty}
              className="btn-primary flex-1 relative overflow-hidden group"
            >
              {isLoading ? (
                <>
                  <div className="absolute inset-0 bg-white/20 animate-scan"></div>
                  <span className="relative z-10 flex items-center gap-2">
                    <Search className="w-5 h-5 animate-pulse" /> Analyzing...
                  </span>
                </>
              ) : (
                <span className="relative z-10 flex items-center gap-2">
                  <Search className="w-5 h-5" /> Analyze Email
                </span>
              )}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default EmailAnalyzer;
