# 01-core-python — 47: Advanced Exceptions — Errors You Can Build On

## Topic Overview

Basic `try/except` catches errors; advanced exception design *uses* them as
control signals. Real AI services distinguish retryable failures (429 rate
limits, 503 overloads, timeouts) from fatal ones (400 bad requests, auth
failures) and route each differently. This lecture covers custom exception
hierarchies, chaining with `raise ... from`, `ExceptionGroup` for parallel
fan-out (3.11+), `contextlib.suppress`, the subtle `finally` semantics, the
EAFP vs LBYL idiom, and the retry-with-backoff pattern every networked
service needs.

For AI engineers this is the daily reality of LLM calls: they fail, they rate
limit, they return malformed JSON, and fifty parallel embedding calls rarely
all succeed. The code that classifies failures and retries only the retryable
ones is the code that keeps a RAG service alive under load.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design a package exception hierarchy with one base class and refined subclasses
2. Chain exceptions with `raise ... from` and explain `__cause__` vs `__context__`
3. Collect multiple failures into an `ExceptionGroup` and dispatch them with `except*`
4. Swallow specific exceptions with `contextlib.suppress` and know when it is safe
5. Explain `finally` semantics, including the return-override trap
6. Implement bounded retry with exponential backoff and jitter
7. Distinguish EAFP from LBYL and choose the right one per situation
8. Write narrow excepts and never swallow `KeyboardInterrupt` or `SystemExit`
9. Route classified errors to the right handling path in a request pipeline

## Prerequisites

| Need | Where |
|------|-------|
| Basic `try/except/else/finally` | `30-try-except.py` |
| Raising and catching builtin exceptions | `30-try-except.py` |
| Iterating and list building (for fan-out patterns) | `20-for.py`, `13-lists.py` |
| Context managers | `02-advanced-python/03-context-managers-lecture.md` |

## 1. Custom Exception Hierarchies

A package should expose **one base exception** so callers can catch broadly
and safely, then refine behavior with subclasses. The rule "narrow at the
call site" means your library code may raise any subclass, but your public
API documents the base class. Callers then use `isinstance` checks to decide
the action — this is how a client library tells you *what you can do about*
the failure.

```python
class AIServiceError(Exception):
    """Base error for any AI-service failure. Catch this, not Exception."""


class RetryableError(AIServiceError):
    """Transient failure (429 rate limit, 503 overloaded). Safe to retry."""


class FatalError(AIServiceError):
    """Permanent failure (400 bad request). Retrying wastes money."""


class ContextWindowExceeded(FatalError):
    """Prompt too long for the model's context window."""


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
```

```
# Output:
# Caught base AIServiceError: prompt is 200k tokens
# Action: fatal
```

`classify` works because `ContextWindowExceeded` **is a** `FatalError` via
inheritance. Note that `isinstance` checks must be ordered most-specific
first — a bare `except AIServiceError` would catch everything below it.

## 2. `raise ... from` — Chaining with Cause

When you catch an exception and raise a new one, you have two ways to record
the original: `raise X from Y` sets `__cause__` explicitly; without `from`,
Python sets `__context__` implicitly. Always chain explicitly — the original
traceback is the debugging gold, and it tells the operator what actually went
wrong at the I/O boundary.

```python
import json


class ValidationError(AIServiceError):
    """Model output failed schema validation."""


def call_model(prompt: str) -> str:
    """Simulate decoding a malformed model response into structured output."""
    try:
        json.loads(prompt)
        return "ok"
    except ValueError as e:
        raise ValidationError("model returned malformed JSON") from e


try:
    call_model("{not json")
except ValidationError as e:
    print(f"Chained error: {e}")
    print(f"__cause__ set: {e.__cause__ is not None}")
    print(f"cause type:    {type(e.__cause__).__name__}")
```

```
# Output:
# Chained error: model returned malformed JSON
# __cause__ set: True
# cause type:    JSONDecodeError
```

