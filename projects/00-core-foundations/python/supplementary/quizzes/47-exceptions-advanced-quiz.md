# Advanced Exceptions Quiz

## Topic Overview
This quiz covers advanced exception handling: custom hierarchies, exception
chaining with `raise ... from`, `ExceptionGroup` and `except*` (Python 3.11+),
`contextlib.suppress`, `finally` semantics, EAFP vs LBYL, and retry policies.
These are the patterns that keep LLM-backed services alive when APIs rate
limit and fail in structured ways.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is the output of this code?**
```python
class ApiError(Exception): ...
class RateLimited(ApiError): ...

try:
    raise RateLimited("429")
except ApiError as e:
    print(f"caught {type(e).__name__}")
```

A) caught RateLimited
B) caught ApiError
C) Error: RateLimited is not caught by ApiError
D) caught Exception

**Difficulty:** Easy

---

### Question 2
**Which exception classes are NOT subclasses of `Exception`?**

A) ValueError and TypeError
B) KeyboardInterrupt and SystemExit
C) RuntimeError and OSError
D) KeyError and IndexError

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
try:
    raise ValueError("inner")
except ValueError as e:
    raise RuntimeError("outer") from e
```

A) RuntimeError with `__cause__` pointing at the ValueError
B) RuntimeError with `__context__` pointing at the ValueError
C) ValueError only, RuntimeError is swallowed
D) Both exceptions printed as separate unhandled errors

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
def f() -> str:
    try:
        return "from try"
    finally:
        return "from finally"

print(f())
```

A) from try
B) from finally
C) None
D) SyntaxError

**Difficulty:** Medium

---

### Question 5
**What is the purpose of `contextlib.suppress(FileNotFoundError)`?**

A) It deletes the file if it exists
B) It swallows only FileNotFoundError inside the block
C) It suppresses all exceptions inside the block
D) It raises FileNotFoundError if the file exists

**Difficulty:** Easy

---

### Question 6
**What is the output of this code?**
```python
from contextlib import suppress

with suppress(ValueError):
    raise TypeError("boom")
print("after")
```

A) after
B) nothing — the program crashes with TypeError
C) after, then TypeError
D) ValueError

**Difficulty:** Medium

---

### Question 7
**What is the output of this code?**
```python
try:
    raise ExceptionGroup("g", [ValueError("a"), TypeError("b")])
except* ValueError as eg:
    print(f"caught {len(eg.exceptions)}")
```

A) caught 1
B) caught 2
C) Error: ExceptionGroup cannot be caught with except*
D) caught 0

**Difficulty:** Medium

---

### Question 8
**Which of these retry policies is correct for an LLM API wrapper?**

A) Retry every exception 5 times with fixed 1s delay
B) Retry only transient errors (429/503/timeout), with bounded exponential
   backoff and jitter; let 400/401 propagate
C) Retry fatal errors too, because the API may recover
D) Never retry anything; any retry is wasted money

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
def safe_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")

print(safe_divide(1, 0))
```

A) 0.0
B) inf
C) Error: division by zero
D) None

**Difficulty:** Easy

---

### Question 10
**Which is the correct EAFP-style way to read a config file that may not exist?**

A) `if os.path.exists(path): return open(path).read()` — then assume success
B) `try: return open(path).read() except FileNotFoundError: return ""`
C) `try: return open(path).read() except: return ""`
D) `open(path).read()` — let it crash

**Difficulty:** Medium

---

### Question 11
**What does bare `except:` catch that `except Exception:` does not?**

A) ValueError and TypeError
B) KeyboardInterrupt and SystemExit
C) Nothing — they are identical
D) Only user-defined exceptions

**Difficulty:** Easy

---

### Question 12
**What is the output of this code?**
```python
class Base(Exception): ...
class Sub(Base): ...

try:
    raise Sub()
except Base:
    print("base")
except Sub:
    print("sub")
