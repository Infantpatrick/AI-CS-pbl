import React from 'react';
import { Mail, Settings, BrainCircuit, Link as LinkIcon, BarChart3, ShieldCheck, FileText, Lock, Shield, Key, Cpu, Database, Layout } from 'lucide-react';

export default function HowItWorks() {
  return (
    <div className="max-w-6xl mx-auto space-y-16 animate-in fade-in slide-in-from-bottom-4 duration-500 py-6 pb-20">
      
      <div className="text-center max-w-3xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold mb-4 text-text-primary tracking-tight">How PhishGuard AI Works</h1>
        <p className="text-text-secondary text-lg">Understand how PhishGuard AI analyzes emails using BERT, URL analysis, and risk assessment.</p>
      </div>

      {/* SECTION 1 - HOW THE SYSTEM WORKS */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-text-primary border-b border-border-subtle pb-2">1. End-to-End Pipeline</h2>
        <div className="relative py-8">
          <div className="absolute left-[39px] sm:left-1/2 sm:-ml-[1px] top-0 bottom-0 w-0.5 bg-gradient-to-b from-transparent via-primary/30 to-transparent">
             <div className="w-full h-1/4 bg-gradient-to-b from-transparent via-primary to-transparent animate-scan absolute top-0"></div>
          </div>

          <div className="space-y-12 relative z-10">
            {/* EMAIL */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <Mail className="w-5 h-5 text-text-secondary" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-right transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-r-4 border-r-primary/50">
                  <h3 className="text-lg font-bold mb-2 text-text-primary">Email</h3>
                  <ul className="text-text-secondary text-sm space-y-1 font-medium list-disc pl-4">
                    <li>User selects an email from Inbox</li>
                    <li>Email subject and body are passed to analysis</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* TEXT PREPROCESSING */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center sm:flex-row-reverse group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <Settings className="w-5 h-5 text-text-primary" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-left transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-l-4 border-l-primary/50">
                  <h3 className="text-lg font-bold mb-2 text-text-primary">Text Preprocessing</h3>
                  <p className="text-text-secondary text-sm mb-3 font-medium">Subject and body are formatted using the canonical preprocessing pipeline.</p>
                  <div className="bg-background/80 p-3 rounded-lg border border-border-subtle font-mono text-xs text-text-muted leading-relaxed whitespace-pre-wrap">
                    [SUBJECT]{"\n"}{"{subject}"}{"\n\n"}[BODY]{"\n"}{"{body}"}
                  </div>
                </div>
              </div>
            </div>

            {/* BERT ANALYSIS */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <BrainCircuit className="w-5 h-5 text-primary" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-right transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-r-4 border-r-primary/50">
                  <div className="absolute inset-0 bg-primary/5 opacity-20 pointer-events-none"></div>
                  <h3 className="text-lg font-bold mb-2 text-primary">BERT Analysis</h3>
                  <ul className="text-text-secondary text-sm space-y-1 font-medium list-disc pl-4 relative z-10">
                    <li>Fine-tuned BERT model analyzes the email</li>
                    <li>Binary classification</li>
                    <li>Class 0 = Legitimate</li>
                    <li>Class 1 = Malicious</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* URL ANALYSIS */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center sm:flex-row-reverse group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <LinkIcon className="w-5 h-5 text-accent" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-left transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-l-4 border-l-primary/50">
                  <h3 className="text-lg font-bold mb-2 text-text-primary">URL Analysis</h3>
                  <ul className="text-text-secondary text-sm space-y-1 font-medium list-disc pl-4">
                    <li>URLs are extracted from the email</li>
                    <li>Static URL indicators are analyzed</li>
                    <li>URLs are NOT visited or executed</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* RISK ASSESSMENT */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <BarChart3 className="w-5 h-5 text-warning" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-right transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-r-4 border-r-primary/50">
                  <h3 className="text-lg font-bold mb-2 text-text-primary">Risk Assessment</h3>
                  <p className="text-text-secondary text-sm mb-3 font-medium">Combines BERT prediction/probability with URL indicators.</p>
                  <div className="bg-background/80 p-3 rounded-lg border border-border-subtle font-mono text-xs text-text-muted leading-relaxed">
                    Produces:<br/>- LOW<br/>- MEDIUM<br/>- HIGH
                  </div>
                </div>
              </div>
            </div>

            {/* FINAL CLASSIFICATION */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center sm:flex-row-reverse group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <ShieldCheck className="w-5 h-5 text-success" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-left transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-l-4 border-l-primary/50">
                  <h3 className="text-lg font-bold mb-4 text-text-primary">Final Classification</h3>
                  <div className="space-y-3 font-mono text-sm">
                    <div className="flex items-center gap-4">
                      <span className="text-text-secondary w-16">LOW</span>
                      <span className="font-bold text-success">🟢 LEGITIMATE</span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-text-secondary w-16">MEDIUM</span>
                      <span className="font-bold text-warning">🟠 SPAM</span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-text-secondary w-16">HIGH</span>
                      <span className="font-bold text-danger">🔴 PHISHING</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* REPORT */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center group">
              <div className="absolute left-[16px] sm:left-1/2 sm:-ml-6 flex items-center justify-center w-12 h-12 rounded-full border-4 border-background bg-surface shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-transform group-hover:scale-110">
                <FileText className="w-5 h-5 text-text-primary" />
              </div>
              <div className="w-full sm:w-1/2 pl-16 sm:pl-0 sm:px-12 sm:text-right transition-all duration-300 group-hover:-translate-y-1">
                <div className="glass-card p-5 relative overflow-hidden text-left border border-r-4 border-r-primary/50">
                  <h3 className="text-lg font-bold mb-2 text-text-primary">Report</h3>
                  <ul className="text-text-secondary text-sm space-y-1 font-medium list-disc pl-4">
                    <li>Complete analysis is stored/generated</li>
                    <li>User can view the detailed report</li>
                  </ul>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* SECTION 2 - BERT MODEL */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-text-primary border-b border-border-subtle pb-2">2. BERT Email Classification Model</h2>
        <div className="glass-card p-8 flex flex-col md:flex-row gap-8 items-start">
          <div className="w-full md:w-1/3 shrink-0 flex items-center justify-center">
            <div className="relative w-48 h-48 bg-primary/5 border border-primary/20 rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(56,189,248,0.1)]">
               <BrainCircuit className="w-16 h-16 text-primary animate-pulse" />
               <div className="absolute inset-0 rounded-full border-[3px] border-primary/30 border-dashed animate-[spin_10s_linear_infinite]"></div>
            </div>
          </div>
          <div className="flex-1 space-y-4">
            <p className="text-text-secondary text-lg leading-relaxed mb-6">
              BERT analyzes the contextual meaning of the email text and estimates whether the message is legitimate or malicious.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-background/50 p-4 rounded-xl border border-border-subtle">
                <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Model</p>
                <p className="font-mono text-sm font-semibold text-text-primary">BERT (bert-base-uncased)</p>
              </div>
              <div className="bg-background/50 p-4 rounded-xl border border-border-subtle">
                <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Task</p>
                <p className="font-mono text-sm font-semibold text-text-primary">Binary Email Classification</p>
              </div>
              <div className="bg-background/50 p-4 rounded-xl border border-border-subtle">
                <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Classes</p>
                <p className="font-mono text-sm font-semibold text-text-primary">0 — Legitimate<br/>1 — Malicious</p>
              </div>
              <div className="bg-background/50 p-4 rounded-xl border border-border-subtle">
                <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Input</p>
                <p className="font-mono text-sm font-semibold text-text-primary">Email Subject + Email Body</p>
              </div>
              <div className="bg-background/50 p-4 rounded-xl border border-border-subtle">
                <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Maximum Sequence Length</p>
                <p className="font-mono text-sm font-semibold text-text-primary">256 tokens</p>
              </div>
              <div className="bg-background/50 p-4 rounded-xl border border-border-subtle">
                <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Framework</p>
                <p className="font-mono text-sm font-semibold text-text-primary">PyTorch + Hugging Face Transformers</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 3 - MODEL PERFORMANCE */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-text-primary border-b border-border-subtle pb-2">3. Model Performance</h2>
        <div className="glass-card p-8 flex flex-col items-center justify-center text-center py-16">
          <div className="w-16 h-16 bg-surface border border-border-strong rounded-full flex items-center justify-center mb-6">
            <BarChart3 className="w-8 h-8 text-text-muted" />
          </div>
          <p className="text-text-secondary text-lg max-w-xl">
            Performance metrics will be displayed after the production BERT model has been fully trained and validated.
          </p>
        </div>
      </section>

      {/* SECTION 4 - RISK CLASSIFICATION */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-text-primary border-b border-border-subtle pb-2">4. Risk Classification</h2>
        <div className="glass-card p-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-32 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
          
          <p className="text-text-secondary text-lg leading-relaxed mb-8 relative z-10 max-w-3xl">
            Risk classification is an application-level assessment based on the BERT malicious probability and static URL indicators. BERT itself remains a binary classifier.
          </p>

          <div className="grid md:grid-cols-3 gap-6 relative z-10">
            <div className="bg-success/5 border border-success/20 p-6 rounded-xl flex flex-col items-center text-center">
              <span className="text-4xl mb-4">🟢</span>
              <p className="font-mono font-bold text-success text-xl tracking-wide mb-1">LOW</p>
              <p className="text-sm text-text-secondary uppercase tracking-widest font-semibold">LEGITIMATE</p>
            </div>
            
            <div className="bg-warning/5 border border-warning/20 p-6 rounded-xl flex flex-col items-center text-center shadow-[0_0_15px_rgba(245,158,11,0.05)]">
              <span className="text-4xl mb-4">🟠</span>
              <p className="font-mono font-bold text-warning text-xl tracking-wide mb-1">MEDIUM</p>
              <p className="text-sm text-text-secondary uppercase tracking-widest font-semibold">SPAM</p>
            </div>
            
            <div className="bg-danger/5 border border-danger/20 p-6 rounded-xl flex flex-col items-center text-center shadow-[0_0_15px_rgba(239,68,68,0.1)]">
              <span className="text-4xl mb-4">🔴</span>
              <p className="font-mono font-bold text-danger text-xl tracking-wide mb-1">HIGH</p>
              <p className="text-sm text-text-secondary uppercase tracking-widest font-semibold">PHISHING</p>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 5 - SECURITY & PRIVACY */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-text-primary border-b border-border-subtle pb-2">5. Security & Privacy</h2>
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
          <div className="glass-card p-6 flex flex-col hover:-translate-y-1 transition-transform">
            <div className="w-10 h-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mb-4">
              <Lock className="w-5 h-5 text-primary" />
            </div>
            <h3 className="font-bold text-text-primary mb-2">No URL Visiting</h3>
            <p className="text-sm text-text-secondary leading-relaxed">URLs are analyzed statically.</p>
          </div>
          
          <div className="glass-card p-6 flex flex-col hover:-translate-y-1 transition-transform">
            <div className="w-10 h-10 rounded-full bg-accent/10 border border-accent/20 flex items-center justify-center mb-4">
              <Shield className="w-5 h-5 text-accent" />
            </div>
            <h3 className="font-bold text-text-primary mb-2">Secure Processing</h3>
            <p className="text-sm text-text-secondary leading-relaxed">Email content is processed through the protected backend.</p>
          </div>
          
          <div className="glass-card p-6 flex flex-col hover:-translate-y-1 transition-transform">
            <div className="w-10 h-10 rounded-full bg-success/10 border border-success/20 flex items-center justify-center mb-4">
              <Key className="w-5 h-5 text-success" />
            </div>
            <h3 className="font-bold text-text-primary mb-2">No Exposed Credentials</h3>
            <p className="text-sm text-text-secondary leading-relaxed">Authentication and OAuth credentials remain backend-side.</p>
          </div>
          
          <div className="glass-card p-6 flex flex-col hover:-translate-y-1 transition-transform">
            <div className="w-10 h-10 rounded-full bg-warning/10 border border-warning/20 flex items-center justify-center mb-4">
              <BrainCircuit className="w-5 h-5 text-warning" />
            </div>
            <h3 className="font-bold text-text-primary mb-2">AI-Based Detection</h3>
            <p className="text-sm text-text-secondary leading-relaxed">BERT analyzes email text for malicious patterns.</p>
          </div>
        </div>
      </section>

      {/* SECTION 6 - TECHNOLOGY STACK */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-text-primary border-b border-border-subtle pb-2">6. Technology Stack</h2>
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-surface/50 p-4 rounded-xl border border-border-subtle flex items-center">
            <Layout className="w-6 h-6 text-primary mr-4 shrink-0" />
            <div>
              <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Frontend</p>
              <p className="font-mono text-sm text-text-primary font-semibold">React + Vite</p>
            </div>
          </div>
          
          <div className="bg-surface/50 p-4 rounded-xl border border-border-subtle flex items-center">
            <Database className="w-6 h-6 text-accent mr-4 shrink-0" />
            <div>
              <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Backend</p>
              <p className="font-mono text-sm text-text-primary font-semibold">FastAPI + Python</p>
            </div>
          </div>
          
          <div className="bg-surface/50 p-4 rounded-xl border border-border-subtle flex items-center">
            <BrainCircuit className="w-6 h-6 text-warning mr-4 shrink-0" />
            <div>
              <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">AI/ML</p>
              <p className="font-mono text-sm text-text-primary font-semibold">BERT + PyTorch + Hugging Face Transformers</p>
            </div>
          </div>
          
          <div className="bg-surface/50 p-4 rounded-xl border border-border-subtle flex items-center">
            <FileText className="w-6 h-6 text-success mr-4 shrink-0" />
            <div>
              <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Analysis</p>
              <p className="font-mono text-sm text-text-primary font-semibold">URL Extraction + Risk Assessment</p>
            </div>
          </div>
          
          <div className="bg-surface/50 p-4 rounded-xl border border-border-subtle flex items-center md:col-span-2">
            <Database className="w-6 h-6 text-text-secondary mr-4 shrink-0" />
            <div>
              <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">Database</p>
              <p className="font-mono text-sm text-text-primary font-semibold">Existing project database</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
