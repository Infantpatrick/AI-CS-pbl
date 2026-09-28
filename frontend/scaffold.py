import os

base_dir = r"D:\AICS PROJECT\frontend\src"

files = {
    "api/client.js": """import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  try {
    const res = await api.get('/health', { timeout: 8000 });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false, error };
  }
};

export const getModelInfo = async () => {
  try {
    const res = await api.get('/model-info', { timeout: 8000 });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false, error };
  }
};

export const predict = async (subject, body, signal) => {
  try {
    const res = await api.post('/predict', { subject, body }, { signal, timeout: 60000 });
    return { success: true, data: res.data };
  } catch (error) {
    if (axios.isCancel(error)) {
      return { success: false, error: 'Analysis cancelled', cancelled: true };
    }
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Can\\'t reach the analysis service. Check that the backend is running and try again.' 
    };
  }
};
""",

    "api/normalizers.js": """export const normalizeRiskResponse = (data) => {
  return {
    prediction: (data.prediction || 'UNKNOWN').toUpperCase(),
    phishingProbability: typeof data.phishing_probability === 'number' ? data.phishing_probability : 0,
    legitimateProbability: typeof data.legitimate_probability === 'number' ? data.legitimate_probability : 0,
    confidence: typeof data.confidence === 'number' ? data.confidence : 0,
    riskLevel: (data.risk_level || 'UNKNOWN').toUpperCase(),
    urlsFound: typeof data.urls_found === 'number' ? data.urls_found : 0,
    urlIndicators: Array.isArray(data.url_indicators) ? data.url_indicators : [],
    riskReasons: Array.isArray(data.risk_reasons) ? data.risk_reasons : []
  };
};
""",

    "main.jsx": """import React from 'react';
import ReactDOM from 'react-dom/client';
import '@fontsource/inter';
import '@fontsource/jetbrains-mono';
import App from './app/App';
import './styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",
    
    "app/App.jsx": """import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppShell from '../components/layout/AppShell';
import Dashboard from '../pages/Dashboard';
import Analyze from '../pages/Analyze';
import Results from '../pages/Results';
import UrlAnalysis from '../pages/UrlAnalysis';
import HowItWorks from '../pages/HowItWorks';
import ModelPerformance from '../pages/ModelPerformance';
import About from '../pages/About';

function App() {
  const [analysisState, setAnalysisState] = useState({
    status: 'idle',
    result: null,
    error: null,
    submittedInput: null
  });

  return (
    <Router>
      <AppShell>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analyze" element={<Analyze analysisState={analysisState} setAnalysisState={setAnalysisState} />} />
          <Route path="/results" element={<Results analysisState={analysisState} setAnalysisState={setAnalysisState} />} />
          <Route path="/url-analysis" element={<UrlAnalysis analysisState={analysisState} />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/performance" element={<ModelPerformance />} />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </Router>
  );
}

export default App;
""",

    "components/layout/AppShell.jsx": """import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, LayoutDashboard, Search, FileText, Link as LinkIcon, Info, Activity, Menu, X } from 'lucide-react';
import ApiStatusPill from './ApiStatusPill';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/analyze', label: 'Analyze Email', icon: Search },
  { path: '/results', label: 'Results', icon: FileText },
  { path: '/url-analysis', label: 'URL Analysis', icon: LinkIcon },
  { path: '/how-it-works', label: 'How It Works', icon: Info },
  { path: '/performance', label: 'Model Performance', icon: Activity },
  { path: '/about', label: 'About', icon: Shield },
];

