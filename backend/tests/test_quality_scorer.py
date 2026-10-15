import pytest
from backend.analyzer.quality_scorer import QualityScorer

def test_perfect_score():
    score = QualityScorer.calculate_score([])
    assert score == 100
    assert QualityScorer.get_rating(score) == "Excellent"

def test_deductions_by_severity():
    findings = [
        {"rule_id": "r1", "line": 1, "severity": "Critical"}, # -20
        {"rule_id": "r2", "line": 2, "severity": "High"},     # -10
        {"rule_id": "r3", "line": 3, "severity": "Medium"},   # -5
        {"rule_id": "r4", "line": 4, "severity": "Low"},      # -2
        {"rule_id": "r5", "line": 5, "severity": "Info"}       # -0
    ]
    score = QualityScorer.calculate_score(findings)
    assert score == 63
    assert QualityScorer.get_rating(score) == "Needs Improvement"

def test_score_clamped_at_zero():
    findings = [
        {"rule_id": f"r{i}", "line": i, "severity": "Critical"} for i in range(10)
    ]
    # 10 * 20 = 200 penalty -> clamped to 0
    score = QualityScorer.calculate_score(findings)
    assert score == 0
    assert QualityScorer.get_rating(score) == "Poor"

def test_deduplication_prevents_double_penalizing():
    findings = [
        {"rule_id": "print-usage", "line": 5, "severity": "Low"},
        {"rule_id": "print-usage", "line": 5, "severity": "Low"}
    ]
    score = QualityScorer.calculate_score(findings)
    assert score == 98  # only deducted 2 once
