import React from 'react';
import { getSeverityColor } from '../../utils/formatAnalysis';
import { AlertTriangle, ArrowUpRight } from 'lucide-react';

export const WarningItem = ({ warning, onNavigate }) => {
  const line = warning.line;
  const severity = warning.severity || 'Low';
  const colors = getSeverityColor(severity);

  return (
    <div
      onClick={() => onNavigate && line && onNavigate(line)}
      className={`p-3 rounded-lg border ${colors.border} ${colors.bg} hover:border-slate-500/50 transition-all cursor-pointer group`}
    >
      <div className="flex items-center justify-between gap-2 mb-1.5">
        <div className="flex items-center gap-2">
          {line && (
            <span className="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-dark-900 border border-dark-700 text-slate-300 group-hover:border-emerald-500/50 group-hover:text-emerald-300 transition-colors">
              LINE {line}
            </span>
          )}
          <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded border ${colors.badge}`}>
            {severity}
          </span>
          <span className="text-[10px] font-mono text-slate-400">
            {warning.rule_id || warning.code}
          </span>
        </div>

        {line && (
          <span className="text-[10px] text-slate-400 group-hover:text-emerald-400 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
            <span>Jump to line</span>
            <ArrowUpRight className="w-3 h-3" />
          </span>
        )}
      </div>

      <div className="text-xs font-medium text-slate-200 mb-1">
        {warning.message}
      </div>

      {warning.suggestion && (
        <div className="text-[11px] text-slate-400 bg-dark-900/60 p-2 rounded border border-dark-800 font-mono">
          <span className="text-emerald-400 font-semibold mr-1.5">Fix:</span>
          {warning.suggestion}
        </div>
      )}
    </div>
  );
};

export default WarningItem;
