import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShieldAlert, ShieldCheck, AlertTriangle, HelpCircle, Activity, Link as LinkIcon, AlertCircle, BarChart3, Database } from 'lucide-react';

export default function Results({ analysisState, setAnalysisState }) {
  const navigate = useNavigate();

  if (analysisState.status !== 'success' || !analysisState.result) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center p-8 animate-in fade-in zoom-in duration-500">
        <div className="relative mb-6">
          <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full"></div>
          <Activity className="w-16 h-16 text-primary relative z-10" />
        </div>
        <h2 className="text-2xl font-bold mb-2 text-text-primary">No analysis yet</h2>
        <p className="text-text-secondary mb-8 max-w-sm">Submit an email to view the comprehensive BERT risk assessment results.</p>
        <button
          onClick={() => navigate('/analyze')}
          className="btn-primary"
        >
          Analyze Email
        </button>
      </div>
    );
  }

  const { result } = analysisState;
  const isPhishing = result.appClassification === 'PHISHING';
  const isSpam = result.appClassification === 'SPAM';
  const riskColor = result.riskLevel === 'HIGH' ? 'text-danger' : result.riskLevel === 'MEDIUM' ? 'text-warning' : 'text-success';
  const confidencePercent = (result.confidence * 100).toFixed(1);

  return (
    <div className="space-y-6 pb-12 animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-6xl mx-auto pt-4">
      
      {/* Dramatic Status Banner */}
      <div className={`relative overflow-hidden p-8 rounded-2xl border-2 flex flex-col md:flex-row items-center justify-between shadow-2xl ${
        isPhishing ? 'bg-danger/5 border-danger/40' : isSpam ? 'bg-warning/5 border-warning/40' : 'bg-success/5 border-success/40'
      }`}>
        <div className={`absolute top-0 right-0 p-32 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none ${isPhishing ? 'bg-danger/20' : isSpam ? 'bg-warning/20' : 'bg-success/20'}`}></div>
        
        <div className="flex items-center relative z-10 w-full md:w-auto mb-6 md:mb-0">
          <div className={`p-4 rounded-full mr-6 ${isPhishing ? 'bg-danger/20 text-danger' : isSpam ? 'bg-warning/20 text-warning' : 'bg-success/20 text-success'}`}>
            {isPhishing ? <ShieldAlert className="w-12 h-12" /> : isSpam ? <AlertTriangle className="w-12 h-12" /> : <ShieldCheck className="w-12 h-12" />}
          </div>
          <div>
            <h2 className={`text-3xl md:text-4xl font-bold tracking-tight uppercase ${isPhishing ? 'text-danger' : isSpam ? 'text-warning' : 'text-success'}`}>
              {isPhishing ? '🔴 PHISHING' : isSpam ? '🟠 SPAM' : '🟢 LEGITIMATE'}
            </h2>
            <p className="text-text-secondary mt-2 flex items-center font-mono text-sm">
              <Database className="w-4 h-4 mr-2" /> Application Classification
            </p>
          </div>
        </div>

        {/* Circular Confidence Visualization */}
        <div className="relative z-10 shrink-0 flex items-center justify-center">
          <div className="relative w-32 h-32 rounded-full flex items-center justify-center bg-background shadow-inner" style={{
            background: `conic-gradient(${isPhishing ? '#F87171' : '#34D399'} ${confidencePercent}%, transparent 0)`
          }}>
            <div className="absolute inset-1 bg-surface rounded-full flex flex-col items-center justify-center border border-border-strong">
              <span className="text-2xl font-mono font-bold text-text-primary">{confidencePercent}%</span>
              <span className="text-[10px] text-text-muted uppercase tracking-widest mt-1">Confidence</span>
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card bg-warning/5 border-warning/20 p-4 flex items-start space-x-3">
        <AlertCircle className="w-5 h-5 text-warning shrink-0 mt-0.5" />
        <div className="text-sm text-text-secondary">
          <span className="font-semibold text-warning">Limitation Notice:</span> This is a model prediction, not a definitive verdict. With the 0.70 threshold, legitimate emails may still occasionally be flagged (25.31% FPR). <Link to="/performance" className="text-primary hover:text-primary-strong hover:underline ml-1 transition-colors">View Model Performance</Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center group hover:-translate-y-1">
          <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-2">Assessed Risk Level</p>
          <div className={`flex items-center text-4xl font-bold tracking-tight ${riskColor} mb-4`}>
            {result.riskLevel === 'HIGH' && <AlertTriangle className="w-10 h-10 mr-3" />}
            {result.riskLevel === 'MEDIUM' && <AlertTriangle className="w-10 h-10 mr-3" />}
            {result.riskLevel === 'LOW' && <ShieldCheck className="w-10 h-10 mr-3" />}
            {result.riskLevel === 'UNKNOWN' && <HelpCircle className="w-10 h-10 mr-3" />}
            {result.riskLevel}
          </div>
          <div className="border-t border-border-subtle pt-4 w-full">
            <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-1">BERT Prediction</p>
            <p className={`font-mono text-sm font-semibold ${result.prediction === 'PHISHING' ? 'text-danger' : 'text-success'}`}>
              {result.prediction}
            </p>
          </div>
        </div>

        <div className="glass-card p-6 flex flex-col justify-center">
          <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-4 text-center">Prediction Probability</p>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1 text-xs">
                <span className="text-danger font-medium uppercase tracking-wider">Phishing</span>
                <span className="font-mono text-text-primary">{(result.phishingProbability * 100).toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full bg-background rounded-full overflow-hidden border border-border-subtle">
                <div 
                  className="h-full bg-danger shadow-[0_0_10px_rgba(248,113,113,0.8)]" 
                  style={{ width: `${result.phishingProbability * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1 text-xs">
                <span className="text-success font-medium uppercase tracking-wider">Legitimate</span>
                <span className="font-mono text-text-primary">{(result.legitimateProbability * 100).toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full bg-background rounded-full overflow-hidden border border-border-subtle">
                <div 
                  className="h-full bg-success shadow-[0_0_10px_rgba(52,211,153,0.8)]" 
                  style={{ width: `${result.legitimateProbability * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div className="glass-card p-6 flex flex-col items-center justify-center text-center group hover:-translate-y-1">
          <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-2">URLs Found</p>
          <div className="text-5xl font-mono font-bold text-primary mb-3 text-shadow-glow">
            {result.urlsFound}
          </div>
          {result.urlsFound > 0 && (
            <Link to="/url-analysis" className="text-xs font-medium text-text-secondary flex items-center hover:text-primary transition-colors bg-elevated px-3 py-1.5 rounded-full border border-border-subtle hover:border-primary/50">
              <LinkIcon className="w-3.5 h-3.5 mr-2 text-primary" /> View URL Analysis
            </Link>
          )}
        </div>
      </div>

      <div className="glass-card p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-32 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
        <h3 className="font-semibold text-lg mb-6 text-text-primary flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-primary" />
          Risk Assessment Factors
        </h3>
        
        {/* Visual Categories for Risk Reasons */}
        <div className="mb-6 space-y-4">
           <div>
             <div className="flex justify-between text-xs mb-1">
               <span className="text-text-secondary uppercase tracking-wider font-semibold">BERT Classification</span>
               <span className="text-primary font-mono">Weight: High</span>
             </div>
             <div className="h-1.5 w-full bg-background rounded-full overflow-hidden flex">
                <div className="h-full bg-primary w-[80%]"></div>
             </div>
           </div>
           <div>
             <div className="flex justify-between text-xs mb-1">
               <span className="text-text-secondary uppercase tracking-wider font-semibold">URL Analysis</span>
               <span className="text-accent font-mono">Weight: Medium</span>
             </div>
             <div className="h-1.5 w-full bg-background rounded-full overflow-hidden flex">
                <div className="h-full bg-accent w-[60%]"></div>
             </div>
           </div>
        </div>

        {result.riskReasons.length > 0 ? (
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
            {result.riskReasons.map((reason, i) => (
              <li key={i} className="flex items-start bg-background/50 p-4 rounded-xl border border-border-subtle group hover:border-primary/30 transition-colors">
                <div className="p-1.5 rounded-full bg-elevated border border-border-strong mr-3 shrink-0 group-hover:bg-primary/10 transition-colors">
                  <AlertCircle className={`w-4 h-4 ${reason.toLowerCase().includes('phishing') ? 'text-danger' : 'text-primary'}`} />
                </div>
                <span className="text-text-secondary text-sm leading-relaxed">{reason}</span>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-text-muted italic text-sm p-6 text-center bg-background/50 rounded-xl border border-border-subtle mt-8">
            No specific risk reasons generated by backend rules.
          </div>
        )}
      </div>

      <div className="flex justify-end gap-4 pt-4">
        <button
          onClick={() => {
            setAnalysisState(prev => ({ ...prev, status: 'idle', result: null, error: null }));
          }}
          className="px-6 py-3 bg-elevated border border-border-strong text-text-primary text-sm font-semibold rounded-xl hover:bg-surface transition-colors"
        >
          Edit & Re-analyze
        </button>
        <button
          onClick={() => {
            setAnalysisState({ status: 'idle', result: null, error: null, submittedInput: null });
          }}
          className="px-6 py-3 bg-surface hover:bg-surface-hover border border-border-strong text-text-primary text-sm font-semibold rounded-xl transition-colors"
        >
          New Analysis
        </button>
        {result.reportId && (
          <button
            onClick={() => navigate(`/reports/${result.reportId}`)}
            className="btn-primary"
          >
            View Full Report
          </button>
        )}
      </div>
    </div>
  );
}
