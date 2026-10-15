import React from 'react';
import { Loader2, Cpu } from 'lucide-react';

export const LoadingState = () => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center rounded-xl bg-dark-900/60 border border-dark-700/60 space-y-4">
      <div className="relative">
        <div className="w-14 h-14 rounded-full border-2 border-emerald-500/20 border-t-emerald-400 animate-spin flex items-center justify-center" />
        <Cpu className="w-6 h-6 text-emerald-400 absolute inset-0 m-auto animate-pulse" />
      </div>
      <div>
        <h4 className="text-sm font-semibold text-white">Analyzing Python Source</h4>
        <p className="text-xs text-slate-400 mt-1 max-w-xs font-mono">
          Parsing AST, evaluating token streams, computing cyclomatic complexity and static rules...
        </p>
      </div>
    </div>
  );
};

export default LoadingState;
