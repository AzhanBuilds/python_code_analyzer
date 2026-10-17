import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Cpu, Lock, Mail, AlertCircle, ArrowRight, Eye, EyeOff, Loader2 } from 'lucide-react';

export const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated, error: authError, clearError } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [apiError, setApiError] = useState(null);

  const redirectPath = location.state?.from?.pathname || '/';

  useEffect(() => {
    if (isAuthenticated) {
      navigate(redirectPath, { replace: true });
    }
    clearError();
  }, [isAuthenticated, navigate, redirectPath]);

  const validateForm = () => {
    const errors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email.trim()) {
      errors.email = 'Email address is required.';
    } else if (!emailRegex.test(email.trim())) {
      errors.email = 'Please enter a valid email address.';
    }

    if (!password) {
      errors.password = 'Password is required.';
    } else if (password.length < 8) {
      errors.password = 'Password must be at least 8 characters.';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError(null);

    if (!validateForm()) {
      return;
    }

    setSubmitting(true);
    try {
      await login(email.trim(), password);
      navigate(redirectPath, { replace: true });
    } catch (err) {
      setApiError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans selection:bg-emerald-500/30 selection:text-emerald-200">
      {/* Background radial glow */}
      <div className="fixed inset-0 pointer-events-none opacity-20">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500 rounded-full blur-[140px]" />
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10 px-4">
        {/* Brand Header */}
        <div className="flex flex-col items-center text-center">
          <div className="p-3 rounded-2xl bg-forest-900/70 border border-forest-500/30 shadow-xl shadow-forest-950/60 mb-4">
            <Cpu className="w-8 h-8 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-white">
            Sign in to Python Analyzer
          </h2>
          <p className="mt-1.5 text-xs text-slate-400 font-mono">
            Safe AST static code analysis and quality insights
          </p>
        </div>

        {/* Card */}
        <div className="mt-8 bg-dark-900/80 border border-dark-800/90 rounded-2xl p-6 sm:p-8 shadow-2xl backdrop-blur-md">
          {/* Server Error Alert */}
          {(apiError || authError) && (
            <div className="mb-6 p-3.5 rounded-xl bg-rose-950/40 border border-rose-800/50 text-rose-300 text-sm flex items-start gap-2.5 animate-fadeIn">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
              <div className="flex-1 text-xs sm:text-sm font-medium">
                {apiError || authError}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5" noValidate>
            {/* Email Field */}
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-slate-300 mb-1.5 font-mono">
                Email Address
              </label>
              <div className="relative rounded-lg shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (formErrors.email) setFormErrors({ ...formErrors, email: null });
                  }}
                  placeholder="developer@example.com"
                  className={`block w-full pl-9 pr-3 py-2.5 bg-dark-850/90 border rounded-lg text-sm text-slate-100 placeholder-slate-500 transition-all focus:outline-none focus:ring-1 ${
                    formErrors.email
                      ? 'border-rose-500/80 focus:border-rose-500 focus:ring-rose-500'
                      : 'border-dark-700 focus:border-emerald-500 focus:ring-emerald-500'
                  }`}
                  autoComplete="email"
                  autoFocus
                />
              </div>
              {formErrors.email && (
                <p className="mt-1.5 text-xs text-rose-400 font-mono flex items-center gap-1">
                  <span>•</span> {formErrors.email}
                </p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-medium uppercase tracking-wider text-slate-300 font-mono">
                  Password
                </label>
              </div>
              <div className="relative rounded-lg shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (formErrors.password) setFormErrors({ ...formErrors, password: null });
                  }}
                  placeholder="••••••••••••"
                  className={`block w-full pl-9 pr-10 py-2.5 bg-dark-850/90 border rounded-lg text-sm text-slate-100 placeholder-slate-500 transition-all focus:outline-none focus:ring-1 ${
                    formErrors.password
                      ? 'border-rose-500/80 focus:border-rose-500 focus:ring-rose-500'
                      : 'border-dark-700 focus:border-emerald-500 focus:ring-emerald-500'
                  }`}
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-500 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {formErrors.password && (
                <p className="mt-1.5 text-xs text-rose-400 font-mono flex items-center gap-1">
                  <span>•</span> {formErrors.password}
                </p>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={submitting}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:bg-dark-700 disabled:text-slate-500 text-white font-medium text-sm shadow-lg shadow-emerald-950/50 hover:shadow-emerald-900/60 transition-all cursor-pointer disabled:cursor-not-allowed mt-2"
            >
              {submitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Signing in...</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Switch to Register */}
          <div className="mt-6 pt-5 border-t border-dark-800 text-center">
            <p className="text-xs text-slate-400">
              Don't have an account yet?{' '}
              <Link
                to="/register"
                className="font-medium text-emerald-400 hover:text-emerald-300 underline underline-offset-4 transition-colors"
              >
                Create an account
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
