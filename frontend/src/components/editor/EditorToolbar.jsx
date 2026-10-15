import React from 'react';
import { Play, RotateCcw, FileCode, Loader2 } from 'lucide-react';

export const EditorToolbar = ({
  onAnalyze,
  onClear,
  onLoadExample,
  loading,
  lineCount,
  charCount,
}) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2.5 px-4 py-2.5 bg-dark-850 border-b border-dark-700/80">
      {/* Primary Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={onAnalyze}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white transition-all shadow-md shadow-emerald-950/40 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {loading ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-100" />
              <span>Analyzing Code...</span>
            </>
          ) : (
            <>
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Analyze Code</span>
            </>
          )}
        </button>

        <button
          onClick={() => onLoadExample('advanced')}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg bg-dark-800 hover:bg-dark-700 active:scale-95 text-slate-300 hover:text-white border border-dark-600/80 transition-all disabled:opacity-50 cursor-pointer"
        >
          <FileCode className="w-3.5 h-3.5 text-emerald-400" />
          <span>Load Example</span>
        </button>

        <button
          onClick={onClear}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg bg-dark-800 hover:bg-rose-950/40 hover:text-rose-300 active:scale-95 text-slate-400 border border-dark-600/80 hover:border-rose-900/50 transition-all disabled:opacity-50 cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Clear</span>
        </button>
      </div>

      {/* Editor Line / Char Meta */}
      <div className="flex items-center gap-3 text-[11px] font-mono text-slate-400">
        <span className="px-2 py-0.5 rounded bg-dark-900 border border-dark-700/60">
          {lineCount} {lineCount === 1 ? 'line' : 'lines'}
        </span>
        <span className="px-2 py-0.5 rounded bg-dark-900 border border-dark-700/60">
          {charCount} chars
        </span>
      </div>
    </div>
  );
};

export default EditorToolbar;
