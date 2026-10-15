import React from 'react';
import { ListTodo, CheckCircle2, ArrowUpRight } from 'lucide-react';

export const TodoFixmePanel = ({ todos = [], fixmes = [], onNavigate }) => {
  const allMarkers = [
    ...todos.map((t) => ({ ...t, badgeColor: 'bg-sky-500/20 text-sky-300 border-sky-500/30' })),
    ...fixmes.map((f) => ({ ...f, badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/30' })),
  ].sort((a, b) => a.line - b.line);

  const count = allMarkers.length;

  return (
    <div className="space-y-2.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ListTodo className="w-4 h-4 text-sky-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            TODO / FIXME
          </h3>
        </div>
        <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-dark-800 text-slate-300 border border-dark-700">
          {count}
        </span>
      </div>

      {count === 0 ? (
        <div className="flex items-center gap-2.5 p-3 rounded-lg bg-dark-850/60 border border-dark-700/60 text-slate-400 text-xs">
          <CheckCircle2 className="w-4 h-4 text-slate-500 flex-shrink-0" />
          <span>No TODO or FIXME comments detected.</span>
        </div>
      ) : (
        <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
          {allMarkers.map((item, idx) => (
            <div
              key={`${item.type}-${item.line}-${idx}`}
              onClick={() => onNavigate && item.line && onNavigate(item.line)}
              className="p-3 rounded-lg bg-dark-850/90 border border-dark-700/70 hover:border-sky-500/40 transition-all cursor-pointer group"
            >
              <div className="flex items-center justify-between gap-2 mb-1">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${item.badgeColor}`}>
                    {item.type}
                  </span>
                  <span className="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-dark-900 border border-dark-700 text-slate-300 group-hover:text-sky-300">
                    LINE {item.line}
                  </span>
                </div>
                <span className="text-[10px] text-slate-400 group-hover:text-sky-400 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                  <span>Jump to line</span>
                  <ArrowUpRight className="w-3 h-3" />
                </span>
              </div>
              <div className="text-xs font-mono text-slate-300 pl-1">
                {item.comment}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TodoFixmePanel;