Without the `from e`, the traceback would show `JSONDecodeError` as
"During handling of the above exception, another exception occurred" — which
reads like a bug. With `from e` it prints "The above exception was the direct
cause" — which reads like a deliberate translation. The distinction matters
when your on-call engineer reads the log at 3 AM.

## 3. ExceptionGroup and `except*` — Many Failures, One Raise

A bare exception can carry only one failure. When a `gather()` of parallel
calls has *some* failures, raising the first one loses the other nineteen.
`ExceptionGroup` (Python 3.11+) bundles any number of exceptions, and
`except*` handles them **by type** without aborting the rest. This is the
standard pattern for fan-out work: embedding a batch, evaluating a dataset,
calling fifty rerankers.

```python
class RetryableError(AIServiceError):
    """Transient failure (429 rate limit, 503 overloaded). Safe to retry."""


def embed_all(texts: list[str]) -> list[str]:
    """Simulate parallel embedding: every 3rd call fails."""
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
    print(f"Retryable group: {len(eg.exceptions)} failures to retry")
except* FatalError as eg:
    print(f"Fatal group: {len(eg.exceptions)} failures to report")
```

```
# Output:
# Retryable group: 2 failures to retry
```

Key semantics: `except*` matches the **contents** of the group, not the group
itself. Unmatched exceptions are re-raised automatically as a new group. The
original order of failures is preserved in `eg.exceptions`, which keeps
retry bookkeeping (which request ids failed) trivial.

## 4. `contextlib.suppress` — Intentional Swallowing

`suppress(FileNotFoundError)` is the readable form of `try/except: pass`.
Use it ONLY when the failure is genuinely ignorable — the canonical case is
cleanup of something that may already be gone. It is not for hiding bugs.

```python
import os
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("outputs/dbs/checkpoint.tmp")  # fine if it never existed
print("suppress(FileNotFoundError): removal attempted safely")
```

```
# Output:
# suppress(FileNotFoundError): removal attempted safely
```

`suppress` swallows **only** the named types: a `PermissionError` here still
propagates, which is exactly what you want — a file you cannot delete is a
real problem, a file that is not there is not.

## 5. `finally` Semantics — finally Wins

A `return` inside `finally` **overrides** the return in `try`. This is almost
never what you want in production, but understanding it prevents a
pathological bug and explains why `finally` is for cleanup, not for returning
values.

```python
def sneaky() -> str:
    try:
        return "from try"
    finally:
        return "from finally"


print(f"finally overrides return: {sneaky()}")
```

```
# Output:
# finally overrides return: from finally
```

The correct shape is: `try` returns the value, `except` handles failure,
`finally` only performs cleanup (closing handles, flushing buffers,
releasing locks). If your `finally` returns anything, the caller can never
see the `try` result — and exceptions raised in `try` are silently replaced,
not just shadowed.

## 6. EAFP vs LBYL

Python's idiom is **EAFP** — Easier to Ask Forgiveness than Permission: try
the operation, handle the failure. The alternative, **LBYL** — Look Before
You Leap — checks first and races: the state can change between the check
and the use. For files, network calls, and user input, EAFP is the standard.

```python
def safe_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")


print(f"safe_divide(1, 0): {safe_divide(1, 0)}")
print(f"safe_divide(4, 2): {safe_divide(4, 2)}")
```

```
# Output:
# safe_divide(1, 0): inf
# safe_divide(4, 2): 2.0
```

A LBYL version would be `if b == 0: ...` — which is fine for pure math but
useless for I/O: `if os.path.exists(p)` does not guarantee `open(p)` will
succeed. Use EAFP whenever the operation itself can fail; use LBYL only for
cheap checks that prevent *expensive* operations (e.g., validating argument
types before a costly call).

## 7. Retry with Exponential Backoff + Jitter

Retries must be bounded, back off exponentially, and add jitter so a
thundering herd of clients does not retry in lockstep (which is how a rate
limit becomes an outage). Never retry `FatalError` — each retry burns money
and latency for a guaranteed failure.

