# NumPy Lecture 32: Dtypes and Precision

## Topic Overview

Every ndarray has a dtype, and the dtype decides three budgets at
once: memory per element, range of representable values, and
precision. `float64` is the safe default, but serving a 7B-parameter
model in float64 is physically impossible — you need float16/float32,
and that means you must know exactly where precision breaks: integer
wraparound, float overflow to `inf`, `nan` poisoning, and the
bit-exactness of `==` on floats.

This lecture covers the dtype zoo (float16/32/64, integers, bool),
casting and promotion rules (including NEP 50 surprises), `nan`/`inf`
semantics, `isclose` as the only correct float equality, structured
dtypes as native tables, and the production pattern — float16 for
inference — with an honest precision budget.

## Learning Objectives

By the end of this lecture, you will be able to:

1. State itemsize for float16/32/64, int8/16/32/64, and bool, and
   convert between memory budgets
2. Predict overflow behavior: integers wrap, floats overflow to `inf`
3. Explain `nan` semantics (`nan != nan`) and use `isnan`, `nanmean`,
   and friends to contain the damage
4. Use `np.isclose`/`np.allclose` with `rtol` and `atol` instead of `==`
5. Build and sort structured arrays with named fields
6. Apply casting rules: promotion in mixed ops and the
   safe/same-kind/unsafe ladder in `astype`
7. Decide when float16 serving is safe and measure its error

## Prerequisites

| Need | Where |
|---|---|
| dtype basics and `astype` | `06-data-types-lecture.md` |
| itemsize and memory accounting | `31-memory-and-strides-lecture.md` |
| Reductions and masking | `24-ufunc-summations-lecture.md`, `15-array-filter-lecture.md` |

---

## 1. The Dtype Zoo and Its Sizes

The dtype fixes `itemsize` — bytes per element — which fixes memory
for any shape. The float family is the AI-relevant one: 2, 4, and 8
bytes for float16, float32, float64.

```python
import numpy as np

for dt in (np.float16, np.float32, np.float64):
    a = np.zeros((1000, 1000), dtype=dt)
    print(f"{dt!s:>8s} itemsize={a.itemsize} nbytes={a.nbytes}")
```

```
  float16 itemsize=2 nbytes=2000000
  float32 itemsize=4 nbytes=4000000
  float64 itemsize=8 nbytes=8000000
```

Halving precision halves memory, and memory bandwidth is usually the
bottleneck in inference. `int8` (1 byte) matters for quantized
weights, `bool` (1 byte) for masks. The conversion rule is
mechanical: `nbytes = size × itemsize`.

---

## 2. Float32 vs Float64: The Precision Budget

float32 has ~7 significant decimal digits; float64 has ~16. For
storing weights, activations, and most aggregates, float32 is plenty;
for condition numbers and near-cancellation math, float64 wins.

```python
rng = np.random.default_rng(42)
f64 = rng.normal(size=(500, 500))
f32 = f64.astype(np.float32)

print(np.allclose(f32, f64, rtol=1e-5))   # True
print(f64.nbytes, "->", f32.nbytes)       # 2000000 -> 1000000
```

```
True
2000000 -> 1000000
```

The failure mode is *accumulation*: sums of millions of float32
values drift; differences of nearly equal large numbers lose all
significance. The question "float32 or float64?" is answered by the
dynamic range of the computation, not by taste.

---

## 3. Overflow: Ints Wrap, Floats Overflow

Fixed-width integers **wrap** — `uint8(255) + 1` is `0`. Floats
**overflow** — the result is `inf`, with a `RuntimeWarning`. Python
ints never wrap (they grow), so the bug appears only after
conversion to an array.

```python
u = np.array([255], dtype=np.uint8)
with np.errstate(over="ignore"):
    wrapped = u + np.uint8(1)
print(int(wrapped[0]))                    # 0 -- wrapped silently

with np.errstate(over="ignore"):
    big = np.float64(1e308) * 10.0
print(np.isinf(big))                      # True -- overflowed
```

```
0
True
```

Wraparound is the classic counter/accumulator bug: a training-loop
counter in `uint8` silently restarts at 0. Check ranges *before*
casting, or use a dtype large enough for the domain.

---

## 4. `nan` and `inf`: The Poison and the Edge

