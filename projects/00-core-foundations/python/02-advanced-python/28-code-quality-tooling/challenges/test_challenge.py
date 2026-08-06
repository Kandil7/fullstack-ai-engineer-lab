"""
Challenge 28: Code Quality Tooling — Hidden Tests
==================================================
Correctness + edge cases + parse-once / single-pass / memory guards.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
import tracemalloc
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
starter = _load("starter")


# --- Bronze: find_mutable_defaults -----------------------------------------

def test_bronze_list_literal():
    assert solution.find_mutable_defaults("def f(a=[]):\n    pass\n") == [(1, "f")]


def test_bronze_dict_and_set_literals():
    src = "def g(a={}):\n    pass\ndef h(b={1, 2}):\n    pass\n"
    assert solution.find_mutable_defaults(src) == [(1, "g"), (3, "h")]


def test_bronze_constructor_calls():
    assert solution.find_mutable_defaults("def f(a=list()):\n    pass\n") == [(1, "f")]
    assert solution.find_mutable_defaults("def f(a=dict()):\n    pass\n") == [(1, "f")]


def test_bronze_immutables_never_flagged():
    src = "def f(a=None, b=5, c='x', d=(1, 2), e=1.5):\n    pass\n"
    assert solution.find_mutable_defaults(src) == []


def test_bronze_mixed_defaults():
    src = "def f(a=None, b=[]):\n    pass\n"
    assert solution.find_mutable_defaults(src) == [(1, "f")]


def test_bronze_nested_function():
    src = "def outer():\n    def inner(x=[]):\n        return x\n    return inner\n"
    assert solution.find_mutable_defaults(src) == [(2, "inner")]


def test_bronze_empty_and_comment_only_source():
    assert solution.find_mutable_defaults("") == []
    assert solution.find_mutable_defaults("# just a comment\n") == []


def test_bronze_mutable_default_in_string_is_safe():
    src = 'def f():\n    """Contains [] in text."""\n    return 1\n'
    assert solution.find_mutable_defaults(src) == []


# --- Silver: analyze --------------------------------------------------------

def test_silver_returns_all_rules():
    result = solution.analyze("def f(x=[]):\n    return x\n")
    assert set(result) == {"B006", "E722", "C901"}
    assert result["B006"] == [(1, "f")]


def test_silver_bare_except_lines():
    src = "try:\n    x()\nexcept:\n    pass\n"
    assert solution.analyze(src)["E722"] == [(3, "bare except")]


def test_silver_named_except_not_flagged():
    src = "try:\n    x()\nexcept ValueError:\n    pass\n"
    assert solution.analyze(src)["E722"] == []


def test_silver_complexity_threshold():
    src = "def f(x):\n    if x:\n        return 1\n    return 0\n"
    assert solution.analyze(src)["C901"] == []  # complexity 2 <= 10
    hits = solution.analyze(src, max_complexity=1)["C901"]
    assert len(hits) == 1 and "f" in hits[0][1]


def test_silver_parse_once_guard(monkeypatch):
    # The point of Silver: ONE ast.parse for all three rules.
    calls = {"n": 0}
    original = ast.parse

    def counting_parse(source, *args, **kwargs):
        calls["n"] += 1
        return original(source, *args, **kwargs)

    monkeypatch.setattr(ast, "parse", counting_parse)
    solution.analyze(
        "def f(x=[]):\n    try:\n        x()\n    except:\n        pass\n")
    assert calls["n"] == 1, "analyze must parse the source exactly once"


def test_silver_does_not_execute_source():
    # The analyzed source must never run: a stray print inside would execute
    # only if the solution evals the code instead of parsing it.
    src = "print('RAN')\ndef f(a=[]):\n    pass\n"
    assert solution.find_mutable_defaults(src) == [(2, "f")]


# --- Gold: lint_source ------------------------------------------------------

def test_gold_empty_result_on_clean():
    src = 'def f(x: int) -> int:\n    """Add one."""\n    return x + 1\n'
    assert solution.lint_source(src) == {}


def test_gold_b006_and_message():
    result = solution.lint_source("def f(x=[]):\n    return x\n")
    assert result["B006"] == [(1, "f")]


def test_gold_noqa_suppresses():
    src = "def f(x=[]):  # noqa: B006\n    return x\n"
    assert solution.lint_source(src) == {}


def test_gold_noqa_without_code_suppresses():
    src = "def f(x=[]):  # noqa\n    return x\n"
    assert solution.lint_source(src) == {}


def test_gold_select_ignore_config():
    src = "def f(x=[]):\n    return x\n"
    config = {"select": ["B006", "E722"]}
    assert set(solution.lint_source(src, config)) == {"B006"}
    config_ignore = {"select": ["B006"], "ignore": ["B006"]}
    assert solution.lint_source(src, config_ignore) == {}


def test_gold_e501_line_length():
    long_line = "x = '" + "a" * 100 + "'\n"
    result = solution.lint_source(long_line)
    assert result["E501"][0][0] == 1


def test_gold_e999_syntax_error_does_not_crash():
    result = solution.lint_source("def broken(:\n")
    assert result["E999"][0][1] == "syntax error"


def test_gold_single_pass_visit_count():
    src = "def f(a):\n    if a:\n        return 1\n    return 0\n"
    solution.lint_source(src)
    total_nodes = sum(1 for _ in ast.walk(ast.parse(src)))
    assert solution.lint_source.last_visit_count == total_nodes, \
        "every AST node visited exactly once (O(N) single pass)"


def test_gold_large_source_performance():
    big = "\n".join(
        p for i in range(2000) for p in
        ('def f%d(a%d):' % (i, i), '    return a%d + 1' % i))
    solution.lint_source(big)
    total_nodes = sum(1 for _ in ast.walk(ast.parse(big)))
    assert solution.lint_source.last_visit_count == total_nodes


def test_gold_memory_guard():
    # The linter must be linear: peak memory within 2x of a bare ast.parse
    # on the same source (the AST dominates; 3.13 nodes are heavy).
    big = "\n".join(
        p for i in range(2000) for p in
        ('def f%d(a%d):' % (i, i), '    return a%d + 1' % i))
    tracemalloc.start()
    ast.parse(big)
    _, parse_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    solution.lint_source(big)
    _, lint_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert lint_peak < parse_peak * 2 + 1_000_000, \
        f"lint peak {lint_peak} must stay ~2x parse peak {parse_peak}"


def test_gold_edge_empty_and_comments():
    assert solution.lint_source("") == {}
    assert solution.lint_source("# nothing here\n\n") == {}


# --- Starter must be unimplemented -----------------------------------------

def test_starter_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.find_mutable_defaults("def f(a=[]):\n    pass\n")
    with pytest.raises(NotImplementedError):
        starter.analyze("def f(x):\n    return x\n")
    with pytest.raises(NotImplementedError):
        starter.lint_source("def f(x):\n    return x\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
