"""
01-core-python — 47: Advanced Exceptions — Errors You Can Build On
===================================================================
Topics: custom exception hierarchies, raise ... from (chaining), ExceptionGroup
        and except*, contextlib.suppress, EAFP vs LBYL, finally semantics,
        retry with exponential backoff and jitter, narrow excepts

Why this matters for AI/backend engineering:
    LLM API calls fail in structured ways: 429/503 are retryable, 400 is not.
    Distinguishing retryable from fatal errors is the difference between a
    resilient service and an incident. Parallel embedding calls need
    ExceptionGroup so three failures out of fifty do not kill the batch.

Run:      python 47-exceptions-advanced.py
Verify:   python 47-exceptions-advanced.py --verify
Reference: https://docs.python.org/3/library/exceptions.html
"""

from __future__ import annotations

import sys
import time
from contextlib import suppress
from typing import Callable

# ============================================================
# 1. Custom Exception Hierarchies
# ============================================================
# A package should expose ONE base exception so callers can catch broadly,
# then refine with subclasses. This is the "narrow at the call site" rule.


class AIServiceError(Exception):
    """Base error for any AI-service failure. Catch this, not Exception."""


class RetryableError(AIServiceError):
    """Transient failure (429 rate limit, 503 overloaded). Safe to retry."""


class FatalError(AIServiceError):
    """Permanent failure (400 bad request). Retrying wastes money."""


class ContextWindowExceeded(FatalError):
    """Prompt too long for the model's context window."""


# Example 1: catching the base class catches all refinements
def classify(e: Exception) -> str:
    if isinstance(e, RetryableError):
        return "retry"
    if isinstance(e, FatalError):
        return "fatal"
    return "unknown"


try:
    raise ContextWindowExceeded("prompt is 200k tokens")
except AIServiceError as e:
    print(f"Caught base AIServiceError: {e}")
    print(f"Action: {classify(e)}")

# Output:
# Caught base AIServiceError: prompt is 200k tokens
# Action: fatal

# ============================================================
# 2. Chaining with `raise ... from`
# ============================================================
# `raise X from Y` sets __cause__ and prints "The above exception was the
# direct cause...". Without `from`, __context__ is set implicitly. Always
# chain: the original traceback is the debugging gold.

# Example 2: explicit chaining
import json  # noqa: E402


def call_model(prompt: str) -> str:
    """Simulate decoding a malformed model response into structured output."""
    try:
        json.loads(prompt)
        return "ok"
    except ValueError as e:
        raise AIServiceError("model returned malformed JSON") from e


try:
    call_model("{not json")
except AIServiceError as e:
    print(f"\nChained error: {e}")
    print(f"  __cause__ set: {e.__cause__ is not None}")
    print(f"  cause type:    {type(e.__cause__).__name__}")

# Output:
# Chained error: model returned malformed JSON
#   __cause__ set: True
#   cause type:    JSONDecodeError

# ============================================================
# 3. ExceptionGroup and except* (Python 3.11+)
# ============================================================
# When a gather() of parallel calls has SOME failures, a bare exception loses
# the successes. ExceptionGroup carries all failures; except* handles them
# by type without aborting the rest.

# Example 3: collecting failures from a fan-out
def embed_all(texts: list[str]) -> list[str]:
    failures: list[Exception] = []
    results: list[str] = []
    for i, t in enumerate(texts):
        if i % 3 == 0:
            failures.append(RetryableError(f"embed call {i} timed out"))
        else:
            results.append(f"vec:{len(t)}")
    if failures:
        raise ExceptionGroup("partial embedding failure", failures)
    return results


try:
    embed_all(["a", "bb", "ccc", "dddd"])
except* RetryableError as eg:
    print(f"\nRetryable group: {len(eg.exceptions)} failures to retry")
except* FatalError as eg:
    print(f"Fatal group: {len(eg.exceptions)} failures to report")

# Output:
# Retryable group: 2 failures to retry

# ============================================================
# 4. contextlib.suppress — Intentional Swallowing
# ============================================================
# suppress(FileNotFoundError) is the readable form of try/except: pass.
# Use ONLY when the failure is genuinely ignorable.

# Example 4: cleanup that may already be done
import os  # noqa: E402

with suppress(FileNotFoundError):
    os.remove("outputs/dbs/checkpoint.tmp")
print("\nsuppress(FileNotFoundError): removal attempted safely")

# Output:
# suppress(FileNotFoundError): removal attempted safely

# ============================================================
# 5. finally Semantics — finally Wins
# ============================================================
# A return inside `finally` OVERRIDES the return in `try`. This is almost
# never what you want in production, but understanding it prevents the bug.

