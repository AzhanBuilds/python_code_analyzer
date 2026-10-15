import React from 'react';
import { Lightbulb, CheckCircle2, ArrowUpRight } from 'lucide-react';

export const SuggestionsPanel = ({ suggestions = [], onNavigate }) => {
  const count = suggestions.length;

  return (
    <div className="space-y-2.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Lightbulb className="w-4 h-4 text-emerald-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            Suggestions
          </h3>
        </div>
        <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-dark-800 text-slate-300 border border-dark-700">
          {count}
        </span>
      </div>

      {count === 0 ? (
        <div className="flex items-center gap-2.5 p-3 rounded-lg bg-dark-850/60 border border-dark-700/60 text-slate-400 text-xs">
          <CheckCircle2 className="w-4 h-4 text-slate-500 flex-shrink-0" />
          <span>No suggestions available.</span>
        </div>
      ) : (
        <div className="space-y-2 max-h-[240px] overflow-y-auto pr-1">
          {suggestions.map((s, idx) => (
            <div
              key={`${s.code}-${s.line}-${idx}`}
              onClick={() => onNavigate && s.line && onNavigate(s.line)}
              className="p-3 rounded-lg bg-dark-850/90 border border-dark-700/70 hover:border-emerald-500/40 transition-all cursor-pointer group"
            >
              <div className="flex items-center justify-between gap-2 mb-1">
                <div className="flex items-center gap-2">
                  {s.line && (
                    <span className="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-dark-900 border border-dark-700 text-slate-300 group-hover:text-emerald-300">
                      LINE {s.line}
                    </span>
                  )}
                  <span className="text-[11px] font-mono text-emerald-400">
                    {s.rule_id || s.code}
                  </span>
                </div>
                {s.line && (
                  <span className="text-[10px] text-slate-400 group-hover:text-emerald-400 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <span>Jump to line</span>
                    <ArrowUpRight className="w-3 h-3" />
                  </span>
                )}
              </div>
              <div className="text-xs text-slate-300">
                {s.message}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SuggestionsPanel;
