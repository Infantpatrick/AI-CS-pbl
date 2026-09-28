import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Shield, LayoutDashboard, Search, FileText, Link as LinkIcon, Info, Activity, Menu, X, Settings, LogOut } from 'lucide-react';
import ApiStatusPill from './ApiStatusPill';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard, protected: true },
  { path: '/inbox', label: 'Inbox', icon: Search, protected: true },
  { path: '/analyze', label: 'Analyze Email', icon: Search, protected: true },
  { path: '/history', label: 'History', icon: FileText, protected: true },
  { path: '/reports', label: 'Reports', icon: Activity, protected: true },
  { path: '/url-analysis', label: 'URL Analysis', icon: LinkIcon, protected: true },
  { path: '/performance', label: 'Performance', icon: Info, protected: false },
  { path: '/about', label: 'About', icon: Shield, protected: false },
  { path: '/profile', label: 'Profile', icon: Shield, protected: true },
  { path: '/settings', label: 'Settings', icon: Settings, protected: true },
];

function getInitials(name) {
  if (!name) return 'OP';
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
}

export default function AppShell({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout, authStatus } = useAuth();
  const { preferences } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const userMenuRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        setMobileMenuOpen(false);
        setUserMenuOpen(false);
      }
    };
    const handleClickOutside = (e) => {
      if (userMenuRef.current && !userMenuRef.current.contains(e.target)) {
        setUserMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleEscape);
    window.addEventListener('mousedown', handleClickOutside);
    return () => {
      window.removeEventListener('keydown', handleEscape);
      window.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  useEffect(() => {
    setMobileMenuOpen(false);
    setUserMenuOpen(false);
  }, [location.pathname]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const SidebarContent = () => {
    const isCompact = preferences?.compactSidebar;
    return (
    <>
      <div className={`h-16 flex items-center shrink-0 border-b border-border-strong bg-surface/50 backdrop-blur-sm relative overflow-hidden ${isCompact ? 'justify-center px-2' : 'px-6'}`}>
        <div className="absolute top-0 left-0 w-full h-full bg-primary/5 pointer-events-none"></div>
        <Shield className={`w-7 h-7 text-primary drop-shadow-[0_0_8px_rgba(56,189,248,0.8)] relative z-10 ${!isCompact ? 'mr-3' : ''}`} />
        {!isCompact && <span className="font-bold text-xl tracking-tight text-text-primary relative z-10">PhishGuard</span>}
      </div>
      <nav className="flex-1 overflow-y-auto py-6">
        <div className={`mb-2 ${isCompact ? 'text-center px-1' : 'px-4'}`}>
          {!isCompact ? (
            <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest">Main Menu</span>
          ) : (
            <div className="h-px bg-border-subtle w-8 mx-auto" />
          )}
        </div>
        <ul className={`space-y-1.5 ${isCompact ? 'px-2' : 'px-3'}`}>
          {navItems.filter(item => !item.protected || user).map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  title={isCompact ? item.label : undefined}
                  className={`flex items-center rounded-xl transition-all duration-200 group ${isCompact ? 'justify-center p-3' : 'px-4 py-2.5'} ${
                    isActive 
                      ? 'bg-primary/10 text-primary font-semibold border border-primary/20 shadow-[inset_0_0_12px_rgba(56,189,248,0.1)]' 
                      : 'text-text-secondary hover:bg-elevated hover:text-text-primary border border-transparent'
                  }`}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <item.icon className={`w-5 h-5 transition-colors ${isActive ? 'text-primary' : 'text-text-muted group-hover:text-text-primary'} ${!isCompact ? 'mr-3' : ''}`} />
                  {!isCompact && item.label}
                  {!isCompact && isActive && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-primary shadow-[0_0_5px_rgba(56,189,248,1)]"></div>}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      {user ? (
        <div className={`p-4 border-t border-border-strong shrink-0 relative bg-surface/30 backdrop-blur-sm ${isCompact ? 'flex justify-center p-2' : ''}`} ref={userMenuRef}>
          <button 
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            title={isCompact ? user.name : undefined}
            className={`flex items-center rounded-xl hover:bg-elevated border border-transparent hover:border-border-subtle transition-all text-left group ${isCompact ? 'p-2 justify-center' : 'w-full p-2'}`}
            aria-expanded={userMenuOpen}
            aria-haspopup="true"
          >
            <div className={`w-10 h-10 rounded-full bg-primary/10 border border-primary/30 text-primary flex items-center justify-center font-bold shrink-0 shadow-[0_0_10px_rgba(56,189,248,0.1)] group-hover:bg-primary/20 transition-colors ${!isCompact ? 'mr-3' : ''}`}>
              {getInitials(user.name)}
            </div>
            {!isCompact && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-text-primary truncate">{user.name}</p>
                <p className="text-xs font-mono text-text-secondary truncate">{user.email}</p>
              </div>
            )}
          </button>

          {userMenuOpen && (
            <div className={`absolute bottom-[calc(100%+8px)] bg-elevated/95 backdrop-blur-xl border border-border-strong rounded-xl shadow-2xl overflow-hidden z-50 animate-in slide-in-from-bottom-2 fade-in duration-200 ${isCompact ? 'left-14 w-48' : 'left-4 right-4'}`}>
              <div className="p-4 border-b border-border-strong bg-surface/50">
                <span className="text-[10px] font-bold text-primary uppercase tracking-widest mb-1 block">Active Operator</span>
                <p className="text-sm font-bold text-text-primary truncate">{user.name}</p>
                <p className="text-xs font-mono text-text-secondary truncate">{user.email}</p>
              </div>
              <div className="p-2">
                <Link to="/settings" className="flex items-center w-full px-3 py-2 text-sm font-medium text-text-secondary hover:bg-background hover:text-text-primary rounded-lg transition-colors">
                  <Settings className="w-4 h-4 mr-3" /> Preferences
                </Link>
                <button onClick={handleLogout} className="flex items-center w-full mt-1 px-3 py-2 text-sm font-medium text-danger hover:bg-danger/10 rounded-lg transition-colors">
                  <LogOut className="w-4 h-4 mr-3" /> Terminate Session
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className={`p-4 border-t border-border-strong shrink-0 bg-surface/30 backdrop-blur-sm ${isCompact ? 'px-2 flex justify-center' : ''}`}>
          <Link to="/login" title={isCompact ? "Operator Access" : undefined} className={`btn-primary ${isCompact ? 'p-2 rounded-full w-10 h-10 flex items-center justify-center' : 'w-full py-2.5 text-sm'}`}>
            {isCompact ? <Shield className="w-5 h-5" /> : 'Operator Access'}
          </Link>
        </div>
      )}
    </>
  );
};

  return (
    <div className="flex h-screen bg-background text-text-primary overflow-hidden selection:bg-primary/30 selection:text-text-primary">
      {/* Dynamic Cyber Background for entire app */}
      <div className="fixed inset-0 pointer-events-none z-[-1]">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-primary/5 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-accent/5 rounded-full blur-[120px]"></div>
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      </div>

      <aside className={`hidden lg:flex flex-col glass-card border-r border-y-0 border-l-0 rounded-none z-20 transition-[width] duration-300 ${preferences?.compactSidebar ? 'w-[80px]' : 'w-[280px]'}`}>
        <SidebarContent />
      </aside>

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <header className="h-16 flex items-center justify-between px-4 sm:px-6 lg:px-8 glass-card border-b border-x-0 border-t-0 rounded-none shrink-0 z-10 sticky top-0">
          <div className="flex items-center lg:hidden">
            <Shield className="w-6 h-6 text-primary mr-2 drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" />
            <span className="font-bold text-lg tracking-tight">PhishGuard</span>
          </div>
          <div className="hidden lg:flex items-center min-w-0 w-1/4">
            <h1 className="text-xl font-bold tracking-tight text-text-primary truncate">
              {navItems.find(i => i.path === location.pathname)?.label || 'Terminal'}
            </h1>
          </div>
          
          <div className="hidden lg:flex flex-1 max-w-xl mx-4">
            <div className="relative w-full">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-text-muted" />
              </div>
              <input
                type="text"
                placeholder="Search emails, analysis, or reports..."
                className="w-full bg-background/50 border border-border-subtle rounded-full pl-10 pr-4 py-2 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-all duration-300"
              />
            </div>
          </div>

          <div className="flex items-center space-x-3 sm:space-x-4 ml-auto">
            <ApiStatusPill />
            
            <button className="hidden sm:flex items-center justify-center w-8 h-8 rounded-full hover:bg-elevated text-text-muted hover:text-primary transition-colors relative">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
              <span className="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full animate-pulse"></span>
            </button>

            {user && (
              <div className="hidden sm:flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 border border-primary/30 text-primary font-bold text-xs shadow-[0_0_8px_rgba(56,189,248,0.2)]">
                {getInitials(user.name)}
              </div>
            )}

            <button 
              className="lg:hidden p-2 bg-elevated border border-border-strong rounded-lg text-text-primary hover:border-primary/50 transition-colors"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </header>
        
        <main className="flex-1 overflow-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
          <div className="max-w-[1600px] mx-auto h-full">
            {children}
          </div>
        </main>
      </div>

      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="fixed inset-0 bg-background/80 backdrop-blur-sm animate-in fade-in duration-200" onClick={() => setMobileMenuOpen(false)}></div>
          <div className="fixed inset-y-0 left-0 w-[280px] glass-card border-r rounded-none flex flex-col animate-in slide-in-from-left duration-300">
            <SidebarContent />
          </div>
        </div>
      )}
    </div>
  );
}
