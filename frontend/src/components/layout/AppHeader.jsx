import React from 'react';
import { Terminal, ShieldCheck, Activity, Cpu } from 'lucide-react';

export const AppHeader = ({ backendReady }) => {
  return (
    <header className="border-b border-dark-700/60 bg-dark-900/80 backdrop-blur-md sticky top-0 z-50 px-4 lg:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-forest-900/60 border border-forest-500/30 text-forest-400 shadow-lg shadow-forest-950/50">
            <Cpu className="w-5 h-5 text-emerald-400 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
                Python Code Analyzer
              </h1>
              <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                v1.0 AST Engine
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Static analysis and code-quality insights without execution
            </p>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex items-center gap-3 self-end sm:self-auto text-xs font-mono">
          <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-md bg-dark-800/80 border border-dark-700 text-slate-300">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Zero-Execution Sandbox</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1 rounded-md bg-dark-800/80 border border-dark-700">
            <span
              className={`w-2 h-2 rounded-full ${
                backendReady === true
                  ? 'bg-emerald-400 shadow-[0_0_8px_#10b981]'
                  : backendReady === false
                  ? 'bg-rose-400 shadow-[0_0_8px_#f43f5e]'
                  : 'bg-amber-400 animate-pulse'
              }`}
            />
            <span className="text-slate-300">
              {backendReady === true
                ? 'Backend Ready'
                : backendReady === false
                ? 'Backend Offline'
                : 'Connecting...'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AppHeader;
