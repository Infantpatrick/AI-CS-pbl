import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { predict, api } from '../api/client';
import { normalizeRiskResponse } from '../api/normalizers';
import { AlertCircle, FileSearch, Send, Trash2, Cpu, ScanSearch, CheckCircle2, Loader } from 'lucide-react';
import Results from './Results';

export default function Analyze({ analysisState, setAnalysisState }) {
  const location = useLocation();
  const initialEmailData = location.state?.emailData || null;

  const [subject, setSubject] = useState(initialEmailData?.subject || analysisState.submittedInput?.subject || '');
  const [sender, setSender] = useState(initialEmailData?.sender || analysisState.submittedInput?.sender || '');
  const [body, setBody] = useState(initialEmailData?.body || analysisState.submittedInput?.body || '');
  const [messageId, setMessageId] = useState(initialEmailData?.messageId || null);
  
  const [analysisStep, setAnalysisStep] = useState(0);

  const abortControllerRef = React.useRef(null);
  const navigate = useNavigate();

  // If navigated here with new state, reset the analysis context
  useEffect(() => {
    if (initialEmailData && analysisState.status !== 'idle') {
      setAnalysisState({ status: 'idle', result: null, error: null, submittedInput: null });
    }
  }, [initialEmailData]);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!subject.trim() && !body.trim()) return;

    setAnalysisState({
      status: 'loading',
      result: null,
      error: null,
      submittedInput: { subject, sender, body, messageId }
    });
    setAnalysisStep(0);

    const abortController = new AbortController();
    abortControllerRef.current = abortController;
    
    try {
      const predictionPromise = predict(subject, body, abortController.signal);
      
      // Step 1: Content received
      setAnalysisStep(1);
      await new Promise(r => setTimeout(r, 600));
      
      // Step 2: Preprocessing
      setAnalysisStep(2);
      await new Promise(r => setTimeout(r, 800));
      
      // Step 3: BERT
      setAnalysisStep(3);

      const res = await predictionPromise;

      if (!res.success && !res.cancelled) {
        throw new Error(res.error);
      }
      
      if (res.cancelled) {
        setAnalysisState({ status: 'idle', result: null, error: null, submittedInput: null });
        return;
      }
      
      // Step 4: URL Analysis
      setAnalysisStep(4);
      await new Promise(r => setTimeout(r, 400));
      
      // Step 5: Risk Assessment
      setAnalysisStep(5);
      await new Promise(r => setTimeout(r, 300));

      // Save to history
      const saveRes = await api.post('/api/analysis', {
        message_id: messageId || ('manual-' + Date.now().toString()),
        subject: subject || '(No Subject)',
        sender: sender || 'Unknown Sender',
        prediction: res.data.prediction,
        phishing_probability: res.data.phishing_probability,
        legitimate_probability: res.data.legitimate_probability,
        confidence: res.data.confidence,
        risk_level: res.data.risk_level,
        urls_found: res.data.urls_found,
        url_indicators: res.data.url_indicators || [],
        risk_reasons: res.data.risk_reasons || [],
        body: body
      });

      setAnalysisState({
        status: 'success',
        result: {
          ...normalizeRiskResponse(res.data),
          reportId: saveRes.data.id
        },
        error: null,
        submittedInput: { subject, sender, body, messageId }
      });
    } catch (err) {
      setAnalysisState({
        status: 'error',
        result: null,
        error: err.message || "Failed to save or process report.",
        submittedInput: { subject, sender, body, messageId }
      });
    }
  };


  const handleClear = () => {
    setSubject('');
    setSender('');
    setBody('');
    setAnalysisState({ status: 'idle', result: null, error: null, submittedInput: null });
  };

  const handleExample = () => {
    setSubject('Urgent: Your account has been suspended');
    setSender('security@paypal-update-alert.com');
    setBody('Dear customer, please click the link below to verify your identity within 24 hours or your account will be permanently closed.\n\nhttp://verify-account-security-update.com');
  };

  if (analysisState.status === 'success') {
    return <Results analysisState={analysisState} setAnalysisState={setAnalysisState} />;
  }

  return (
    <div className="h-full max-w-6xl mx-auto flex flex-col pt-4 pb-12 animate-in fade-in duration-500">

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-text-primary tracking-tight">Analyze Email</h1>
        <p className="text-text-secondary mt-2">Paste your email content below to detect potential phishing threats.</p>
      </div>

      <div className="grid lg:grid-cols-5 gap-8 flex-1">

        {/* Main Input Form */}
        <div className="lg:col-span-3 flex flex-col">
          <form onSubmit={handleAnalyze} className="glass-card p-6 flex-1 flex flex-col space-y-6 relative overflow-hidden">

            {/* Scanner Overlay during loading */}
            {analysisState.status === 'loading' && (
              <div className="absolute inset-0 bg-background/95 backdrop-blur-md z-20 flex flex-col items-center justify-center rounded-2xl animate-in fade-in duration-300">
                <div className="absolute top-0 left-0 w-full h-1 bg-surface">
                  <div 
                    className="h-full bg-primary transition-all duration-300" 
                    style={{ width: `${(analysisStep / 5) * 100}%` }}
                  ></div>
                </div>
                
                <div className="flex flex-col items-center mb-8">
                  <div className="w-16 h-16 rounded-full bg-primary/10 border-2 border-primary/30 flex items-center justify-center mb-4 relative">
                    <Cpu className="w-8 h-8 text-primary animate-pulse" />
                    <div className="absolute inset-0 border-2 border-primary rounded-full animate-ping opacity-20"></div>
                  </div>
                  <h2 className="text-xl font-bold text-text-primary tracking-wide">ANALYZING EMAIL</h2>
                  <p className="text-sm text-text-muted mt-2 font-mono">PhishGuard AI Engine</p>
                </div>

                <div className="space-y-4 max-w-sm w-full px-8">
                  {[
                    { id: 1, text: "Email received" },
                    { id: 2, text: "Text preprocessing" },
                    { id: 3, text: "BERT analysis" },
                    { id: 4, text: "URL analysis" },
                    { id: 5, text: "Risk assessment" }
                  ].map(step => {
                    const status = analysisStep > step.id ? 'complete' : analysisStep === step.id ? 'active' : 'pending';
                    return (
                      <div key={step.id} className="flex items-center gap-3">
                        <div className="w-6 h-6 shrink-0 flex items-center justify-center font-mono">
                          {status === 'complete' && <span className="text-success text-lg">✓</span>}
                          {status === 'active' && <Loader className="w-4 h-4 text-primary animate-spin" />}
                          {status === 'pending' && <span className="text-text-muted text-lg">○</span>}
                        </div>
                        <span className={`font-mono text-sm transition-colors duration-300 ${
                          status === 'complete' ? 'text-text-secondary' : 
                          status === 'active' ? 'text-primary font-bold' : 
                          'text-text-muted opacity-50'
                        }`}>
                          {step.text}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            <div className="flex justify-between items-end">
              <h2 className="text-lg font-bold flex items-center text-text-primary">
                <FileSearch className="w-5 h-5 mr-2 text-primary" />
                Email Content
              </h2>
              <button onClick={handleExample} type="button" className="text-xs text-primary hover:text-primary-strong transition-colors underline-offset-4 hover:underline">
                Load Example
              </button>
            </div>

            <div className="flex flex-col space-y-2">
              <label htmlFor="subject" className="text-xs font-bold text-text-muted uppercase tracking-wider">Email Subject</label>
              <input
                id="subject"
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                disabled={analysisState.status === 'loading'}
                className="glass-input"
                placeholder="[ Enter email subject ]"
              />
            </div>

            <div className="flex flex-col space-y-2">
              <label htmlFor="sender" className="text-xs font-bold text-text-muted uppercase tracking-wider">Sender</label>
              <input
                id="sender"
                type="text"
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                disabled={analysisState.status === 'loading'}
                className="glass-input"
                placeholder="[ Enter sender email or name ]"
              />
            </div>

            <div className="flex flex-col space-y-2 flex-1">
              <label htmlFor="body" className="text-xs font-bold text-text-muted uppercase tracking-wider">Email Body (Required)</label>
              <textarea
                id="body"
                value={body}
                required
                onChange={(e) => setBody(e.target.value)}
                disabled={analysisState.status === 'loading'}
                className="glass-input flex-1 min-h-[240px] resize-y"
                placeholder="[ Paste email body here... ]"
              />
              <div className="text-right text-xs font-mono text-text-dark" aria-live="polite">
                {body.length} chars | {body.trim() ? body.trim().split(/\s+/).length : 0} words
              </div>
            </div>

            {analysisState.status === 'error' && (
              <div className="bg-danger/10 border border-danger/20 text-danger p-4 rounded-xl flex items-start">
                <AlertCircle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
                <span className="text-sm font-medium">{analysisState.error}</span>
              </div>
            )}

            <div className="flex space-x-4 pt-2">
              {analysisState.status === 'loading' ? (
                <button
                  type="button"
                  onClick={() => abortControllerRef.current?.abort()}
                  className="flex-1 btn-primary from-danger to-danger hover:from-danger/80 hover:to-danger shadow-[0_0_15px_rgba(248,113,113,0.25)] hover:shadow-[0_0_20px_rgba(248,113,113,0.4)]"
                >
                  <AlertCircle className="w-5 h-5" />
                  Cancel Analysis
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={!subject.trim() && !body.trim()}
                  className="flex-1 btn-primary"
                >
                  <Send className="w-5 h-5" />
                  Analyze Email
                </button>
              )}
              <button
                type="button"
                onClick={handleClear}
                disabled={analysisState.status === 'loading'}
                className="px-6 py-3 bg-elevated border border-border-strong text-text-primary text-base font-semibold rounded-xl hover:bg-surface transition-colors disabled:opacity-50"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>

        {/* Info Sidebar */}
        <div className="lg:col-span-2 flex flex-col space-y-6">
          <div className="glass-card p-6 flex flex-col relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-20 bg-primary/5 rounded-full blur-2xl -mr-10 -mt-10 transition-transform group-hover:scale-110"></div>
            <Cpu className="w-10 h-10 text-primary mb-4 relative z-10" />
            <h3 className="text-lg font-bold mb-3 text-text-primary relative z-10">AI-Powered Scanning</h3>
            <p className="text-sm text-text-secondary leading-relaxed relative z-10 mb-6">
              Your email will be processed by a fine-tuned BERT architecture and static URL analyzer.
            </p>

            <ul className="space-y-4 text-sm text-text-secondary relative z-10">
              <li className="flex items-start bg-elevated/50 p-3 rounded-lg border border-border-subtle">
                <span className="w-2 h-2 rounded-full bg-primary mt-1.5 mr-3 shrink-0 shadow-[0_0_8px_rgba(56,189,248,0.8)]"></span>
                <span>Contextual classification of subject and body</span>
              </li>
              <li className="flex items-start bg-elevated/50 p-3 rounded-lg border border-border-subtle">
                <span className="w-2 h-2 rounded-full bg-accent mt-1.5 mr-3 shrink-0 shadow-[0_0_8px_rgba(168,85,247,0.8)]"></span>
                <span>Static extraction of URLs without execution</span>
              </li>
              <li className="flex items-start bg-elevated/50 p-3 rounded-lg border border-border-subtle">
                <span className="w-2 h-2 rounded-full bg-success mt-1.5 mr-3 shrink-0 shadow-[0_0_8px_rgba(52,211,153,0.8)]"></span>
                <span>In-memory processing ensuring total privacy</span>
              </li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  );
}
