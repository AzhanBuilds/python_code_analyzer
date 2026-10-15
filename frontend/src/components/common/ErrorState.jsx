import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorState = ({ message, onRetry }) => {
  return (
    <div className="p-6 rounded-xl bg-rose-950/20 border border-rose-500/30 text-rose-200 space-y-3">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-semibold text-rose-300">Analysis Error</h4>
          <p className="text-xs text-rose-200/80 mt-1 leading-relaxed">
            {message || 'Unable to connect to the analyzer. Check that the Flask backend is running and try again.'}
          </p>
        </div>
      </div>

      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-lg bg-rose-900/40 hover:bg-rose-900/60 text-rose-200 border border-rose-500/30 transition-all cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Analysis</span>
        </button>
      )}
    </div>
  );
};

export default ErrorState;
