export const DEFAULT_EXAMPLE_CODE = `# Example Python program
def greet(name):
    """Return a greeting."""
    message = f"Hello, {name}!"
    return message

print(greet("Python"))
`;

export const ADVANCED_EXAMPLE_CODE = `# Advanced Python Analyzer Demo
# TODO: Add caching for expensive computations
# FIXME: Handle potential empty array edge-case

import math
import os

class StatisticsEngine:
    """Computes basic statistical metrics for datasets."""

    def __init__(self, name="DefaultEngine"):
        self.name = name

    def calculate_variance(self, data):
        """Calculate population variance."""
        if not data:
            return 0
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return variance

def process_batch(items):
    engine = StatisticsEngine("BatchProcessor")
    try:
        var = engine.calculate_variance(items)
        print("Calculated variance:", var)
    except:
        pass
    return True
`;

export const getSeverityColor = (severity) => {
  const s = (severity || '').toLowerCase();
  switch (s) {
    case 'critical':
      return {
        bg: 'bg-rose-500/10',
        border: 'border-rose-500/30',
        text: 'text-rose-400',
        badge: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
      };
    case 'high':
      return {
        bg: 'bg-amber-500/10',
        border: 'border-amber-500/30',
        text: 'text-amber-400',
        badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
      };
    case 'medium':
      return {
        bg: 'bg-yellow-500/10',
        border: 'border-yellow-500/30',
        text: 'text-yellow-400',
        badge: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
      };
    case 'low':
      return {
        bg: 'bg-sky-500/10',
        border: 'border-sky-500/30',
        text: 'text-sky-400',
        badge: 'bg-sky-500/20 text-sky-300 border-sky-500/30',
      };
    case 'info':
    default:
      return {
        bg: 'bg-slate-500/10',
        border: 'border-slate-500/30',
        text: 'text-slate-400',
        badge: 'bg-slate-500/20 text-slate-300 border-slate-500/30',
      };
  }
};

export const getScoreColor = (score) => {
  if (score === null || score === undefined) {
    return {
      text: 'text-slate-400',
      stroke: '#64748b',
      bg: 'bg-slate-800/40',
      border: 'border-slate-700/50',
      label: 'Unavailable',
    };
  }
  if (score >= 90) {
    return {
      text: 'text-emerald-400',
      stroke: '#10b981',
      bg: 'bg-emerald-950/20',
      border: 'border-emerald-500/30',
      label: 'Excellent',
    };
  }
  if (score >= 75) {
    return {
      text: 'text-teal-400',
      stroke: '#14b8a6',
      bg: 'bg-teal-950/20',
      border: 'border-teal-500/30',
      label: 'Good',
    };
  }
  if (score >= 60) {
    return {
      text: 'text-amber-400',
      stroke: '#f59e0b',
      bg: 'bg-amber-950/20',
      border: 'border-amber-500/30',
      label: 'Needs Improvement',
    };
  }
  return {
    text: 'text-rose-400',
    stroke: '#f43f5e',
    bg: 'bg-rose-950/20',
    border: 'border-rose-500/30',
    label: 'Poor',
  };
};
