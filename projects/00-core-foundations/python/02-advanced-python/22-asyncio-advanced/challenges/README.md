# Challenge 22: Asyncio Advanced

Orchestrate batches the way production AI services do: prove a semaphore
cap, build a bounded pipeline with backpressure, and make failure
semantics deterministic.

## 🥉 Bronze — Semaphore Cap Is Real (~15 min)

**Task:** Implement `run_limited(n_calls, limit)`: run `n_calls`
simulated API calls (each `await asyncio.sleep(0.01)`) under an
`asyncio.Semaphore(limit)`, tracking the maximum number of coroutines
ever in-flight. Return `(completed, max_in_flight)`.

**Signature:**
```python
def run_limited(n_calls: int, limit: int) -> tuple[int, int]:
```

| Input | Expected |
|---|---|
| `(8, 3)` | `(8, 3)` |
| `(20, 5)` | `(20, 5)` |
| `(5, 10)` | `(5, 5)` |

**Constraints:** `max_in_flight` must never exceed `limit` — and must
*reach* it when `n_calls >= limit`. Fire all tasks with
`asyncio.gather`; the semaphore does the capping.

---

## 🥈 Silver — Bounded Pipeline (~35 min)

**Task:** Implement `pipeline(items, maxsize)`:

- a producer coroutine `put`s every item into an
  `asyncio.Queue(maxsize=maxsize)`, tracking the largest queue size
  ever observed;
- a consumer coroutine `get`s items, sleeps `0.005` s each, and counts
  them;
- return `(processed, max_observed)`.

**Signature:**
```python
def pipeline(items: list[str], maxsize: int) -> tuple[int, int]:
```

| Input | Expected |
|---|---|
| `(["a"] * 20, 2)` | `(20, 2)` |
| `(["a"] * 10, 5)` | `(10, 5)` |

**Constraints:** `max_observed` must be `<= maxsize` *and* the pipeline
must actually fill to the bound when `maxsize` is small. Naive
solution — appending to an unbounded list instead of a queue — observes
sizes above the bound and fails. Run with
`asyncio.run(pipeline(...))` inside the function or document the
wrapper you use.

---

## 🥇 Gold — Deterministic Failure Semantics (~75 min)

**Task:** Implement `run_batch(n, fail_at)` with an
`asyncio.TaskGroup`: create `n` tasks with **staggered delays** so
failure semantics are deterministic:

- tasks with `i < fail_at` sleep `0.005` s, then succeed (they finish
  *before* the failure);
- task `fail_at` sleeps `0.02` s, then raises `ValueError`;
- tasks with `i > fail_at` sleep `5` s (still pending when the group
  cancels them).

Return `(completed, cancelled)` where `completed` counts tasks that ran
to completion and `cancelled` counts tasks the group cancelled after
the failure.

**Signature:**
```python
def run_batch(n: int, fail_at: int) -> tuple[int, int]:
```

| Input | Expected |
|---|---|
| `(5, 2)` | `(2, 2)` — tasks 0,1 done; 3,4 cancelled; 2 failed |
| `(7, 4)` | `(4, 2)` |
| `(3, 0)` | `(0, 2)` |
| `(4, 3)` | `(3, 0)` |

**Constraints:** cancellation is deterministic with the staggered
delays: tasks before `fail_at` complete, tasks after it are still
pending and get cancelled by the group, task `fail_at` itself fails. A
`gather`-based solution returns `cancelled == 0` and fails. Count
cancellation in each task's `except asyncio.CancelledError` handler.

---

## Running

```bash
pytest challenges/22-asyncio-advanced/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/22-asyncio-advanced/test_challenge.py -v
```

## Test File Structure

```
challenges/22-asyncio-advanced/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
