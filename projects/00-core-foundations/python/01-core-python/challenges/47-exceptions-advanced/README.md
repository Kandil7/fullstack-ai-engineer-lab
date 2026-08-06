# Challenge 47: Advanced Exceptions

Classify, chain, retry, and group the failures that every LLM-backed service
sees. The exception hierarchy below is provided for all three tiers — you
implement the handling logic.

## 🥉 Bronze — Error Classification (~15 min)

**Task:** Implement `classify_error(e)`, which maps an exception to the
action a caller should take: `"retry"` for `RetryableError`, `"fatal"` for
`FatalError`, and `"unknown"` otherwise. A `FatalError` **subclass** (like
`ContextWindowExceeded`) must classify as `"fatal"` — use `isinstance`, not
type equality.

**Signature:**
```python
def classify_error(e: Exception) -> str:
```

| Input | Expected |
|---|---|
| `RetryableError("429 rate limited")` | `"retry"` |
| `FatalError("400 bad request")` | `"fatal"` |
| `ContextWindowExceeded("prompt too long")` | `"fatal"` |
| `ValueError("other")` | `"unknown"` |

**Constraints:** Any correct approach passes.

---

## 🥈 Silver — Bounded Retry (~35 min)

**Task:** Implement `call_with_retry(fn, *, max_attempts, base_delay)`, which
calls `fn()` and retries **only** `RetryableError` with exponential backoff
capped at `1.0` seconds (`min(base_delay * 2 ** attempt, 1.0)`). A
`FatalError` (or any other exception) must propagate immediately, untouched.
After `max_attempts` consecutive retryable failures, re-raise the **last**
retryable error, chained (`raise ... from`) so its cause is preserved.

**Signature:**
```python
def call_with_retry(
    fn: Callable[[], str],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.01,
) -> str:
```

| Input | Expected |
|---|---|
| `fn` succeeds on 3rd call, `max_attempts=4` | `"ok"`, fn called exactly 3 times |
| `fn` always raises `RetryableError`, `max_attempts=4` | raises `RetryableError`, fn called exactly 4 times |
| `fn` raises `FatalError("400")` | raises `FatalError`, fn called exactly 1 time |

**Constraints:** `max_attempts <= 10^3`, `fn` is O(1). The tests **count
calls to `fn`** — retrying a fatal error (call count > 1) fails the guard,
and giving up early (call count < `max_attempts` on an always-failing fn)
fails too.

---

## 🥇 Gold — Grouped Fan-Out (~75 min)

**Task:** Implement `gather_results(calls)`, which executes each call
**exactly once**, collects the successes in order, and reports every failure
as one `ExceptionGroup` — the pattern for a 50-embedding batch where 3 fail.
Return `(results, group)` where `results` is `list[str]` and `group` is the
`ExceptionGroup` of failures (original order, original exception objects),
or `None` when nothing failed. The group must contain **all** failures —
successes are not failures, and failures are never dropped.

**Signature:**
```python
def gather_results(
    calls: list[Callable[[], str]],
) -> tuple[list[str], ExceptionGroup | None]:
```

| Input | Expected |
|---|---|
| `[]` | `([], None)` |
| all succeed (`["a", "b"]`) | `(["a", "b"], None)` |
| `["a", raise RetryableError, "c"]` | `(["a", "c"], group of 1)` |
| 3 of 50 fail | 47 results, group with exactly 3 exceptions, in original order |

**Constraints:** `n <= 10^6` calls, **single pass** — each call executes
exactly once (the tests count invocations; re-running failures or the whole
list fails the guard). Group construction must be O(n): build the list
by appending, never by `failures = failures + [e]` concatenation.

**Follow-up:** what breaks first at 10^9 calls? (Answer: the group itself
grows to hold every failure — you would aggregate counts per type and
stream summaries instead of retaining all exception objects.)

---

## Running

```bash
pytest challenges/47-exceptions-advanced/test_challenge.py -v
```

## Test File Structure

```
challenges/47-exceptions-advanced/
├── README.md          # This file
├── starter.py         # Signatures + exception hierarchy only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
