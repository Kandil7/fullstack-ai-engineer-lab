"""
Challenge 47: Advanced Exceptions — Tests
==========================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/47-exceptions-advanced/test_challenge.py -q

Performance guards use operation counting (call counts), never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(
    TARGET, Path(__file__).parent / f"{TARGET}.py"
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


def _flaky(counter: list[int], fail_until: int) -> "callable":
    """Worker that raises RetryableError until `fail_until` calls happened."""

    def fn() -> str:
        counter.append(1)
        if len(counter) < fail_until:
            raise mod.RetryableError("429 rate limited")
        return "ok"

    return fn


class TestClassifyError:
    """Bronze: classification via isinstance, subclasses included."""

    def test_retryable(self) -> None:
        assert mod.classify_error(mod.RetryableError("429")) == "retry"

    def test_fatal(self) -> None:
        assert mod.classify_error(mod.FatalError("400")) == "fatal"

    def test_subclass_classifies_as_base(self) -> None:
        assert mod.classify_error(mod.ContextWindowExceeded("too long")) == "fatal"

    def test_unknown(self) -> None:
        assert mod.classify_error(ValueError("other")) == "unknown"
        assert mod.classify_error(RuntimeError("boom")) == "unknown"

    def test_empty_message(self) -> None:
        assert mod.classify_error(mod.RetryableError()) == "retry"


class TestCallWithRetry:
    """Silver: retry only retryable, bounded, chained final failure."""

    def test_succeeds_on_third_attempt(self) -> None:
        counter: list[int] = []
        result = mod.call_with_retry(_flaky(counter, 3), max_attempts=4, base_delay=0.0)
        assert result == "ok"
        assert len(counter) == 3, "must not retry after success"

    def test_gives_up_after_max_attempts(self) -> None:
        counter: list[int] = []
        with pytest.raises(mod.RetryableError) as exc:
            mod.call_with_retry(_flaky(counter, 999), max_attempts=4, base_delay=0.0)
        assert len(counter) == 4, "exactly max_attempts calls, no more, no fewer"
        assert exc.value.__cause__ is not None, "final failure must be chained from"

    def test_fatal_not_retried(self) -> None:
        counter: list[int] = []

        def fatal() -> str:
            counter.append(1)
            raise mod.FatalError("400 bad request")

        with pytest.raises(mod.FatalError):
            mod.call_with_retry(fatal, max_attempts=4, base_delay=0.0)
        assert len(counter) == 1, "fatal error must not be retried"

    def test_other_exceptions_not_retried(self) -> None:
        counter: list[int] = []

        def value_error() -> str:
            counter.append(1)
            raise ValueError("schema")

        with pytest.raises(ValueError):
            mod.call_with_retry(value_error, max_attempts=4, base_delay=0.0)
        assert len(counter) == 1

    def test_max_attempts_one(self) -> None:
        counter: list[int] = []
        with pytest.raises(mod.RetryableError):
            mod.call_with_retry(_flaky(counter, 2), max_attempts=1, base_delay=0.0)
        assert len(counter) == 1

    def test_first_attempt_success(self) -> None:
        counter: list[int] = []
        result = mod.call_with_retry(_flaky(counter, 1), max_attempts=4, base_delay=0.0)
        assert result == "ok"
        assert len(counter) == 1

    def test_performance_guard_large_attempts(self) -> None:
        """Operation-counting guard: always-failing fn is called exactly
        max_attempts times even when max_attempts is large (10^3)."""
        counter: list[int] = []
        with pytest.raises(mod.RetryableError):
            mod.call_with_retry(_flaky(counter, 10**6), max_attempts=10**3, base_delay=0.0)
        assert len(counter) == 10**3, "bound is exactly max_attempts"


class TestGatherResults:
    """Gold: single-pass fan-out, all failures grouped in order."""

    def test_empty(self) -> None:
        results, group = mod.gather_results([])
        assert results == []
        assert group is None

    def test_all_success(self) -> None:
        results, group = mod.gather_results([lambda: "a", lambda: "b"])
        assert results == ["a", "b"]
        assert group is None

    def test_all_fail(self) -> None:
        failures = [mod.RetryableError("1"), mod.FatalError("2")]
        results, group = mod.gather_results([lambda: (_ for _ in ()).throw(failures[0]),
                                             lambda: (_ for _ in ()).throw(failures[1])])
        assert results == []
        assert group is not None
        assert len(group.exceptions) == 2

    def test_mixed_keeps_order_and_identity(self) -> None:
        e1 = mod.RetryableError("a fail")
        e3 = ValueError("non-hierarchy exception")
        calls = [lambda: "ok1",
                 lambda: (_ for _ in ()).throw(e1),
                 lambda: "ok2",
                 lambda: (_ for _ in ()).throw(e3)]
        results, group = mod.gather_results(calls)
        assert results == ["ok1", "ok2"]
        assert group is not None
        assert group.exceptions[0] is e1, "original exception objects preserved"
        assert group.exceptions[1] is e3
        assert type(group).__name__ == "ExceptionGroup"

    def test_single_pass_call_count_guard(self) -> None:
        """Operation-counting guard: every call executes exactly once."""
        counter: list[int] = []
        n = 300

        def make_fn(i: int) -> "callable":
            def fn() -> str:
                counter.append(i)
                if i % 3 == 0:
                    raise mod.RetryableError(f"worker {i} failed")
                return f"result-{i}"

            return fn

        calls = [make_fn(i) for i in range(n)]
        expected_failures = sum(1 for i in range(n) if i % 3 == 0)
        results, group = mod.gather_results(calls)
        assert len(counter) == n, "each call must execute exactly once (single pass)"
        assert len(results) == n - expected_failures
        assert group is not None and len(group.exceptions) == expected_failures
        # Group order matches the original call order (indices 0, 3, 6, ...)
        assert all(isinstance(x, mod.RetryableError) for x in group.exceptions)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
