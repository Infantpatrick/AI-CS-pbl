import os

base_dir = r"D:\AICS PROJECT"

# Files to update
files = {
    "backend/schemas.py": """from pydantic import BaseModel, Field, root_validator
from typing import List, Optional

class PredictionRequest(BaseModel):
    subject: str = Field(..., max_length=1000, description="The subject of the email")
    body: str = Field(..., max_length=50000, description="The body of the email")

    @root_validator(pre=True)
    def check_not_both_empty(cls, values):
        subject = values.get("subject", "")
        body = values.get("body", "")
        
        if isinstance(subject, str):
            subject = subject.strip()
        if isinstance(body, str):
            body = body.strip()
            
        if not subject and not body:
            raise ValueError("Both subject and body cannot be empty.")
        return values

class RiskResponse(BaseModel):
    prediction: str
    phishing_probability: float
    legitimate_probability: float
    confidence: float
    risk_level: str
    urls_found: int
    url_indicators: List[str]
    risk_reasons: List[str]

class HealthResponse(BaseModel):
    status: str

class ModelInfoResponse(BaseModel):
    model: str
    model_type: str
    status: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
""",

    "backend/app.py": """import os
import sys
import uuid
import hashlib
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.schemas import PredictionRequest, RiskResponse, HealthResponse, ModelInfoResponse, UserCreate, UserLogin, UserResponse
from src.model.risk_assessment import assess_email_risk

app = FastAPI(
    title="PhishGuard AI",
    description="API for the AI-Based Email Phishing Detection using BERT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:3000", "http://localhost:8000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Minimal Auth System (In-Memory for demonstration)
USERS = {} # email -> {"id": str, "name": str, "email": str, "password_hash": str}
SESSIONS = {} # session_id -> email

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=401, detail="Not authenticated")
    email = SESSIONS[session_id]
    user = USERS.get(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/auth/register")
def register(user: UserCreate):
    if user.email in USERS:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    USERS[user.email] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "password_hash": hash_password(user.password)
    }
    return {"message": "Account created successfully. Please sign in."}

@app.post("/auth/login", response_model=UserResponse)
def login(user: UserLogin, response: Response):
    db_user = USERS.get(user.email)
    if not db_user or db_user["password_hash"] != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user.email
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=False, # Set to True in prod with HTTPS
        max_age=3600 * 24
    )
    
    return UserResponse(**db_user)

@app.post("/auth/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}

@app.get("/auth/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    return UserResponse(**user)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "healthy"}

@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    return {
        "model": "BERT",
        "model_type": "bert-base-uncased fine-tuned for phishing classification",
        "status": "loaded"
    }

@app.post("/predict", response_model=RiskResponse)
def predict(request: PredictionRequest):
    try:
        result = assess_email_risk(request.subject, request.body)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during prediction.")
""",

    "frontend/src/api/auth.js": """import { api } from './client';

export const register = async (name, email, password) => {
  try {
    const res = await api.post('/auth/register', { name, email, password });
    return { success: true, data: res.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Unable to create your account. Please check your information and try again.' 
    };
  }
};

export const login = async (email, password) => {
  try {
    // Ensure credentials are sent to set cookies
    const res = await api.post('/auth/login', { email, password }, { withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    if (error.response?.status === 401) {
        return { success: false, error: 'Email or password is incorrect.' };
    }
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Unable to reach the authentication service. Please try again.' 
    };
  }
};

export const logout = async () => {
  try {
    await api.post('/auth/logout', {}, { withCredentials: true });
    return { success: true };
  } catch (error) {
    return { success: false, error: 'Logout failed' };
  }
};

export const getMe = async () => {
  try {
    const res = await api.get('/auth/me', { withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false };
  }
};
""",

    "frontend/src/api/client.js": """import axios from 'axios';

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
    const res = await api.post('/predict', { subject, body }, { signal, timeout: 60000, withCredentials: true });
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

    "frontend/src/contexts/AuthContext.jsx": """import React, { createContext, useState, useEffect, useContext } from 'react';
import { getMe, login as apiLogin, logout as apiLogout, register as apiRegister } from '../api/auth';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authStatus, setAuthStatus] = useState('checking'); // checking, authenticated, unauthenticated

  const refreshUser = async () => {
    setAuthStatus('checking');
    const res = await getMe();
    if (res.success) {
      setUser(res.data);
      setAuthStatus('authenticated');
    } else {
      setUser(null);
      setAuthStatus('unauthenticated');
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email, password) => {
    const res = await apiLogin(email, password);
    if (res.success) {
      setUser(res.data);
      setAuthStatus('authenticated');
      return { success: true };
    }
    return res;
  };

  const logout = async () => {
    await apiLogout();
    setUser(null);
    setAuthStatus('unauthenticated');
  };

  const register = async (name, email, password) => {
    return await apiRegister(name, email, password);
  };

  return (
    <AuthContext.Provider value={{ user, authStatus, login, logout, register, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};
""",

    "frontend/src/components/ProtectedRoute.jsx": """import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function ProtectedRoute({ children }) {
  const { authStatus } = useAuth();
  const location = useLocation();

  if (authStatus === 'checking') {
    return <div className="flex h-full items-center justify-center">Loading...</div>;
  }

  if (authStatus === 'unauthenticated') {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
""",

    "frontend/src/pages/Login.jsx": """import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Shield, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const { login, authStatus } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/';

  useEffect(() => {
    if (authStatus === 'authenticated') {
      navigate(from, { replace: true });
    }
  }, [authStatus, navigate, from]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    const res = await login(email, password);
    if (!res.success) {
      setError(res.error);
      setLoading(false);
    }
    // if success, useEffect will navigate
  };

  if (authStatus === 'checking' || authStatus === 'authenticated') {
    return null;
  }

  return (
    <div className="flex min-h-screen bg-base">
      <div className="hidden lg:flex flex-1 flex-col justify-center px-12 xl:px-24 bg-surface border-r border-strong relative overflow-hidden">
        <div className="absolute inset-0 bg-primary/5 pattern-grid pointer-events-none"></div>
        <div className="relative z-10 space-y-6 max-w-lg">
          <Shield className="w-16 h-16 text-primary" />
          <h1 className="text-4xl font-bold text-text-primary tracking-tight">PhishGuard AI</h1>
          <h2 className="text-xl text-primary font-medium">AI-Powered Email Phishing Detection</h2>
          <p className="text-lg text-text-secondary leading-relaxed">
            Analyze suspicious emails using BERT-based NLP and static URL analysis.
          </p>
        </div>
      </div>
      
      <div className="flex-1 flex flex-col justify-center px-6 sm:px-12 lg:px-24">
        <div className="mx-auto w-full max-w-md space-y-8">
          <div className="text-center lg:text-left">
            <h2 className="text-3xl font-bold text-text-primary tracking-tight">Welcome back</h2>
            <p className="mt-2 text-text-secondary">Sign in to continue to PhishGuard AI.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-danger/10 border border-danger/20 text-danger p-3 rounded-md flex items-start text-sm" aria-live="polite">
                <AlertCircle className="w-5 h-5 mr-2 shrink-0 mt-0.5" />
                {error}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary"
                  placeholder="name@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2.5 text-text-muted hover:text-text-primary"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-semibold bg-primary text-white hover:bg-primary-strong disabled:opacity-50 transition-colors"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-sm text-text-secondary">
            Don't have an account?{' '}
            <Link to="/signup" className="font-semibold text-primary hover:text-primary-strong">
              Create Account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
""",

    "frontend/src/pages/Signup.jsx": """import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, AlertCircle, Eye, EyeOff, CheckCircle2 } from 'lucide-react';
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
      setError("Passwords do not match");
      return;
    }
    
    setLoading(true);
    const res = await register(name, email, password);
    setLoading(false);
    
    if (!res.success) {
      setError(res.error);
    } else {
      setSuccess(res.data.message || "Account created successfully. Please sign in.");
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    }
  };

  return (
    <div className="flex min-h-screen bg-base">
      <div className="hidden lg:flex flex-1 flex-col justify-center px-12 xl:px-24 bg-surface border-r border-strong relative overflow-hidden">
        <div className="absolute inset-0 bg-primary/5 pattern-grid pointer-events-none"></div>
        <div className="relative z-10 space-y-6 max-w-lg">
          <Shield className="w-16 h-16 text-primary" />
          <h1 className="text-4xl font-bold text-text-primary tracking-tight">PhishGuard AI</h1>
          <h2 className="text-xl text-primary font-medium">AI-Powered Email Phishing Detection</h2>
          <p className="text-lg text-text-secondary leading-relaxed">
            Analyze suspicious emails using BERT-based NLP and static URL analysis.
          </p>
        </div>
      </div>
      
      <div className="flex-1 flex flex-col justify-center px-6 sm:px-12 lg:px-24 py-12 overflow-y-auto">
        <div className="mx-auto w-full max-w-md space-y-8">
          <div className="text-center lg:text-left">
            <h2 className="text-3xl font-bold text-text-primary tracking-tight">Create your account</h2>
            <p className="mt-2 text-text-secondary">Join PhishGuard AI today.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-danger/10 border border-danger/20 text-danger p-3 rounded-md flex items-start text-sm" aria-live="polite">
                <AlertCircle className="w-5 h-5 mr-2 shrink-0 mt-0.5" />
                {error}
              </div>
            )}
            
            {success && (
              <div className="bg-success/10 border border-success/20 text-success p-3 rounded-md flex items-start text-sm" aria-live="polite">
                <CheckCircle2 className="w-5 h-5 mr-2 shrink-0 mt-0.5" />
                {success}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary"
                  placeholder="Deva M"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary"
                  placeholder="name@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2.5 text-text-muted hover:text-text-primary"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Confirm Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full bg-elevated border border-strong rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-primary pr-10"
                    placeholder="••••••••"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-semibold bg-primary text-white hover:bg-primary-strong disabled:opacity-50 transition-colors"
            >
              {loading ? 'Creating...' : 'Create Account'}
            </button>
          </form>

          <p className="text-center text-sm text-text-secondary">
            Already have an account?{' '}
            <Link to="/login" className="font-semibold text-primary hover:text-primary-strong">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
""",

    "frontend/src/pages/Settings.jsx": """import React from 'react';
import { Settings as SettingsIcon } from 'lucide-react';

export default function Settings() {
  return (
    <div className="max-w-3xl space-y-8">
      <div>
        <h2 className="text-2xl font-bold flex items-center">
          <SettingsIcon className="w-6 h-6 mr-3 text-primary" />
          Settings
        </h2>
        <p className="text-text-secondary mt-1">Manage application preferences.</p>
      </div>

      <div className="bg-surface border border-subtle rounded-xl overflow-hidden">
        <div className="p-4 border-b border-strong bg-elevated/50 font-semibold">
          Appearance
        </div>
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-text-primary">Theme</p>
              <p className="text-sm text-text-secondary">Select your application theme.</p>
            </div>
            <select disabled className="bg-elevated border border-strong rounded-md px-3 py-1.5 text-text-primary text-sm focus:outline-none">
              <option>Dark</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
""",

    "frontend/src/app/App.jsx": """import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppShell from '../components/layout/AppShell';
import Dashboard from '../pages/Dashboard';
import Analyze from '../pages/Analyze';
import Results from '../pages/Results';
import UrlAnalysis from '../pages/UrlAnalysis';
import HowItWorks from '../pages/HowItWorks';
import ModelPerformance from '../pages/ModelPerformance';
import About from '../pages/About';
import Login from '../pages/Login';
import Signup from '../pages/Signup';
import Settings from '../pages/Settings';
import ProtectedRoute from '../components/ProtectedRoute';
import { AuthProvider } from '../contexts/AuthContext';

function AppContent() {
  const [analysisState, setAnalysisState] = useState({
    status: 'idle',
    result: null,
    error: null,
    submittedInput: null
  });

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      
      <Route path="/" element={<ProtectedRoute><AppShell><Dashboard /></AppShell></ProtectedRoute>} />
      <Route path="/analyze" element={<ProtectedRoute><AppShell><Analyze analysisState={analysisState} setAnalysisState={setAnalysisState} /></AppShell></ProtectedRoute>} />
      <Route path="/results" element={<ProtectedRoute><AppShell><Results analysisState={analysisState} setAnalysisState={setAnalysisState} /></AppShell></ProtectedRoute>} />
      <Route path="/url-analysis" element={<ProtectedRoute><AppShell><UrlAnalysis analysisState={analysisState} /></AppShell></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute><AppShell><Settings /></AppShell></ProtectedRoute>} />
      
      {/* Publicly accessible informational pages, wrapped in AppShell if desired, but they need to handle auth layout appropriately. Let's wrap them in AppShell so they look consistent, but they don't require auth strictly unless we want to hide sidebar. We'll protect them to keep the UX consistent with sidebar containing user profile. Prompt says: "Informational pages may remain public... Document final choice." I'll wrap them in AppShell but NOT ProtectedRoute so they can be viewed without login, BUT AppShell assumes user is logged in for the sidebar profile. 
      Actually, prompt: "Unauthenticated users should be redirected to /login. Informational pages may remain public: /how-it-works, /performance, /about. Document the final choice."
      Since AppShell displays the logged-in user profile, displaying AppShell to unauthenticated users requires a fallback. Let's make all routes protected for simplicity, or handle null user in AppShell. Let's handle null user in AppShell. */}
      
      <Route path="/how-it-works" element={<AppShell><HowItWorks /></AppShell>} />
      <Route path="/performance" element={<AppShell><ModelPerformance /></AppShell>} />
      <Route path="/about" element={<AppShell><About /></AppShell>} />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
""",

    "frontend/src/components/layout/AppShell.jsx": """import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Shield, LayoutDashboard, Search, FileText, Link as LinkIcon, Info, Activity, Menu, X, Settings, LogOut, User } from 'lucide-react';
import ApiStatusPill from './ApiStatusPill';
import { useAuth } from '../../contexts/AuthContext';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard, protected: true },
  { path: '/analyze', label: 'Analyze Email', icon: Search, protected: true },
  { path: '/results', label: 'Results', icon: FileText, protected: true },
  { path: '/url-analysis', label: 'URL Analysis', icon: LinkIcon, protected: true },
  { path: '/how-it-works', label: 'How It Works', icon: Info, protected: false },
  { path: '/performance', label: 'Model Performance', icon: Activity, protected: false },
  { path: '/about', label: 'About', icon: Shield, protected: false },
];

function getInitials(name) {
  if (!name) return 'U';
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
}

export default function AppShell({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout, authStatus } = useAuth();
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

  const SidebarContent = () => (
    <>
      <div className="h-16 flex items-center px-6 border-b border-strong shrink-0">
        <Shield className="w-6 h-6 text-primary mr-2" />
        <span className="font-bold text-lg tracking-wide">PhishGuard AI</span>
      </div>
      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {navItems.filter(item => !item.protected || user).map((item) => {
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

      {user ? (
        <div className="p-4 border-t border-strong shrink-0 relative" ref={userMenuRef}>
          <button 
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="w-full flex items-center p-2 rounded-md hover:bg-elevated transition-colors text-left"
            aria-expanded={userMenuOpen}
            aria-haspopup="true"
          >
            <div className="w-10 h-10 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold mr-3 shrink-0">
              {getInitials(user.name)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-text-primary truncate">{user.name}</p>
              <p className="text-xs text-text-secondary truncate">{user.email}</p>
            </div>
          </button>

          {userMenuOpen && (
            <div className="absolute bottom-full left-4 right-4 mb-2 bg-surface border border-strong rounded-lg shadow-xl overflow-hidden z-50 animate-in slide-in-from-bottom-2 fade-in duration-200">
              <div className="p-3 border-b border-strong">
                <p className="text-sm font-bold text-text-primary truncate">{user.name}</p>
                <p className="text-xs text-text-secondary truncate">{user.email}</p>
              </div>
              <div className="p-1">
                <Link to="/settings" className="flex items-center w-full px-3 py-2 text-sm text-text-secondary hover:bg-elevated hover:text-text-primary rounded-md">
                  <Settings className="w-4 h-4 mr-2" /> Settings
                </Link>
                <button onClick={handleLogout} className="flex items-center w-full px-3 py-2 text-sm text-danger hover:bg-danger/10 rounded-md">
                  <LogOut className="w-4 h-4 mr-2" /> Logout
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="p-4 border-t border-strong shrink-0">
          <Link to="/login" className="flex items-center justify-center w-full py-2 bg-primary text-white rounded-md text-sm font-semibold hover:bg-primary-strong">
            Sign In
          </Link>
        </div>
      )}
    </>
  );

  return (
    <div className="flex h-screen bg-base text-text-primary overflow-hidden">
      <aside className="hidden lg:flex w-64 flex-col bg-surface border-r border-strong z-20">
        <SidebarContent />
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
          <div className="fixed inset-y-0 left-0 w-64 bg-surface shadow-xl flex flex-col">
            <SidebarContent />
          </div>
        </div>
      )}
    </div>
  );
}
"""
}

def scaffold():
    for rel_path, content in files.items():
        full_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Created: {full_path}")

if __name__ == "__main__":
    scaffold()
