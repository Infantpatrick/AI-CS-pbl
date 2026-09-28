import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, AlertCircle, Eye, EyeOff, CheckCircle2, User, Lock, Mail } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    
    if (password !== confirmPassword) {
      setError("Security keys do not match. Please verify.");
      return;
    }
    
    setLoading(true);
    const res = await register(name, email, password);
    setLoading(false);
    
    if (!res.success) {
      setError(res.error);
    } else {
      setSuccess(res.data.message || "Operator clearance granted. Initializing session...");
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    }
  };

  return (
    <div className="flex min-h-screen bg-background text-text-primary">
      <div className="hidden lg:flex flex-1 flex-col justify-center px-12 xl:px-24 bg-surface border-r border-border-strong relative overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary/20 opacity-50 blur-[100px]"></div>
        <div className="absolute right-0 bottom-0 -z-10 m-auto h-[250px] w-[250px] rounded-full bg-accent/20 opacity-50 blur-[80px]"></div>
        
        <div className="relative z-10 space-y-8 max-w-lg">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-primary/10 rounded-2xl border border-primary/20 shadow-[0_0_15px_rgba(56,189,248,0.2)]">
              <Shield className="w-12 h-12 text-primary" />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-text-primary">PhishGuard <span className="text-primary">AI</span></h1>
              <p className="text-sm font-mono text-text-muted uppercase tracking-widest mt-1">v1.0.0 Enterprise</p>
            </div>
          </div>
          <div className="space-y-4">
            <h2 className="text-2xl text-text-primary font-bold">Operator Registration</h2>
            <p className="text-text-secondary leading-relaxed text-lg">
              Create your security credentials to access the AI-powered email threat detection dashboard.
            </p>
          </div>
        </div>
      </div>
      
      <div className="flex-1 flex flex-col justify-center px-6 sm:px-12 lg:px-24 py-12 overflow-y-auto relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>
        <div className="mx-auto w-full max-w-md space-y-8 relative z-10 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="text-center lg:text-left">
            <h2 className="text-3xl font-bold tracking-tight text-text-primary">Request Access</h2>
            <p className="mt-2 text-text-secondary font-medium">Establish a new operator identity.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6 glass-card p-8">
            {error && (
              <div className="bg-danger/10 border border-danger/20 text-danger p-4 rounded-xl flex items-start text-sm animate-in fade-in zoom-in-95 duration-200" aria-live="polite">
                <AlertCircle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
                {error}
              </div>
            )}
            
            {success && (
              <div className="bg-success/10 border border-success/20 text-success p-4 rounded-xl flex items-start text-sm animate-in fade-in zoom-in-95 duration-200" aria-live="polite">
                <CheckCircle2 className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
                {success}
              </div>
            )}

            <div className="space-y-5">
              <div>
                <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Operator Name</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-text-muted" />
                  </div>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="glass-input pl-10"
                    placeholder="John Doe"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Email Address</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-text-muted" />
                  </div>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="glass-input pl-10"
                    placeholder="name@example.com"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Security Key</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-text-muted" />
                  </div>
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="glass-input pl-10 pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-text-muted hover:text-primary transition-colors"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Verify Security Key</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-text-muted" />
                  </div>
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="glass-input pl-10 pr-10"
                    placeholder="••••••••"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary mt-2"
            >
              {loading ? 'Processing...' : 'Register Operator'}
            </button>
          </form>

          <p className="text-center text-sm text-text-secondary">
            Already have clearance?{' '}
            <Link to="/login" className="font-bold text-primary hover:text-primary-strong transition-colors hover:underline underline-offset-4">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
