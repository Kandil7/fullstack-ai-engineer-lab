"""Challenge 45 solution — reference implementation with reasoning comments."""
from __future__ import annotations

import inspect
import traceback


def run_test(fn) -> tuple[bool, str]:
    """Run a zero-arg test; return (passed, error_message)."""
    try:
        fn()
        return True, ""
    except Exception as e:  # noqa: BLE001 - the framework reports, not hides
        return False, f"{type(e).__name__}: {e}"


def assert_raises(fn, exc_type: type) -> None:
    """Mini pytest.raises: pass if fn raises exc_type (or a subclass)."""
    try:
        fn()
    except exc_type:
        return
    except Exception:
        raise AssertionError(f"{fn} raised the wrong exception type")
    raise AssertionError(f"{fn} did not raise {exc_type.__name__}")


def run_suite(module) -> dict[str, bool]:
    """Discover test_* callables and run each, isolating failures.

    Discovery is by attribute name + callable check; a failing test must not
    stop the remaining tests, so each runs through run_test().
    """
    results: dict[str, bool] = {}
    for name in sorted(dir(module)):
        if not name.startswith("test_"):
            continue
        fn = getattr(module, name)
        if not callable(fn):
            continue
        ok, _ = run_test(fn)
        results[name] = ok
    return results


def summarize(results: dict[str, bool]) -> str:
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    return f"{passed} passed, {failed} failed"
