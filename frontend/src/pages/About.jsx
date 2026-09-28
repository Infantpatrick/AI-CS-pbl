import React from 'react';
import { Shield, Brain, LayoutTemplate, Lock, Cpu, Server, FileCode2 } from 'lucide-react';

export default function About() {
  return (
    <div className="max-w-4xl mx-auto space-y-12 pb-12 pt-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="text-center relative">
        <div className="absolute top-0 left-1/2 -ml-32 p-32 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>
        <Shield className="w-20 h-20 text-primary mx-auto mb-6 relative z-10 drop-shadow-[0_0_15px_rgba(56,189,248,0.5)]" />
        <h2 className="text-4xl font-bold mb-4 text-text-primary tracking-tight relative z-10">PhishGuard AI</h2>
        <p className="text-primary text-xl font-mono uppercase tracking-widest relative z-10 mb-2">v1.0.0 Production</p>
        <p className="text-text-secondary text-lg max-w-2xl mx-auto relative z-10">Advanced AI-Based Email Phishing Detection Platform</p>
      </div>

      <section className="glass-card p-8 relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-transparent to-accent/5 opacity-50 group-hover:opacity-100 transition-opacity"></div>
        <h3 className="text-2xl font-bold text-text-primary mb-6 relative z-10 text-center">AI-Based Email Phishing Detection Using BERT</h3>
        
        <div className="grid md:grid-cols-2 gap-6 relative z-10 max-w-3xl mx-auto">
          <div className="space-y-4">
            <div className="flex flex-col bg-background/50 p-3 rounded-lg border border-border-subtle">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Model</span>
              <span className="font-mono text-primary font-bold">bert-base-uncased</span>
            </div>
            <div className="flex flex-col bg-background/50 p-3 rounded-lg border border-border-subtle">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Framework</span>
              <span className="font-mono text-text-primary">PyTorch + Hugging Face Transformers</span>
            </div>
            <div className="flex flex-col bg-background/50 p-3 rounded-lg border border-border-subtle">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Dataset</span>
              <span className="font-mono text-text-primary">87,886 cleaned emails</span>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex flex-col bg-background/50 p-3 rounded-lg border border-border-subtle">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Classes</span>
              <span className="font-mono text-text-primary">0 = Legitimate, 1 = Phishing</span>
            </div>
            <div className="flex flex-col bg-background/50 p-3 rounded-lg border border-border-subtle">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Backend</span>
              <span className="font-mono text-success">FastAPI</span>
            </div>
            <div className="flex flex-col bg-background/50 p-3 rounded-lg border border-border-subtle">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Frontend</span>
              <span className="font-mono text-primary-strong">React + Vite</span>
            </div>
          </div>
        </div>

        <p className="text-text-secondary text-sm leading-relaxed max-w-3xl mx-auto mt-8 relative z-10 text-center italic border-t border-border-strong pt-4">
          "BERT-based email phishing classification using bert-base-uncased."
        </p>
      </section>

      <section className="space-y-6">
        <h3 className="text-2xl font-bold text-text-primary text-center tracking-tight mb-8">Technology Stack</h3>
        <div className="grid md:grid-cols-2 gap-6">
          
          <div className="glass-card p-6 hover:-translate-y-1 transition-transform group">
            <div className="flex items-center mb-4">
              <div className="p-2.5 rounded-lg bg-accent/20 border border-accent/30 mr-4 group-hover:bg-accent/30 transition-colors">
                <Brain className="w-6 h-6 text-accent" />
              </div>
              <h4 className="text-lg font-bold text-text-primary">AI & Inference</h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {['BERT', 'PyTorch', 'Transformers', 'NumPy', 'Scikit-learn'].map(tech => (
                <span key={tech} className="px-3 py-1 bg-background/80 border border-border-subtle rounded-md text-xs font-mono text-text-secondary hover:text-text-primary hover:border-accent/50 transition-colors">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          <div className="glass-card p-6 hover:-translate-y-1 transition-transform group">
            <div className="flex items-center mb-4">
              <div className="p-2.5 rounded-lg bg-success/20 border border-success/30 mr-4 group-hover:bg-success/30 transition-colors">
                <Server className="w-6 h-6 text-success" />
              </div>
              <h4 className="text-lg font-bold text-text-primary">Backend API</h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {['Python 3.10+', 'FastAPI', 'Uvicorn', 'Pydantic', 'REST'].map(tech => (
                <span key={tech} className="px-3 py-1 bg-background/80 border border-border-subtle rounded-md text-xs font-mono text-text-secondary hover:text-text-primary hover:border-success/50 transition-colors">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          <div className="glass-card p-6 hover:-translate-y-1 transition-transform group md:col-span-2">
            <div className="flex items-center mb-4">
              <div className="p-2.5 rounded-lg bg-primary/20 border border-primary/30 mr-4 group-hover:bg-primary/30 transition-colors">
                <LayoutTemplate className="w-6 h-6 text-primary" />
              </div>
              <h4 className="text-lg font-bold text-text-primary">Frontend Interface</h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {['React 18', 'Vite', 'Tailwind CSS v3', 'Lucide Icons', 'React Router'].map(tech => (
                <span key={tech} className="px-3 py-1 bg-background/80 border border-border-subtle rounded-md text-xs font-mono text-text-secondary hover:text-text-primary hover:border-primary/50 transition-colors">
                  {tech}
                </span>
              ))}
            </div>
          </div>

        </div>
      </section>

      <section className="glass-card bg-surface/50 p-8 border-border-strong relative overflow-hidden">
        <div className="absolute right-0 bottom-0 p-32 bg-warning/5 rounded-full blur-3xl -mr-16 -mb-16 pointer-events-none"></div>
        <div className="flex items-center mb-6 relative z-10">
          <Lock className="w-6 h-6 text-text-primary mr-3" />
          <h3 className="text-xl font-bold text-text-primary">Security & Privacy Principles</h3>
        </div>
        <ul className="space-y-4 relative z-10">
          <li className="flex items-start bg-background/50 p-4 rounded-xl border border-border-subtle">
            <span className="w-2 h-2 rounded-full bg-primary mt-1.5 mr-3 shrink-0"></span>
            <div>
              <strong className="block text-sm text-text-primary mb-1 tracking-wide uppercase">Static Extraction Only</strong>
              <span className="text-sm text-text-secondary leading-relaxed">URLs are parsed dynamically via regex but are strictly isolated. They are never resolved, fetched, or executed by the backend engine.</span>
            </div>
          </li>
          <li className="flex items-start bg-background/50 p-4 rounded-xl border border-border-subtle">
            <span className="w-2 h-2 rounded-full bg-accent mt-1.5 mr-3 shrink-0"></span>
            <div>
              <strong className="block text-sm text-text-primary mb-1 tracking-wide uppercase">Volatile Memory Processing</strong>
              <span className="text-sm text-text-secondary leading-relaxed">User email payloads exist only in RAM during the inference lifecycle. No caching, no database persistence, and no logs containing PII.</span>
            </div>
          </li>
          <li className="flex items-start bg-background/50 p-4 rounded-xl border border-border-subtle">
            <span className="w-2 h-2 rounded-full bg-success mt-1.5 mr-3 shrink-0"></span>
            <div>
              <strong className="block text-sm text-text-primary mb-1 tracking-wide uppercase">Client-Side Obfuscation</strong>
              <span className="text-sm text-text-secondary leading-relaxed">The frontend acts as a dumb terminal. No API secrets or critical classification rules are exposed to the client browser.</span>
            </div>
          </li>
        </ul>
      </section>

      <section className="p-6 border border-border-subtle border-dashed rounded-xl text-center bg-background/30">
        <Cpu className="w-6 h-6 text-text-muted mx-auto mb-3 opacity-50" />
        <h3 className="text-sm font-bold text-text-muted uppercase tracking-widest mb-4">Future Capabilities</h3>
        <div className="flex flex-wrap justify-center gap-3">
          <span className="text-xs text-text-secondary bg-elevated px-3 py-1.5 rounded-full">Ensemble modeling</span>
          <span className="text-xs text-text-secondary bg-elevated px-3 py-1.5 rounded-full">External Threat Feeds</span>
          <span className="text-xs text-text-secondary bg-elevated px-3 py-1.5 rounded-full">DKIM/SPF Validation</span>
        </div>
      </section>
    </div>
  );
}
