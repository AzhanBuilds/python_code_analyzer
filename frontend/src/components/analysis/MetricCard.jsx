import React from 'react';

export const MetricCard = ({ label, value, icon: Icon, description }) => {
  return (
    <div className="p-3 rounded-lg bg-dark-850/80 border border-dark-700/60 hover:border-dark-600 transition-all group">
      <div className="flex items-center justify-between text-slate-400 mb-1.5">
        <span className="text-[11px] font-medium text-slate-400 group-hover:text-slate-300">
          {label}
        </span>
        {Icon && <Icon className="w-3.5 h-3.5 text-emerald-400/70 group-hover:text-emerald-400" />}
      </div>
      <div className="text-xl font-bold font-mono text-white tracking-tight">
        {value !== null && value !== undefined ? value : '--'}
      </div>
      {description && (
        <div className="text-[10px] text-slate-400 mt-0.5 truncate" title={description}>
          {description}
        </div>
      )}
    </div>
  );
};

export default MetricCard;