```

A) sub
B) base
C) base, then sub
D) sub, then base

**Difficulty:** Easy

---

### Question 13
**A batch of 50 embedding calls fails: 3 return 429 (retryable) and 1 returns
400 (fatal). What is the best way to report this?**

A) Raise the first failure you see; the other three are lost
B) Collect all failures into one `ExceptionGroup` and dispatch with `except*`
C) Raise a plain ValueError summarizing the counts
D) Silently ignore the 4 failures and return the 46 successes

**Difficulty:** Medium

---

### Question 14
**What is the output of this code?**
```python
def chain():
    try:
        int("x")
    except ValueError as e:
        raise TypeError("bad") from e

try:
    chain()
except TypeError as e:
    print(type(e.__cause__).__name__)
```

A) ValueError
B) TypeError
C) None
D) bad

**Difficulty:** Medium

---

### Question 15
**Why should a `finally` block never contain a `return`?**

A) It is a syntax error
B) It overrides the `try` block's return value and replaces any in-flight exception
C) It makes the function return None
D) It only runs when no exception occurred

**Difficulty:** Medium

---

### Question 16
**Which exception hierarchy design is correct for a library?**

A) Raise builtins only; callers cannot subclass them
B) One base exception per package, refined by subclasses for each failure mode
C) A single exception class for every error in the package
D) Reuse `Exception` directly everywhere

**Difficulty:** Medium

---

### Question 17
**What is the output of this code?**
```python
def outer():
    try:
        raise KeyError("k")
    except KeyError:
        raise ValueError("v")

try:
    outer()
except ValueError as e:
    print(e.__context__ is not None, e.__cause__ is not None)
```

A) True False
B) False True
C) True True
D) False False

**Difficulty:** Hard

---

### Question 18
**In a retry loop with exponential backoff and jitter, why is jitter important?**

A) It makes retries faster
B) Without it, all clients retry in lockstep, turning a rate limit into a thundering herd
C) It converts fatal errors into retryable ones
D) It is required for Python's `time.sleep` to work

**Difficulty:** Medium

---

### Question 19
**What is the output of this code?**
```python
try:
    raise ExceptionGroup("g", [ValueError("a"), TypeError("b")])
except* ValueError as eg:
    print(f"v:{len(eg.exceptions)}", end=" ")
except* TypeError as eg:
    print(f"t:{len(eg.exceptions)}", end=" ")
