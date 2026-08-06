"""Challenge 28 solution — reference implementation with reasoning comments.

Why ast and not regex: the AST knows structure. A regex can't tell a real
`except:` from one inside a string literal; the AST can. Everything here
is a single parse + single walk, which is what keeps it O(N).
"""
from __future__ import annotations

import ast

RULES = ("B006", "E722", "C901", "E501", "E999")


def _is_mutable_default(node: ast.AST) -> bool:
    """True if a default node is a mutable literal or mutable constructor.

    Immutables (None, int, str, tuple, frozenset) must never match.
    """
    if isinstance(node, (ast.List, ast.Dict, ast.Set)):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id in ("list", "dict", "set")
    return False


def find_mutable_defaults(source: str) -> list[tuple[int, str]]:
    """Return [(line, function_name)] for mutable default arguments.

    ast.walk visits every node once: O(N) time, O(N) worst-case space for
    the walker stack. The source is parsed but never executed, so this is
    safe on untrusted input.
    """
    tree = ast.parse(source)
    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(_is_mutable_default(d) for d in node.args.defaults):
                hits.append((node.lineno, node.name))
    return hits


def _count_decisions(node: ast.AST) -> int:
    """Cyclomatic decision points inside a subtree: O(subtree size)."""
    count = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While,
                              ast.ExceptHandler, ast.IfExp, ast.Assert)):
            count += 1
        elif isinstance(child, ast.BoolOp):
            count += len(child.values) - 1
    return count


def _top_level_functions(tree: ast.Module) -> list[ast.FunctionDef]:
    """Top-level function definitions only, in source order."""
    return [n for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def analyze(source: str, max_complexity: int = 10
            ) -> dict[str, list[tuple[int, str]]]:
    """Return {"B006": ..., "E722": ..., "C901": ...} with ONE ast.parse.

    All three rules share one parse and one walk over tree.body — the
    parse-once constraint is the point: re-parsing per rule triples the
    cost for zero benefit.
    """
    tree = ast.parse(source)
    result: dict[str, list[tuple[int, str]]] = {"B006": [], "E722": [], "C901": []}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(_is_mutable_default(d) for d in node.args.defaults):
                result["B006"].append((node.lineno, node.name))
        elif isinstance(node, ast.Try):
            for handler in node.handlers:
                if handler.type is None:
                    result["E722"].append((handler.lineno, "bare except"))

    for fn in _top_level_functions(tree):
        complexity = 1 + _count_decisions(fn)
        if complexity > max_complexity:
            result["C901"].append(
                (fn.lineno, f"{fn.name}: complexity {complexity} > {max_complexity}"))

    return result


def _suppressed_lines(source: str) -> set[int]:
    """Line numbers carrying a noqa comment of any form."""
    return {i + 1 for i, line in enumerate(source.splitlines())
            if "# noqa" in line}


class _LintVisitor(ast.NodeVisitor):
    """One visitor, one pass: every node touched exactly once.

    visit_count lets the test assert O(N) single-pass behavior — the
    performance guard for Gold.
    """

    def __init__(self, max_line_length: int) -> None:
        self.max_line_length = max_line_length
        self.visit_count = 0
        self.violations: dict[str, list[tuple[int, str]]] = {}

    def _add(self, rule: str, line: int, message: str) -> None:
        self.violations.setdefault(rule, []).append((line, message))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        self._function(node)
        self.generic_visit(node)

    def _function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if any(_is_mutable_default(d) for d in node.args.defaults):
            self._add("B006", node.lineno, node.name)

    def visit_Try(self, node: ast.Try) -> None:  # noqa: N802
        for handler in node.handlers:
            if handler.type is None:
                self._add("E722", handler.lineno, "bare except")
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        self.visit_count += 1
        super().generic_visit(node)

    def finish(self, source: str, suppressed: set[int],
               max_complexity: int) -> None:
        """Post-pass rules that need full-tree or text context."""
        for i, line in enumerate(source.splitlines()):
            if len(line) > self.max_line_length:
                self._add("E501", i + 1, f"{len(line)} chars")
        for fn in _top_level_functions(self.tree):  # type: ignore[attr-defined]
            complexity = 1 + _count_decisions(fn)
            if complexity > max_complexity:
                self._add("C901", fn.lineno,
                          f"{fn.name}: complexity {complexity} > {max_complexity}")
        self._apply_noqa(suppressed)

    def _apply_noqa(self, suppressed: set[int]) -> None:
        for rule in list(self.violations):
            self.violations[rule] = [
                v for v in self.violations[rule] if v[0] not in suppressed]
            if not self.violations[rule]:
                del self.violations[rule]


def lint_source(source: str,
                config: dict[str, list[str]] | None = None
                ) -> dict[str, list[tuple[int, str]]]:
    """Full linter: select/ignore config, noqa suppression, E999 safety.

    Why a NodeVisitor instead of repeated ast.walk: one pass over the tree,
    O(N) total, and the visitor count doubles as the performance proof.
    """
    config = config or {}
    selected = set(config.get("select", list(RULES)))
    ignored = set(config.get("ignore", []))
    active = {r for r in selected if r not in ignored}
    max_len = int(config.get("max_line_length", [88])[0]) \
        if config.get("max_line_length") else 88
    max_complexity = int(config.get("max_complexity", [10])[0]) \
        if config.get("max_complexity") else 10

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        lint_source.last_visit_count = 0
        return {"E999": [(exc.lineno or 0, "syntax error")]}

    visitor = _LintVisitor(max_len)
    visitor.tree = tree
    visitor.visit(tree)
    visitor.finish(source, _suppressed_lines(source), max_complexity)
    lint_source.last_visit_count = visitor.visit_count

    return {rule: v for rule, v in visitor.violations.items() if rule in active}
