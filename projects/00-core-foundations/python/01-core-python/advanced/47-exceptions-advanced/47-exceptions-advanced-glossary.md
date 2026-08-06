# 47: Advanced Exceptions — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `BaseException` | Builtin | Root of the exception hierarchy; never catch this |
| bare `except:` | Anti-pattern | Catches `KeyboardInterrupt` and `SystemExit` — never use |
| `__cause__` | Attribute | The original exception, set explicitly by `raise X from Y` |
| `__context__` | Attribute | The exception in flight when another is raised, set implicitly |
| `contextlib.suppress` | Context manager | Swallows only the named exception types |
| EAFP | Idiom | Try the operation, handle the failure (Python's default) |
| `except*` | Statement | Matches exception types inside an `ExceptionGroup` (3.11+) |
| `ExceptionGroup` | Class | One raise carrying many exceptions (3.11+) |
| Exception hierarchy | Design | One base exception per package, refined by subclasses |
| `finally` | Clause | Runs always; its `return` overrides the `try` result |
| `raise ... from` | Statement | Explicitly chains a new exception to its cause |
| Retryable error | Category | Transient failure (429/503/timeout) — safe to retry |
| Fatal error | Category | Permanent failure (400/401) — retrying wastes money |
| `logger.exception` | Method | Logs a message plus the current traceback |
| Jitter | Pattern | Randomizes backoff delays to break thundering herds |
| Narrow except | Practice | Catch only what the call site can act on |
| Exponential backoff | Pattern | Delays grow 2x per attempt, capped at a maximum |
| `sys.exc_info()` | Function | Returns the (type, value, traceback) of the active exception |
| LBYL | Idiom | Look Before You Leap — check first; races on I/O |
| `raise` (bare) | Statement | Re-raises the current exception unchanged |

## Detailed Definitions

### `__cause__`
**Definition**: The exception set by an explicit `raise X from Y` chain. It
tells the reader (and the traceback printer) that `Y` caused `X`, so the
original failure is preserved as first-class data.

**Example**:
```python
try:
    json.loads("{bad")
except ValueError as e:
    raise ValueError("cannot parse") from e
# Traceback shows: "The above exception was the direct cause..."
```

**Complexity**: O(1) to attach; traceback printing costs O(depth).

**Related**: `__context__`, `raise ... from`

### `__context__`
**Definition**: The exception that was being handled when another exception
was raised *without* an explicit `from`. It is set implicitly and is a
fallback — explicit `from` is always clearer.

**Example**:
```python
try:
    1 / 0
except ZeroDivisionError:
    raise ValueError("math failed")  # __context__ = ZeroDivisionError
```

**Complexity**: O(1).

**Related**: `__cause__`, `raise ... from`

### `BaseException`
**Definition**: The root of all exception classes. `KeyboardInterrupt` and
`SystemExit` inherit from it directly, not from `Exception` — which is why
`except Exception` cannot stop Ctrl-C but bare `except:` can.

**Example**:
```python
print(issubclass(KeyboardInterrupt, BaseException))  # True
print(issubclass(KeyboardInterrupt, Exception))      # False
```

**Complexity**: O(1).

**Related**: `Exception`, bare `except:`

### bare `except:`
**Definition**: An `except` with no type that catches *everything*, including
`KeyboardInterrupt` and `SystemExit`. It hides Ctrl-C and every bug at once;
it is the anti-pattern every code review rejects.

**Example**:
```python
# WRONG
try:
    run()
except:  # noqa: E722 - never do this
    pass
```

**Complexity**: O(1) to enter; unbounded cost to your debugging.

**Related**: `BaseException`, `Exception`

### EAFP
**Definition**: Easier to Ask Forgiveness than Permission — Python's default
error-handling idiom. Attempt the operation and handle the exception, rather
than checking preconditions that can change between check and use.

**Example**:
```python
def read_config(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""
```

**Complexity**: O(1) overhead when no exception occurs.

**Related**: LBYL, narrow except

### `ExceptionGroup`
**Definition**: A single exception that carries a list of exceptions
(Python 3.11+). The standard way to report *partial* failure from fan-out
work, so no failure is lost and successes can be returned alongside.

**Example**:
```python
failures = [ValueError("a"), TypeError("b")]
eg = ExceptionGroup("2 of 50 failed", failures)
print(len(eg.exceptions))  # 2
```

**Complexity**: O(n) to build, O(n) space.

**Related**: `except*`, `asyncio.gather`

### `except*`
**Definition**: The statement that handles exceptions *inside* an
`ExceptionGroup` by type. Only matching exceptions are consumed; unmatched
ones are re-raised as a new group.

**Example**:
```python
try:
    raise ExceptionGroup("g", [ValueError("v"), TypeError("t")])
except* ValueError as eg:
    print(len(eg.exceptions))  # 1
```

**Complexity**: O(n) dispatch over the group contents.

**Related**: `ExceptionGroup`, `try/except`

### exception hierarchy
**Definition**: The design pattern of one base exception per package with
subclasses for each failure mode. Callers catch the base and use
`isinstance` to decide the action — retry, report, or ignore.

**Example**:
```python
class ApiError(Exception): ...
class RateLimited(ApiError): ...
class AuthFailed(ApiError): ...

try:
    raise RateLimited()
except RateLimited:
    print("retry")
except ApiError:
    print("report")
```

**Complexity**: O(1) per `isinstance` check.

**Related**: narrow except, retryable error

### exponential backoff
**Definition**: A retry policy where the delay grows by a constant factor
(usually 2) per attempt, capped at a maximum, so a service under stress gets
progressively more time to recover.

**Example**:
```python
delays = [min(0.05 * 2 ** i, 2.0) for i in range(5)]
print(delays)  # [0.05, 0.1, 0.2, 0.4, 0.8]
```

**Complexity**: O(1) per attempt; total sleep is bounded by the cap.

**Related**: jitter, retryable error

### fatal error
**Definition**: A permanent failure — 400 bad request, 401 auth, 402 quota.
Retrying cannot succeed and only burns money and latency. Fatal errors must
propagate to the caller immediately.

**Example**:
```python
class FatalError(Exception): ...

try:
    raise FatalError("400")
except FatalError:
    print("do not retry")  # logs and reports
```

**Complexity**: O(1).

**Related**: retryable error, exception hierarchy

### `finally`
**Definition**: The clause that runs whether or not an exception occurred.
It is for cleanup only: a `return` inside `finally` overrides the `try`
result and replaces any in-flight exception.

**Example**:
```python
def f() -> str:
    try:
        return "try"
    finally:
        return "finally"

print(f())  # finally
```

**Complexity**: O(1).

**Related**: `try/except`, return override

### jitter
**Definition**: Randomization of backoff delays so that many clients
retrying at the same instant do not stay synchronized. Without jitter, a
rate limit becomes a thundering-herd outage.

**Example**:
```python
import random
rng = random.Random(42)
delays = [0.05 * (1 + rng.random()) for _ in range(3)]
print([round(d, 3) for d in delays])  # [0.062, 0.089, 0.089]
```

**Complexity**: O(1) per attempt.

**Related**: exponential backoff, retryable error

### LBYL
**Definition**: Look Before You Leap — checking preconditions before acting.
It races on I/O (a file can vanish between `exists()` and `open()`), so EAFP
is preferred for operations that can fail; LBYL is useful for cheap checks
that prevent expensive work.

**Example**:
```python
# LBYL - fine for pure validation
if not isinstance(x, int):
    raise TypeError("x must be int")
```

**Complexity**: O(1) per check.

**Related**: EAFP

### `logger.exception`
**Definition**: The logging method that records a message plus the current
exception's full traceback, without raising. Use it in the `except` block to
preserve observability while continuing.

**Example**:
```python
import logging
logging.basicConfig(level=logging.ERROR)

try:
    1 / 0
except ZeroDivisionError:
    logging.exception("division failed")  # traceback attached
```

**Complexity**: O(traceback depth) to format.

**Related**: narrow except, `sys.exc_info()`

### narrow except
**Definition**: The practice of catching only the exception types the call
site can meaningfully act on, and letting everything else propagate. The
corollary: never catch `Exception` (or worse, bare `except:`) in library
code.

**Example**:
```python
try:
    return int(raw)
except ValueError:
    return None  # only this failure is handled
```

**Complexity**: O(1).

**Related**: exception hierarchy, bare `except:`

### `raise ... from`
**Definition**: The syntax that raises a new exception while explicitly
linking it to the original via `__cause__`. The traceback prints "The above
exception was the direct cause of the following exception".

**Example**:
```python
try:
    int("x")
except ValueError as e:
    raise RuntimeError("bad input") from e
```

**Complexity**: O(1).

**Related**: `__cause__`, `__context__`

### retryable error
**Definition**: A transient failure — 429 rate limit, 503 overload, timeout
— that can succeed on a later attempt. Retrying is correct, but must be
bounded, backed off, and jittered.

**Example**:
```python
class RetryableError(Exception): ...

for attempt in range(3):
    try:
        result = call()
        break
    except RetryableError:
        if attempt == 2:
            raise
```

**Complexity**: O(attempts * call cost).

**Related**: fatal error, exponential backoff, jitter

### `suppress`
**Definition**: `contextlib.suppress(*exceptions)` — a context manager that
swallows only the named exception types. The readable replacement for
`try/except: pass`, for failures that are genuinely ignorable.

**Example**:
```python
from contextlib import suppress
import os

with suppress(FileNotFoundError):
    os.remove("gone.tmp")  # no error if it never existed
print("safe")
```

**Complexity**: O(1) entry/exit.

**Related**: narrow except, EAFP

### `sys.exc_info()`
**Definition**: Returns the `(type, value, traceback)` triple of the
exception currently being handled, or `(None, None, None)` outside an
`except` block. Useful when you must re-raise or inspect a traceback
programmatically.

**Example**:
```python
import sys

try:
    raise ValueError("x")
except ValueError:
    etype, evalue, etb = sys.exc_info()
    print(etype.__name__, evalue)  # ValueError x
```

**Complexity**: O(1).

**Related**: `logger.exception`, traceback

## Key Concepts Summary

### The Classification Ladder
- **BaseException** — never catch directly (includes `KeyboardInterrupt`, `SystemExit`).
- **Exception** — the widest sane catch, and only in top-level handlers.
- **Package base** (e.g. `AIServiceError`) — the documented public contract.
- **Leaf types** (`RetryableError`, `FatalError`, `ValidationError`) — the
  action signals the call site routes on.

### The Retry Rule
- Retry **only** retryable errors: bounded attempts, exponential backoff,
  capped delay, jitter.
- Never retry fatal errors: a 400 is still a 400 on attempt five, and you
  have paid for it five times.

### Fan-Out Rule
- One failure from a batch should not discard the other 49.
- Raise an `ExceptionGroup` with every failure; handle with `except*`;
  unmatched types re-raise automatically.

### Cleanup Rule
- `finally` is for cleanup, never for `return`.
- `with` blocks (context managers) replace most `try/finally` code.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `__cause__` — ___
2. `ExceptionGroup` — ___
3. `except*` — ___
4. `suppress` — ___
5. EAFP — ___
6. bare `except:` — ___
7. jitter — ___
8. fatal error — ___
9. `raise ... from` — ___
10. narrow except — ___

A. Swallows only the named exception types
B. Catches everything, including Ctrl-C — never use
C. The explicit chain to the original exception
D. One raise carrying many exceptions (3.11+)
E. Retrying this cannot succeed; propagate immediately
F. Randomizes backoff so retries do not synchronize
G. Try the operation, then handle the failure
H. Dispatch by type over a group's contents
I. Catch only what the call site can act on
J. Raises a new exception linked to its cause

**Answers:** 1-C, 2-D, 3-H, 4-A, 5-G, 6-B, 7-F, 8-E, 9-J, 10-I