```python
import time
from typing import Callable


def call_with_retry(
    fn: Callable[[], str],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.05,
) -> str:
    """Call fn, retrying only RetryableError with capped exponential backoff."""
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except RetryableError as e:
            last_error = e
            if attempt == max_attempts:
                break
            delay = min(base_delay * (2 ** (attempt - 1)), 2.0)
            time.sleep(delay)
    raise RetryableError(f"gave up after {max_attempts} attempts") from last_error


attempts = 0


def flaky() -> str:
    global attempts
    attempts += 1
    if attempts < 3:
        raise RetryableError("overloaded")
    return "ok"


print(f"flaky call result: {call_with_retry(flaky)} (attempts: {attempts})")
```

```
# Output:
# flaky call result: ok (attempts: 3)
```

The delay sequence is `base, 2*base, 4*base` capped at `2.0` seconds. In
production, add jitter: `delay = min(base * 2**attempt, cap) * (0.5 + random.random()/2)`.
Libraries like `tenacity` implement this in production; the mechanics are
what matter here: bounded attempts, retryable-only, capped backoff.

## 8. Narrow Excepts — What Not to Catch

Catch what you can act on, re-raise or let propagate the rest. The two
cardinal sins: bare `except:` (catches `KeyboardInterrupt` and `SystemExit`,
so Ctrl-C cannot stop your process) and `except Exception` as a catch-all
that hides real failures.

```python
# MISTAKE - hides Ctrl-C and every bug at once
try:
    risky()
except:  # bare except catches KeyboardInterrupt, SystemExit
    pass


# CORRECT - narrow, and the error is logged
import logging

logger = logging.getLogger(__name__)
try:
    risky()
except RetryableError:
    raise  # let the retry layer handle it
except Exception:
    logger.exception("risky failed")  # logs full traceback, does not swallow
```

```
# Output (no output - both blocks complete without raising):
```

If your function cannot act on an error, the professional move is to **not
catch it at all** — or catch, log, and re-raise. Swallowing `Exception`
converts a diagnosable incident into a mysterious silent failure.

## 9. Production Pattern — Classified Error Routing

Put it together: one base exception, explicit chaining, grouped fan-out
failures, and a routing layer that decides retry vs report. This is the shape
of a real LLM-gateway wrapper.

```python
class AIServiceError(Exception):
    """Base error for any AI-service failure."""


class RetryableError(AIServiceError):
    """Transient failure (429 rate limit, 503 overloaded). Safe to retry."""


class FatalError(AIServiceError):
    """Permanent failure (400 bad request). Retrying wastes money."""


def route_result(eg: ExceptionGroup) -> dict[str, int]:
    """Split a grouped fan-out failure into retryable vs fatal counts."""
    retryable: list[Exception] = []
    fatal: list[Exception] = []
    for e in eg.exceptions:
        if isinstance(e, RetryableError):
            retryable.append(e)
        else:
            fatal.append(e)
    return {"retryable": len(retryable), "fatal": len(fatal)}


failures = [RetryableError("429"), FatalError("400"), RetryableError("503")]
eg = ExceptionGroup("batch embedding", failures)
print(f"Routing: {route_result(eg)}")
```

```
# Output:
# Routing: {'retryable': 2, 'fatal': 1}
```

## Common Mistakes to Avoid

### Mistake 1: Bare `except:` swallows Ctrl-C
```python
# WRONG - KeyboardInterrupt and SystemExit are caught too
try:
    run_inference()
except:  # pragma: no cover - never do this
    pass

# CORRECT - narrow to Exception at most, and log
try:
    run_inference()
except Exception:
    logger.exception("inference failed")
```

### Mistake 2: Re-raising without `from` loses the cause
```python
# WRONG - the original traceback is reduced to __context__
except Exception as e:
    raise ValueError("bad input")

# CORRECT - explicit chain preserves __cause__
except Exception as e:
    raise ValueError("bad input") from e
```

