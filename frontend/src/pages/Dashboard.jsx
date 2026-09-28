import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Search, Activity, Lock, Database, Cpu, Target, AlertTriangle } from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total_emails_scanned: 0,
    phishing_detected: 0,
    legitimate_emails: 0,
    high_risk_emails: 0
  });
  const [recentAnalyses, setRecentAnalyses] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/api/analysis/stats', { withCredentials: true });
        setStats(res.data);
      } catch (err) {
        console.error("Failed to load stats", err);
      }
      try {
        const histRes = await api.get('/api/analysis/history', { withCredentials: true });
        setRecentAnalyses(histRes.data.slice(0, 5));
      } catch (err) {
        console.error("Failed to load history", err);
      }
    };
    if (user) fetchData();
  }, [user]);
  
  const metrics = [
    { label: 'Total Scanned', value: stats.total_emails_scanned, icon: Database, color: 'text-primary' },
    { label: 'Phishing', value: stats.phishing_detected, icon: AlertTriangle, color: 'text-danger' },
    { label: 'Legitimate', value: stats.legitimate_emails, icon: ShieldAlert, color: 'text-success' },
    { label: 'High Risk', value: stats.high_risk_emails, icon: Activity, color: 'text-warning' },
    { label: 'BERT Model', value: 'bert-base', icon: Cpu, color: 'text-text-muted' },
  ];

  return (
    <div className="h-full flex flex-col py-6 space-y-8 animate-in fade-in duration-500">
      
      {/* Header section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-3xl sm:text-4xl font-bold text-text-primary tracking-tight">
            Welcome back
          </h1>
          <p className="text-lg text-text-secondary mt-2">
            AI-powered email security overview
          </p>
        </div>
        <div className="flex gap-4">
          <Link 
            to="/analyze"
            className="btn-primary"
          >
            <Search className="w-5 h-5" />
            Analyze Email
          </Link>
        </div>
      </div>

      {/* Gmail Connection Banner */}
      {user && !user.has_gmail && (
        <div className="glass-card bg-primary/5 border-primary/20 p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 relative overflow-hidden group">
          <div className="flex items-start gap-4 z-10">
            <div className="p-3 bg-primary/10 rounded-xl shrink-0">
              <svg className="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22 6C22 4.9 21.1 4 20 4H4C2.9 4 2 4.9 2 6V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6ZM20 6L12 11L4 6H20ZM20 18H4V8L12 13L20 8V18Z"/>
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-bold text-text-primary mb-1">Connect your Gmail</h3>
              <p className="text-sm text-text-secondary max-w-2xl">
                Connect your Gmail account so PhishGuard AI can securely retrieve and analyze your emails for phishing threats.
              </p>
            </div>
          </div>
          <button 
            onClick={() => window.location.href = 'http://localhost:8000/auth/gmail/url'}
            className="btn-primary shrink-0 z-10"
          >
            Connect Gmail
          </button>
        </div>
      )}

      {/* Model Status Card */}
      <div className="glass-card bg-surface p-6 flex flex-col sm:flex-row items-start sm:items-center gap-6 relative overflow-hidden group border-border-subtle">
        <div className="p-3 bg-surface-hover rounded-xl shrink-0">
          <Cpu className="w-6 h-6 text-text-muted" />
        </div>
        <div className="flex-1 z-10">
          <h3 className="text-md font-bold text-text-primary mb-1">Model Information</h3>
          <p className="text-sm text-text-secondary">
            Current BERT evaluation status: Model evaluation in progress.
            Metrics are shown only after validated evaluation is completed.
          </p>
        </div>
      </div>
      
      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-7 gap-4 sm:gap-6">
        {metrics.map((m, i) => (
          <div key={i} className="glass-card p-5 group hover:-translate-y-1">
            <div className={`p-3 rounded-xl bg-surface border border-border-subtle inline-block mb-4 ${m.color}`}>
              <m.icon className="w-5 h-5" />
            </div>
            <p className="text-2xl font-mono font-bold text-text-primary">{m.value}</p>
            <p className="text-xs text-text-muted mt-1 font-medium">{m.label}</p>
          </div>
        ))}
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
        <div className="glass-card p-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-24 bg-primary/5 rounded-full blur-2xl -mr-12 -mt-12 transition-transform group-hover:scale-110"></div>
          <ShieldAlert className="w-8 h-8 text-primary mb-4 relative z-10" />
          <h3 className="font-semibold text-text-primary mb-2 text-lg relative z-10">BERT Classification</h3>
          <p className="text-sm text-text-secondary leading-relaxed relative z-10">Fine-tuned BERT model classifies email subject and body content using state-of-the-art NLP.</p>
        </div>
        <div className="glass-card p-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-24 bg-accent/5 rounded-full blur-2xl -mr-12 -mt-12 transition-transform group-hover:scale-110"></div>
          <Lock className="w-8 h-8 text-accent mb-4 relative z-10" />
          <h3 className="font-semibold text-text-primary mb-2 text-lg relative z-10">Static URL Analysis</h3>
          <p className="text-sm text-text-secondary leading-relaxed relative z-10">URLs are extracted and analyzed dynamically without ever executing or visiting them.</p>
        </div>
        <div className="glass-card p-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-24 bg-success/5 rounded-full blur-2xl -mr-12 -mt-12 transition-transform group-hover:scale-110"></div>
          <Activity className="w-8 h-8 text-success mb-4 relative z-10" />
          <h3 className="font-semibold text-text-primary mb-2 text-lg relative z-10">Risk Assessment</h3>
          <p className="text-sm text-text-secondary leading-relaxed relative z-10">Backend combines model output and URL indicators into a unified comprehensive risk level.</p>
        </div>
      </div>

      {/* Recent Analyses */}
      <div className="glass-card flex flex-col mt-8">
        <div className="p-6 border-b border-border-subtle">
          <h2 className="text-xl font-bold text-text-primary">Recent Analyses</h2>
        </div>
        {recentAnalyses.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-border-subtle bg-surface-hover">
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Email</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Result</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Risk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle">
                {recentAnalyses.map(analysis => (
                  <tr key={analysis.id} className="hover:bg-surface-hover/50 transition-colors">
                    <td className="p-4">
                      <p className="text-sm font-medium text-text-primary truncate max-w-xs">{analysis.subject}</p>
                    </td>
                    <td className="p-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${analysis.prediction === 'PHISHING' ? 'bg-danger/10 text-danger' : 'bg-success/10 text-success'}`}>
                        {analysis.prediction}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${analysis.risk_level === 'CRITICAL' || analysis.risk_level === 'HIGH' ? 'bg-warning/10 text-warning' : 'bg-success/10 text-success'}`}>
                        {analysis.risk_level}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center flex flex-col items-center">
            <p className="text-text-secondary mb-4">No analyses yet. Analyze your first email.</p>
            <Link to="/analyze" className="btn-primary text-sm">
              Analyze Your First Email
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
