import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Calendar, Cpu, AlertTriangle, ShieldCheck, Link as LinkIcon, Loader } from 'lucide-react';
import { predict, api } from '../api/client';
import { useAuth } from '../contexts/AuthContext';
import { getAppClassification } from '../api/normalizers';

export default function EmailView() {
  const { messageId } = useParams();
  const { user } = useAuth();
  
  const [email, setEmail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [analysisError, setAnalysisError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEmail = async () => {
      try {
        const response = await api.get(`/api/gmail/message/${messageId}`, { withCredentials: true });
        setEmail(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to fetch email details.');
      } finally {
        setLoading(false);
      }
    };
    if (user?.has_gmail) {
      fetchEmail();
    }
  }, [messageId, user]);

  const handleAnalyzeClick = () => {
    // Transfer to Analysis Email page
    navigate('/analyze', {
      state: {
        emailData: {
          subject: email.subject,
          sender: email.sender,
          recipient: email.recipient,
          date: email.date,
          body: email.body,
          messageId: email.id
        }
      }
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  if (error || !email) {
    const errorMsg = typeof error === 'string' ? error : 
                     Array.isArray(error) ? error.map(e => e.msg || JSON.stringify(e)).join(', ') :
                     typeof error === 'object' && error !== null ? JSON.stringify(error) :
                     'Email not found.';
    return (
      <div className="p-6 bg-danger/10 text-danger rounded-xl border border-danger/20 flex flex-col items-start">
        <AlertTriangle className="w-6 h-6 mb-2" />
        <p className="break-words w-full">{errorMsg}</p>
        <Link to="/inbox" className="text-danger hover:text-danger-strong font-bold underline mt-4 block">Return to Inbox</Link>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col space-y-6 animate-in fade-in duration-500 pb-12">
      <div>
        <Link to="/inbox" className="inline-flex items-center text-sm font-medium text-text-secondary hover:text-primary transition-colors mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Inbox
        </Link>
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <h1 className="text-2xl sm:text-3xl font-bold text-text-primary break-words">
            {email.subject}
          </h1>
          {email.analysis ? (
            <div className="flex flex-col gap-2">
              <div className="flex flex-wrap gap-2 mb-2">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold ${getAppClassification(email.analysis.risk_level) === 'PHISHING' ? 'bg-danger/10 text-danger' : getAppClassification(email.analysis.risk_level) === 'SPAM' ? 'bg-warning/10 text-warning' : 'bg-success/10 text-success'}`}>
                  Application Classification: {getAppClassification(email.analysis.risk_level) === 'PHISHING' ? '🔴 PHISHING' : getAppClassification(email.analysis.risk_level) === 'SPAM' ? '🟠 SPAM' : '🟢 LEGITIMATE'}
                </span>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold ${email.analysis.risk_level === 'HIGH' || email.analysis.risk_level === 'CRITICAL' ? 'bg-danger/10 text-danger' : email.analysis.risk_level === 'MEDIUM' ? 'bg-warning/10 text-warning' : 'bg-success/10 text-success'}`}>
                  Risk Level: {email.analysis.risk_level}
                </span>
              </div>
              <div className="flex gap-2">
                <button onClick={() => navigate(`/reports/${email.analysis.id}`)} className="btn-primary shrink-0 bg-surface text-text-primary hover:bg-surface-hover border border-border-strong">
                  View Report
                </button>
                <button onClick={handleAnalyzeClick} className="btn-primary shrink-0">
                  <Cpu className="w-4 h-4 mr-2" /> Re-analyze
                </button>
              </div>
            </div>
          ) : (
            <button onClick={handleAnalyzeClick} className="btn-primary shrink-0 shadow-[0_0_15px_rgba(var(--primary-default),0.4)]">
              <Cpu className="w-5 h-5 mr-2" /> Analyze with BERT
            </button>
          )}
        </div>
      </div>

      <div className="glass-card p-6 flex flex-col space-y-6">
        <h2 className="text-lg font-bold border-b border-border-subtle pb-2">EMAIL DETAILS</h2>
        <div className="flex flex-col sm:flex-row gap-6 border-b border-border-subtle pb-6">
          <div className="flex-1 space-y-4">
            <div className="flex items-start gap-3">
              <User className="w-5 h-5 text-text-muted shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-1">From</p>
                <p className="font-medium text-text-primary break-all">{email.sender}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <User className="w-5 h-5 text-text-muted shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-1">To</p>
                <p className="font-medium text-text-primary break-all">{email.recipient || 'N/A'}</p>
              </div>
            </div>
          </div>
          <div className="sm:w-1/3">
            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-text-muted shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-1">Date</p>
                <p className="font-medium text-text-primary">{email.date}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div>
          <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-4">Message Body</p>
          <div className="bg-surface/50 border border-border-subtle rounded-xl p-4 md:p-6 whitespace-pre-wrap font-mono text-sm text-text-secondary leading-relaxed overflow-x-auto max-h-[300px]">
            {email.body}
          </div>
        </div>
      </div>
    </div>
  );
}


