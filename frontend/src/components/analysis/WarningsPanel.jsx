import React from 'react';
import WarningItem from './WarningItem';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

export const WarningsPanel = ({ warnings = [], onNavigate }) => {
  const count = warnings.length;

  return (
    <div className="space-y-2.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            Warnings
          </h3>
        </div>
        <span
          className={`text-xs font-mono font-bold px-2 py-0.5 rounded-full ${
            count > 0
              ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
          }`}
        >
          {count}
        </span>
      </div>

      {count === 0 ? (
        <div className="flex items-center gap-2.5 p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/20 text-emerald-300 text-xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>No warnings found. Code conforms to current inspection rules.</span>
        </div>
      ) : (
        <div className="space-y-2 max-h-[280px] overflow-y-auto pr-1">
          {warnings.map((w, index) => (
            <WarningItem key={`${w.code}-${w.line}-${index}`} warning={w} onNavigate={onNavigate} />
          ))}
        </div>
      )}
    </div>
  );
};

export default WarningsPanel;
