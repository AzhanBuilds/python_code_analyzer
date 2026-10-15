# Python Code Analyzer

A professional full-stack web application for static Python code analysis and code quality insights, built with React, Vite, Tailwind CSS, Monaco Editor, and a Python Flask backend.

---

## Features

- **Safe Static Analysis Sandbox:** Analyzes Python source code purely as data via Python's `ast` parser and `tokenize` engine. **Submitted code is never executed or evaluated.**
- **Monaco Code Editor:** Syntax highlighting, line numbers, word wrap, code selection, and real-time line/character counts.
- **Dynamic Quality Score:** Computes a deterministic quality score (0–100) based on detected findings and severity penalties.
- **8 Comprehensive AST Metrics:**
  - **Total Lines:** Physical source line count.
  - **Functions:** Synchronous and asynchronous function definitions.
  - **Classes:** Class definitions.
  - **Imports:** Import statements.
  - **Loops:** `for`, `async for`, and `while` loop constructs.
  - **Conditions:** `if` statements and ternary expressions.
  - **Comments:** Tokenized comments (distinguishing comments from `#` in strings).
  - **Cyclomatic Complexity:** Module and function-level decision points.
- **Modular Rule Engine:**
  - `print-usage` (Low severity: recommends logger for application output)
  - `line-too-long` (Configurable threshold, default 100 chars)
  - `missing-function-docstring` and `missing-class-docstring`
  - `function-too-long` (Configurable threshold, default 50 lines)
  - `bare-except` (High severity: flags dangerous bare `except:` blocks)
  - `unused-import` (Conservative check for unused imported symbols)
  - `high-complexity` (Flags functions exceeding complexity thresholds)
  - `todo-comment` and `fixme-comment`
- **TODO / FIXME Scanner:** Case-insensitive detection of `# TODO` and `# FIXME` comments with line numbers.
- **Interactive Finding Navigation:** Clicking any warning, suggestion, or comment jump-links and highlights the line in the Monaco editor.
- **Responsive Developer UI:** Sleek dark-mode aesthetic with desktop 2-column layout and mobile-stacked view.

---

## Project Structure

```text
d:/python analyzer/
├── backend/
│   ├── app.py                      # Flask application factory and entry point
│   ├── config.py                   # Configuration and thresholds
│   ├── requirements.txt            # Python dependencies (Flask, Flask-CORS, pytest)
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── analyzer_service.py     # Pipeline coordinator
│   │   ├── syntax_analyzer.py      # ast.parse & syntax diagnostics
│   │   ├── metrics_analyzer.py     # 8 AST metrics & complexity calculator
│   │   ├── rules_engine.py         # Static analysis rules
│   │   ├── todo_scanner.py         # Tokenize-based TODO/FIXME scanner
│   │   └── quality_scorer.py       # Deterministic scoring & rating
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analysis.py             # POST /api/analyze
│   │   └── health.py               # GET /api/health
│   └── tests/
│       ├── test_api.py             # API route tests & validations
│       ├── test_metrics.py         # Metrics calculations tests
│       ├── test_rules.py           # Static rule engine tests
│       ├── test_todo_scanner.py    # Comment scanner tests
│       ├── test_quality_scorer.py  # Quality score tests
│       └── test_security.py        # Mandatory security verification tests
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── analysis/           # AnalysisResults, QualityScore, MetricsGrid, Panels
│   │   │   ├── common/             # Loading, Error, Empty states
│   │   │   ├── editor/             # CodeEditor (Monaco), EditorToolbar
│   │   │   └── layout/             # AnalyzerLayout, AppHeader
│   │   ├── hooks/                  # useAnalyzer.js
│   │   ├── services/               # analyzerApi.js
│   │   ├── styles/                 # Tailwind custom tokens & styles
│   │   ├── utils/                  # formatAnalysis.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── postcss.config.js
│   └── .env & .env.example
├── prd.md                          # Full Product Requirements Document
└── README.md
```

---

## Getting Started

### 1. Prerequisites
- **Node.js**: v18+ (tested on Node v24)
- **Python**: 3.10+ (tested on Python 3.14)

### 2. Run the Backend (Flask)

In a terminal:
```bash
cd backend
python -m pip install -r requirements.txt
python -m backend.app
```
Or directly from the project root:
```bash
python -m backend.app
```
The backend will start at: `http://127.0.0.1:5000`  
Health check: `http://127.0.0.1:5000/api/health`

### 3. Run the Frontend (Vite + React)

In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## Running Automated Tests

Run the backend unit, integration, and security test suite using `pytest`:

```bash
python -m pytest backend/tests -v
```

All 28 tests cover:
- Syntax analysis & edge cases
- All 8 metrics (lines, functions, classes, imports, loops, conditions, comments, complexity)
- Static analysis rules (`print-usage`, `bare-except`, `unused-import`, `line-too-long`, docstrings)
- Deterministic quality score bounds and deductions
- API payload validations, error codes (400, 413, 500)
- **Mandatory Security Test:** Verifies that commands like `os.system(...)` and `subprocess.run(...)` are never executed.

---

## API Contract

### `GET /api/health`
Response:
```json
{
  "status": "ok",
  "service": "python-code-analyzer"
}
```

### `POST /api/analyze`
Request:
```json
{
  "code": "print('hello world')\n"
}
```

Response:
```json
{
  "status": "success",
  "valid": true,
  "quality_score": 98,
  "quality_rating": "Excellent",
  "metrics": {
    "total_lines": 1,
    "functions": 0,
    "classes": 0,
    "imports": 0,
    "loops": 0,
    "conditions": 0,
    "comments": 0,
    "cyclomatic_complexity": 1
  },
  "warnings": [
    {
      "code": "print-usage",
      "line": 1,
      "severity": "Low",
      "message": "print() is used in the code.",
      "suggestion": "Use a logger instead of print() for application output."
    }
  ],
  "suggestions": [
    {
      "code": "print-usage",
      "line": 1,
      "message": "Use a logger instead of print() for application output."
    }
  ],
  "todos": [],
  "fixmes": [],
  "summary": {
    "warning_count": 1,
    "suggestion_count": 1,
    "todo_count": 0,
    "fixme_count": 0,
    "quality_rating": "Excellent"
  }
}
```
