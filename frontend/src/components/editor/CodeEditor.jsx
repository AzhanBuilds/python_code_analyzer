import React, { useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Terminal, Code2 } from 'lucide-react';

export const CodeEditor = ({ code, onChange, targetLine }) => {
  const editorRef = useRef(null);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
  };

  // Jump to line when user clicks a finding or warning
  useEffect(() => {
    if (editorRef.current && targetLine?.line) {
      const line = targetLine.line;
      editorRef.current.revealLineInCenter(line);
      editorRef.current.setPosition({ lineNumber: line, column: 1 });
      editorRef.current.focus();

      // Temporary line highlight decoration
      const decorations = editorRef.current.deltaDecorations(
        [],
        [
          {
            range: {
              startLineNumber: line,
              startColumn: 1,
              endLineNumber: line,
              endColumn: 1000,
            },
            options: {
              isWholeLine: true,
              className: 'bg-emerald-500/20 border-l-4 border-emerald-400',
            },
          },
        ]
      );

      const timer = setTimeout(() => {
        if (editorRef.current) {
          editorRef.current.deltaDecorations(decorations, []);
        }
      }, 2500);

      return () => clearTimeout(timer);
    }
  }, [targetLine]);

  return (
    <div className="flex flex-col h-full bg-dark-900 border border-dark-700/80 rounded-xl overflow-hidden shadow-xl">
      {/* Editor Header */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-dark-850/90 border-b border-dark-700/70">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
          <Code2 className="w-4 h-4 text-emerald-400" />
          <span>Python Code Editor</span>
        </div>
        <div className="flex items-center gap-2 text-[11px] font-mono">
          <span className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-dark-900 text-slate-300 border border-dark-700">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            Python 3.x
          </span>
        </div>
      </div>

      {/* Monaco Editor Container */}
      <div className="flex-1 min-h-[460px] lg:min-h-[620px] bg-[#1e1e1e] relative">
        <Editor
          height="100%"
          language="python"
          theme="vs-dark"
          value={code}
          onChange={(val) => onChange(val || '')}
          onMount={handleEditorDidMount}
          options={{
            fontSize: 13,
            fontFamily: "'JetBrains Mono', Consolas, 'Fira Code', monospace",
            minimap: { enabled: false },
            lineNumbers: 'on',
            lineNumbersMinChars: 3,
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            tabSize: 4,
            insertSpaces: true,
            automaticLayout: true,
            padding: { top: 12, bottom: 12 },
            renderLineHighlight: 'all',
          }}
          loading={
            <div className="flex items-center justify-center h-full text-slate-400 font-mono text-xs">
              Loading Python Editor...
            </div>
          }
        />
      </div>
    </div>
  );
};

export default CodeEditor;
