import React from 'react';
import { Link, AlertTriangle, ShieldCheck } from 'lucide-react';
import { cn } from './EmailAnalyzer';

const URLAnalysis = ({ urlsFound, urlIndicators }) => {
  if (urlsFound === 0) {
    return (
      <div className="glass-card p-6 flex flex-col items-center justify-center text-center h-full min-h-[200px]">
        <div className="w-12 h-12 bg-white/5 rounded-full flex items-center justify-center mb-4">
          <Link className="w-6 h-6 text-gray-400" />
        </div>
        <h4 className="text-white font-medium mb-1">No URLs Detected</h4>
        <p className="text-sm text-gray-400">There are no URLs in this email to analyze.</p>
      </div>
    );
  }

  return (
    <div className="glass-card p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Link className="w-5 h-5 text-accent" />
          URL Analysis
        </h3>
        <span className="px-3 py-1 bg-white/5 rounded-full text-xs font-medium text-gray-300 border border-white/10">
          {urlsFound} {urlsFound === 1 ? 'URL' : 'URLs'} Found
        </span>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {urlIndicators?.map((urlData, idx) => {
          const hasSuspicious = urlData.indicators && urlData.indicators.length > 0;
          
          return (
            <div key={idx} className={cn(
              "p-4 rounded-xl border transition-colors",
              hasSuspicious ? "bg-red-500/5 border-red-500/20" : "bg-white/5 border-white/10"
            )}>
              <div className="flex items-start justify-between mb-3">
                <div className="overflow-hidden pr-4">
                  <p className="text-sm text-gray-200 font-medium truncate" title={urlData.url}>
                    {urlData.url}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Domain: {urlData.domain}</p>
                </div>
                {hasSuspicious ? (
                  <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
                ) : (
                  <ShieldCheck className="w-5 h-5 text-green-400 flex-shrink-0" />
                )}
              </div>
              
              <div className="flex flex-wrap gap-2 mb-3">
                <span className={cn(
                  "text-[10px] uppercase font-bold px-2 py-1 rounded-sm",
                  urlData.uses_https ? "bg-green-500/20 text-green-300" : "bg-red-500/20 text-red-300"
                )}>
                  {urlData.uses_https ? 'HTTPS' : 'HTTP'}
                </span>
                <span className="text-[10px] uppercase font-bold px-2 py-1 rounded-sm bg-white/10 text-gray-300">
                  Length: {urlData.url_length}
                </span>
              </div>

              {hasSuspicious && (
                <div className="mt-3 pt-3 border-t border-red-500/20">
                  <p className="text-xs text-red-300/80 mb-2 font-medium">Suspicious Indicators:</p>
                  <ul className="space-y-1">
                    {urlData.indicators.map((ind, i) => (
                      <li key={i} className="text-xs text-red-200/70 flex items-start gap-1.5">
                        <span className="text-red-400 mt-0.5">•</span> {ind}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default URLAnalysis;
