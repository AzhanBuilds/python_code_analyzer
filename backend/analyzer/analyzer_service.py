from typing import Dict, Any, Optional
from .syntax_analyzer import SyntaxAnalyzer
from .metrics_analyzer import MetricsAnalyzer
from .rules_engine import RulesEngine
from .todo_scanner import TodoScanner
from .quality_scorer import QualityScorer
from ..config import Config

class AnalyzerService:
    """Coordinates static analysis stages and builds response structure."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.rules_engine = RulesEngine(
            max_line_length=self.config.MAX_LINE_LENGTH,
            max_function_lines=self.config.MAX_FUNCTION_LINES,
            max_complexity=self.config.MAX_COMPLEXITY_THRESHOLD
        )

    def analyze_code(self, source_code: str) -> Dict[str, Any]:
        """
        Runs the full static analysis pipeline safely without executing code.
        """
        # Always scan for comments/TODOs even if syntax error exists
        todo_results = TodoScanner.scan_comments(source_code)
        todos = todo_results["todos"]
        fixmes = todo_results["fixmes"]

        # Parse AST syntax
        is_valid, tree, syntax_error = SyntaxAnalyzer.parse_source(source_code)

        if not is_valid:
            return {
                "status": "syntax_error",
                "valid": False,
                "syntax_error": syntax_error,
                "quality_score": None,
                "quality_rating": "Unavailable",
                "metrics": None,
                "warnings": [
                    {
                        "rule_id": "syntax-error",
                        "code": "syntax-error",
                        "line": syntax_error.get("line") or 1,
                        "column": syntax_error.get("column") or 0,
                        "severity": "Critical",
                        "message": f"Syntax Error: {syntax_error.get('message', 'Invalid syntax')}",
                        "suggestion": "Fix syntax error to enable complete code inspection."
                    }
                ],
                "suggestions": [
                    {
                        "rule_id": "syntax-error",
                        "code": "syntax-error",
                        "line": syntax_error.get("line") or 1,
                        "message": f"Fix syntax error: {syntax_error.get('message', 'Invalid syntax')}."
                    }
                ],
                "todos": todos,
                "fixmes": fixmes,
                "summary": {
                    "warning_count": 1,
                    "suggestion_count": 1,
                    "todo_count": len(todos),
                    "fixme_count": len(fixmes),
                    "quality_rating": "Unavailable"
                }
            }

        # Calculate metrics
        metrics = MetricsAnalyzer.calculate_metrics(source_code, tree)

        # Run static rules
        rules_output = self.rules_engine.analyze(source_code, tree, todos, fixmes)
        warnings = rules_output["warnings"]
        suggestions = rules_output["suggestions"]
        all_findings = rules_output["all_findings"]

        # Calculate deterministic quality score
        quality_score = QualityScorer.calculate_score(all_findings, self.config.PENALTIES)
        quality_rating = QualityScorer.get_rating(quality_score)

        return {
            "status": "success",
            "valid": True,
            "syntax_error": None,
            "quality_score": quality_score,
            "quality_rating": quality_rating,
            "metrics": metrics,
            "warnings": warnings,
            "suggestions": suggestions,
            "todos": todos,
            "fixmes": fixmes,
            "summary": {
                "warning_count": len(warnings),
                "suggestion_count": len(suggestions),
                "todo_count": len(todos),
                "fixme_count": len(fixmes),
                "quality_rating": quality_rating
            }
        }
