import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppShell from '../components/layout/AppShell';
import Dashboard from '../pages/Dashboard';
import Analyze from '../pages/Analyze';
import History from '../pages/History';
import UrlAnalysis from '../pages/UrlAnalysis';
import HowItWorks from '../pages/HowItWorks';

import About from '../pages/About';
import Login from '../pages/Login';
import Signup from '../pages/Signup';
import Settings from '../pages/Settings';
import Inbox from '../pages/Inbox';
import Reports from '../pages/Reports';
import Profile from '../pages/Profile';
import EmailView from '../pages/EmailView';
import ProtectedRoute from '../components/ProtectedRoute';
import { AuthProvider } from '../contexts/AuthContext';
import { ThemeProvider } from '../contexts/ThemeContext';

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
      <Route path="/dashboard" element={<ProtectedRoute><AppShell><Dashboard /></AppShell></ProtectedRoute>} />
      <Route path="/analyze" element={<ProtectedRoute><AppShell><Analyze analysisState={analysisState} setAnalysisState={setAnalysisState} /></AppShell></ProtectedRoute>} />
      <Route path="/history" element={<ProtectedRoute><AppShell><History /></AppShell></ProtectedRoute>} />
      <Route path="/reports" element={<Navigate to="/history" replace />} />
      <Route path="/reports/:id" element={<ProtectedRoute><AppShell><Reports /></AppShell></ProtectedRoute>} />
      <Route path="/profile" element={<ProtectedRoute><AppShell><Profile /></AppShell></ProtectedRoute>} />
      <Route path="/url-analysis" element={<ProtectedRoute><AppShell><UrlAnalysis analysisState={analysisState} /></AppShell></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute><AppShell><Settings /></AppShell></ProtectedRoute>} />
      <Route path="/inbox" element={<ProtectedRoute><AppShell><Inbox /></AppShell></ProtectedRoute>} />
      <Route path="/inbox/:messageId" element={<ProtectedRoute><AppShell><EmailView /></AppShell></ProtectedRoute>} />
      
      {/* Publicly accessible informational pages, wrapped in AppShell if desired, but they need to handle auth layout appropriately. Let's wrap them in AppShell so they look consistent, but they don't require auth strictly unless we want to hide sidebar. We'll protect them to keep the UX consistent with sidebar containing user profile. Prompt says: "Informational pages may remain public... Document final choice." I'll wrap them in AppShell but NOT ProtectedRoute so they can be viewed without login, BUT AppShell assumes user is logged in for the sidebar profile. 
      Actually, prompt: "Unauthenticated users should be redirected to /login. Informational pages may remain public: /how-it-works, /performance, /about. Document the final choice."
      Since AppShell displays the logged-in user profile, displaying AppShell to unauthenticated users requires a fallback. Let's make all routes protected for simplicity, or handle null user in AppShell. Let's handle null user in AppShell. */}
      
      <Route path="/performance" element={<AppShell><HowItWorks /></AppShell>} />
      <Route path="/how-it-works" element={<Navigate to="/performance" replace />} />
      <Route path="/about" element={<AppShell><About /></AppShell>} />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <AppContent />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