`nan` is "not a number" and is not equal to anything — including
itself. It poisons every reduction it touches: `sum`, `mean`, `max`
all return `nan`. `inf` behaves like a very large number in
arithmetic, but `inf - inf` is `nan`.

```python
x = np.array([1.0, np.nan, 3.0])
print(np.nan != np.nan)      # True
print(x.sum())               # nan -- poisoned
print(np.isnan(x))           # [False  True False]
print(np.nanmean(x))         # 2.0 -- skips the nan

y = np.array([1.0, np.inf])
print(y.sum())               # inf
print(np.inf - np.inf)       # nan
```

```
True
nan
[False  True False]
2.0
inf
nan
```

The production rule: **find nans at the boundary** (`np.isnan`,
`np.isfinite`) rather than discovering them in aggregates. The
`np.nan*` family (`nanmean`, `nansum`, `nanmax`) exists for data
with legitimately missing values — use it deliberately, not as a
default that hides bugs.

---

## 5. `isclose`: The Only Correct Float Equality

`0.1 + 0.2 == 0.3` is `False` — float representation is binary, the
sum rounds differently. `np.isclose` compares with a tolerance:
`|a - b| <= atol + rtol * |b|`.

```python
a = 0.1 + 0.2
b = 0.3
print(a == b)                       # False
print(np.isclose(a, b))             # True
print(np.allclose(np.array([a]), np.array([b])))   # True

# atol is the guard near zero:
print(np.isclose(1e-12, 0.0, rtol=1e-5))            # False
print(np.isclose(1e-12, 0.0, rtol=1e-5, atol=1e-12))  # True
```

```
False
True
True
False
True
```

The `atol` case is the subtle one: relative tolerance is meaningless
when the true value is zero, so absolute tolerance covers it. This is
why every `_verify()` block in this module asserts with
`np.allclose`, never with `==`.

---

## 6. Structured Dtypes: A Table in One Buffer

A structured dtype packs named, typed fields into one array — the
NumPy-native "table". Fields are accessed by name; sorting can target
a field.

```python
rec = np.zeros(3, dtype=[("score", np.float32), ("id", np.int32)])
rec["score"] = [0.9, 0.4, 0.7]
rec["id"] = [7, 3, 11]

print(rec["score"])                     # [0.9 0.4 0.7]
print(rec[1])                           # (0.4, 3)
print(np.sort(rec, order="score")["id"])  # [ 3 11  7]
print(rec.nbytes)                       # 24 = 3 * (4 + 4)
```

```
[0.9 0.4 0.7]
(0.4, 3)
[ 3 11  7]
24
```

Structured arrays are the low-level ancestors of pandas DataFrames:
single buffer, field-level vectorized ops, zero copy between
components. Reach for them when you need a typed record layout for
interop (files, C structs) without pulling in pandas.

---

## 7. Casting Rules: Promotion and the safe/same-kind/unsafe Ladder

Mixed-dtype arithmetic follows promotion rules. Since NumPy 2.0
(NEP 50), Python scalars are "weak" and array dtypes dominate —
with surprises worth memorizing:

```python
i = np.arange(3, dtype=np.int64)
f = np.arange(3, dtype=np.float32)

print((i + f).dtype)          # float64 -- float32 cannot hold int64
print((i + 0.5).dtype)        # float64 -- python float is weak
print((i + 1).dtype)          # int64   -- python int stays weak
```

```
float64
float64
int64
```

Explicit `astype` uses the casting ladder: `safe` (no data loss),
`same_kind` (e.g., float64→float32), `unsafe` (float→int). Float→int
requires `unsafe` — and truncates toward zero.

```python
x = np.array([1.9, -2.7])
print(x.astype(np.int64, casting="unsafe"))   # [ 1 -2]
try:
    x.astype(np.int64, casting="safe")
except TypeError as e:
    print("safe rejected:", str(e)[:40])
```

```
[ 1 -2]
safe rejected: Cannot cast array data from dtype('float64')
```

---

## 8. float16 for Inference

Serving casts weights and activations to float16: memory halves
again versus float32 (quarters versus float64), and memory-bound
inference speeds up roughly 2×. The cost is precision: ~3 significant
decimal digits, with worst-case relative error near zero reaching
several percent.

