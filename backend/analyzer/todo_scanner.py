import io
import re
import tokenize
from typing import Dict, List, Any

class TodoScanner:
    """Scans Python comments for TODO and FIXME markers using tokenize."""

    TODO_PATTERN = re.compile(r"#\s*(TODO)\b(?:\s*[:\-]?\s*(.*))?", re.IGNORECASE)
    FIXME_PATTERN = re.compile(r"#\s*(FIXME)\b(?:\s*[:\-]?\s*(.*))?", re.IGNORECASE)

    @classmethod
    def scan_comments(cls, source_code: str) -> Dict[str, Any]:
        """
        Scans source code for TODO and FIXME markers exclusively within comment tokens.
        String literals containing 'TODO' or 'FIXME' are ignored.
        """
        todos: List[Dict[str, Any]] = []
        fixmes: List[Dict[str, Any]] = []
        comment_tokens_count = 0

        if not source_code:
            return {
                "todos": todos,
                "fixmes": fixmes,
                "total_comment_tokens": 0,
                "total_markers": 0
            }

        try:
            tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)
            for tok_type, tok_string, (srow, scol), (erow, ecol), line in tokens:
                if tok_type == tokenize.COMMENT:
                    comment_tokens_count += 1
                    raw_comment = tok_string.strip()

                    # Check for TODO
                    todo_match = cls.TODO_PATTERN.search(raw_comment)
                    if todo_match:
                        marker_type = "TODO"
                        message = (todo_match.group(2) or "").strip()
                        todos.append({
                            "type": marker_type,
                            "line": srow,
                            "column": scol,
                            "comment": raw_comment,
                            "message": message or raw_comment
                        })

                    # Check for FIXME
                    fixme_match = cls.FIXME_PATTERN.search(raw_comment)
                    if fixme_match:
                        marker_type = "FIXME"
                        message = (fixme_match.group(2) or "").strip()
                        fixmes.append({
                            "type": marker_type,
                            "line": srow,
                            "column": scol,
                            "comment": raw_comment,
                            "message": message or raw_comment
                        })
        except tokenize.TokenError:
            # In case of unclosed string or token error, fallback to line-by-line comment parsing safely
            lines = source_code.splitlines()
            for idx, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    comment_tokens_count += 1
                    todo_match = cls.TODO_PATTERN.search(stripped)
                    if todo_match:
                        todos.append({
                            "type": "TODO",
                            "line": idx,
                            "column": line.find("#"),
                            "comment": stripped,
                            "message": (todo_match.group(2) or "").strip() or stripped
                        })
                    fixme_match = cls.FIXME_PATTERN.search(stripped)
                    if fixme_match:
                        fixmes.append({
                            "type": "FIXME",
                            "line": idx,
                            "column": line.find("#"),
                            "comment": stripped,
                            "message": (fixme_match.group(2) or "").strip() or stripped
                        })
        except Exception:
            pass

        return {
            "todos": todos,
            "fixmes": fixmes,
            "total_comment_tokens": comment_tokens_count,
            "total_markers": len(todos) + len(fixmes)
        }
