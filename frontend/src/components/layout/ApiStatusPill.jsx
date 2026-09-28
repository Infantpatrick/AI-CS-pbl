import React, { useState, useEffect } from 'react';
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
      {status === 'checking' ? 'Checking API' : status === 'connected' ? 'API Online' : 'API Unreachable'}
    </div>
  );
}