```python
def cast_weights_for_serving(weights):
    return weights.astype(np.float16)

w64 = np.random.default_rng(42).normal(size=(1024, 1024))
w16 = cast_weights_for_serving(w64)
rel_err = np.abs(w16.astype(np.float64) - w64) / (np.abs(w64) + 1e-12)
print(w16.dtype)                          # float16
print(w64.nbytes, "->", w16.nbytes)       # 8388608 -> 2097152
print(round(float(rel_err.max()), 4))     # 0.0457 worst-case
```

```
float16
8388608 -> 2097152
0.0457
```

The decision is a precision *budget*: measure the error on the real
weight distribution (as above), decide with the model owner whether
the 4× memory saving is worth ~5% worst-case relative error, and
evaluate the actual metric — never the cast in isolation.

---

## 9. Common Mistakes to Avoid

### Mistake 1: Comparing floats with `==`
```
# WRONG — bit-exact comparison fails on 0.1 + 0.2
if a == b: ...
# CORRECT
if np.isclose(a, b, rtol=1e-5, atol=1e-8): ...
```

### Mistake 2: Assuming integer overflow saturates
```
# WRONG — wraps silently to 0
counter = np.array([255], dtype=np.uint8) + np.uint8(1)
# CORRECT — validate the range before conversion
assert values.max() < 2**16, "range check before uint16 cast"
```

### Mistake 3: Letting `nan` flow into aggregates
```
# WRONG — mean() returns nan and nobody notices until eval time
loss = errors.mean()
# CORRECT — assert finiteness at the boundary
assert np.all(np.isfinite(errors)), "non-finite errors at batch end"
```

### Mistake 4: Using `nanmean` as a default
```
# WRONG — silently hides missing data
avg = np.nanmean(x)
# CORRECT — know the missingness first
print("n_missing:", int(np.isnan(x).sum()))
avg = np.nanmean(x)   # deliberate, documented choice
```

### Mistake 5: Forgetting `astype` copies and casts loudly
```
# WRONG — float->int without acknowledging truncation
ids = scores.astype(np.int64)   # truncates, not rounds
# CORRECT — round first, cast deliberately
ids = np.rint(scores).astype(np.int64)
```

---

## 10. Best Practices

1. **Default to float32 in pipelines** unless the math demands
   float64; audit the aggregates, not the storage.
2. **Check ranges before downcasting integers** — wraparound is
   silent and undebuggable after the fact.
3. **Guard every numerical boundary with `np.isfinite`** — the error
   message you write today beats the nan you find at 3am.
4. **Use `np.isclose`/`np.allclose` for float equality everywhere**,
   including tests; choose `atol` for near-zero comparisons.
5. **Never let `nan` ride through reductions**; use `np.nan*` only
   when missingness is expected and counted.
6. **Reach for structured dtypes** when you need typed records with
   field-level vectorized ops and no pandas dependency.
7. **Know your promotion rules** (NEP 50): python scalars are weak,
   array dtypes dominate; verify mixed-dtype results explicitly.
8. **Prefer explicit casting kinds** (`casting="safe"`) so silent
   truncation cannot ship.
9. **Measure the float16 error on the real weight distribution**
   before serving; decide with a precision budget, not a default.
10. **Assert dtypes in `_verify()`** (`arr.dtype == np.float32`) —
    dtype is a contract, like shape.

---

## 11. Complexity and Cost

Memory is the dominant cost; precision is the trade.

| dtype | itemsize | 1M elements | Precision (decimal digits) | Typical use |
|---|---|---|---|---|
| `float16` | 2 B | 2 MB | ~3 | quantized serving |
| `float32` | 4 B | 4 MB | ~7 | standard ML storage |
| `float64` | 8 B | 8 MB | ~16 | conditioning-critical math |
| `int8` | 1 B | 1 MB | exact small ints | quantized weights |
| `int64` | 8 B | 8 MB | exact | indices, counters |
| `bool` | 1 B | 1 MB | 2 values | masks |

| Operation | Time | Space | Note |
|---|---|---|---|
| `astype` cast | O(n) | O(n) copy | always a copy |
| `isclose` | O(n) | O(n) mask | prefer over `==` |
| `nanmean` | O(n) | O(n) mask | skip-with-count semantics |
| structured sort | O(n log n) | O(n) | `order=` selects the field |
| mixed-dtype op | O(n) | O(n) | promotion may widen dtype |

**Scale note:** at 10M × 768 embeddings, float64 is 61 GB, float32
30 GB, float16 15 GB. The dtype choice is the cheapest memory
optimization available — it costs one line.

