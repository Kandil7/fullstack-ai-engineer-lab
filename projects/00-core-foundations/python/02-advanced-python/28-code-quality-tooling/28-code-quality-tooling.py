"""
Advanced Python — 28: Code Quality Tooling
=============================================
Topics: ruff (lint+format), black, mypy, pre-commit, bandit, pip-audit,
complexity metrics, CI gating, noqa discipline

Why this matters for AI/backend engineering:
    ML codebases move fast: a notebook becomes a service in weeks. A lint gate
    catches the mutable-default and bare-except bugs that notebook-derived
    code ships with, before they corrupt a training run or crash an endpoint.
    The rules are implemented as pure-Python ast checks so they run anywhere
    (including offline CI with no ruff installed) — the same ideas the real
    tools encode, testable in-process.

Run:      python 28-code-quality-tooling.py
Verify:   python 28-code-quality-tooling.py --verify
Reference: https://docs.python.org/3/library/ast.html
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass, field


# ============================================================
# 1. The Lint Pipeline
# ============================================================
# Linting = parse source into an AST, walk the tree, flag patterns.
# This is exactly what ruff/flake8 do; the ast module gives us the
# same machinery with zero dependencies.
# Complexity: O(N) time / O(N) space over the AST — every node visited once.

# Example 1: the AST is a tree of nodes, not text
sample = "def f(x):\n    return x + 1\n"
tree = ast.parse(sample)
print(f"Module body has {len(tree.body)} statement(s): "
      f"{type(tree.body[0]).__name__} at line {tree.body[0].lineno}")

# Output:
# Module body has 1 statement(s): FunctionDef at line 1


# ============================================================
# 2. Rule: Mutable Default Arguments (ruff B006)
# ============================================================
# def f(items=[]): ... shares ONE list across all calls. The classic
# notebook bug. Detect: defaults that are list/dict/set literals or
# calls to list()/dict()/set().

def find_mutable_defaults(source: str) -> list[tuple[int, str]]:
    """Return [(line, function_name)] for functions with mutable defaults.

    AST walk is O(N) over the tree; no code is executed, so this is
    safe to run on untrusted source.
    """
    tree = ast.parse(source)
    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults:
                bad = isinstance(default, (ast.List, ast.Dict, ast.Set))
                if isinstance(default, ast.Call) and isinstance(default.func, ast.Name):
                    bad = bad or default.func.id in ("list", "dict", "set")
                if bad:
                    hits.append((node.lineno, node.name))
    return hits


# Example 2: catching the bug
bad_source = (
    "def append_item(store=[]):\n"
    "    store.append(1)\n"
    "    return store\n"
    "\n"
    "def log(msg, level='info'):\n"
    "    print(level, msg)\n"
)
print(f"Mutable defaults found: {find_mutable_defaults(bad_source)}")

# Output:
# Mutable defaults found: [(1, 'append_item')]


# ============================================================
# 3. Rule: Bare Except (ruff E722)
# ============================================================
# except: catches KeyboardInterrupt and SystemExit too, swallowing
# Ctrl-C during a long training job. Always name the exception.

def find_bare_excepts(source: str) -> list[int]:
    """Return line numbers of bare `except:` handlers. O(N) AST walk."""
    tree = ast.parse(source)
    hits: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                if handler.type is None:
                    hits.append(handler.lineno)
    return hits


# Example 3: bare except vs named except
except_source = (
    "try:\n"
    "    risky()\n"
    "except:\n"          # BARE — swallows KeyboardInterrupt
    "    pass\n"
    "try:\n"
    "    risky()\n"
    "except ValueError:\n"   # named — correct
    "    pass\n"
)
print(f"Bare excepts at lines: {find_bare_excepts(except_source)}")

# Output:
# Bare excepts at lines: [3]


# ============================================================
# 4. Rule: Cyclomatic Complexity (ruff C901)
# ============================================================
# Complexity = 1 + number of decision points (if/for/while/except/
# and/or/ternary). Roughly: "how many independent paths". Teams gate
# at 10; anything above ~15 is untestable.

def _count_decisions(node: ast.AST) -> int:
    """Count decision points in a subtree. O(subtree size)."""
    count = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While,
                              ast.ExceptHandler, ast.IfExp, ast.Assert)):
            count += 1
        elif isinstance(child, ast.BoolOp):
            count += len(child.values) - 1
    return count


def complexity_by_function(source: str) -> dict[str, int]:
    """Map top-level function name -> cyclomatic complexity. O(N)."""
    tree = ast.parse(source)
    result: dict[str, int] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = 1 + _count_decisions(node)
    return result


def complexity_violations(source: str, max_complexity: int = 10
                          ) -> list[tuple[int, str]]:
    """Return [(lineno, message)] for functions over the cap. O(N)."""
    tree = ast.parse(source)
    hits: list[tuple[int, str]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = 1 + _count_decisions(node)
            if complexity > max_complexity:
                hits.append((node.lineno,
                             f"{node.name}: complexity {complexity} > "
                             f"{max_complexity}"))
    return hits


# Example 4: complexity of a clean vs tangled function
complex_source = (
    "def simple(x):\n"
    "    return x * 2\n"
    "\n"
    "def tangled(a, b, c):\n"
    "    if a and b or c:\n"
    "        for i in range(10):\n"
    "            if i % 2:\n"
    "                pass\n"
    "    return None\n"
)
print(f"Complexities: {complexity_by_function(complex_source)}")

# Output:
# Complexities: {'simple': 1, 'tangled': 6}


# ============================================================
# 5. Rule: Docstrings, Line Length, Trailing Whitespace
# ============================================================
# D100: public functions need docstrings. E501: lines > max length.
# W291: trailing whitespace (invisible diffs in review).

def missing_docstrings(source: str) -> list[tuple[int, str]]:
    """Return [(line, name)] for functions/classes without docstrings."""
    tree = ast.parse(source)
    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node) is None:
                hits.append((node.lineno, node.name))
    return hits


def line_length_violations(source: str, max_len: int = 88) -> list[tuple[int, int]]:
    """Return [(line, actual_length)] for lines over max_len. O(L)."""
    return [(i + 1, len(line))
            for i, line in enumerate(source.splitlines())
            if len(line) > max_len]


def trailing_whitespace_lines(source: str) -> list[int]:
    """Return line numbers ending in space/tab. O(L)."""
    return [i + 1 for i, line in enumerate(source.splitlines())
            if line != line.rstrip()]


# Example 5: three text-level rules at once
messy_source = (
    "def no_doc(a):\n"
    "    return a\n"
    "\n"
    "x = 1  \n"      # trailing spaces
    "y = 'a line that is definitely longer than eighty eight characters for sure'\n"
)
print(f"Missing docstrings: {missing_docstrings(messy_source)}")
print(f"Long lines: {line_length_violations(messy_source, 60)}")
print(f"Trailing whitespace: {trailing_whitespace_lines(messy_source)}")

# Output:
# Missing docstrings: [(1, 'no_doc')]
# Long lines: [(5, 76)]
# Trailing whitespace: [4]


# ============================================================
# 6. noqa Discipline
# ============================================================
# `# noqa: CODE` suppresses a rule on one line. Discipline: suppress
# only what you understand, always with a reason on the same line.
# A blanket `# noqa` on a file hides future bugs.

def suppressed_lines(source: str) -> set[int]:
    """Return line numbers carrying a noqa comment. O(L)."""
    return {i + 1 for i, line in enumerate(source.splitlines())
            if "# noqa" in line}


# Example 6: noqa scoped to one line
noqa_source = (
    "import os\n"
    "\n"
    "def handler():\n"
    "    try:\n"
    "        os.remove('tmp.txt')\n"
    "    except OSError:  # noqa: BLE001 - missing file is fine here\n"
    "        pass\n"
)
print(f"Suppressed lines: {sorted(suppressed_lines(noqa_source))}")

# Output:
# Suppressed lines: [6]


# ============================================================
# 7. CI Gating
# ============================================================
# The gate runs on every PR. Rules selectable/ignorable via config;
# the gate FAILS the build when violations land. Pre-commit runs it
# locally so CI only sees clean code.

RULES = ("B006", "E722", "C901", "D100", "E501", "W291")


@dataclass
class LintConfig:
    """Which rules run, and the thresholds. Matches ruff's select/ignore."""
    select: set[str] = field(default_factory=lambda: set(RULES))
    ignore: set[str] = field(default_factory=set)
    max_line_length: int = 88
    max_complexity: int = 10


