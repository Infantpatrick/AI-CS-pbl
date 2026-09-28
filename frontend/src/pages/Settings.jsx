import React from 'react';
import { Settings as SettingsIcon, User, Shield, Terminal, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Settings() {
  const { user, logout } = useAuth();

  const getInitials = (name) => {
    if (!name) return 'O';
    return name.charAt(0).toUpperCase();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500 pt-4 pb-12">
      <div>
        <h2 className="text-3xl font-bold flex items-center tracking-tight text-text-primary">
          <SettingsIcon className="w-8 h-8 mr-4 text-primary" />
          Settings
        </h2>
        <p className="text-text-secondary mt-2">Manage application preferences and account details.</p>
      </div>

      <div className="glass-card overflow-hidden border-border-strong relative">
        <div className="p-5 border-b border-border-strong bg-elevated flex items-center">
          <User className="w-5 h-5 mr-3 text-primary" />
          <h3 className="font-bold text-text-primary tracking-wide">Account Identity</h3>
        </div>
        <div className="p-8 flex flex-col sm:flex-row gap-8 items-start">
          <div className="w-24 h-24 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center text-4xl font-bold text-primary shrink-0 shadow-[0_0_20px_rgba(56,189,248,0.2)]">
            {getInitials(user?.name)}
          </div>
          <div className="space-y-6 flex-1 w-full">
            <div>
              <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Operator Name</label>
              <input
                type="text"
                readOnly
                value={user?.name || ''}
                className="glass-input cursor-not-allowed opacity-70 w-full"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Operator Email</label>
              <input
                type="text"
                readOnly
                value={user?.email || ''}
                className="glass-input cursor-not-allowed opacity-70 w-full"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card overflow-hidden border-border-strong">
        <div className="p-5 border-b border-border-strong bg-elevated flex items-center">
          <Terminal className="w-5 h-5 mr-3 text-accent" />
          <h3 className="font-bold text-text-primary tracking-wide">Application</h3>
        </div>
        <div className="p-8">
           <div className="flex justify-between items-center bg-background/50 p-4 rounded-xl border border-border-subtle">
             <div>
               <p className="font-bold text-text-primary mb-1">System Version</p>
               <p className="text-sm text-text-secondary">PhishGuard AI Enterprise Build</p>
             </div>
             <span className="font-mono text-primary font-bold text-sm bg-primary/10 px-3 py-1 rounded">v1.0.0</span>
           </div>
        </div>
      </div>

      <div className="glass-card overflow-hidden border-border-strong border-danger/30">
        <div className="p-5 border-b border-border-strong bg-danger/5 flex items-center">
          <Shield className="w-5 h-5 mr-3 text-danger" />
          <h3 className="font-bold text-text-primary tracking-wide">Security</h3>
        </div>
        <div className="p-8">
           <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-background/50 p-6 rounded-xl border border-danger/20">
             <div className="mb-4 sm:mb-0">
               <p className="font-bold text-text-primary mb-1">Active Session</p>
               <p className="text-sm text-text-secondary">Revoke access and clear all volatile authentication tokens.</p>
             </div>
             <button
               onClick={logout}
               className="btn-primary from-danger to-danger hover:from-danger/80 hover:to-danger shadow-[0_0_15px_rgba(248,113,113,0.25)] hover:shadow-[0_0_20px_rgba(248,113,113,0.4)] whitespace-nowrap flex items-center"
             >
               <LogOut className="w-5 h-5 mr-2" />
               Terminate Session
             </button>
           </div>
        </div>
      </div>

    </div>
  );
}
