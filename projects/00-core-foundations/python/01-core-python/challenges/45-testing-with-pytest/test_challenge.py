"""
Challenge 45: Testing — Hidden Tests
====================================
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).parent

def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

solution = _load("solution")
import pytest


def test_run_test_passes():
    ok, msg = solution.run_test(lambda: None)
    assert ok is True and msg == ""


def test_run_test_fails_with_message():
    ok, msg = solution.run_test(lambda: 1 / 0)
    assert ok is False
    assert "division by zero" in msg or "ZeroDivisionError" in msg


def test_run_test_never_raises():
    ok, _ = solution.run_test(lambda: (_ for _ in ()).throw(ValueError("boom")))
    assert ok is False


def test_assert_raises_matching():
    solution.assert_raises(lambda: 1 / 0, ZeroDivisionError)  # no raise


def test_assert_raises_subclass_ok():
    solution.assert_raises(lambda: (_ for _ in ()).throw(ValueError()), Exception)


def test_assert_raises_wrong_type():
    with pytest.raises(AssertionError):
        solution.assert_raises(lambda: 1, ValueError)


def test_assert_raises_no_exception():
    with pytest.raises(AssertionError):
        solution.assert_raises(lambda: None, ValueError)


# --- Gold: mini suite -------------------------------------------------------

def _good():
    return 1


def _bad():
    raise RuntimeError("nope")


def _also_bad():
    raise ValueError("bad")


class _FakeModule:
    """Simulates a module whose test_* functions we want to run."""
    def __init__(self):
        self.test_good = _good
        self.test_bad = _bad
        self.test_also_bad = _also_bad
        self.helper_not_a_test = lambda: None  # must be ignored


def test_run_suite_discovers_and_reports():
    results = solution.run_suite(_FakeModule())
    assert set(results) == {"test_good", "test_bad", "test_also_bad"}, \
        "only test_* callables, all of them"
    assert results["test_good"] is True
    assert results["test_bad"] is False
    assert results["test_also_bad"] is False


def test_run_suite_continues_after_failures():
    results = solution.run_suite(_FakeModule())
    # a failure in one test must not prevent others from running
    assert results["test_also_bad"] is False  # reached despite test_bad failing


def test_summarize():
    assert solution.summarize({"a": True, "b": False, "c": False}) == "1 passed, 2 failed"
    assert solution.summarize({}) == "0 passed, 0 failed"
    assert solution.summarize({"a": True}) == "1 passed, 0 failed"


def test_run_suite_on_empty_module():
    class Empty:
        pass
    assert solution.run_suite(Empty) == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
