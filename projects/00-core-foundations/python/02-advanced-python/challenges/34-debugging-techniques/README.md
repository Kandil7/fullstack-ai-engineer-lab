# Challenge 34: Debugging Techniques

Build the debugging toolkit: full-stack logging, a boundary-asserting
pipeline debugger that finds silent bugs, and a deterministic repro
harness. The final tier is a mini `git bisect` over configs.

## 🥉 Bronze — Full-Stack Logging (~15 min)

**Task:** Implement `capture(fn) -> str` that runs a zero-arg callable
and returns the **full traceback** (via `traceback.format_exc`) if it
raises, or `""` if it succeeds. Also implement
`format_exception_text(exc: BaseException) -> str` using
`traceback.format_exception`.

| Input | Expected |
|-------|----------|
| `capture(lambda: 1/0)` | starts with `"Traceback (most recent call last):"`, contains `"ZeroDivisionError"` |
| `capture(lambda: None)` | `""` |
| `format_exception_text(ValueError("x"))` | contains `"ValueError: x"` |

**Constraints:** n ≤ 10^3 calls. Never let the exception escape.

---

## 🥈 Silver — Boundary-Asserting Pipeline (~35 min)

**Task:** Implement `DebugPipeline` that runs a 3-stage pipeline
(`load` → `process` → `emit`) and **detects silent bugs** by asserting
invariants at each boundary:

```python
class DebugPipeline:
    def run(self, chunks: list[str]) -> list[str]: ...
```

- Stage 1 (`load`): strip; **assert** every chunk non-empty.
- Stage 2 (`process`): dedupe preserving order; **assert** no item is
  lost (count ≤ input count, all outputs are strings).
- Stage 3 (`emit`): sort by length; return.

Raises `AssertionError` with a stage-named message when an invariant
breaks; otherwise returns the final list.

| Input | Expected |
|-------|----------|
| `[" a ", "b", "a"]` | `["a", "b"]` (deduped, stable-sorted by length) |
| `[" ok ", ""]` | `AssertionError` mentioning `stage-1` |
| `["x", None]` | `AssertionError` (stage-1 type invariant) |

**Constraints:** n ≤ 10^3 chunks. Each assertion message must name its
stage. All runs deterministic (no randomness).

---

## 🥇 Gold — Repro Harness + Config Bisect (~75 min)

**Task:** Two pieces:

1. `make_repro(shuffle_seed: int) -> Callable[[list[str]], list[str]]`
   — returns a deterministic shuffler using `random.Random(seed)`.
   Assert that two calls with the same seed produce identical output
   and that different seeds differ.

2. `bisect_bad(configs: list[str], bad_from: int) -> tuple[int, int]`
   — returns `(first_bad_index, probes_used)`, finding the first index
   where behavior goes bad, with `probes_used ≤ ceil(log2(n)) + 1`.

| Input | Expected |
|-------|----------|
| `make_repro(42)(["a","b","c"])` twice | identical lists |
| `make_repro(1)(x) == make_repro(2)(x)` | `False` (different seeds) |
| `bisect_bad([f"c{i}" for i in range(100)], 42)` | `(42, probes ≤ 8)` |
| `bisect_bad(..., 0)` | `(0, probes ≤ 2)` (first is bad) |
| `bisect_bad(..., 99)` | `(99, probes ≤ 8)` (last is bad) |

**Constraints:** no wall-clock timing; probe count is counted
deterministically. n ≤ 10^4 configs.

**Follow-up:** how would you use `make_repro` on a real RAG bug — which
sources of randomness would you freeze first?

---

## Running

```bash
pytest challenges/34-debugging-techniques/test_challenge.py -v
```
