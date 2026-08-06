# Challenge 21: Concurrency Comparison

Pick the right concurrency model, prove I/O overlap with a measurement,
and make CPU work actually parallel on Windows.

## 🥉 Bronze — Choose the Model (~15 min)

**Task:** Implement `choose_model(workload, calls)`, the decision table
from lecture 21: I/O-bound work with many calls → `"async"`; I/O-bound
with few calls → `"threads"`; CPU-bound → `"processes"` (the GIL makes
threads useless there).

**Signature:**
```python
def choose_model(workload: str, calls: int) -> str:
```

| Input | Expected |
|---|---|
| `("io", 10)` | `"threads"` |
| `("io", 10_000)` | `"async"` |
| `("cpu", 1)` | `"processes"` |
| `("cpu", 1_000_000)` | `"processes"` |
| `("gpu", 5)` | `ValueError` |

**Constraints:** any correct approach passes — this tier is about the
decision table, not timing.

---

## 🥈 Silver — Prove I/O Overlap (~35 min)

**Task:** Implement `run_io_overlap(sleeps, delay)`: run `sleeps`
simulated I/O waits of `delay` seconds using a `ThreadPoolExecutor`
(max_workers=8) and return the **total elapsed time**. Sequential
execution takes `sleeps * delay`; overlapping execution must take far
less.

**Signature:**
```python
def run_io_overlap(sleeps: int, delay: float) -> float:
```

| Input | Expected |
|---|---|
| `(8, 0.05)` | `< 0.24` (sequential would be 0.40) |
| `(16, 0.05)` | `< 0.48` (sequential would be 0.80) |

**Constraints:** the test asserts `elapsed < sleeps * delay * 0.6` — a
sequential loop (the naive solution) returns `sleeps * delay` and
fails. Use `time.perf_counter`; the sleep is the point, so the result
is timing-robust.

---

## 🥇 Gold — CPU Work in Parallel (~75 min)

**Task:** Implement two functions plus a top-level worker:

1. `run_cpu_parallel(chunks, work)` — split `work` into `chunks` equal
   units and compute them across a `ProcessPoolExecutor` (one unit per
   worker); return the **elapsed time**.
2. `run_cpu_sequential(chunks, work)` — the same total work in a
   plain loop; return the elapsed time.
3. `_cpu_worker(n)` — at **module top level** (Windows `spawn`
   requires importable workers): returns `sum(i * i for i in range(n))`.

**Signatures:**
```python
def run_cpu_parallel(chunks: int, work: int) -> float
def run_cpu_sequential(chunks: int, work: int) -> float
def _cpu_worker(n: int) -> int
```

| Input | Expected |
|---|---|
| `_cpu_worker(5)` | `30` |
| `run_cpu_parallel(4, 10_000_000)` | `< run_cpu_sequential(4, 10_000_000) * 0.85` |

**Constraints:** the perf test asserts the parallel run beats the
sequential run — threads would fail it (the GIL serializes bytecode).
The test also inspects `_cpu_worker.__qualname__`: a nested/lambda
worker contains `"<locals>"` and would break under Windows spawn, so it
must be defined at module level.

---

## Running

```bash
pytest challenges/21-concurrency-comparison/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/21-concurrency-comparison/test_challenge.py -v
```

## Test File Structure

```
challenges/21-concurrency-comparison/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
