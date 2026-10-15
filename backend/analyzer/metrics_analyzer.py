import ast
from typing import Dict, Any, List, Optional
from .todo_scanner import TodoScanner

class MetricsAnalyzer:
    """Calculates code metrics from AST and source tokens without executing code."""

    @classmethod
    def calculate_metrics(cls, source_code: str, tree: Optional[ast.AST]) -> Dict[str, Any]:
        """
        Calculates all 8 required metrics:
        - total_lines
        - functions
        - classes
        - imports
        - loops
        - conditions
        - comments
        - cyclomatic_complexity
        """
        # 1. Total lines
        if not source_code:
            total_lines = 0
        else:
            lines = source_code.splitlines()
            total_lines = len(lines)

        # 2. Comments count from tokenize
        scan_result = TodoScanner.scan_comments(source_code)
        comments_count = scan_result["total_comment_tokens"]

        if tree is None:
            return {
                "total_lines": total_lines,
                "functions": 0,
                "classes": 0,
                "imports": 0,
                "loops": 0,
                "conditions": 0,
                "comments": comments_count,
                "cyclomatic_complexity": 0
            }

        # AST nodes counting
        function_nodes = []
        class_nodes = []
        import_count = 0
        loop_count = 0
        condition_count = 0

        for node in ast.walk(tree):
            # Functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_nodes.append(node)
            # Classes
            elif isinstance(node, ast.ClassDef):
                class_nodes.append(node)
            # Imports (count import statements, not imported names)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_count += 1
            # Loops
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                loop_count += 1
            # Conditions
            elif isinstance(node, (ast.If, ast.IfExp)):
                condition_count += 1

        functions_count = len(function_nodes)
        classes_count = len(class_nodes)

        # Cyclomatic complexity
        complexity = cls.calculate_cyclomatic_complexity(source_code, tree, function_nodes)

        return {
            "total_lines": total_lines,
            "functions": functions_count,
            "classes": classes_count,
            "imports": import_count,
            "loops": loop_count,
            "conditions": condition_count,
            "comments": comments_count,
            "cyclomatic_complexity": complexity
        }

    @classmethod
    def count_decision_points_in_node(cls, node: ast.AST, stop_at_functions: bool = True) -> int:
        """Counts decision points within an AST node, avoiding nested function bodies if stop_at_functions is True."""
        decisions = 0
        
        # Traverse node children
        for child in ast.iter_child_nodes(node):
            if stop_at_functions and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Do not recurse into nested function bodies for this scope
                continue

            if isinstance(child, (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)):
                decisions += 1
            elif isinstance(child, ast.BoolOp):
                # 'a and b and c' has (len - 1) boolean decision branches
                decisions += max(1, len(child.values) - 1)

            decisions += cls.count_decision_points_in_node(child, stop_at_functions=stop_at_functions)

        return decisions

    @classmethod
    def calculate_function_complexities(cls, function_nodes: List[ast.AST]) -> List[Dict[str, Any]]:
        """Calculates complexity per function (1 + decision points in that function)."""
        func_complexities = []
        for fn in function_nodes:
            decisions = cls.count_decision_points_in_node(fn, stop_at_functions=True)
            func_complexities.append({
                "name": getattr(fn, "name", "<anonymous>"),
                "line": getattr(fn, "lineno", 1),
                "complexity": 1 + decisions,
                "node": fn
            })
        return func_complexities

    @classmethod
    def calculate_cyclomatic_complexity(cls, source_code: str, tree: ast.AST, function_nodes: List[ast.AST]) -> int:
        """
        Aggregate cyclomatic complexity:
        - For an empty file, returns 0.
        - For a valid non-empty file with no decisions, returns 1.
        - Otherwise, calculates module-level decision points + function decision points + 1.
        """
        if not source_code or not source_code.strip():
            return 0

        # Calculate module-level decisions (outside top-level functions)
        module_decisions = 0
        for child in ast.iter_child_nodes(tree):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if isinstance(child, (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)):
                module_decisions += 1
            elif isinstance(child, ast.BoolOp):
                module_decisions += max(1, len(child.values) - 1)
            module_decisions += cls.count_decision_points_in_node(child, stop_at_functions=True)

        # Sum of decisions across all functions
        total_func_decisions = 0
        for fn in function_nodes:
            total_func_decisions += cls.count_decision_points_in_node(fn, stop_at_functions=True)

        total_decisions = module_decisions + total_func_decisions
        return max(1, 1 + total_decisions)