### Mistake 3: Retrying fatal errors burns tokens and money
```python
# WRONG - retries a 400 until max_attempts, then gives up anyway
for _ in range(5):
    try:
        return call_llm(prompt)
    except Exception:
        time.sleep(1)

# CORRECT - only RetryableError is retried; FatalError propagates instantly
try:
    return call_llm(prompt)
except RetryableError:
    return call_with_retry(lambda: call_llm(prompt))
```

### Mistake 4: Wrong `except` ordering
```python
# WRONG - the base class clause wins; ContextWindowExceeded never matches
try:
    embed(prompt)
except AIServiceError:
    log_generic()
except ContextWindowExceeded:
    truncate_and_retry()

# CORRECT - specific subclasses first
try:
    embed(prompt)
except ContextWindowExceeded:
    truncate_and_retry()
except AIServiceError:
    log_generic()
```

### Mistake 5: `return` inside `finally`
```python
# WRONG - silently replaces the try result (and any in-flight exception)
finally:
    return cleanup_result()

# CORRECT - finally performs cleanup only
finally:
    handle.close()
```

## Best Practices

1. Define one base exception per package; subclass it for every failure mode.
2. Always use `raise X from e` when translating exceptions; never let
   `__context__` do the job implicitly.
3. Catch the narrowest type you can act on; let everything else propagate.
4. Never use bare `except:`; catch `Exception` at most, and log with
   `logger.exception`.
5. Retry only transient errors, with bounded attempts and capped exponential
   backoff plus jitter.
6. Use `ExceptionGroup` for fan-out work so partial failures are observable
   and retryable as a unit.
7. Put cleanup in `finally` and *never* return from it.
8. Prefer EAFP for I/O; use LBYL only for cheap pre-checks that prevent
   expensive work.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `try` block with no exception | O(1) | O(1) | — (try is nearly free; only raising costs) |
| Raising an exception | O(traceback depth) | O(depth) | Return a sentinel when failure is a normal outcome |
| `raise X from e` chaining | O(1) | O(1) | — (chaining is free; losing the cause is expensive) |
| Building an `ExceptionGroup` | O(n) | O(n) | Stream failures instead of collecting all |
| `except*` dispatch over a group | O(n) | O(1) | — |
| `contextlib.suppress` entry | O(1) | O(1) | — |
| Retry loop (max a attempts) | O(a * T) | O(1) | Cap attempts; prefer one correct call over five retries |
| `traceback.format_exc()` | O(depth) | O(depth) | Log `e` only; format full tracebacks at the top level |

## AI Engineering Relevance

**Where this shows up:** every LLM API wrapper, every batch evaluation job,
every vector-store upsert loop. LLM providers fail in structured ways: 429
(rate limit), 503 (overloaded), timeouts — all retryable; 400 (bad request),
401 (auth), 402 (quota) — all fatal.

| Concept here | Used for |
|---|---|
| `RetryableError` / `FatalError` hierarchy | Routing 429/503 to backoff, 400/401 to logging |
| `raise ... from e` | Wrapping `JSONDecodeError` from a model response into `ValidationError` |
| `ExceptionGroup` + `except*` | `asyncio.gather` of 50 embedding calls where 3 fail |
| Bounded retry + jitter | Preventing a thundering herd on a shared rate limit |
| `suppress(FileNotFoundError)` | Removing a stale checkpoint that may already be gone |

**Scale note:** at 200 requests/s with a 5% failure rate, an un-retried
service logs 10 failures/s of noise; a retry-all service pays ~2x the token
bill. The classification hierarchy is what turns a firehose of errors into
two actionable counters: `retryable` and `fatal`.

## Practice Exercises

