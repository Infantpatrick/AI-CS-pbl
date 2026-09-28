import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { FileText, Search, AlertTriangle, ShieldCheck, Loader } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { getAppClassification } from '../api/normalizers';

export default function History() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get('/api/analysis/history', { withCredentials: true });
        setHistory(response.data);
      } catch (err) {
        setError(err.message || 'Failed to load history');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-danger/10 text-danger rounded-xl border border-danger/20 flex items-start gap-3">
        <AlertTriangle className="w-6 h-6 mb-2 shrink-0" />
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-text-primary">Analysis History</h1>
        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input 
            type="text" 
            placeholder="Search history..." 
            className="glass-input pl-9 text-sm py-2"
          />
        </div>
      </div>

      <div className="glass-card flex-1 overflow-hidden flex flex-col">
        <div className="overflow-y-auto flex-1 p-0">
          {history.length === 0 ? (
            <div className="p-12 text-center flex flex-col items-center">
              <FileText className="w-12 h-12 text-text-muted mb-4" />
              <h3 className="text-lg font-bold text-text-primary mb-2">No Analysis History</h3>
              <p className="text-text-secondary mb-6">You haven't analyzed any emails yet.</p>
              <Link to="/inbox" className="btn-primary">Go to Inbox</Link>
            </div>
          ) : (
            <table className="w-full text-left border-collapse min-w-[600px]">
              <thead>
                <tr className="border-b border-border-subtle bg-surface/50">
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Date</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Subject</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Sender</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">BERT Prediction</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">Risk Level</th>
                  <th className="p-4 text-xs font-bold text-text-muted uppercase tracking-wider">App Classification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-surface-hover transition-colors cursor-pointer" onClick={() => navigate(`/reports/${item.id}`)}>
                    <td className="p-4 text-sm text-text-secondary whitespace-nowrap">
                      {new Date(item.analyzed_at).toLocaleString()}
                    </td>
                    <td className="p-4 text-sm font-medium text-text-primary max-w-[200px] truncate">
                      {item.subject}
                    </td>
                    <td className="p-4 text-sm text-text-secondary max-w-[150px] truncate">
                      {item.sender.replace(/<.*>/, '').trim()}
                    </td>
                    <td className="p-4 text-sm">
                      <span className="inline-flex items-center text-xs font-bold text-text-primary whitespace-nowrap">
                        {item.prediction}
                      </span>
                    </td>
                    <td className="p-4 text-sm">
                      <span className={`font-bold ${item.risk_level === 'HIGH' ? 'text-danger' : item.risk_level === 'MEDIUM' ? 'text-warning' : 'text-success'}`}>
                        {item.risk_level}
                      </span>
                    </td>
                    <td className="p-4 text-sm">
                      {getAppClassification(item.risk_level) === 'PHISHING' && (
                        <span className="inline-flex items-center text-xs font-bold text-danger whitespace-nowrap">
                          🔴 PHISHING
                        </span>
                      )}
                      {getAppClassification(item.risk_level) === 'SPAM' && (
                        <span className="inline-flex items-center text-xs font-bold text-warning whitespace-nowrap">
                          🟠 SPAM
                        </span>
                      )}
                      {getAppClassification(item.risk_level) === 'LEGITIMATE' && (
                        <span className="inline-flex items-center text-xs font-bold text-success whitespace-nowrap">
                          🟢 LEGITIMATE
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
