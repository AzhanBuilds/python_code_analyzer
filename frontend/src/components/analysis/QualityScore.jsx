import React from 'react';
import { getScoreColor } from '../../utils/formatAnalysis';
import { Award, ShieldAlert, Sparkles } from 'lucide-react';

export const QualityScore = ({ score, status }) => {
  const isSyntaxError = status === 'syntax_error' || score === null;
  const color = getScoreColor(isSyntaxError ? null : score);

  // SVG circular gauge properties
  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const validScore = score !== null && score !== undefined ? Math.max(0, Math.min(100, score)) : 0;
  const strokeDashoffset = isSyntaxError
    ? circumference
    : circumference - (validScore / 100) * circumference;

  return (
    <div className={`p-4 rounded-xl border ${color.border} ${color.bg} transition-all`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Award className={`w-4 h-4 ${color.text}`} />
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            Quality Score
          </span>
        </div>
        <span
          className={`text-xs font-mono font-medium px-2.5 py-0.5 rounded-full border ${color.border} ${color.text} bg-dark-900/60`}
        >
          {color.label}
        </span>
      </div>

      <div className="flex items-center justify-between gap-4">
        {/* Score Numbers */}
        <div>
          {isSyntaxError ? (
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-slate-400 font-mono">--</span>
              <span className="text-xs text-slate-400 font-mono">/ 100</span>
            </div>
          ) : (
            <div className="flex items-baseline gap-1.5">
              <span className={`text-4xl font-extrabold font-mono tracking-tight ${color.text}`}>
                {score}
              </span>
              <span className="text-sm font-semibold text-slate-400 font-mono">/ 100</span>
            </div>
          )}

          <p className="text-xs text-slate-400 mt-1 max-w-[260px]">
            {isSyntaxError
              ? 'Syntax error detected. Fix code syntax to compute structural score.'
              : score >= 90
              ? 'Exceptional code quality with few or zero static findings.'
              : score >= 75
              ? 'Clean code with minor suggestions or style improvements.'
              : score >= 60
              ? 'Multiple warnings or complexity flags detected.'
              : 'Significant issues or code defects requiring refactoring.'}
          </p>
        </div>

        {/* Circular Gauge */}
        <div className="relative w-20 h-20 flex-shrink-0 flex items-center justify-center">
          <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 96 96">
            {/* Background ring */}
            <circle
              cx="48"
              cy="48"
              r={radius}
              className="text-dark-800"
              strokeWidth="7"
              stroke="currentColor"
              fill="transparent"
            />
            {/* Value ring */}
            <circle
              cx="48"
              cy="48"
              r={radius}
              stroke={color.stroke}
              strokeWidth="7"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-700 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center font-mono">
            <span className={`text-xs font-bold ${color.text}`}>
              {isSyntaxError ? 'N/A' : `${score}%`}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QualityScore;