@dataclass
class LintReport:
    """A machine-readable result for the CI gate."""
    violations: dict[str, list[tuple[int, str]]] = field(default_factory=dict)
    clean: bool = True

    def sorted_violations(self) -> dict[str, list[tuple[int, str]]]:
        """Return violations sorted by line for stable diffs."""
        return {rule: sorted(v) for rule, v in self.violations.items()}


def lint_source(source: str, config: LintConfig | None = None) -> LintReport:
    """Run all selected rules; honor noqa; produce a gate report. O(N)."""
    config = config or LintConfig()
    active = {r for r in config.select if r not in config.ignore}
    report = LintReport()

    # Parse once, reuse for every AST rule (the efficient pattern).
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        report.violations["E999"] = [(exc.lineno or 0, "syntax error")]
        report.clean = False
        return report

    suppressed = suppressed_lines(source)

    def check(rule: str, hits: list[tuple[int, str]]) -> None:
        """Record hits not suppressed by a noqa on the same line."""
        if rule not in active:
            return
        kept = [h for h in hits if h[0] not in suppressed]
        if kept:
            report.violations[rule] = kept
            report.clean = False

    check("B006", find_mutable_defaults(source))
    check("E722", [(line, "bare except") for line in find_bare_excepts(source)])
    check("D100", missing_docstrings(source))
    check("E501", [(line, f"{length} chars") for line, length
                   in line_length_violations(source, config.max_line_length)])
    check("W291", [(line, "trailing whitespace")
                   for line in trailing_whitespace_lines(source)])
    check("C901", complexity_violations(source, config.max_complexity))
    return report


