import React from 'react';
import QualityScore from './QualityScore';
import MetricsGrid from './MetricsGrid';
import WarningsPanel from './WarningsPanel';
import SuggestionsPanel from './SuggestionsPanel';
import TodoFixmePanel from './TodoFixmePanel';
import LoadingState from '../common/LoadingState';
import ErrorState from '../common/ErrorState';
import EmptyState from '../common/EmptyState';
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  Clock,
} from 'lucide-react';

export const AnalysisResults = ({
  result,
  status,
  errorMessage,
  onRetry,
  onNavigate,
  onAnalyze,
}) => {
  // Determine output state banner
  const getStatusBadge = () => {
    switch (status) {
      case 'loading':
        return {
          icon: Clock,
          text: 'Analyzing code...',
          color: 'text-amber-400 border-amber-500/30 bg-amber-500/10',
        };
      case 'success':
        return {
          icon: CheckCircle2,
          text: 'Analysis completed',
          color: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
        };
      case 'syntax_error':
        return {
          icon: AlertTriangle,
          text: 'Syntax error detected',
          color: 'text-rose-400 border-rose-500/30 bg-rose-500/10',
        };
      case 'error':
        return {
          icon: XCircle,
          text: 'Analysis failed',
          color: 'text-rose-400 border-rose-500/30 bg-rose-500/10',
        };
      case 'idle':
      default:
        return {
          icon: HelpCircle,
          text: 'Ready to analyze',
          color: 'text-slate-400 border-dark-700 bg-dark-800',
        };
    }
  };

  const statusBadge = getStatusBadge();
  const StatusIcon = statusBadge.icon;

  return (
    <div className="flex flex-col h-full bg-dark-900 border border-dark-700/80 rounded-xl overflow-hidden shadow-xl">
      {/* 1. Header: ANALYSIS OUTPUT */}
      <div className="flex items-center justify-between px-4 py-3 bg-dark-850/90 border-b border-dark-700/70">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-400" />
          <h2 className="text-xs font-bold tracking-wider uppercase text-white">
            Analysis Output
          </h2>
        </div>
        <div
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-medium border ${statusBadge.color}`}
        >
          <StatusIcon className="w-3.5 h-3.5" />
          <span>{statusBadge.text}</span>
        </div>
      </div>

      {/* Main Results Body */}
      <div className="flex-1 p-4 lg:p-5 overflow-y-auto space-y-6">
        {status === 'loading' && <LoadingState />}

        {status === 'error' && (
          <ErrorState message={errorMessage} onRetry={onRetry} />
        )}

        {status === 'idle' && <EmptyState onAnalyze={onAnalyze} />}

        {(status === 'success' || status === 'syntax_error') && result && (
          <>
            {/* Syntax Error Diagnostic Banner if present */}
            {status === 'syntax_error' && result.syntax_error && (
              <div
                onClick={() =>
                  result.syntax_error.line && onNavigate(result.syntax_error.line)
                }
                className="p-3.5 rounded-xl bg-rose-950/30 border border-rose-500/40 text-rose-200 cursor-pointer hover:border-rose-400 transition-all group"
              >
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40">
                      {result.syntax_error.category || 'SyntaxError'}
                    </span>
                    {result.syntax_error.line && (
                      <span className="text-[11px] font-mono font-bold px-2 py-0.5 rounded bg-dark-900 text-rose-300 border border-rose-800">
                        LINE {result.syntax_error.line}
                        {result.syntax_error.column ? ` : COL ${result.syntax_error.column}` : ''}
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] text-rose-300/80 group-hover:text-rose-200">
                    Click to view error line
                  </span>
                </div>
                <div className="text-xs font-mono text-rose-200 mt-1">
                  {result.syntax_error.message}
                </div>
                {result.syntax_error.text && (
                  <div className="mt-2 text-xs font-mono p-2 rounded bg-dark-950/80 border border-rose-900/60 text-slate-300 overflow-x-auto">
                    {result.syntax_error.text}
                  </div>
                )}
              </div>
            )}

            {/* 2. QUALITY SCORE */}
            <QualityScore score={result.quality_score} status={status} />

            {/* 3. CODE METRICS */}
            <MetricsGrid metrics={result.metrics} />

            {/* 4. WARNINGS */}
            <WarningsPanel warnings={result.warnings} onNavigate={onNavigate} />

            {/* 5. SUGGESTIONS */}
            <SuggestionsPanel suggestions={result.suggestions} onNavigate={onNavigate} />

            {/* 6. TODO / FIXME */}
            <TodoFixmePanel
              todos={result.todos}
              fixmes={result.fixmes}
              onNavigate={onNavigate}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default AnalysisResults;
