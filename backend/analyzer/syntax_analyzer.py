import ast
from typing import Dict, Any, Optional, Tuple

class SyntaxAnalyzer:
    """Analyzes Python source code syntax using ast.parse without code execution."""

    @staticmethod
    def parse_source(source_code: str) -> Tuple[bool, Optional[ast.AST], Optional[Dict[str, Any]]]:
        """
        Parses the provided Python source code.

        Returns:
            Tuple of (is_valid, ast_tree, error_dict)
            If valid: (True, tree, None)
            If invalid: (False, None, error_dict)
        """
        if not source_code or source_code.strip() == "":
            # Empty source is valid Python syntax (empty module)
            try:
                tree = ast.parse("")
                return True, tree, None
            except Exception:
                pass

        try:
            tree = ast.parse(source_code)
            return True, tree, None
        except (SyntaxError, IndentationError) as err:
            category = "IndentationError" if isinstance(err, IndentationError) else "SyntaxError"
            error_info = {
                "category": category,
                "message": err.msg or str(err),
                "line": err.lineno,
                "column": err.offset,
                "text": err.text.strip() if err.text else None
            }
            return False, None, error_info
        except Exception as err:
            return False, None, {
                "category": "SyntaxError",
                "message": f"Parsing failure: {str(err)}",
                "line": None,
                "column": None,
                "text": None
            }