# Example 5: finally overriding a return
def sneaky() -> str:
    try:
        return "from try"
    finally:
        return "from finally"


print(f"\nfinally overrides return: {sneaky()}")

# Output:
# finally overrides return: from finally

# ============================================================
# 6. Production Pattern — Retry with Exponential Backoff + Jitter
# ============================================================
# Retries must be bounded, back off exponentially, and add jitter so a thundering
# herd of clients does not retry in lockstep. Never retry FatalError.


def call_with_retry(
    fn: Callable[[], str],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.05,
) -> str:
    """Call fn, retrying only RetryableError with capped exponential backoff.

    Chosen over tenacity here so the mechanics are visible; tenacity does the
    same thing in production.
    """
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except RetryableError as e:
            last_error = e
            if attempt == max_attempts:
                break
            delay = min(base_delay * (2 ** (attempt - 1)), 2.0)
            time.sleep(delay)  # jitter omitted for deterministic tests
    raise RetryableError(f"gave up after {max_attempts} attempts") from last_error


# Example 6: succeeds on the third attempt
attempts = 0


def flaky() -> str:
    global attempts
    attempts += 1
    if attempts < 3:
        raise RetryableError("overloaded")
    return "ok"


print(f"\nflaky call result: {call_with_retry(flaky)} (attempts: {attempts})")

# Output:
# flaky call result: ok (attempts: 3)

# ============================================================
# 7. EAFP vs LBYL
# ============================================================
# Python idiom is EAFP (Easier to Ask Forgiveness than Permission): try the
# operation, handle the failure. LBYL (Look Before You Leap) races — the state
# can change between the check and the use.

# Example 7: EAFP beats LBYL
def safe_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")


print(f"safe_divide(1, 0): {safe_divide(1, 0)}")
print(f"safe_divide(4, 2): {safe_divide(4, 2)}")

# Output:
# safe_divide(1, 0): inf
# safe_divide(4, 2): 2.0

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: bare `except:` swallows KeyboardInterrupt and SystemExit
#   bad = try: risky()  except: pass          # hides Ctrl-C
# CORRECT:
#   good = try: risky()  except Exception: log.exception("risky failed")

# MISTAKE: catching Exception and re-raising loses the traceback
#   bad = except Exception as e: raise ValueError("x")   # __context__ only
# CORRECT:
#   good = except Exception as e: raise ValueError("x") from e

# MISTAKE: retrying fatal errors burns tokens/money
#   bad = for _ in range(5): try: call() except Exception: sleep()
# CORRECT:
#   good = retry only RetryableError, cap attempts, jitter delays

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # Hierarchy and classification
    assert classify(ContextWindowExceeded("x")) == "fatal", \
        "subclass must be caught as its base type"
    assert classify(RetryableError("y")) == "retry", \
        "RetryableError must classify as retry"

    # Chaining sets __cause__
    try:
        call_model("{bad")
    except AIServiceError as e:
        assert e.__cause__ is not None, "raise ... from must set __cause__"
        assert isinstance(e.__cause__, ValueError), "cause type preserved"

    # ExceptionGroup carries multiple failures
    try:
        embed_all(["a", "bb", "ccc", "dddd"])
    except* RetryableError as eg:
        assert len(eg.exceptions) == 2, "expected 2 retryable failures"

    # suppress swallows only the named type
    with suppress(FileNotFoundError):
        os.remove("outputs/dbs/does-not-exist.tmp")
    assert not os.path.exists("outputs/dbs/does-not-exist.tmp"), \
        "suppress must not raise"

    # finally overrides return
    assert sneaky() == "from finally", "finally return overrides try return"

    # Retry succeeds on attempt 3 without touching attempts counter again
    global attempts
    attempts = 0
    assert call_with_retry(flaky) == "ok"
    assert attempts == 3, "must succeed on exactly the third attempt"

    # EAFP divide
    assert safe_divide(1, 0) == float("inf"), "division by zero -> inf"

    # Retry must NOT retry fatal errors (fails fast)
    try:
        call_with_retry(lambda: (_ for _ in ()).throw(FatalError("400")))
        assert False, "fatal error must propagate immediately"
    except FatalError:
        pass

    print("[OK] 47-exceptions-advanced: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. One package base exception; refine with subclasses")
        print("2. raise ... from keeps the original traceback")
        print("3. ExceptionGroup + except* for parallel fan-out failures")
        print("4. Retry only RetryableError, with bounded backoff")
        print("5. Prefer EAFP; never bare except:")
        _verify()