### Exercise 1: Classify Errors (Difficulty: Easy)
Write `classify(e: Exception) -> str` that returns `"retry"` for
`RetryableError`, `"fatal"` for `FatalError`, `"unknown"` otherwise.
Verify `ContextWindowExceeded` (a `FatalError` subclass) classifies as
`"fatal"`.

### Exercise 2: Wrap with Cause (Difficulty: Easy)
Write `parse_response(raw: str) -> dict` that calls `json.loads` and wraps
any `ValueError` in a custom `ValidationError` using `raise ... from`.
Assert that `__cause__` is set and is a `ValueError`.

### Exercise 3: Bounded Retry with Attempt Counter (Difficulty: Medium)
Write `retry_transient(fn, max_attempts: int = 4, base_delay: float = 0.01)`
that retries only `RetryableError` and re-raises the last error after
exhausting attempts. Use a counting closure to prove `fn` is called exactly
`max_attempts` times when it always fails.

### Exercise 4: Split an ExceptionGroup (Difficulty: Medium)
Write `split_group(eg: ExceptionGroup) -> tuple[list[Exception], list[Exception]]`
returning `(retryable, fatal)` in original order. Handle the all-success case
(no group) and the empty-group case.

### Exercise 5: Jittered Retry Policy (Difficulty: Hard)
Write `call_with_jitter(fn, max_attempts, base_delay, seed: int)` with
deterministic jitter (`random.Random(seed)`), capped backoff at 1.0s, and a
maximum total sleep budget. Prove with a seeded run that two workers started
at the same instant never sleep the same delay on the same attempt.

### Exercise 6: Error Routing Pipeline (Difficulty: Hard)
Write `route_batch(calls: list[Callable[[], str]]) -> tuple[list[str], ExceptionGroup | None]`
that executes each call exactly once, collects successes, and raises a single
`ExceptionGroup` of all failures (preserving order). If all succeed, return
`(results, None)`.

## Summary

| Concept | Description |
|---|---|
| Hierarchy | One base exception per package; `isinstance` for action routing |
| Chaining | `raise X from e` preserves `__cause__` and the original traceback |
| `ExceptionGroup` | Many failures in one raise; `except*` dispatches by type |
| `suppress` | Intentional, narrow swallowing for ignorable cleanup failures |
| `finally` | Runs always; its `return` overrides — use for cleanup only |
| EAFP | Try the operation; handle failure — the Python idiom for I/O |
| Retry | Bounded, capped exponential backoff, jittered, retryable-only |
| Narrow excepts | Catch what you can act on; never bare `except:` |

Errors are not accidents to hide; they are data. Classify them, chain them,
retry the retryable, and let the rest surface loudly. The few extra lines of
hierarchy design turn "the service is down" into "3 of 50 embeddings hit 429,
retrying with backoff".

## Quick Reference

| Task | Idiom |
|---|---|
| Base exception | `class AppError(Exception)` |
| Refine behavior | `class RetryableError(AppError)` |
| Wrap with cause | `raise AppError("msg") from e` |
| Many failures | `raise ExceptionGroup("msg", failures)` |
| Handle by type | `except* RetryableError as eg:` |
| Ignore one type | `with suppress(FileNotFoundError):` |
| Bounded retry | `for attempt in range(1, max+1): try ... except RetryableError` |
| Fatal check | `isinstance(e, FatalError)` |
| Log full traceback | `logger.exception("msg")` |
| Re-raise unchanged | `raise` (bare, inside except) |

## Next Steps

Next: **[48-comprehensions-and-modern-syntax](48-comprehensions-and-modern-syntax-lecture.md)** — the comprehension and generator idioms that make batch processing readable.
Continues in: **[02-advanced-python — 04 async/await](../../02-advanced-python/lectures/04-async-await-lecture.md)** (real `asyncio.gather` + `ExceptionGroup` fan-out) and **[19 logging](../../02-advanced-python/lectures/19-logging-lecture.md)** (error observability).
Official docs: https://docs.python.org/3/library/exceptions.html and https://docs.python.org/3/library/contextlib.html