# Example 7: gating a bad file vs a clean one
bad_file = (
    "def process(data=[]):\n"          # B006
    "    try:\n"
    "        return data.pop()\n"
    "    except:\n"                    # E722
    "        pass\n"
)
clean_file = (
    "def process(data: list[int]) -> int:\n"
    "    \"\"\"Pop the last item; return 0 on empty input.\"\"\"\n"
    "    try:\n"
    "        return data.pop()\n"
    "    except IndexError:\n"
    "        return 0\n"
)
report_bad = lint_source(bad_file)
report_good = lint_source(clean_file)
print(f"Bad file clean? {report_bad.clean}  violations: "
      f"{sorted(report_bad.violations)}")
print(f"Good file clean? {report_good.clean}")

# Output:
# Bad file clean? False  violations: ['B006', 'D100', 'E722']
# Good file clean? True


# ============================================================
# 8. Production Pattern
# ============================================================
# The full toolchain, not just the linter: ruff formats and lints,
# black guarantees a single style, mypy checks types statically,
# pre-commit runs all of it locally, bandit scans for security
# smells, pip-audit checks dependencies against CVE feeds.
# The gate() below is what a CI pipeline calls.

def gate(path: str, config: LintConfig | None = None) -> bool:
    """Lint a file from disk; True = ship it. Reads file, O(file size)."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            source = fh.read()
    except OSError:
        return False
    return lint_source(source, config).clean


# Example 8: reading our own file through the gate (self-lint)
import os  # noqa: E402 - import here to keep the demo self-contained

SELF = os.path.join(os.path.dirname(__file__), "28-code-quality-tooling.py")
print(f"Self-lint passes the gate? {gate(SELF)}")

# Output:
# Self-lint passes the gate? True


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: disabling a rule project-wide because one spot annoys you
#   [tool.ruff] ignore = ["E722"]      # hides every future bare except
# CORRECT: per-line suppression with a reason
#   except:  # noqa: E722 - caller validated input; deliberate catch-all
#
# MISTAKE: running lint only in CI, never locally
#   Lint runs at commit time (pre-commit), not after merge.
#
# MISTAKE: using text regexes instead of ast for Python checks
#   regex can't know that `except:` inside a string literal is safe;
#   the AST knows. Prefer ast for anything structural.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:  # noqa: C901 - 12 asserts are flat, not nested; suppress with reason
    """Assert every claim this file makes. Silent on success."""
    assert find_mutable_defaults("def f(a=[]):\n    return a\n") == [(1, "f")], \
        "mutable default argument must be detected"
    assert find_mutable_defaults("def f(a=None):\n    return a\n") == [], \
        "None default must NOT be flagged as mutable"
    assert find_mutable_defaults("def f(a=list()):\n    return a\n") == [(1, "f")], \
        "list() call default must be detected"

    assert find_bare_excepts("try:\n    x()\nexcept ValueError:\n    pass\n") == [], \
        "named except must not be flagged"
    assert find_bare_excepts("try:\n    x()\nexcept:\n    pass\n") == [3], \
        "bare except must be flagged at its own line"

    assert complexity_by_function("def f(x):\n    return x\n") == {"f": 1}, \
        "linear function has complexity 1"
    assert complexity_by_function(
        "def f(x):\n    if x:\n        return 1\n    return 0\n") == {"f": 2}, \
        "one branch adds one point of complexity"

    assert missing_docstrings("def f():\n    pass\n") == [(1, "f")], \
        "missing docstring must be reported"
    assert missing_docstrings('def f():\n    """doc."""\n    pass\n') == [], \
        "docstring presence must be respected"

    assert line_length_violations("x = '0123456789'\n", 5) == [(1, 16)], \
        "overlong line must be reported with actual length"
    assert trailing_whitespace_lines("a = 1  \nb = 2\n") == [1], \
        "trailing whitespace must be found"

    bad = lint_source("def f(x=[]):\n    return x\n")
    assert not bad.clean and "B006" in bad.violations, \
        "gate must fail on mutable defaults"

    suppressed_ok = lint_source(
        "def f(x=[]):  # noqa: B006 - API contract requires a shared list\n"
        "    return x\n")
    assert suppressed_ok.clean, \
        "noqa with a rule code must suppress that rule on that line"

    gated = LintConfig(ignore={"E722"})
    assert lint_source("try:\n    x()\nexcept:\n    pass\n", gated).clean, \
        "config ignore must disable a rule"

    assert lint_source("def broken(:\n").violations.get("E999"), \
        "syntax errors must be reported, not crash the gate"

    assert gate(__file__), \
        "this file must pass its own gate (self-lint)"

    print("[OK] 28-code-quality-tooling: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Lint rules are AST walks: parse once, walk O(N), flag patterns")
        print("2. noqa is per-line discipline, never a project-wide escape hatch")
        print("3. CI gates on the report, and pre-commit runs it before merge")
        print("4. ruff/black/mypy/bandit/pip-audit are the production stack")
        _verify()
