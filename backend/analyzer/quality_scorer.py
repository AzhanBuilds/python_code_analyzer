from typing import List, Dict, Any, Optional

class QualityScorer:
    """Calculates deterministic code quality score based on findings and penalties."""

    DEFAULT_PENALTIES = {
        "critical": 20,
        "high": 10,
        "medium": 5,
        "low": 2,
        "info": 0
    }

    @classmethod
    def calculate_score(
        cls,
        findings: List[Dict[str, Any]],
        penalties: Optional[Dict[str, int]] = None
    ) -> int:
        """
        Calculates a quality score between 0 and 100.
        Base is 100. Each distinct finding deducts points according to severity.
        """
        weights = penalties or cls.DEFAULT_PENALTIES
        score = 100

        # Deduplicate findings by (rule_id, line, severity)
        seen = set()
        for finding in findings:
            rule_id = finding.get("rule_id") or finding.get("code") or "unknown"
            line = finding.get("line") or 0
            severity = (finding.get("severity") or "info").lower()
            key = (rule_id, line, severity)
            if key in seen:
                continue
            seen.add(key)

            deduction = weights.get(severity, 0)
            score -= deduction

        return max(0, min(100, score))

    @classmethod
    def get_rating(cls, score: Optional[int]) -> str:
        """Returns visual status label for a given score."""
        if score is None:
            return "Unavailable"
        if score >= 90:
            return "Excellent"
        if score >= 75:
            return "Good"
        if score >= 60:
            return "Needs Improvement"
        return "Poor"
