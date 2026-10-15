import ast
import pytest
from backend.analyzer.syntax_analyzer import SyntaxAnalyzer
from backend.analyzer.metrics_analyzer import MetricsAnalyzer

def test_empty_source():
    metrics = MetricsAnalyzer.calculate_metrics("", None)
    assert metrics["total_lines"] == 0
    assert metrics["functions"] == 0
    assert metrics["classes"] == 0
    assert metrics["imports"] == 0
    assert metrics["loops"] == 0
    assert metrics["conditions"] == 0
    assert metrics["comments"] == 0
    assert metrics["cyclomatic_complexity"] == 0

def test_sample_program_from_prd_section_20():
    code = """# Example program
# Display a message
print("Hello, world!")"""
    is_valid, tree, error = SyntaxAnalyzer.parse_source(code)
    assert is_valid is True
    metrics = MetricsAnalyzer.calculate_metrics(code, tree)

    assert metrics["total_lines"] == 3
    assert metrics["functions"] == 0
    assert metrics["classes"] == 0
    assert metrics["imports"] == 0
    assert metrics["loops"] == 0
    assert metrics["conditions"] == 0
    assert metrics["comments"] == 2
    assert metrics["cyclomatic_complexity"] == 1

def test_functions_and_classes_count():
    code = """
class MyClass:
    def sync_method(self):
        pass

async def async_worker():
    pass
"""
    is_valid, tree, error = SyntaxAnalyzer.parse_source(code)
    assert is_valid is True
    metrics = MetricsAnalyzer.calculate_metrics(code, tree)

    assert metrics["classes"] == 1
    assert metrics["functions"] == 2

def test_imports_counting():
    code = """
import os, sys
from pathlib import Path, PurePath
import math
"""
    is_valid, tree, error = SyntaxAnalyzer.parse_source(code)
    assert is_valid is True
    metrics = MetricsAnalyzer.calculate_metrics(code, tree)

    # 3 import statements (not 5 imported names)
    assert metrics["imports"] == 3

def test_loops_and_conditions_count():
    code = """
for i in range(10):
    if i > 5:
        while True:
            break
val = 1 if i == 0 else 2
"""
    is_valid, tree, error = SyntaxAnalyzer.parse_source(code)
    assert is_valid is True
    metrics = MetricsAnalyzer.calculate_metrics(code, tree)

    assert metrics["loops"] == 2      # for, while
    assert metrics["conditions"] == 2 # if, ifexp

def test_comments_inside_string_not_counted():
    code = """
# This is a real comment
message = "This # is not a comment and # neither is this"
"""
    is_valid, tree, error = SyntaxAnalyzer.parse_source(code)
    assert is_valid is True
    metrics = MetricsAnalyzer.calculate_metrics(code, tree)

    assert metrics["comments"] == 1

def test_cyclomatic_complexity_with_branches():
    code = """
def evaluate(x, y):
    if x > 0:
        if y > 0:
            return 1
        else:
            return 2
    return 0
"""
    is_valid, tree, error = SyntaxAnalyzer.parse_source(code)
    assert is_valid is True
    metrics = MetricsAnalyzer.calculate_metrics(code, tree)

    # 2 if statements = 2 decisions + 1 base = 3
    assert metrics["cyclomatic_complexity"] == 3
