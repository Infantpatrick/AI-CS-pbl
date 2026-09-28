import React from 'react';
import { Shield, Link as LinkIcon, Info, Globe, AlertOctagon } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function UrlAnalysis({ analysisState }) {
  if (analysisState.status !== 'success' || !analysisState.result) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center animate-in fade-in zoom-in duration-500">
        <div className="relative mb-6">
          <div className="absolute inset-0 bg-accent/20 blur-xl rounded-full"></div>
          <LinkIcon className="w-16 h-16 text-accent relative z-10" />
        </div>
        <h2 className="text-2xl font-bold mb-2 text-text-primary">No URLs to analyze</h2>
        <p className="text-text-secondary max-w-sm mb-8">Analyze an email to extract and inspect embedded URLs without execution.</p>
        <Link to="/analyze" className="btn-primary">
          Analyze Email
        </Link>
      </div>
    );
  }

  const { result } = analysisState;

  return (
    <div className="space-y-6 pb-12 max-w-5xl mx-auto pt-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-text-primary tracking-tight">URL Analysis</h1>
          <p className="text-text-secondary mt-2 flex items-center">
            <Globe className="w-4 h-4 mr-2" />
            Static URL extraction & inspection
          </p>
        </div>
        <div className="glass-card px-5 py-2.5 flex items-center shadow-lg border-primary/20 bg-primary/5">
          <span className="text-xs text-text-muted uppercase tracking-widest mr-3 font-semibold">URLs Extracted</span>
          <span className="text-2xl font-mono font-bold text-primary">{result.urlsFound}</span>
        </div>
      </div>

      <div className="glass-card bg-accent/5 border-accent/20 p-5 flex items-start space-x-4 relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-32 bg-accent/10 rounded-full blur-3xl -mr-16 -mt-16 transition-transform group-hover:scale-110"></div>
        <div className="p-3 bg-accent/20 rounded-xl shrink-0 border border-accent/30">
          <Shield className="w-6 h-6 text-accent" />
        </div>
        <div className="text-sm text-text-secondary relative z-10 pt-1">
          <span className="font-bold text-accent block mb-1 text-base tracking-wide uppercase">Static Analysis Only</span>
          <p className="leading-relaxed">URLs are dynamically extracted but <strong className="text-text-primary">never visited, downloaded, or executed</strong>. All indicators are heuristic signals derived from the raw string and do not represent confirmed threats.</p>
        </div>
      </div>

      {result.urlsFound === 0 ? (
        <div className="glass-card p-12 text-center flex flex-col items-center justify-center">
          <Shield className="w-12 h-12 text-text-muted mb-4 opacity-50" />
          <h3 className="text-xl font-bold text-text-primary mb-2">No URLs Detected</h3>
          <p className="text-text-secondary">The analyzed email did not contain any embedded links.</p>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="glass-card overflow-hidden border-border-strong relative">
            <div className="p-5 border-b border-border-strong bg-elevated flex items-center">
              <LinkIcon className="w-5 h-5 mr-3 text-primary" />
              <h3 className="font-bold text-text-primary tracking-wide">Extracted URLs</h3>
            </div>
            <div className="p-6">
              {result.extractedUrls && result.extractedUrls.length > 0 ? (
                <ul className="space-y-3">
                  {result.extractedUrls.map((url, idx) => (
                    <li key={idx} className="bg-background/80 p-3 rounded-lg border border-border-subtle font-mono text-sm text-text-primary break-all">
                      URL: {url}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-text-secondary italic">URLs were detected but not returned in the response.</p>
              )}
            </div>
          </div>

          <div className="glass-card overflow-hidden border-border-strong relative">
            <div className="p-5 border-b border-border-strong bg-elevated flex items-center">
              <AlertOctagon className="w-5 h-5 mr-3 text-warning" />
              <h3 className="font-bold text-text-primary tracking-wide">Detected URL Indicators</h3>
            </div>
          
          <div className="p-6">
            {result.urlIndicators && result.urlIndicators.length > 0 ? (
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.urlIndicators.map((indicator, idx) => (
                  <li key={idx} className="flex items-start bg-background/80 p-4 rounded-xl border border-border-subtle group hover:border-accent/40 transition-colors">
                    <span className="w-2 h-2 rounded-full bg-accent mt-1.5 mr-3 shrink-0 shadow-[0_0_8px_rgba(168,85,247,0.8)]"></span>
                    <span className="font-mono text-sm text-text-primary break-all leading-relaxed">{indicator}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center p-8 bg-background/50 rounded-xl border border-border-subtle border-dashed">
                <Info className="w-8 h-8 text-text-muted mx-auto mb-3" />
                <p className="text-sm text-text-secondary">No suspicious URL indicators were returned by the backend.</p>
              </div>
            )}
          </div>
        </div>
        </div>
      )}
    </div>
  );
}
