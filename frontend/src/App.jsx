import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppHeader from './components/layout/AppHeader';
import AnalyzerLayout from './components/layout/AnalyzerLayout';
import CodeEditor from './components/editor/CodeEditor';
import EditorToolbar from './components/editor/EditorToolbar';
import AnalysisResults from './components/analysis/AnalysisResults';
import LoginPage from './components/auth/LoginPage';
import RegisterPage from './components/auth/RegisterPage';
import ProtectedRoute from './components/auth/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import useAnalyzer from './hooks/useAnalyzer';

function AnalyzerWorkspace() {
  const {
    code,
    setCode,
    result,
    status,
    errorMessage,
    backendReady,
    targetLine,
    runAnalysis,
    clearCode,
    loadExample,
    navigateToLine,
  } = useAnalyzer();

  const lines = code ? code.split('\n').length : 0;
  const chars = code ? code.length : 0;

  return (
    <div className="min-h-screen flex flex-col bg-dark-950 text-slate-100 font-sans selection:bg-emerald-500/30 selection:text-emerald-200">
      {/* Header */}
      <AppHeader backendReady={backendReady} />

      {/* Main Workspace Layout */}
      <AnalyzerLayout
        editorSlot={
          <div className="flex flex-col space-y-3">
            <EditorToolbar
              onAnalyze={() => runAnalysis(code)}
              onClear={clearCode}
              onLoadExample={loadExample}
              loading={status === 'loading'}
              lineCount={lines}
              charCount={chars}
            />
            <CodeEditor
              code={code}
              onChange={setCode}
              targetLine={targetLine}
            />
          </div>
        }
        resultsSlot={
          <AnalysisResults
            result={result}
            status={status}
            errorMessage={errorMessage}
            onRetry={() => runAnalysis(code)}
            onNavigate={navigateToLine}
            onAnalyze={() => runAnalysis(code)}
          />
        }
      />

      {/* Footer */}
      <footer className="mt-auto border-t border-dark-800/80 bg-dark-900/60 py-3.5 px-4 text-center text-xs text-slate-400 font-mono">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Python Static Code Analyzer • Deterministic AST & Token Inspection</span>
          <span className="text-emerald-400/80">Code is never executed on server • Safe sandbox</span>
        </div>
      </footer>
    </div>
  );
}

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AnalyzerWorkspace />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
