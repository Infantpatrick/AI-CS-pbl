import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Search, CheckCircle, AlertTriangle, HelpCircle, Loader } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { getAppClassification } from '../api/normalizers';

export default function Inbox() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("ALL");
  const navigate = useNavigate();

  useEffect(() => {
    if (!user?.has_gmail) {
      setLoading(false);
      return;
    }

    const fetchInbox = async () => {
      try {
        const response = await api.get('/api/gmail/inbox');
        if (response.data && response.data.messages) {
          setMessages(response.data.messages);
        } else {
          setMessages([]);
        }
      } catch (err) {
        setError(err.message || 'Failed to fetch inbox');
      } finally {
        setLoading(false);
      }
    };

    fetchInbox();
  }, [user]);

  if (!user?.has_gmail) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <Mail className="w-16 h-16 text-text-muted mb-4" />
        <h2 className="text-2xl font-bold text-text-primary mb-2">Gmail Not Connected</h2>
        <p className="text-text-secondary mb-6 max-w-md">
          You need to connect your Gmail account to view and analyze your inbox messages.
        </p>
        <button 
          onClick={() => window.location.href = 'http://localhost:8000/auth/gmail/url'}
          className="btn-primary"
        >
          Connect Gmail
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-danger/10 text-danger rounded-xl border border-danger/20">
        <AlertTriangle className="w-6 h-6 mb-2" />
        <p>{error}</p>
      </div>
    );
  }

  const filteredMessages = messages.filter(msg => {
    const appClass = getAppClassification(msg.risk_level);
    if (filter !== "ALL" && appClass !== filter && !(filter === "Not Analyzed" && appClass === "UNKNOWN")) return false;
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      return (msg.subject?.toLowerCase().includes(term) || msg.sender?.toLowerCase().includes(term));
    }
    return true;
  });

  return (
    <div className="flex flex-col h-full animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold text-text-primary">Inbox</h1>
          <button 
            onClick={() => {
              setLoading(true);
              api.get('/api/gmail/inbox').then(res => {
                setMessages(res.data?.messages || []);
                setLoading(false);
              }).catch(err => {
                setError(err.message);
                setLoading(false);
              });
            }}
            className="p-2 text-text-muted hover:text-primary transition-colors bg-surface border border-border-strong rounded-lg shadow-sm hover:shadow"
            title="Refresh Inbox"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21v-5h5"/></svg>
          </button>
        </div>
        <div className="flex items-center gap-3">
          <select 
            className="glass-input py-2 px-3 text-sm"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="ALL">All Messages</option>
            <option value="PHISHING">Phishing</option>
            <option value="SPAM">Spam</option>
            <option value="LEGITIMATE">Legitimate</option>
            <option value="Not Analyzed">Not Analyzed</option>
          </select>
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
            <input 
              type="text" 
              placeholder="Search emails..." 
              className="glass-input pl-9 text-sm py-2"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="glass-card flex-1 overflow-hidden flex flex-col">
        <div className="overflow-y-auto flex-1">
          {filteredMessages.length === 0 ? (
            <div className="p-8 text-center text-text-muted">No messages found.</div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-border-subtle bg-surface-hover">
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Sender</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Subject</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Date</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle">
                {filteredMessages.map((msg) => (
                  <tr key={msg.id} className="hover:bg-surface-hover transition-colors cursor-pointer" onClick={() => navigate(`/inbox/${msg.id}`)}>
                    <td className="p-4">
                      <p className="text-sm font-bold text-text-primary truncate max-w-xs">
                        {msg.sender.replace(/<.*>/, '').trim()}
                      </p>
                    </td>
                    <td className="p-4">
                      <p className="text-sm font-medium text-text-primary truncate max-w-md">
                        {msg.subject}
                      </p>
                    </td>
                    <td className="p-4">
                      <p className="text-sm text-text-muted whitespace-nowrap">
                        {msg.date.split(' ').slice(1,3).join(' ')}
                      </p>
                    </td>
                    <td className="p-4">
                      {getAppClassification(msg.risk_level) === 'PHISHING' && (
                        <span className="inline-flex items-center text-xs font-bold text-danger whitespace-nowrap">
                          🔴 PHISHING
                        </span>
                      )}
                      {getAppClassification(msg.risk_level) === 'SPAM' && (
                        <span className="inline-flex items-center text-xs font-bold text-warning whitespace-nowrap">
                          🟠 SPAM
                        </span>
                      )}
                      {getAppClassification(msg.risk_level) === 'LEGITIMATE' && (
                        <span className="inline-flex items-center text-xs font-bold text-success whitespace-nowrap">
                          🟢 LEGITIMATE
                        </span>
                      )}
                      {(!msg.risk_level || getAppClassification(msg.risk_level) === 'UNKNOWN') && (
                        <span className="inline-flex items-center text-xs font-bold text-text-muted whitespace-nowrap">
                          ⚪ NOT ANALYZED
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
