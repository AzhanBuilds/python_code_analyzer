import ast
from typing import Dict, List, Any, Optional, Set
from .metrics_analyzer import MetricsAnalyzer

class RulesEngine:
    """Runs modular static-analysis rules on Python AST and source text."""

    def __init__(
        self,
        max_line_length: int = 100,
        max_function_lines: int = 50,
        max_complexity: int = 10
    ):
        self.max_line_length = max_line_length
        self.max_function_lines = max_function_lines
        self.max_complexity = max_complexity

    def analyze(
        self,
        source_code: str,
        tree: Optional[ast.AST],
        todos: List[Dict[str, Any]],
        fixmes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executes static analysis rules.

        Returns:
            Dict containing:
            - warnings: List[Dict]
            - suggestions: List[Dict]
            - all_findings: List[Dict]
        """
        warnings: List[Dict[str, Any]] = []
        suggestions: List[Dict[str, Any]] = []
        findings: List[Dict[str, Any]] = []

        if not source_code:
            return {"warnings": [], "suggestions": [], "all_findings": []}

        # 1. Line-level text rules (runs even if AST is not available)
        self._check_line_length(source_code, warnings, suggestions, findings)

        # 2. Comment markers
        self._check_comment_markers(todos, fixmes, warnings, suggestions, findings)

        # 3. AST-dependent rules
        if tree is not None:
            self._check_print_usage(tree, warnings, suggestions, findings)
            self._check_docstrings_and_length(tree, warnings, suggestions, findings)
            self._check_bare_except(tree, warnings, suggestions, findings)
            self._check_unused_imports(tree, warnings, suggestions, findings)
            self._check_complexity(tree, warnings, suggestions, findings)

        # Sort findings by line number
        warnings.sort(key=lambda x: (x.get("line") or 0, x.get("severity") or ""))
        suggestions.sort(key=lambda x: (x.get("line") or 0))

        return {
            "warnings": warnings,
            "suggestions": suggestions,
            "all_findings": findings
        }

    def _check_line_length(
        self,
        source_code: str,
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rule 2: line-too-long"""
        for idx, line in enumerate(source_code.splitlines(), start=1):
            if len(line) > self.max_line_length:
                finding = {
                    "rule_id": "line-too-long",
                    "code": "line-too-long",
                    "line": idx,
                    "column": self.max_line_length + 1,
                    "severity": "Low",
                    "message": f"Line {idx} exceeds {self.max_line_length} characters ({len(line)} chars).",
                    "suggestion": "Break long lines into multiple lines to improve readability."
                }
                warnings.append(finding)
                suggestions.append({
                    "rule_id": "line-too-long",
                    "code": "line-too-long",
                    "line": idx,
                    "message": "Break long lines into multiple lines to improve readability."
                })
                findings.append(finding)

    def _check_comment_markers(
        self,
        todos: List[Dict[str, Any]],
        fixmes: List[Dict[str, Any]],
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rules 8: todo-comment and fixme-comment"""
        for todo in todos:
            finding = {
                "rule_id": "todo-comment",
                "code": "todo-comment",
                "line": todo["line"],
                "column": todo.get("column", 1),
                "severity": "Info",
                "message": f"TODO comment found: {todo['message']}",
                "suggestion": f"Resolve pending task: {todo['message']}"
            }
            warnings.append(finding)
            suggestions.append({
                "rule_id": "todo-comment",
                "code": "todo-comment",
                "line": todo["line"],
                "message": f"Complete pending TODO: '{todo['message']}'."
            })
            findings.append(finding)

        for fixme in fixmes:
            finding = {
                "rule_id": "fixme-comment",
                "code": "fixme-comment",
                "line": fixme["line"],
                "column": fixme.get("column", 1),
                "severity": "Medium",
                "message": f"FIXME comment found: {fixme['message']}",
                "suggestion": f"Address code defect or temporary fix: {fixme['message']}"
            }
            warnings.append(finding)
            suggestions.append({
                "rule_id": "fixme-comment",
                "code": "fixme-comment",
                "line": fixme["line"],
                "message": f"Fix known issue: '{fixme['message']}'."
            })
            findings.append(finding)

    def _check_print_usage(
        self,
        tree: ast.AST,
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rule 1: print-usage"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id == "print":
                    finding = {
                        "rule_id": "print-usage",
                        "code": "print-usage",
                        "line": getattr(node, "lineno", 1),
                        "column": getattr(node, "col_offset", 0),
                        "severity": "Low",
                        "message": "print() is used in the code.",
                        "suggestion": "Use a logger instead of print() for application output."
                    }
                    warnings.append(finding)
                    suggestions.append({
                        "rule_id": "print-usage",
                        "code": "print-usage",
                        "line": getattr(node, "lineno", 1),
                        "message": "Use a logger instead of print() for application output."
                    })
                    findings.append(finding)

    def _check_docstrings_and_length(
        self,
        tree: ast.AST,
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rules 3, 4, 5: missing-function-docstring, missing-class-docstring, function-too-long"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Missing docstring
                if ast.get_docstring(node) is None:
                    finding = {
                        "rule_id": "missing-function-docstring",
                        "code": "missing-function-docstring",
                        "line": node.lineno,
                        "column": node.col_offset,
                        "severity": "Low",
                        "message": f"Function '{node.name}' is missing a docstring.",
                        "suggestion": f"Add a docstring explaining the purpose and arguments of '{node.name}'."
                    }
                    warnings.append(finding)
                    suggestions.append({
                        "rule_id": "missing-function-docstring",
                        "code": "missing-function-docstring",
                        "line": node.lineno,
                        "message": f"Add a docstring explaining the purpose and arguments of '{node.name}'."
                    })
                    findings.append(finding)

                # Function too long
                end_line = getattr(node, "end_lineno", node.lineno)
                func_length = end_line - node.lineno + 1
                if func_length > self.max_function_lines:
                    finding = {
                        "rule_id": "function-too-long",
                        "code": "function-too-long",
                        "line": node.lineno,
                        "column": node.col_offset,
                        "severity": "Medium",
                        "message": f"Function '{node.name}' is too long ({func_length} lines > {self.max_function_lines} limit).",
                        "suggestion": f"Consider breaking function '{node.name}' into smaller, focused helper functions."
                    }
                    warnings.append(finding)
                    suggestions.append({
                        "rule_id": "function-too-long",
                        "code": "function-too-long",
                        "line": node.lineno,
                        "message": f"Consider breaking function '{node.name}' into smaller, focused helper functions."
                    })
                    findings.append(finding)

            elif isinstance(node, ast.ClassDef):
                if ast.get_docstring(node) is None:
                    finding = {
                        "rule_id": "missing-class-docstring",
                        "code": "missing-class-docstring",
                        "line": node.lineno,
                        "column": node.col_offset,
                        "severity": "Low",
                        "message": f"Class '{node.name}' is missing a docstring.",
                        "suggestion": f"Add a docstring explaining the class responsibilities."
                    }
                    warnings.append(finding)
                    suggestions.append({
                        "rule_id": "missing-class-docstring",
                        "code": "missing-class-docstring",
                        "line": node.lineno,
                        "message": f"Add a docstring explaining the class responsibilities."
                    })
                    findings.append(finding)

    def _check_bare_except(
        self,
        tree: ast.AST,
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rule 6: bare-except"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    finding = {
                        "rule_id": "bare-except",
                        "code": "bare-except",
                        "line": node.lineno,
                        "column": node.col_offset,
                        "severity": "High",
                        "message": "Bare 'except:' handler catches all exceptions including system exits.",
                        "suggestion": "Catch specific exceptions (e.g., 'except Exception:' or 'except ValueError:') instead of bare 'except:'."
                    }
                    warnings.append(finding)
                    suggestions.append({
                        "rule_id": "bare-except",
                        "code": "bare-except",
                        "line": node.lineno,
                        "message": "Catch specific exceptions instead of a bare 'except:'."
                    })
                    findings.append(finding)

    def _check_unused_imports(
        self,
        tree: ast.AST,
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rule 7: unused-import (conservative check)"""
        imported_symbols: Dict[str, Dict[str, Any]] = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    symbol_name = alias.asname or alias.name
                    imported_symbols[symbol_name] = {
                        "line": node.lineno,
                        "column": node.col_offset,
                        "name": alias.name
                    }
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    symbol_name = alias.asname or alias.name
                    imported_symbols[symbol_name] = {
                        "line": node.lineno,
                        "column": node.col_offset,
                        "name": alias.name
                    }

        if not imported_symbols:
            return

        # Collect all referenced names (except in import nodes)
        used_names: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                used_names.add(node.value.id)

        for sym, meta in imported_symbols.items():
            if sym not in used_names:
                finding = {
                    "rule_id": "unused-import",
                    "code": "unused-import",
                    "line": meta["line"],
                    "column": meta["column"],
                    "severity": "Medium",
                    "message": f"Imported module or symbol '{meta['name']}' appears to be unused.",
                    "suggestion": f"Remove unused import '{meta['name']}' to keep the namespace clean."
                }
                warnings.append(finding)
                suggestions.append({
                    "rule_id": "unused-import",
                    "code": "unused-import",
                    "line": meta["line"],
                    "message": f"Remove unused import '{meta['name']}'."
                })
                findings.append(finding)

    def _check_complexity(
        self,
        tree: ast.AST,
        warnings: List[Dict[str, Any]],
        suggestions: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> None:
        """Rule 9: high-complexity"""
        function_nodes = [
            n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        func_complexities = MetricsAnalyzer.calculate_function_complexities(function_nodes)

        for fc in func_complexities:
            if fc["complexity"] > self.max_complexity:
                finding = {
                    "rule_id": "high-complexity",
                    "code": "high-complexity",
                    "line": fc["line"],
                    "column": 0,
                    "severity": "Medium",
                    "message": f"Function '{fc['name']}' has high cyclomatic complexity ({fc['complexity']} > {self.max_complexity}).",
                    "suggestion": "Simplify conditional logic or extract sub-routines to reduce complexity."
                }
                warnings.append(finding)
                suggestions.append({
                    "rule_id": "high-complexity",
                    "code": "high-complexity",
                    "line": fc["line"],
                    "message": f"Simplify conditional logic in function '{fc['name']}' to reduce cyclomatic complexity."
                })
                findings.append(finding)
