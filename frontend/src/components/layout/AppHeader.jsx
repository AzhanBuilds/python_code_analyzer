import React from 'react';
import { ShieldCheck, Cpu, LogOut, User as UserIcon } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const AppHeader = ({ backendReady }) => {
  const { user, isAuthenticated, logout } = useAuth();

  const getInitials = (name) => {
    if (!name) return 'U';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  };

  return (
    <header className="border-b border-dark-700/60 bg-dark-900/80 backdrop-blur-md sticky top-0 z-50 px-4 lg:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-forest-900/60 border border-forest-500/30 text-forest-400 shadow-lg shadow-forest-950/50">
            <Cpu className="w-5 h-5 text-emerald-400 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <Link to="/" className="text-lg font-bold tracking-tight text-white hover:text-emerald-400 transition-colors flex items-center gap-2">
                Python Code Analyzer
              </Link>
              <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                v1.0 AST Engine
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Static analysis and code-quality insights without execution
            </p>
          </div>
        </div>

        {/* Right Section: Status Indicators & User Profile */}
        <div className="flex items-center flex-wrap gap-3 self-end sm:self-auto text-xs font-mono">
          <div className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-dark-800/80 border border-dark-700 text-slate-300">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Zero-Execution Sandbox</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-dark-800/80 border border-dark-700">
            <span
              className={`w-2 h-2 rounded-full ${
                backendReady === true
                  ? 'bg-emerald-400 shadow-[0_0_8px_#10b981]'
                  : backendReady === false
                  ? 'bg-rose-400 shadow-[0_0_8px_#f43f5e]'
                  : 'bg-amber-400 animate-pulse'
              }`}
            />
            <span className="text-slate-300">
              {backendReady === true
                ? 'Backend Ready'
                : backendReady === false
                ? 'Backend Offline'
                : 'Connecting...'}
            </span>
          </div>

          {/* User Profile / Auth State */}
          {isAuthenticated && user ? (
            <div className="flex items-center gap-2.5 pl-2 border-l border-dark-700">
              <div className="flex items-center gap-2 px-2.5 py-1 rounded-md bg-dark-800/90 border border-dark-700/80 text-slate-200">
                <div className="w-6 h-6 rounded-full bg-forest-900 border border-forest-500/40 text-emerald-400 flex items-center justify-center text-[11px] font-bold">
                  {getInitials(user.display_name)}
                </div>
                <div className="flex flex-col text-left">
                  <span className="text-xs font-medium text-slate-200 leading-none truncate max-w-[120px]">
                    {user.display_name}
                  </span>
                  <span className="text-[10px] text-slate-400 leading-none truncate max-w-[120px] font-mono mt-0.5">
                    {user.email}
                  </span>
                </div>
              </div>

              <button
                onClick={logout}
                title="Log out"
                className="flex items-center gap-1 px-2.5 py-1.5 rounded-md bg-dark-800 hover:bg-rose-950/40 hover:border-rose-800/60 border border-dark-700 text-slate-400 hover:text-rose-300 transition-all cursor-pointer"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 pl-2 border-l border-dark-700">
              <Link
                to="/login"
                className="px-3 py-1.5 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition-all shadow-md shadow-emerald-950/40"
              >
                Sign In
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default AppHeader;
