import React from 'react';
import MetricCard from './MetricCard';
import {
  FileText,
  Boxes,
  Layers,
  ArrowDownLeft,
  Repeat,
  GitFork,
  MessageSquare,
  Activity,
} from 'lucide-react';

export const MetricsGrid = ({ metrics }) => {
  const m = metrics || {};

  const items = [
    {
      label: 'Total Lines',
      value: m.total_lines,
      icon: FileText,
      description: 'Physical source lines',
    },
    {
      label: 'Functions',
      value: m.functions,
      icon: Boxes,
      description: 'Sync & async definitions',
    },
    {
      label: 'Classes',
      value: m.classes,
      icon: Layers,
      description: 'Class structures',
    },
    {
      label: 'Imports',
      value: m.imports,
      icon: ArrowDownLeft,
      description: 'Import statements',
    },
    {
      label: 'Loops',
      value: m.loops,
      icon: Repeat,
      description: 'For, AsyncFor & While',
    },
    {
      label: 'Conditions',
      value: m.conditions,
      icon: GitFork,
      description: 'If & ternary branches',
    },
    {
      label: 'Comments',
      value: m.comments,
      icon: MessageSquare,
      description: 'Tokenized comments',
    },
    {
      label: 'Cyclomatic Complexity',
      value: m.cyclomatic_complexity,
      icon: Activity,
      description: 'Decision path complexity',
    },
  ];

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Code Metrics
        </h3>
        <span className="text-[10px] font-mono text-slate-400">8 AST attributes</span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
        {items.map((item) => (
          <MetricCard
            key={item.label}
            label={item.label}
            value={item.value}
            icon={item.icon}
            description={item.description}
          />
        ))}
      </div>
    </div>
  );
};

export default MetricsGrid;
