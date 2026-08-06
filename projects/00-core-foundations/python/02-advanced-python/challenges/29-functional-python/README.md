# Challenge 29: Functional Python

Build a *cacheable pure pipeline* — the pattern that makes ML
preprocessing reproducible: pure transforms, memoized once, replayable
forever.

## 🥉 Bronze — Pure Transform (~15 min)

**Task:** Implement `square_evens(numbers: list[int]) -> list[int]` that
returns a NEW list with the squares of the even inputs, using `map` +
`filter` (not a comprehension). The input list must never be mutated.

**Signature:**
```python
def square_evens(numbers: list[int]) -> list[int]: ...
```

| Input | Expected |
|-------|----------|
| `[1, 2, 3, 4]` | `[4, 16]` |
| `[]` | `[]` |
| `[2, 2]` | `[4, 4]` |
| `[1, 3, 5]` | `[]` |

**Constraints:** n ≤ 10^3. Input must be unmodified (the test checks the
caller's list is unchanged after the call).

---

## 🥈 Silver — Composable, Memoized Pipeline (~35 min)

**Task:** Implement `compose(g, f)` (returns `g(f(x))`) and
`memoize(fn)` — a wrapper that caches results by argument tuple and
returns them on repeat calls. Then build
`pipeline(data: list[int]) -> list[int]` = `normalize -> double ->
square` where `normalize` strips negatives to zero, `double` doubles,
`square` squares — each written as a pure `map` over the list.

**Signature:**
```python
def compose(g, f): ...
def memoize(fn): ...
def pipeline(data: list[int]) -> list[int]: ...
```

| Input | Expected |
|-------|----------|
| `pipeline([1, -2, 3])` | `[4, 0, 36]` |
| `compose(square, double)(3)` | `36` (square(double(3))) |

**Constraints:** n ≤ 10^4. `memoize` must be **pure**: it may not change
the results, only the cost — the test wraps a call-counting function and
asserts the second call with the same argument does not re-invoke it.

---

## 🥇 Gold — Fingerprinted Cacheable Pipeline (~75 min)

**Task:** Implement `cacheable_pipeline(steps: list[callable], data:
list[int]) -> list[int]` that applies the steps in order AND caches the
whole pipeline result keyed by a **fingerprint** `(tuple(data), id of
steps tuple)`. A repeat call with equal data must not re-run any step.

Also implement `steps_fingerprint(steps: list[callable]) -> tuple` — a
stable, hashable identity for a step list (e.g. their `__qualname__`
tuple), so the same steps in a different order produce a different key.

**Signature:**
```python
def steps_fingerprint(steps: list[callable]) -> tuple: ...
def cacheable_pipeline(steps: list[callable], data: list[int]) -> list[int]: ...
```

| Input | Expected |
|-------|----------|
| `cacheable_pipeline([double, square], [1, 2])` | `[4, 16]` |
| `steps_fingerprint([double, square]) != steps_fingerprint([square, double])` | `True` |

**Constraints:** n ≤ 10^5 items; caching must make the second identical
call run **zero** step invocations (operation-count guard: a wrapped
step counter stays at its first-call value); `cacheable_pipeline` must
be pure — no mutation of `data` or the steps, and equal data must always
give equal output. Memory: the cache may grow, but each entry is O(1)
per item — a `tracemalloc` check on a 50k-item run keeps peak under
8 MB.

**Follow-up:** what breaks when `data` contains unhashable items?
(Answer: fingerprinting must serialize or tuple-ify them; lists become
tuples, dicts become sorted-item tuples.)

---

## Running

```bash
pytest challenges/29-functional-python/test_challenge.py -v
```
