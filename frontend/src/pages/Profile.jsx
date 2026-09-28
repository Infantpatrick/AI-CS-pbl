import React, { useState, useEffect } from 'react';
import { User, Mail, Shield, CheckCircle, Clock, Settings, Monitor, Moon, Sun, Palette, Layout, Trash2, ChevronRight, Activity, AlertTriangle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { getDashboardStats, getAnalysisHistory } from '../api/client';
import { Link } from 'react-router-dom';

export default function Profile() {
  const { user } = useAuth();
  const { preferences, updatePreference, resetPreferences } = useTheme();
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingStats, setLoadingStats] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoadingStats(true);
      try {
        const [statsRes, historyRes] = await Promise.all([
          getDashboardStats(),
          getAnalysisHistory()
        ]);
        
        if (statsRes.success) setStats(statsRes.data);
        if (historyRes.success) setHistory(historyRes.data);
      } catch (err) {
        console.error("Failed to load profile data", err);
      } finally {
        setLoadingStats(false);
      }
    };
    
    if (user) {
      fetchData();
    }
  }, [user]);



  const isGoogleAccount = user?.has_gmail || false; // Approximation based on existing data

  const getRiskBadge = (risk) => {
    switch (risk) {
      case 'LOW': return <span className="px-2 py-1 bg-success/20 text-success rounded-md text-xs font-bold">LOW</span>;
      case 'MEDIUM': return <span className="px-2 py-1 bg-warning/20 text-warning rounded-md text-xs font-bold">MEDIUM</span>;
      case 'HIGH': return <span className="px-2 py-1 bg-danger/20 text-danger rounded-md text-xs font-bold">HIGH</span>;
      default: return null;
    }
  };

  const getClassificationBadge = (risk) => {
    switch (risk) {
      case 'LOW': return <span className="flex items-center text-success text-sm font-medium"><div className="w-2 h-2 rounded-full bg-success mr-2"></div> LEGITIMATE</span>;
      case 'MEDIUM': return <span className="flex items-center text-warning text-sm font-medium"><div className="w-2 h-2 rounded-full bg-warning mr-2"></div> SPAM</span>;
      case 'HIGH': return <span className="flex items-center text-danger text-sm font-medium"><div className="w-2 h-2 rounded-full bg-danger mr-2"></div> PHISHING</span>;
      default: return null;
    }
  };

  return (
    <div className="h-full flex flex-col space-y-8 animate-in fade-in duration-500 max-w-6xl mx-auto pb-12">
      <h1 className="text-3xl font-bold text-text-primary">Profile & Settings</h1>
      
      {/* 1. PROFILE HEADER */}
      <div className="glass-card p-8 flex flex-col md:flex-row items-center md:items-start space-y-4 md:space-y-0 md:space-x-8">
        <div className="w-24 h-24 rounded-full bg-primary/10 border-2 border-primary/30 flex items-center justify-center shrink-0 shadow-[0_0_15px_rgba(var(--primary-default),0.2)]">
          <User className="w-12 h-12 text-primary" />
        </div>
        <div className="flex-1 text-center md:text-left">
          <h2 className="text-3xl font-bold text-text-primary mb-1">{user?.name || 'Operator'}</h2>
          <p className="text-text-secondary font-mono text-lg mb-4">{user?.email}</p>
          <div className="flex flex-wrap justify-center md:justify-start gap-3">
            <span className="flex items-center px-3 py-1 bg-surface rounded-full border border-border-subtle text-sm text-text-secondary">
              {isGoogleAccount ? <Mail className="w-4 h-4 mr-2 text-primary" /> : <Shield className="w-4 h-4 mr-2 text-primary" />}
              {isGoogleAccount ? 'Google Account' : 'Email Account'}
            </span>
            <span className="flex items-center px-3 py-1 bg-success/10 border border-success/30 rounded-full text-sm text-success font-medium">
              <CheckCircle className="w-4 h-4 mr-2" />
              Active
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN */}
        <div className="space-y-8 lg:col-span-1">
          
          {/* 2. ACCOUNT INFORMATION */}
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-text-primary flex items-center mb-6 border-b border-border-subtle pb-4">
              <Shield className="w-5 h-5 mr-2 text-primary" />
              Account Information
            </h3>
            <div className="space-y-4 text-sm">
              <div>
                <p className="text-text-muted mb-1 uppercase text-xs font-bold tracking-wider">Full Name</p>
                <p className="text-text-primary font-medium">{user?.name}</p>
              </div>
              <div>
                <p className="text-text-muted mb-1 uppercase text-xs font-bold tracking-wider">Email Address</p>
                <p className="text-text-primary font-mono">{user?.email}</p>
              </div>
              <div>
                <p className="text-text-muted mb-1 uppercase text-xs font-bold tracking-wider">Authentication Method</p>
                <p className="text-text-primary">{isGoogleAccount ? 'Google OAuth' : 'Standard Authentication'}</p>
              </div>
            </div>
          </div>

          {/* 3. ANALYSIS OVERVIEW */}
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-text-primary flex items-center mb-6 border-b border-border-subtle pb-4">
              <Activity className="w-5 h-5 mr-2 text-primary" />
              Analysis Overview
            </h3>
            {loadingStats ? (
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-border-subtle rounded w-3/4"></div>
                <div className="h-4 bg-border-subtle rounded w-1/2"></div>
              </div>
            ) : stats ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-surface rounded-lg border border-border-subtle">
                  <span className="text-text-secondary">Total Analyzed</span>
                  <span className="text-xl font-bold text-text-primary">{stats.total_emails_scanned || 0}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-surface rounded-lg border border-border-subtle">
                  <span className="text-text-secondary">Legitimate</span>
                  <span className="text-lg font-bold text-success">{stats.legitimate_emails || 0}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-surface rounded-lg border border-border-subtle">
                  <span className="text-text-secondary">Spam / Medium Risk</span>
                  <span className="text-lg font-bold text-warning">{stats.spam_emails || 0}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-surface rounded-lg border border-border-subtle">
                  <span className="text-text-secondary">Phishing / High Risk</span>
                  <span className="text-lg font-bold text-danger">{stats.high_risk_emails || stats.phishing_detected || 0}</span>
                </div>
              </div>
            ) : (
              <p className="text-text-muted text-sm italic">No data available</p>
            )}
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="space-y-8 lg:col-span-2">
          
          {/* 5. APPEARANCE / THEME SETTINGS */}
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-text-primary flex items-center mb-6 border-b border-border-subtle pb-4">
              <Palette className="w-5 h-5 mr-2 text-primary" />
              Appearance & Theme
            </h3>
            
            <div className="space-y-8">
              {/* Theme Selection */}
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-3">Theme</p>
                <div className="flex space-x-3">
                  {['dark', 'light', 'system'].map(t => (
                    <button
                      key={t}
                      onClick={() => updatePreference('theme', t)}
                      className={`flex-1 py-2 px-4 rounded-xl border flex items-center justify-center transition-all ${
                        preferences.theme === t 
                          ? 'border-primary bg-primary/10 text-primary shadow-[0_0_10px_rgba(var(--primary-default),0.2)]' 
                          : 'border-border-subtle bg-surface text-text-secondary hover:border-primary/50'
                      }`}
                    >
                      {t === 'dark' && <Moon className="w-4 h-4 mr-2" />}
                      {t === 'light' && <Sun className="w-4 h-4 mr-2" />}
                      {t === 'system' && <Monitor className="w-4 h-4 mr-2" />}
                      <span className="capitalize">{t}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Accent Color */}
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-3">Accent Color</p>
                <div className="flex space-x-4">
                  {[
                    { id: 'cyan', color: 'bg-cyan-500' },
                    { id: 'blue', color: 'bg-blue-500' },
                    { id: 'purple', color: 'bg-purple-500' },
                    { id: 'green', color: 'bg-emerald-500' }
                  ].map(acc => (
                    <button
                      key={acc.id}
                      onClick={() => updatePreference('accent', acc.id)}
                      className={`w-10 h-10 rounded-full ${acc.color} transition-all flex items-center justify-center ${
                        preferences.accent === acc.id ? 'ring-2 ring-white ring-offset-2 ring-offset-background scale-110' : 'opacity-70 hover:opacity-100'
                      }`}
                      title={acc.id}
                    >
                      {preferences.accent === acc.id && <CheckCircle className="w-5 h-5 text-white" />}
                    </button>
                  ))}
                </div>
              </div>

              {/* Interface Preferences */}
              <div>
                <p className="text-sm font-bold text-text-muted uppercase tracking-wider mb-3">Interface Preferences</p>
                <div className="space-y-3">
                  {[
                    { id: 'glassmorphism', label: 'Glassmorphism Effects', desc: 'Enable blurred backgrounds on cards' },
                    { id: 'glow', label: 'Glow Effects', desc: 'Enable subtle glowing borders and shadows' },
                    { id: 'compactSidebar', label: 'Compact Sidebar', desc: 'Use a narrower sidebar navigation' }
                  ].map(pref => (
                    <div key={pref.id} className="flex items-center justify-between p-3 bg-surface rounded-xl border border-border-subtle">
                      <div>
                        <p className="font-medium text-text-primary">{pref.label}</p>
                        <p className="text-xs text-text-muted">{pref.desc}</p>
                      </div>
                      <button 
                        onClick={() => updatePreference(pref.id, !preferences[pref.id])}
                        className={`w-12 h-6 rounded-full transition-colors relative ${preferences[pref.id] ? 'bg-primary' : 'bg-gray-600'}`}
                      >
                        <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${preferences[pref.id] ? 'left-7' : 'left-1'}`}></div>
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-border-subtle flex justify-end">
                <button 
                  onClick={resetPreferences}
                  className="flex items-center text-sm text-text-muted hover:text-text-primary transition-colors"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Reset Appearance
                </button>
              </div>
            </div>
          </div>

          {/* 4. RECENT ANALYSIS */}
          <div className="glass-card p-6 overflow-hidden flex flex-col">
            <h3 className="text-lg font-bold text-text-primary flex items-center mb-6 border-b border-border-subtle pb-4">
              <Clock className="w-5 h-5 mr-2 text-primary" />
              Recent Analysis
            </h3>
            
            <div className="flex-1 overflow-auto">
              {loadingStats ? (
                <div className="animate-pulse space-y-4">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="h-16 bg-surface rounded-xl border border-border-subtle"></div>
                  ))}
                </div>
              ) : history && history.length > 0 ? (
                <div className="space-y-3">
                  {history.slice(0, 5).map((item) => (
                    <div key={item.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-surface rounded-xl border border-border-subtle hover:border-border-strong transition-colors gap-4">
                      <div className="flex-1 min-w-0">
                        <p className="text-text-primary font-medium truncate" title={item.subject}>{item.subject || '(No Subject)'}</p>
                        <p className="text-xs text-text-muted mt-1">
                          {new Date(item.analyzed_at + 'Z').toLocaleString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-4 shrink-0">
                        <div className="hidden md:block">
                          {getClassificationBadge(item.risk_level)}
                        </div>
                        <div>
                          {getRiskBadge(item.risk_level)}
                        </div>
                        <Link 
                          to={`/reports/${item.id}`}
                          className="flex items-center text-sm font-medium text-primary hover:text-primary-strong transition-colors"
                        >
                          View Report <ChevronRight className="w-4 h-4 ml-1" />
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <AlertTriangle className="w-12 h-12 text-text-muted mx-auto mb-3 opacity-50" />
                  <p className="text-text-muted italic">No recent analysis data available</p>
                </div>
              )}
            </div>
            
            {history && history.length > 5 && (
              <div className="mt-4 pt-4 border-t border-border-subtle text-center">
                <Link to="/history" className="text-sm font-bold text-primary hover:text-primary-strong transition-colors">
                  View All History
                </Link>
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}