---

## 12. AI Engineering Relevance

**Where this shows up:** model serving (float16 quantization),
feature stores (float32), training loops (mixed precision), index
IDs (int64), and every `_verify()` assertion in this module.

| Concept here | Used for |
|---|---|
| float16/32/64 sizing | serving memory: 15/30/61 GB for 10M×768 |
| wraparound | counters, token IDs, and indices overflowing |
| `nan`/`inf` handling | loss curves, eval metrics, embedding gaps |
| `isclose` | test contracts, retrieval threshold comparisons |
| structured dtypes | typed record interop (parquet-ish rows in NumPy) |
| casting rules | weight downcasting without silent truncation |

**Scale note:** at 200 req/s, float16 serving halves memory traffic
per request — the single most cost-effective serving change in most
deployments, provided the precision budget is measured and accepted.

---

## 13. Practice Exercises

### Exercise 1: Memory Ledger (Difficulty: Easy)
For `(1_000_000, 128)` arrays, compute nbytes for float64, float32,
float16, and int8. State the savings of each downcast.

### Exercise 2: Wrap Detective (Difficulty: Easy)
Demonstrate wraparound for `int8` (127 + 1), `uint16` (65535 + 1),
and `int64` with `np.array(2**63 - 1, dtype=np.int64) + 1`. Verify
with `np.errstate`.

### Exercise 3: isclose Budget (Difficulty: Medium)
For `x = 1e-8` and `y = 0.0`, find `rtol`/`atol` combinations where
`np.isclose(x, y)` is True and False. Explain why `atol` matters.

### Exercise 4: Structured Records (Difficulty: Medium)
Build a `(100,)` structured array with fields `("user", "U16")`,
`("score", "f4")`, `("clicks", "i4")`. Sort by score descending,
find the top-5 users by score, and assert the field dtypes.

### Exercise 5: float16 Budget (Difficulty: Hard)
Take `w = rng.normal(size=(2048, 2048))`. Compute the float16 cast
error (max relative, mean relative, and the fraction of elements
with relative error > 1%). Repeat with `w * 100` (large magnitude)
and `w / 100` (small magnitude). Write a paragraph on when the
cast is acceptable.

---

## 14. Summary

| Concept | Description |
|---|---|
| itemsize | 2/4/8 bytes for float16/32/64; memory = size × itemsize |
| overflow | ints wrap silently; floats overflow to `inf` |
| `nan`/`inf` | `nan != nan`; poisons reductions; `nanmean` skips |
| `isclose` | rtol + atol — the only correct float equality |
| structured dtypes | named typed fields in one buffer |
| casting ladder | safe / same-kind / unsafe; float→int is unsafe |
| float16 serving | 4× memory savings vs float64; measure the error |

Precision is a budget you allocate explicitly: dtype for memory,
tolerance for comparisons, and guards for `nan`/`inf` at the
boundaries. Engineers who treat dtype as an implementation detail
ship wraparound counters and poisoned aggregates; engineers who
treat it as a contract ship services that run at half the memory.

---

## 15. Quick Reference

| Task | Idiom |
|---|---|
| Downcast for serving | `w.astype(np.float16)` |
| Float equality | `np.isclose(a, b, rtol=1e-5, atol=1e-8)` |
| Find bad values | `np.isnan(x)`, `np.isinf(x)`, `np.isfinite(x)` |
| Skip nans | `np.nanmean(x)`, `np.nansum(x)` |
| Structured array | `np.zeros(n, dtype=[("name", "U16"), ("v", "f4")])` |
| Sort by field | `np.sort(rec, order="name")` |
| Safe cast | `x.astype(np.int64, casting="safe")` |
| Bytes per element | `arr.itemsize`, `arr.nbytes` |

---

## Next Steps

Next: **[33 — Linear Algebra](33-linear-algebra-lecture.md)** —
`@`, `solve` over `inv`, decompositions, norms, conditioning, and
cosine similarity as matmul.
Continues in: **[Phase 3 — SciPy statistics](../../scipy/13-statistical-tests-lecture.md)**
where p-values demand the same honesty as precision budgets.
Official docs: [NumPy dtypes](https://numpy.org/doc/stable/reference/arrays.dtypes.html),
[`np.isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html),
[NEP 50](https://numpy.org/neps/nep-0050-scalar-promotion.html).