```

A) v:1 t:1
B) v:2
C) t:2
D) Error: cannot have two except* blocks

**Difficulty:** Hard

---

### Question 20
**An always-failing `fn` is passed to `call_with_retry(fn, max_attempts=3)`.
`fn` raises `RetryableError`. How many times is `fn` called, and what does
the final exception look like?**

A) 3 calls; the third RetryableError propagates
B) 1 call; the first RetryableError propagates
C) 3 calls; a new RetryableError raised `from` the last one propagates
D) Infinite calls; the loop never exits

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You understand production error handling.
- 14-17: Good job! Review the questions you missed.
- 10-13: Fair. Revisit chaining and ExceptionGroup.
- Below 10: Keep practicing! Review the advanced exceptions material.

---

## Answer Key

1. **A) caught RateLimited** — Subclass instances are caught by their base
   class handler. The handler binds `e` to the *actual* raised object, so
   `type(e).__name__` is `RateLimited`. Distractors: B confuses the handler
   type with the raised type; C wrongly claims base classes don't catch
   subclasses (they do — that is the point of `except Base`); D is wrong
   because `Exception` is not involved here.

2. **B) KeyboardInterrupt and SystemExit** — They inherit directly from
   `BaseException`, not `Exception`, so `except Exception` never catches them.
   A, C, and D are all ordinary subclasses of `Exception`.

3. **A) RuntimeError with `__cause__` pointing at the ValueError** —
   `raise ... from e` sets `__cause__` explicitly. B describes implicit
   `__context__` (no `from`). C is wrong — the ValueError is not swallowed.
   D is wrong — the chained exception is reported as one RuntimeError whose
   traceback shows the cause.

4. **B) from finally** — A `return` in `finally` overrides the `try` return.
   A is what naive reading expects but `finally` wins. C is wrong — the
   function does return a value. D is wrong — this is valid Python.

5. **B) It swallows only FileNotFoundError inside the block** — `suppress`
   takes an explicit type list and swallows only those. A describes `os.remove`.
   C is wrong — other exceptions propagate. D is backwards — `suppress` never
   raises.

6. **B) nothing — the program crashes with TypeError** — `suppress(ValueError)`
   swallows *only* `ValueError`; the raised `TypeError` is not named, so it
   propagates and "after" never prints. A assumes suppress is a catch-all.
   C is wrong — the crash happens before any later print. D is wrong —
   `suppress` never raises the named type; it swallows it.

7. **A) caught 1** — `except*` matches exceptions *inside* the group by
   type. Only the ValueError matches this handler; the TypeError is
   re-raised as a new group. B counts the whole group; C is wrong — `except*`
   exists for exactly this (3.11+); D is wrong — at least the ValueError is
   matched.

8. **B) Retry only transient errors (429/503/timeout), with bounded
   exponential backoff and jitter; let 400/401 propagate** — this is the
   classification pattern. A retries fatal errors and burns money; C is the
   same mistake stated differently; D throws away the ability to survive
   transient overload.

9. **B) inf** — the handler returns `float("inf")`. A invents a default
   return; C forgets the handler; D confuses this with an implicit return.

10. **B) `try: return open(path).read() except FileNotFoundError: return ""`**
    — EAFP with a narrow except. A is LBYL and races (file can vanish between
    check and open). C uses bare `except:` which also swallows
    KeyboardInterrupt. D is not error handling.

11. **B) KeyboardInterrupt and SystemExit** — bare `except:` catches
    everything, including these. A lists exceptions both catch. C is wrong —
    they differ exactly here. D is backwards.

12. **B) base** — handlers are checked in order; `except Base` matches `Sub`
    first, so `except Sub` never runs. A assumes most-specific matching
    happens automatically; C and D assume multiple handlers run.

13. **B) Collect all failures into one `ExceptionGroup` and dispatch with
    `except*`** — this preserves every failure and lets you retry the 3
    retryable ones while reporting the fatal one. A loses 3 failures; C
    destroys the structured error types; D hides failures entirely.

14. **A) ValueError** — `raise TypeError from e` sets `__cause__` to the
    original ValueError. B is the outer type, not the cause. C is wrong —
    `from` guarantees a cause. D is the message, not a type.

15. **B) It overrides the `try` block's return value and replaces any
    in-flight exception** — the return override trap. A is wrong — it is
    legal. C is wrong — it returns the `finally` value. D is wrong —
    `finally` runs always.

16. **B) One base exception per package, refined by subclasses for each
    failure mode** — the standard library pattern (`OSError` and friends).
    A is wrong — builtins can be subclassed. C loses granularity. D makes
    callers unable to distinguish failure modes.

17. **A) True False** — `raise ValueError("v")` without `from` sets
    `__context__` (the KeyError being handled) and `__cause__` stays None.
    B is the reverse of reality; C would require `from`; D ignores
    `__context__` entirely.

18. **B) Without it, all clients retry in lockstep, turning a rate limit
    into a thundering herd** — jitter desynchronizes retries. A is wrong —
    jitter does not make retries faster. C is wrong — jitter changes timing,
    not error class. D is false.

19. **A) v:1 t:1** — each `except*` handler consumes its matching
    exceptions from the group, so the ValueError is caught by the first and
    the TypeError by the second. B and C count only one type; D is wrong —
    multiple `except*` blocks are the intended design.

20. **C) 3 calls; a new RetryableError raised `from` the last one
    propagates** — bounded retry calls exactly `max_attempts` times, then
    raises a chained final error so the traceback preserves the last cause.
    A loses the chaining contract; B stops too early; D violates the bound.

---

*Quiz completed! How did you score?*
