"""
Challenge 47: Advanced Exceptions — Reference Solution
=======================================================
"""

from __future__ import annotations

from typing import Callable


class AIServiceError(Exception):
    """Base error for any AI-service failure. Catch this, not Exception."""


class RetryableError(AIServiceError):
    """Transient failure (429 rate limit, 503 overloaded). Safe to retry."""


class FatalError(AIServiceError):
    """Permanent failure (400 bad request). Retrying wastes money."""


class ContextWindowExceeded(FatalError):
    """Prompt too long for the model's context window."""


def classify_error(e: Exception) -> str:
    """Return 'retry' for RetryableError, 'fatal' for FatalError, else 'unknown'.

    Why isinstance: subclass checks must classify by base type, so
    ContextWindowExceeded (a FatalError) is 'fatal'. Order matters:
    most-specific first.
    """
    if isinstance(e, RetryableError):
        return "retry"
    if isinstance(e, FatalError):
        return "fatal"
    return "unknown"


def call_with_retry(
    fn: Callable[[], str],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.01,
) -> str:
    """Call fn, retrying ONLY RetryableError with capped exponential backoff.

    Why this approach: only RetryableError is caught (fatal and other
    errors propagate untouched), the delay caps at 1.0s, and the final
    failure is chained `from` the last error so the traceback tells the
    whole story. O(max_attempts) calls, O(1) extra space.
    """
    last_error: RetryableError | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except RetryableError as e:
            last_error = e
            if attempt == max_attempts:
                break
            import time

            time.sleep(min(base_delay * 2 ** attempt, 1.0))
    assert last_error is not None
    raise RetryableError(f"gave up after {max_attempts} attempts") from last_error


def gather_results(
    calls: list[Callable[[], str]],
) -> tuple[list[str], ExceptionGroup | None]:
    """Run each call exactly once; return (successes, ExceptionGroup | None).

    Why this approach: a single pass collects successes and appends
    failures to one list (O(1) amortized per append, O(n) total). If
    anything failed, the failures become an ExceptionGroup so the caller
    can dispatch them with except* — no failure is lost, order is kept.
    """
    results: list[str] = []
    failures: list[Exception] = []
    for fn in calls:
        try:
            results.append(fn())
        except Exception as e:
            failures.append(e)
    if failures:
        return results, ExceptionGroup("partial failure", failures)
    return results, None
