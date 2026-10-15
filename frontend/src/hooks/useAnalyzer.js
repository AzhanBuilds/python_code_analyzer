import { useState, useCallback, useEffect } from 'react';
import { analyzeCode, checkHealth } from '../services/analyzerApi';
import { DEFAULT_EXAMPLE_CODE, ADVANCED_EXAMPLE_CODE } from '../utils/formatAnalysis';

export const useAnalyzer = () => {
  const [code, setCode] = useState(DEFAULT_EXAMPLE_CODE);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'success' | 'syntax_error' | 'error'
  const [errorMessage, setErrorMessage] = useState(null);
  const [backendReady, setBackendReady] = useState(null);
  const [targetLine, setTargetLine] = useState(null);

  // Initial backend health check
  useEffect(() => {
    checkHealth()
      .then((data) => {
        setBackendReady(data.status === 'ok');
      })
      .catch(() => {
        setBackendReady(false);
      });
  }, []);

  const runAnalysis = useCallback(async (codeToAnalyze = code) => {
    if (!codeToAnalyze || codeToAnalyze.trim() === '') {
      setErrorMessage('Please provide Python source code to analyze.');
      setStatus('error');
      return;
    }

    setStatus('loading');
    setErrorMessage(null);

    try {
      const data = await analyzeCode(codeToAnalyze);
      setResult(data);
      if (data.status === 'syntax_error') {
        setStatus('syntax_error');
      } else {
        setStatus('success');
      }
      setBackendReady(true);
    } catch (err) {
      if (err.isCancelled) return;
      setStatus('error');
      setErrorMessage(err.message || 'An error occurred during analysis.');
      setBackendReady(false);
    }
  }, [code]);

  const clearCode = useCallback(() => {
    setCode('');
    setResult(null);
    setStatus('idle');
    setErrorMessage(null);
    setTargetLine(null);
  }, []);

  const loadExample = useCallback((type = 'advanced') => {
    const example = type === 'advanced' ? ADVANCED_EXAMPLE_CODE : DEFAULT_EXAMPLE_CODE;
    setCode(example);
    setResult(null);
    setStatus('idle');
    setErrorMessage(null);
    setTargetLine(null);
  }, []);

  const navigateToLine = useCallback((line) => {
    if (line) {
      setTargetLine({ line, timestamp: Date.now() });
    }
  }, []);

  return {
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
  };
};

export default useAnalyzer;
