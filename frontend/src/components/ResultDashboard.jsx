import React from 'react';
import { ShieldAlert, ShieldCheck, Info, PieChart, Activity, AlertTriangle } from 'lucide-react';
import { cn } from './EmailAnalyzer';
import URLAnalysis from './URLAnalysis';
import { getAppClassification } from '../api/normalizers';

const ResultDashboard = ({ result }) => {
  if (!result) return null;

  const {
    prediction,
    phishing_probability,
    legitimate_probability,
    confidence,
    risk_level,
    urls_found,
    url_indicators,
    risk_reasons
  } = result;

  const isHighRisk = risk_level === 'HIGH';
  const isMediumRisk = risk_level === 'MEDIUM';
  const isLowRisk = risk_level === 'LOW';

  const formatProb = (val) => Math.round(val * 100);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 relative z-10 animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-3xl font-bold text-white">Analysis Results</h2>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-400">Confidence Score:</span>
          <span className="px-3 py-1 bg-white/10 rounded-full text-white font-bold text-sm border border-white/10">
            {formatProb(confidence)}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Main Classification Card */}
        <div className={cn(
          "glass-card p-8 lg:col-span-2 relative overflow-hidden flex flex-col justify-center min-h-[300px]",
          isHighRisk ? "shadow-[0_0_40px_rgba(239,68,68,0.15)] border-red-500/30" :
          isMediumRisk ? "shadow-[0_0_40px_rgba(245,158,11,0.15)] border-amber-500/30" :
          "shadow-[0_0_40px_rgba(16,185,129,0.15)] border-green-500/30"
        )}>
          {/* Background Glow */}
          <div className={cn(
            "absolute top-0 right-0 w-64 h-64 rounded-full blur-[100px] -z-10 opacity-50",
            isHighRisk ? "bg-red-500" : isMediumRisk ? "bg-amber-500" : "bg-green-500"
          )}></div>

          <div className="flex flex-col md:flex-row items-center gap-8 z-10">
            <div className={cn(
              "w-32 h-32 rounded-full flex items-center justify-center flex-shrink-0 relative",
              isHighRisk ? "bg-red-500/10" : isMediumRisk ? "bg-amber-500/10" : "bg-green-500/10"
            )}>
              {/* Outer ring */}
              <div className={cn(
                "absolute inset-0 rounded-full border-4 opacity-20",
                isHighRisk ? "border-red-500" : isMediumRisk ? "border-amber-500" : "border-green-500"
              )}></div>
              
              {isHighRisk ? (
                <ShieldAlert className="w-16 h-16 text-red-500" />
              ) : isMediumRisk ? (
                <AlertTriangle className="w-16 h-16 text-amber-500" />
              ) : (
                <ShieldCheck className="w-16 h-16 text-green-500" />
              )}
            </div>

            <div className="text-center md:text-left flex-1">
              <p className="text-sm font-semibold tracking-wider text-gray-400 uppercase mb-2">Application Classification</p>
              <h3 className={cn(
                "text-4xl sm:text-5xl font-extrabold mb-2 uppercase",
                isHighRisk ? "text-red-400" : isMediumRisk ? "text-amber-400" : "text-green-400"
              )}>
                {getAppClassification(risk_level) === 'PHISHING' ? '🔴 PHISHING' : getAppClassification(risk_level) === 'SPAM' ? '🟠 SPAM' : '🟢 LEGITIMATE'}
              </h3>
              <p className="text-sm font-medium text-gray-400 mb-4 uppercase tracking-widest border-t border-white/10 pt-2 inline-block">
                BERT Prediction: <span className={prediction === 'PHISHING' ? 'text-red-400' : 'text-green-400'}>{prediction}</span>
              </p>
              
              {/* Probability Bars */}
              <div className="space-y-4 mt-6">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-400 font-medium">Phishing Probability</span>
                    <span className="text-red-400 font-bold">{formatProb(phishing_probability)}%</span>
                  </div>
                  <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 rounded-full transition-all duration-1000" style={{ width: `${formatProb(phishing_probability)}%` }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-400 font-medium">Legitimate Probability</span>
                    <span className="text-green-400 font-bold">{formatProb(legitimate_probability)}%</span>
                  </div>
                  <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-green-500 rounded-full transition-all duration-1000" style={{ width: `${formatProb(legitimate_probability)}%` }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Risk Assessment & Reasons */}
        <div className="glass-card p-6 flex flex-col h-full">
          <div className="flex items-center gap-3 mb-6">
            <Activity className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold text-white">Risk Assessment</h3>
          </div>
          
          <div className="mb-6 flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
            <span className="text-gray-300 font-medium">Overall Risk</span>
            <span className={cn(
              "px-4 py-1.5 rounded-md font-bold tracking-widest uppercase text-sm",
              isHighRisk ? "bg-red-500/20 text-red-400 border border-red-500/30" : 
              isMediumRisk ? "bg-amber-500/20 text-amber-400 border border-amber-500/30" : 
              "bg-green-500/20 text-green-400 border border-green-500/30"
            )}>
              {risk_level}
            </span>
          </div>

          <div className="flex-1">
            <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
              <Info className="w-4 h-4" /> Why this classification?
            </h4>
            <ul className="space-y-3">
              {risk_reasons?.map((reason, idx) => (
                <li key={idx} className="text-sm text-gray-300 bg-white/5 p-3 rounded-lg border border-white/5 flex items-start gap-2">
                  <span className={cn(
                    "w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0",
                    isHighRisk ? "bg-red-400" : isMediumRisk ? "bg-amber-400" : "bg-green-400"
                  )}></span>
                  {reason}
                </li>
              ))}
              {(!risk_reasons || risk_reasons.length === 0) && (
                <li className="text-sm text-gray-500 italic">No specific reasons provided by the model.</li>
              )}
            </ul>
          </div>
        </div>

        {/* URL Analysis Section */}
        <div className="lg:col-span-3 h-[350px]">
          <URLAnalysis urlsFound={urls_found} urlIndicators={url_indicators} />
        </div>

      </div>
    </div>
  );
};

export default ResultDashboard;
