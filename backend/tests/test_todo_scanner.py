import pytest
from backend.analyzer.todo_scanner import TodoScanner

def test_todo_and_fixme_scanner():
    code = """# TODO: validate input
# FIXME: handle missing data
def process():
    # todo lowercase task
    pass
# FixMe another issue
"""
    result = TodoScanner.scan_comments(code)
    assert len(result["todos"]) == 2
    assert len(result["fixmes"]) == 2
    assert result["total_markers"] == 4

    assert result["todos"][0]["line"] == 1
    assert "validate input" in result["todos"][0]["message"]
    assert result["fixmes"][0]["line"] == 2
    assert "handle missing data" in result["fixmes"][0]["message"]

def test_todo_inside_string_is_ignored():
    code = """
notes = "TODO: this is inside a string and not a comment"
# Real comment
fixme_msg = "FIXME: also inside string"
"""
    result = TodoScanner.scan_comments(code)
    assert len(result["todos"]) == 0
    assert len(result["fixmes"]) == 0
    assert result["total_comment_tokens"] == 1

def test_empty_source():
    result = TodoScanner.scan_comments("")
    assert result["todos"] == []
    assert result["fixmes"] == []
    assert result["total_markers"] == 0
