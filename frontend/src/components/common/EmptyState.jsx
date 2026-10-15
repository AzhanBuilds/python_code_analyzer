import React from 'react';
import { Play, Sparkles, Terminal } from 'lucide-react';

export const EmptyState = ({ onAnalyze }) => {
  return (
    <div className="flex flex-col items-center justify-center p-10 text-center rounded-xl bg-dark-900/60 border border-dark-700/60 space-y-4">
      <div className="p-3 rounded-full bg-dark-800 border border-dark-700 text-emerald-400">
        <Terminal className="w-6 h-6" />
      </div>
      <div>
        <h4 className="text-sm font-semibold text-white">Ready for Analysis</h4>
        <p className="text-xs text-slate-400 mt-1 max-w-sm">
          Click <span className="text-emerald-400 font-semibold">Analyze Code</span> to run static syntax inspection, compute complexity, and generate actionable improvement insights.
        </p>
      </div>

      {onAnalyze && (
        <button
          onClick={onAnalyze}
          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-md shadow-emerald-950/40 cursor-pointer"
        >
          <Play className="w-3.5 h-3.5 fill-current" />
          <span>Analyze Code Now</span>
        </button>
      )}
    </div>
  );
};

export default EmptyState;