export default function AppShell({ children }) {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') setMobileMenuOpen(false);
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, []);

  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  return (
    <div className="flex h-screen bg-base text-text-primary overflow-hidden">
      <aside className="hidden lg:flex w-64 flex-col bg-surface border-r border-strong z-20">
        <div className="h-16 flex items-center px-6 border-b border-strong shrink-0">
          <Shield className="w-6 h-6 text-primary mr-2" />
          <span className="font-bold text-lg tracking-wide">PhishGuard AI</span>
        </div>
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-3">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center px-3 py-2 rounded-md transition-colors ${
                      isActive ? 'bg-primary/10 text-primary-strong' : 'text-text-secondary hover:bg-elevated hover:text-text-primary'
                    }`}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    <item.icon className="w-5 h-5 mr-3" />
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </aside>

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <header className="h-16 flex items-center justify-between px-4 sm:px-6 lg:px-8 bg-surface border-b border-strong shrink-0 z-10">
          <div className="flex items-center lg:hidden">
            <Shield className="w-6 h-6 text-primary mr-2" />
            <span className="font-bold text-lg">PhishGuard AI</span>
          </div>
          <div className="hidden lg:block">
            <h1 className="text-xl font-semibold capitalize">{navItems.find(i => i.path === location.pathname)?.label || 'PhishGuard AI'}</h1>
          </div>
          <div className="flex items-center space-x-4">
            <ApiStatusPill />
            <button 
              className="lg:hidden p-2 text-text-secondary hover:text-text-primary"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </header>
        
        <main className="flex-1 overflow-auto bg-base p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto h-full">
            {children}
          </div>
        </main>
      </div>

      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setMobileMenuOpen(false)}></div>
          <div className="fixed inset-y-0 left-0 w-64 bg-surface shadow-xl">
            <div className="h-16 flex items-center justify-between px-6 border-b border-strong">
              <span className="font-bold text-lg">Menu</span>
              <button onClick={() => setMobileMenuOpen(false)} className="p-2 -mr-2"><X className="w-5 h-5" /></button>
            </div>
            <nav className="p-4">
              <ul className="space-y-2">
                {navItems.map((item) => {
                  const isActive = location.pathname === item.path;
                  return (
                    <li key={item.path}>
                      <Link
                        to={item.path}
                        className={`flex items-center px-4 py-3 rounded-md ${
                          isActive ? 'bg-primary/10 text-primary-strong' : 'text-text-secondary'
                        }`}
                      >
                        <item.icon className="w-5 h-5 mr-3" />
                        {item.label}
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </nav>
          </div>
        </div>
      )}
    </div>
  );
}
""",

    "components/layout/ApiStatusPill.jsx": """import React, { useState, useEffect } from 'react';
import { Activity, CheckCircle2, AlertCircle } from 'lucide-react';
import { getHealth } from '../../api/client';

export default function ApiStatusPill() {
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    let mounted = true;
    const check = async () => {
      const res = await getHealth();
      if (mounted) {
        setStatus(res.success ? 'connected' : 'unreachable');
      }
    };
    check();
    const interval = setInterval(() => {
      if (document.visibilityState === 'visible') {
        check();
      }
    }, 30000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className={`flex items-center px-3 py-1 rounded-full text-xs font-mono font-medium border
      ${status === 'checking' ? 'border-strong text-text-muted bg-elevated' : ''}
      ${status === 'connected' ? 'border-success/30 text-success bg-success/10' : ''}
      ${status === 'unreachable' ? 'border-danger/30 text-danger bg-danger/10' : ''}
    `}>
      {status === 'checking' && <Activity className="w-3 h-3 mr-2 animate-pulse" />}
      {status === 'connected' && <CheckCircle2 className="w-3 h-3 mr-2" />}
      {status === 'unreachable' && <AlertCircle className="w-3 h-3 mr-2" />}
      API {status === 'checking' ? 'Checking...' : status === 'connected' ? 'Connected' : 'Unreachable'}
    </div>
  );
}
""",

    "pages/Dashboard.jsx": """import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Search, Activity, Lock } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="h-full flex flex-col justify-center py-10">
      <div className="max-w-4xl mx-auto text-center space-y-8">
        <div className="inline-flex items-center justify-center px-3 py-1 rounded-full border border-primary/30 bg-primary/10 text-primary text-xs font-bold tracking-widest uppercase mb-4">
          <Activity className="w-4 h-4 mr-2" />
          AI + CYBERSECURITY + NLP
        </div>
        
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-text-primary tracking-tight leading-tight">
          AI-Powered Email <br className="hidden sm:block" /> Phishing Detection
        </h1>
        
        <p className="text-lg sm:text-xl text-text-secondary max-w-2xl mx-auto">
          Detect suspicious emails using BERT-based NLP and static URL analysis.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
          <Link 
            to="/analyze"
            className="flex items-center justify-center px-8 py-3 bg-primary text-white text-base font-semibold rounded-md hover:bg-primary-strong transition-colors w-full sm:w-auto"
          >
            <Search className="w-5 h-5 mr-2" />
            Analyze Email
          </Link>
          <Link 
            to="/how-it-works"
            className="flex items-center justify-center px-8 py-3 bg-elevated border border-strong text-text-primary text-base font-semibold rounded-md hover:bg-strong transition-colors w-full sm:w-auto"
          >
            How It Works
          </Link>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-16">
          <div className="p-6 bg-surface border border-subtle rounded-xl text-left shadow-lg">
            <ShieldAlert className="w-8 h-8 text-primary mb-4" />
            <h3 className="font-semibold text-text-primary mb-2 text-lg">BERT Classification</h3>
            <p className="text-sm text-text-secondary leading-relaxed">Fine-tuned BERT model classifies email subject and body content.</p>
          </div>
          <div className="p-6 bg-surface border border-subtle rounded-xl text-left shadow-lg">
            <Lock className="w-8 h-8 text-accent mb-4" />
            <h3 className="font-semibold text-text-primary mb-2 text-lg">Static URL Analysis</h3>
            <p className="text-sm text-text-secondary leading-relaxed">URLs are extracted and analyzed without being visited or executed.</p>
          </div>
          <div className="p-6 bg-surface border border-subtle rounded-xl text-left shadow-lg">
            <Activity className="w-8 h-8 text-success mb-4" />
            <h3 className="font-semibold text-text-primary mb-2 text-lg">Risk Assessment</h3>
            <p className="text-sm text-text-secondary leading-relaxed">Backend combines model output and URL indicators into a unified risk level.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
""",

    "pages/Analyze.jsx": """import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { predict } from '../api/client';
import { normalizeRiskResponse } from '../api/normalizers';
import { AlertCircle, FileSearch, Send, Trash2 } from 'lucide-react';

export default function Analyze({ analysisState, setAnalysisState }) {
  const [subject, setSubject] = useState(analysisState.submittedInput?.subject || '');
  const [body, setBody] = useState(analysisState.submittedInput?.body || '');
  const navigate = useNavigate();

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!subject.trim() && !body.trim()) return;

    setAnalysisState({
      status: 'loading',
      result: null,
      error: null,
      submittedInput: { subject, body }
    });

    const abortController = new AbortController();
    const res = await predict(subject, body, abortController.signal);
    
    if (res.success) {
      setAnalysisState({
        status: 'success',
        result: normalizeRiskResponse(res.data),
        error: null,
        submittedInput: { subject, body }
      });
      navigate('/results');
    } else {
      setAnalysisState({
        status: 'error',
        result: null,
        error: res.error,
        submittedInput: { subject, body }
      });
    }
  };

  const handleClear = () => {
    setSubject('');
    setBody('');
    setAnalysisState({ status: 'idle', result: null, error: null, submittedInput: null });
  };

  const handleExample = () => {
    setSubject('Urgent: Your account has been suspended');
    setBody('Dear customer, please click the link below to verify your identity within 24 hours or your account will be permanently closed.\\n\\nhttp://verify-account-security-update.com');
  };

  return (
    <div className="grid lg:grid-cols-2 gap-8 h-full">
      <div className="flex flex-col">
        <div className="flex justify-between items-end mb-4">
          <h2 className="text-xl font-bold">Email Input</h2>
          <button onClick={handleExample} type="button" className="text-xs text-primary hover:underline">Use example input</button>
        </div>
        
        <form onSubmit={handleAnalyze} className="flex-1 flex flex-col space-y-4">
          <div className="flex flex-col space-y-1">
            <label htmlFor="subject" className="text-sm font-medium text-text-secondary">Subject</label>
            <input
              id="subject"
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              disabled={analysisState.status === 'loading'}
              className="bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary font-mono text-sm"
              placeholder="Email subject..."
            />
            <div className="text-right text-xs text-text-muted" aria-live="polite">
              {subject.length} chars
            </div>
          </div>

          <div className="flex flex-col space-y-1 flex-1">
            <label htmlFor="body" className="text-sm font-medium text-text-secondary">Body</label>
            <textarea
              id="body"
              value={body}
              onChange={(e) => setBody(e.target.value)}
              disabled={analysisState.status === 'loading'}
              className="bg-elevated border border-strong rounded-md px-4 py-3 text-text-primary focus:outline-none focus:border-primary font-mono text-sm flex-1 min-h-[240px] resize-y"
              placeholder="Paste email content here..."
            />
            <div className="text-right text-xs text-text-muted" aria-live="polite">
              {body.length} chars | {body.trim() ? body.trim().split(/\\s+/).length : 0} words
            </div>
          </div>

          {analysisState.status === 'error' && (
            <div className="bg-danger/10 border border-danger/20 text-danger p-4 rounded-md flex items-start">
              <AlertCircle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
              <span className="text-sm">{analysisState.error}</span>
            </div>
          )}

          <div className="flex space-x-4 pt-4">
            <button
              type="submit"
              disabled={analysisState.status === 'loading' || (!subject.trim() && !body.trim())}
              className="flex-1 flex items-center justify-center px-6 py-3 bg-primary text-white text-base font-semibold rounded-md hover:bg-primary-strong transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {analysisState.status === 'loading' ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5 mr-2" />
                  Analyze Email
                </>
              )}
            </button>
            <button
              type="button"
              onClick={handleClear}
              disabled={analysisState.status === 'loading'}
              className="px-6 py-3 bg-elevated border border-strong text-text-primary text-base font-semibold rounded-md hover:bg-strong transition-colors disabled:opacity-50"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>

      <div className="hidden lg:flex flex-col p-8 bg-elevated border border-strong rounded-xl items-center justify-center text-center">
        <FileSearch className="w-16 h-16 text-primary/40 mb-6" />
        <h3 className="text-xl font-bold mb-4 text-text-primary">How your email is handled</h3>
        <ul className="space-y-4 text-sm text-text-secondary max-w-sm text-left">
          <li className="flex items-start">
            <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 mr-3 shrink-0"></span>
            Analyzed using an AI model fine-tuned for phishing detection.
          </li>
          <li className="flex items-start">
            <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 mr-3 shrink-0"></span>
            URLs are extracted and evaluated statically without visiting them.
          </li>
          <li className="flex items-start">
            <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 mr-3 shrink-0"></span>
            Data is strictly processed in memory and never persisted or shared.
          </li>
        </ul>
      </div>
    </div>
  );
}
""",

    "pages/Results.jsx": """import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShieldAlert, ShieldCheck, AlertTriangle, HelpCircle, Activity, Link as LinkIcon, AlertCircle } from 'lucide-react';

export default function Results({ analysisState, setAnalysisState }) {
  const navigate = useNavigate();

  if (analysisState.status !== 'success' || !analysisState.result) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center p-8">
        <Activity className="w-16 h-16 text-text-muted mb-6" />
        <h2 className="text-2xl font-bold mb-2">No analysis yet</h2>
        <p className="text-text-secondary mb-8">Submit an email to view the risk assessment results.</p>
        <button
          onClick={() => navigate('/analyze')}
          className="px-6 py-2 bg-primary text-white rounded-md font-semibold hover:bg-primary-strong"
        >
          Analyze Email
        </button>
      </div>
    );
  }

  const { result } = analysisState;
  const isPhishing = result.prediction === 'PHISHING';
  const riskColor = result.riskLevel === 'HIGH' ? 'text-danger' : result.riskLevel === 'MEDIUM' ? 'text-warning' : 'text-success';

  return (
    <div className="space-y-8 pb-12">
      <div className={`p-6 rounded-xl border flex items-center shadow-lg ${
        isPhishing ? 'bg-danger/10 border-danger/30 text-danger' : 'bg-success/10 border-success/30 text-success'
      }`}>
        {isPhishing ? <ShieldAlert className="w-12 h-12 mr-6 shrink-0" /> : <ShieldCheck className="w-12 h-12 mr-6 shrink-0" />}
        <div>
          <h2 className="text-2xl font-bold tracking-tight">
            {isPhishing ? 'PHISHING DETECTED' : 'LEGITIMATE'}
          </h2>
          <p className="opacity-90 mt-1">Based on BERT classification and static analysis.</p>
        </div>
      </div>

      <div className="bg-elevated border border-strong rounded-xl p-4 flex items-start space-x-3">
        <AlertCircle className="w-5 h-5 text-warning shrink-0 mt-0.5" />
        <div className="text-sm">
          <span className="font-semibold text-text-primary">Limitation:</span> This is a model prediction, not a verdict. On the held-out test set the model produced a 62.98% false-positive rate, so legitimate emails can be flagged. <Link to="/performance" className="text-primary hover:underline ml-1">View Model Performance</Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-surface border border-subtle rounded-xl p-6 flex flex-col items-center justify-center text-center">
          <p className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Assessed Risk</p>
          <div className={`flex items-center text-3xl font-bold ${riskColor}`}>
            {result.riskLevel === 'HIGH' && <AlertTriangle className="w-8 h-8 mr-3" />}
            {result.riskLevel === 'MEDIUM' && <AlertTriangle className="w-8 h-8 mr-3" />}
            {result.riskLevel === 'LOW' && <ShieldCheck className="w-8 h-8 mr-3" />}
            {result.riskLevel === 'UNKNOWN' && <HelpCircle className="w-8 h-8 mr-3" />}
            {result.riskLevel}
          </div>
        </div>

        <div className="bg-surface border border-subtle rounded-xl p-6 flex flex-col items-center justify-center text-center">
          <p className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Model Confidence</p>
          <div className="text-4xl font-mono font-bold text-text-primary">
            {(result.confidence * 100).toFixed(1)}%
          </div>
        </div>

        <div className="bg-surface border border-subtle rounded-xl p-6 flex flex-col items-center justify-center text-center">
          <p className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">URLs Found</p>
          <div className="text-4xl font-mono font-bold text-text-primary mb-2">
            {result.urlsFound}
          </div>
          {result.urlsFound > 0 && (
            <Link to="/url-analysis" className="text-sm text-primary flex items-center hover:underline">
              <LinkIcon className="w-4 h-4 mr-1" /> View URL Analysis
            </Link>
          )}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-surface border border-subtle rounded-xl p-6">
          <h3 className="font-semibold text-lg mb-6 text-text-primary">Probability Breakdown</h3>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2 text-sm">
                <span className="text-danger font-medium">Phishing Probability</span>
                <span className="font-mono text-text-primary">{(result.phishingProbability * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 w-full bg-elevated rounded-full overflow-hidden">
                <div 
                  className="h-full bg-danger transition-all duration-700 ease-out" 
                  style={{ width: `${result.phishingProbability * 100}%` }}
                  role="progressbar" 
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2 text-sm">
                <span className="text-success font-medium">Legitimate Probability</span>
                <span className="font-mono text-text-primary">{(result.legitimateProbability * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 w-full bg-elevated rounded-full overflow-hidden">
                <div 
                  className="h-full bg-success transition-all duration-700 ease-out" 
                  style={{ width: `${result.legitimateProbability * 100}%` }}
                  role="progressbar" 
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-surface border border-subtle rounded-xl p-6">
          <h3 className="font-semibold text-lg mb-4 text-text-primary">Risk Reasons</h3>
          {result.riskReasons.length > 0 ? (
            <ul className="space-y-3">
              {result.riskReasons.map((reason, i) => (
                <li key={i} className="flex items-start bg-elevated p-3 rounded-md border border-strong text-sm">
                  <AlertCircle className="w-4 h-4 text-warning mr-3 shrink-0 mt-0.5" />
                  <span className="text-text-primary">{reason}</span>
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-text-muted italic text-sm p-4 bg-elevated rounded-md">No specific risk reasons returned.</div>
          )}
        </div>
      </div>

      <div className="flex justify-end space-x-4">
        <button
          onClick={() => {
            setAnalysisState({ status: 'idle', result: null, error: null, submittedInput: null });
            navigate('/analyze');
          }}
          className="px-6 py-2 bg-elevated border border-strong text-text-primary font-semibold rounded-md hover:bg-strong"
        >
          New Analysis
        </button>
        <button
          onClick={() => {
            setAnalysisState(prev => ({ ...prev, status: 'idle', result: null, error: null }));
            navigate('/analyze');
          }}
          className="px-6 py-2 bg-primary text-white font-semibold rounded-md hover:bg-primary-strong"
        >
          Edit & Re-analyze
        </button>
      </div>
    </div>
  );
}
""",

    "pages/UrlAnalysis.jsx": """import React from 'react';
import { Shield, Link as LinkIcon, Info } from 'lucide-react';

export default function UrlAnalysis({ analysisState }) {
  if (analysisState.status !== 'success' || !analysisState.result) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center">
        <LinkIcon className="w-12 h-12 text-text-muted mb-4" />
        <h2 className="text-xl font-bold mb-2">No URLs to analyze</h2>
        <p className="text-text-secondary">Analyze an email to view URL details.</p>
      </div>
    );
  }

  const { result } = analysisState;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">URL Analysis</h2>
        <div className="bg-elevated px-4 py-2 rounded-full border border-strong font-mono text-sm">
          URLs found: <span className="text-primary font-bold">{result.urlsFound}</span>
        </div>
      </div>

      <div className="bg-surface border border-subtle p-4 rounded-xl flex items-start space-x-3">
        <Shield className="w-5 h-5 text-accent shrink-0 mt-0.5" />
        <div className="text-sm text-text-secondary">
          <span className="font-semibold text-text-primary block mb-1">Static analysis only.</span>
          URLs are never visited, downloaded or executed. Indicators are signals, not confirmed threats.
        </div>
      </div>

      {result.urlsFound === 0 ? (
        <div className="bg-elevated border border-strong rounded-xl p-8 text-center text-text-muted">
          No URLs found in the analyzed email.
        </div>
      ) : (
        <div className="bg-surface border border-subtle rounded-xl overflow-hidden">
          <div className="p-4 border-b border-strong bg-elevated/50 font-semibold flex items-center text-text-primary">
            <Info className="w-4 h-4 mr-2 text-text-secondary" />
            Detected Indicators
          </div>
          <div className="p-4">
            {result.urlIndicators && result.urlIndicators.length > 0 ? (
              <ul className="space-y-3">
                {result.urlIndicators.map((indicator, idx) => (
                  <li key={idx} className="font-mono text-sm bg-elevated border border-strong p-3 rounded-md break-all text-text-primary">
                    {indicator}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-text-muted italic">No specific indicators returned by the backend.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
""",

    "pages/HowItWorks.jsx": """import React from 'react';
import { FileText, Cpu, Activity, ShieldAlert, BarChart } from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      icon: FileText,
      title: 'Email Input',
      desc: 'Raw email subject and body are provided.',
      detail: 'The frontend safely transmits the text payload to the FastAPI backend without executing any contained content.'
    },
    {
      icon: Cpu,
      title: 'BERT Tokenization & Encoding',
      desc: 'Text is tokenized using the bert-base-uncased tokenizer.',
      detail: 'The email is processed through the fine-tuned BERT encoder layers to extract dense representations.'
    },
    {
      icon: Activity,
      title: 'Classification',
      desc: 'Classification head produces logits and probabilities.',
      detail: 'Inference is run using model.eval() and torch.no_grad(). The output is mapped to Phishing or Legitimate.'
    },
    {
      icon: BarChart,
      title: 'Static URL Analysis',
      desc: 'URLs are extracted and evaluated statically.',
      detail: 'The backend extracts URLs and checks length, IP-based domains, excessive subdomains, and other static indicators without ever visiting the links.'
    },
    {
      icon: ShieldAlert,
      title: 'Risk Assessment & Final Result',
      desc: 'Combined model output and URL signals determine risk.',
      detail: 'The system computes a final risk level (LOW, MEDIUM, HIGH) and returns JSON for the frontend to display.'
    }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4">How It Works</h2>
        <p className="text-text-secondary">PhishGuard AI employs a multi-stage pipeline combining modern NLP with static heuristics to assess email risk.</p>
      </div>

      <div className="space-y-6">
        {steps.map((step, idx) => (
          <div key={idx} className="bg-surface border border-subtle p-6 rounded-xl relative overflow-hidden">
            <div className="flex items-start">
              <div className="w-12 h-12 bg-elevated border border-strong rounded-lg flex items-center justify-center shrink-0 mr-6 z-10">
                <step.icon className="w-6 h-6 text-primary" />
              </div>
              <div className="flex-1 z-10">
                <h3 className="text-lg font-bold text-text-primary mb-1">
                  <span className="text-primary-strong mr-2">{idx + 1}.</span> {step.title}
                </h3>
                <p className="text-text-secondary mb-3">{step.desc}</p>
                <div className="bg-base p-4 rounded-md border border-strong">
                  <p className="text-sm font-mono text-text-muted">{step.detail}</p>
                </div>
              </div>
            </div>
            {idx < steps.length - 1 && (
              <div className="absolute left-[44px] top-[72px] bottom-[-24px] w-0.5 bg-strong z-0 hidden sm:block"></div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
""",

    "pages/ModelPerformance.jsx": """import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function ModelPerformance() {
  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-12">
      <div>
        <h2 className="text-3xl font-bold mb-2">Model Performance</h2>
        <p className="text-text-secondary">Documented offline evaluation results on the held-out test set.</p>
      </div>

      <div className="bg-warning/10 border border-warning/30 p-6 rounded-xl flex items-start space-x-4">
        <AlertCircle className="w-6 h-6 text-warning shrink-0 mt-0.5" />
        <div>
          <h3 className="font-bold text-warning mb-1">Known limitation</h3>
          <p className="text-sm text-warning/90">
            The model achieves high phishing recall but has a relatively high false-positive rate, meaning some legitimate emails may be incorrectly flagged.<br/><br/>
            It misses few phishing emails (112 of 4,443) but flags many legitimate emails (2,737 of 4,346).
          </p>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: 'Accuracy', value: '67.58%' },
          { label: 'Precision', value: '61.28%' },
          { label: 'Recall', value: '97.48%', highlight: true },
          { label: 'F1 Score', value: '75.25%' },
          { label: 'Test samples', value: '8,789' }
        ].map((m, i) => (
          <div key={i} className="bg-surface border border-subtle p-4 rounded-xl text-center">
            <p className="text-xs font-semibold text-text-secondary uppercase mb-1">{m.label}</p>
            <p className={`text-2xl font-mono font-bold ${m.highlight ? 'text-primary' : 'text-text-primary'}`}>{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-surface border border-subtle p-6 rounded-xl">
          <h3 className="font-bold text-lg mb-6">Confusion Matrix</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-success/10 border border-success/30 p-4 rounded-lg text-center">
              <div className="text-xs text-success mb-1">True Negative (Legitimate)</div>
              <div className="text-xl font-mono font-bold text-success">1,609</div>
            </div>
            <div className="bg-danger/10 border border-danger/30 p-4 rounded-lg text-center">
              <div className="text-xs text-danger mb-1">False Positive (Flagged Legitimate)</div>
              <div className="text-xl font-mono font-bold text-danger">2,737</div>
            </div>
            <div className="bg-warning/10 border border-warning/30 p-4 rounded-lg text-center">
              <div className="text-xs text-warning mb-1">False Negative (Missed Phishing)</div>
              <div className="text-xl font-mono font-bold text-warning">112</div>
            </div>
            <div className="bg-danger/10 border border-danger/30 p-4 rounded-lg text-center">
              <div className="text-xs text-danger mb-1">True Positive (Caught Phishing)</div>
              <div className="text-xl font-mono font-bold text-danger">4,331</div>
            </div>
          </div>
          <div className="mt-6 space-y-2 text-sm font-mono text-text-muted">
            <div className="flex justify-between"><span className="text-text-secondary">False Positive Rate:</span> <span>62.98%</span></div>
            <div className="flex justify-between"><span className="text-text-secondary">False Negative Rate:</span> <span>2.52%</span></div>
          </div>
        </div>

        <div className="bg-surface border border-subtle p-6 rounded-xl">
          <h3 className="font-bold text-lg mb-6">Dataset Breakdown</h3>
          <table className="w-full text-sm text-left">
            <tbody className="divide-y divide-strong font-mono">
              {[
                { label: 'Raw Emails', value: '101,136' },
                { label: 'Duplicates removed', value: '13,250' },
                { label: 'Final Dataset', value: '87,886', highlight: true },
                { label: 'Legitimate', value: '43,459' },
                { label: 'Phishing', value: '44,427' },
                { label: 'Training Set', value: '70,308' },
                { label: 'Validation Set', value: '8,789' },
                { label: 'Test Set', value: '8,789' },
              ].map((row, i) => (
                <tr key={i}>
                  <td className={`py-2 ${row.highlight ? 'text-primary font-bold' : 'text-text-secondary'}`}>{row.label}</td>
                  <td className={`py-2 text-right ${row.highlight ? 'text-primary font-bold' : 'text-text-primary'}`}>{row.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-4 pt-4 border-t border-strong text-xs text-text-muted space-y-1">
            <p>Sources: CEAS (38,963), Enron (29,423), Other/Phishing_Email.csv (6,134), SpamAssassin (5,672), Nigerian Fraud (3,284), Ling-Spam (2,859), Nazario (1,551)</p>
          </div>
        </div>
      </div>
    </div>
  );
}
""",

    "pages/About.jsx": """import React from 'react';
import { Shield } from 'lucide-react';

export default function About() {
  return (
    <div className="max-w-3xl mx-auto space-y-10 pb-12">
      <div className="text-center border-b border-strong pb-10">
        <Shield className="w-16 h-16 text-primary mx-auto mb-6" />
        <h2 className="text-3xl font-bold mb-4">About PhishGuard AI</h2>
        <p className="text-text-secondary text-lg">AI-Based Email Phishing Detection</p>
      </div>

      <section className="space-y-4">
        <h3 className="text-xl font-bold text-primary">Purpose & Solution</h3>
        <p className="text-text-secondary leading-relaxed">
          This project was developed to detect sophisticated email phishing attempts. It uses a fine-tuned BERT model (bert-base-uncased) to perform NLP analysis on email subject and body text, complemented by static URL analysis for a comprehensive risk assessment.
        </p>
      </section>

      <section className="space-y-4">
        <h3 className="text-xl font-bold text-primary">Technology Stack</h3>
        <div className="flex flex-wrap gap-2">
          {['Python', 'BERT', 'NLP', 'PyTorch', 'Hugging Face Transformers', 'Pandas', 'NumPy', 'Scikit-learn', 'FastAPI', 'React', 'Vite', 'Tailwind CSS'].map(tech => (
            <span key={tech} className="px-3 py-1 bg-elevated border border-strong rounded-full text-sm font-mono text-text-primary">
              {tech}
            </span>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h3 className="text-xl font-bold text-primary">Security Considerations</h3>
        <ul className="list-disc pl-5 space-y-2 text-text-secondary text-sm">
          <li><strong>Static Analysis Only:</strong> URLs are evaluated statically and are never visited, fetched, or executed by the backend.</li>
          <li><strong>In-Memory Processing:</strong> The frontend does not store or persist email content (no localStorage, cookies, etc.).</li>
          <li><strong>No Client Secrets:</strong> All complex analysis runs securely on the backend. The frontend only displays returned information.</li>
        </ul>
      </section>

      <section className="space-y-4 bg-surface p-6 rounded-xl border border-subtle">
        <h3 className="text-xl font-bold text-text-muted">Possible future work (not implemented)</h3>
        <ul className="list-disc pl-5 space-y-2 text-text-muted text-sm">
          <li>Threshold tuning and calibration for false positive reduction</li>
          <li>Integration of additional datasets for better generalization</li>
          <li>Richer URL reputation via external threat feeds</li>
          <li>Detailed email header (DKIM/SPF) analysis</li>
        </ul>
      </section>
    </div>
  );
}
""",

    "styles/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --bg-base: #070B14;
    --bg-surface: #0D1424;
    --bg-elevated: #141D33;
    
    --border-subtle: rgba(148, 163, 184, 0.14);
    --border-strong: rgba(148, 163, 184, 0.28);
    
    --primary: #38BDF8;
    --primary-strong: #0EA5E9;
    --accent: #818CF8;
    
    --success: #34D399;
    --warning: #FBBF24;
    --danger: #F87171;
    
    --text-primary: #E8EDF7;
    --text-secondary: #A3AFC5;
    --text-muted: #7F8BA3;
  }

  body {
    background-color: var(--bg-base);
    color: var(--text-primary);
    color-scheme: dark;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }
}

@layer utilities {
  .bg-base { background-color: var(--bg-base); }
  .bg-surface { background-color: var(--bg-surface); }
  .bg-elevated { background-color: var(--bg-elevated); }
  
  .border-subtle { border-color: var(--border-subtle); }
  .border-strong { border-color: var(--border-strong); }
  
  .text-primary { color: var(--primary); }
  .text-primary-strong { color: var(--primary-strong); }
  .text-accent { color: var(--accent); }
  .text-success { color: var(--success); }
  .text-warning { color: var(--warning); }
  .text-danger { color: var(--danger); }
  
  .text-text-primary { color: var(--text-primary); }
  .text-text-secondary { color: var(--text-secondary); }
  .text-text-muted { color: var(--text-muted); }
  
  .bg-primary { background-color: var(--primary); }
  .bg-primary-strong { background-color: var(--primary-strong); }
  .bg-success { background-color: var(--success); }
  .bg-danger { background-color: var(--danger); }
  .bg-warning { background-color: var(--warning); }
  
  .font-mono {
    font-family: 'JetBrains Mono', monospace;
  }
}
"""
}

def scaffold():
    # Remove old files optionally, but let's just create new ones, and we'll fix tailwind later.
    for rel_path, content in files.items():
        full_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Created: {full_path}")

if __name__ == "__main__":
    scaffold()
