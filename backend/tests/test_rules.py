import pytest
from backend.analyzer.syntax_analyzer import SyntaxAnalyzer
from backend.analyzer.rules_engine import RulesEngine
from backend.analyzer.todo_scanner import TodoScanner

def test_print_usage_rule():
    code = "print('Hello world')"
    is_valid, tree, _ = SyntaxAnalyzer.parse_source(code)
    engine = RulesEngine()
    results = engine.analyze(code, tree, [], [])

    print_warnings = [w for w in results["warnings"] if w["code"] == "print-usage"]
    assert len(print_warnings) == 1
    assert print_warnings[0]["severity"] == "Low"
    assert "print() is used" in print_warnings[0]["message"]

def test_bare_except_rule():
    code = """
try:
    x = 1 / 0
except:
    pass
"""
    is_valid, tree, _ = SyntaxAnalyzer.parse_source(code)
    engine = RulesEngine()
    results = engine.analyze(code, tree, [], [])

    bare_warnings = [w for w in results["warnings"] if w["code"] == "bare-except"]
    assert len(bare_warnings) == 1
    assert bare_warnings[0]["severity"] == "High"

def test_missing_docstrings():
    code = """
class UndocumentedClass:
    def undocumented_func(self):
        pass

def documented_func():
    \"\"\"This is documented.\"\"\"
    return True
"""
    is_valid, tree, _ = SyntaxAnalyzer.parse_source(code)
    engine = RulesEngine()
    results = engine.analyze(code, tree, [], [])

    codes = [w["code"] for w in results["warnings"]]
    assert "missing-class-docstring" in codes
    assert "missing-function-docstring" in codes

def test_unused_import_rule():
    code = """
import math
import os
print(math.pi)
"""
    is_valid, tree, _ = SyntaxAnalyzer.parse_source(code)
    engine = RulesEngine()
    results = engine.analyze(code, tree, [], [])

    unused = [w for w in results["warnings"] if w["code"] == "unused-import"]
    assert len(unused) == 1
    assert "os" in unused[0]["message"]

def test_line_too_long_rule():
    long_line = "# " + "a" * 120
    is_valid, tree, _ = SyntaxAnalyzer.parse_source(long_line)
    engine = RulesEngine(max_line_length=100)
    results = engine.analyze(long_line, tree, [], [])

    long_warnings = [w for w in results["warnings"] if w["code"] == "line-too-long"]
    assert len(long_warnings) == 1
