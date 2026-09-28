import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api/client';
import { getAppClassification } from '../api/normalizers';
import { ShieldAlert, ShieldCheck, AlertTriangle, HelpCircle, Activity, Link as LinkIcon, AlertCircle, BarChart3, Database, User, Calendar, Cpu } from 'lucide-react';

export default function Reports() {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await api.get(`/api/analysis/report/${id}`, { withCredentials: true });
        const data = response.data;
        // Parse JSON lists safely
        try {
          data.risk_reasons = typeof data.risk_reasons === 'string' ? JSON.parse(data.risk_reasons || '[]') : [];
          data.url_indicators = typeof data.url_indicators === 'string' ? JSON.parse(data.url_indicators || '[]') : [];
        } catch (e) {
          data.risk_reasons = [];
          data.url_indicators = [];
        }
        setReport(data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load report');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Activity className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="p-6 bg-danger/10 text-danger rounded-xl border border-danger/20 flex items-start gap-3">
        <AlertTriangle className="w-6 h-6 mb-2 shrink-0" />
        <p>{error || 'Report not found'}</p>
      </div>
    );
  }

  const appClassification = getAppClassification(report.risk_level);
  const isPhishing = appClassification === 'PHISHING';
  const isSpam = appClassification === 'SPAM';
  const riskColor = report.risk_level === 'HIGH' ? 'text-danger' : report.risk_level === 'MEDIUM' ? 'text-warning' : 'text-success';
  const confidencePercent = (report.confidence * 100).toFixed(1);

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

      {/* Email Information */}
      <div className="glass-card p-6 flex flex-col space-y-6">
        <h3 className="font-semibold text-lg text-text-primary flex items-center border-b border-border-subtle pb-4">
          <Cpu className="w-5 h-5 mr-2 text-primary" />
          Email Information
        </h3>
        <div className="flex flex-col sm:flex-row gap-6">
          <div className="flex-1 space-y-4">
            <div className="flex items-start gap-3">
              <User className="w-5 h-5 text-text-muted shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-1">From</p>
                <p className="font-medium text-text-primary break-all">{report.sender.replace(/<.*>/, '').trim() || 'Unknown Sender'}</p>
                <p className="text-xs text-text-secondary break-all">{report.sender.match(/<([^>]+)>/)?.[1] || report.sender}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-text-muted shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-1">Subject</p>
                <p className="font-medium text-text-primary break-all">{report.subject}</p>
              </div>
            </div>
          </div>
          <div className="sm:w-1/3 space-y-4">
            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-text-muted shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-1">Analysis Date</p>
                <p className="font-medium text-text-primary">{new Date(report.analyzed_at).toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>
        
        {report.body && (
          <div>
            <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-4 mt-2">Message Body</p>
            <div className="bg-surface/50 border border-border-subtle rounded-xl p-4 md:p-6 whitespace-pre-wrap font-mono text-sm text-text-secondary leading-relaxed overflow-x-auto">
              {report.body}
            </div>
          </div>
        )}
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center group hover:-translate-y-1">
          <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-2">Assessed Risk Level</p>
          <div className={`flex items-center text-4xl font-bold tracking-tight ${riskColor} mb-4`}>
            {report.risk_level === 'HIGH' && <AlertTriangle className="w-10 h-10 mr-3" />}
            {report.risk_level === 'MEDIUM' && <AlertTriangle className="w-10 h-10 mr-3" />}
            {report.risk_level === 'LOW' && <ShieldCheck className="w-10 h-10 mr-3" />}
            {report.risk_level === 'UNKNOWN' && <HelpCircle className="w-10 h-10 mr-3" />}
            {report.risk_level}
          </div>
          <div className="border-t border-border-subtle pt-4 w-full">
            <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-1">BERT Prediction</p>
            <p className={`font-mono text-sm font-semibold ${report.prediction === 'PHISHING' ? 'text-danger' : 'text-success'}`}>
              {report.prediction}
            </p>
          </div>
        </div>

        <div className="glass-card p-6 flex flex-col justify-center">
          <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-4 text-center">BERT Classification Probabilities</p>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1 text-xs">
                <span className="text-danger font-medium uppercase tracking-wider">Phishing</span>
                <span className="font-mono text-text-primary">{(report.phishing_probability * 100).toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full bg-background rounded-full overflow-hidden border border-border-subtle">
                <div 
                  className="h-full bg-danger shadow-[0_0_10px_rgba(248,113,113,0.8)]" 
                  style={{ width: `${report.phishing_probability * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1 text-xs">
                <span className="text-success font-medium uppercase tracking-wider">Legitimate</span>
                <span className="font-mono text-text-primary">{(report.legitimate_probability * 100).toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full bg-background rounded-full overflow-hidden border border-border-subtle">
                <div 
                  className="h-full bg-success shadow-[0_0_10px_rgba(52,211,153,0.8)]" 
                  style={{ width: `${report.legitimate_probability * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div className="glass-card p-6 flex flex-col items-center justify-center text-center group hover:-translate-y-1">
          <p className="text-xs font-bold text-text-muted uppercase tracking-widest mb-2">URLs Found</p>
          <div className="text-5xl font-mono font-bold text-primary mb-3 text-shadow-glow">
            {report.urls_found}
          </div>
        </div>
      </div>

      <div className="glass-card p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-32 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
        <h3 className="font-semibold text-lg mb-6 text-text-primary flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-primary" />
          Risk Assessment & Suspicious Indicators
        </h3>
        
        {report.risk_reasons && report.risk_reasons.length > 0 ? (
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            {report.risk_reasons.map((reason, i) => (
              <li key={i} className="flex items-start bg-background/50 p-4 rounded-xl border border-border-subtle group hover:border-primary/30 transition-colors">
                <div className="p-1.5 rounded-full bg-elevated border border-border-strong mr-3 shrink-0 group-hover:bg-primary/10 transition-colors">
                  <AlertCircle className={`w-4 h-4 ${reason.toLowerCase().includes('phishing') ? 'text-danger' : 'text-primary'}`} />
                </div>
                <span className="text-text-secondary text-sm leading-relaxed">{reason}</span>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-text-muted italic text-sm p-6 text-center bg-background/50 rounded-xl border border-border-subtle mt-4">
            No suspicious indicators detected.
          </div>
        )}
      </div>

      {report.url_indicators && report.url_indicators.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-sm font-bold text-text-muted uppercase tracking-wider mb-4 flex items-center">
            <LinkIcon className="w-4 h-4 mr-2" /> Extracted URLs
          </h3>
          <ul className="space-y-3">
            {report.url_indicators.map((indicator, i) => (
              <li key={i} className="flex flex-col p-3 bg-surface rounded-lg border border-border-subtle">
                <span className="text-sm text-text-primary break-all font-mono mb-1">{indicator}</span>
                <span className="text-xs text-danger font-bold uppercase tracking-wider">Risk: High</span>
              </li>
            ))}
          </ul>
          <div className="mt-4 p-3 bg-warning/10 border border-warning/20 rounded-lg flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-warning shrink-0" />
            <p className="text-xs text-warning">Security restriction: Extracted URLs are evaluated statically and cannot be visited or executed automatically.</p>
          </div>
        </div>
      )}

      {report.urls_found === 0 && (
        <div className="glass-card p-6 flex items-center justify-center text-text-muted italic text-sm">
          No URLs detected.
        </div>
      )}
    </div>
  );
}
