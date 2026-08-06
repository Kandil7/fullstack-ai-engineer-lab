# NumPy Lecture 30: Vectorization

## Topic Overview

Vectorization is the practice of expressing array math so that the
per-element work happens inside compiled C (and eventually BLAS/GPU
kernels) instead of inside the Python interpreter. The same operation —
clamp a value, sum a column, normalize an embedding — runs 10–100×
faster as a vectorized expression than as a `for` loop, and the gap
widens with data size.

This lecture teaches the rewrite patterns: ufunc elementwise
expressions, `np.where` as a vectorized if-else, boolean masking for
select/update, `einsum` for explicit axis algebra, and the honest
exceptions — when a loop is truly unavoidable and how to shrink it.
It also demolishes one popular myth: `np.vectorize` is *not* fast; it
is a loop in disguise.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Rewrite an elementwise Python loop as a single vectorized expression
2. Replace scalar `if/else` logic with `np.where` and `np.clip`
3. Use boolean masks for selection, updates, and conditional reductions
4. Read and write `einsum` subscripts for dot, outer, trace, transpose,
   and batch matmul — and verify them against `@` and `.T`
5. Explain when a Python loop is genuinely unavoidable (ragged data,
   data-dependent control flow) and how to keep Python overhead to
   O(#rows) rather than O(#elements)
6. Explain why `np.vectorize` does not speed anything up

## Prerequisites

| Need | Where |
|---|---|
| Broadcasting rules and `newaxis` | `29-broadcasting-deep-lecture.md` |
| Ufuncs and elementwise arithmetic | `19-ufunc-intro-lecture.md`, `21-ufunc-arithmetic-lecture.md` |
| Boolean filtering and `np.where` | `15-array-filter-lecture.md` |
| Axis semantics of reductions | `24-ufunc-summations-lecture.md` |
| Views vs copies | `07-copy-vs-view-lecture.md` |

---

## 1. The Loop → Vectorized Rewrite

Every elementwise Python loop has the same shape: visit each element
through the interpreter, apply scalar logic, store. The vectorized
version is one expression over the whole array. Both are O(n) work;
the loop adds O(n) interpreter overhead — the constant factor that
costs 10–100×.

```python
import numpy as np

def relu_loop(values):
    out = np.empty_like(values)
    for i in range(values.size):
        out[i] = values[i] if values[i] > 0 else 0.0
    return out

def relu_vec(values):
    return np.maximum(values, 0.0)

x = np.random.default_rng(42).normal(size=1_000_000)
print(np.array_equal(relu_loop(x), relu_vec(x)))   # True
```

```
True
```

The two functions are numerically identical; only the execution path
differs. The loop version is the reference you keep in your head —
never in production.

---

## 2. `np.where`: The Vectorized If-Else

`np.where(cond, a, b)` selects elementwise from `a` and `b`. Both arms
are computed, then one element from each position is kept — so it is
not a branch at all, it is a gather.

```python
def clip_where(values, lo, hi):
    return np.where(values < lo, lo,
                    np.where(values > hi, hi, values))

data = np.random.default_rng(0).normal(size=100_000)
print(np.array_equal(clip_where(data, -1.0, 1.0),
                     np.clip(data, -1.0, 1.0)))        # True

signed = np.where(data > 0, 1.0, np.where(data < 0, -1.0, 0.0))
print(np.array_equal(signed, np.sign(data)))           # True
```

```
True
True
```

Nested `np.where` reads as `elif` chains. When the operation is
standard (clip, sign, abs), prefer the dedicated ufunc — it is faster
and clearer than the where-chain.

---

## 3. Masking: Select, Update, Reduce

A boolean mask selects positions; combined with fancy indexing it
replaces the filter-then-update loop.

```python
scores = np.random.default_rng(1).normal(size=1_000_000)
mask = scores < 0
scores[mask] = 0.0                # vectorized scatter: one pass

vals = np.random.default_rng(2).normal(size=1_000_000)
print(int((vals > 0).sum()))                    # count positives
print(np.allclose(vals[vals > 0].sum(),
                  np.where(vals > 0, vals, 0.0).sum()))  # True
```

```
500533
True
```

Two idioms here: mask-then-assign for updates, mask-then-reduce for
conditional aggregates. The `np.where` form is the "keep shape"
variant — useful when the result must stay aligned with the input.

---

## 4. `einsum`: Explicit Axis Algebra

`einsum` names every axis and the output layout in one string. The
same notation covers matmul, outer products, traces, transposes, and
batched products — and the subscripts document the math in the code.

```python
A = np.random.default_rng(3).normal(size=(4, 5))
B = np.random.default_rng(4).normal(size=(5, 6))

print(np.allclose(np.einsum("ij,jk->ik", A, B), A @ B))   # True
print(np.einsum("ii->", np.ones((5, 5))))                 # 5.0 trace
print(np.einsum("i,j->ij", np.ones(3), np.ones(4)).shape) # (3, 4)
print(np.array_equal(np.einsum("ij->ji", A), A.T))        # True

# Batched: "b" is the batch axis on both operands and the output.
batch = np.random.default_rng(5).normal(size=(8, 4, 5))
print(np.allclose(np.einsum("bij,jk->bik", batch, B),
                  batch @ B))                             # True
```

```
True
5.0
(3, 4)
True
True
```

A repeated index on the input side means "sum over this axis"; an
index on the output side means "keep this axis". The rules take an
hour to internalize and pay off forever — einsum is how you *see*
attention scores, batched similarity, and tensor contractions.

---

## 5. When a Loop Is Unavoidable

Two cases defeat full vectorization: ragged data (rows of different
lengths cannot live in one dense array) and control flow that depends
on row *content*. The professional pattern: loop over the small outer
axis, vectorize the inner work.

```python
def row_stats_ragged(rows):
    """Per-row mean/std for ragged rows."""
    return np.array([(r.mean(), r.std()) for r in rows])

rng = np.random.default_rng(6)
ragged = [rng.normal(size=n) for n in (3, 7, 2, 5)]
print(row_stats_ragged(ragged).shape)     # (4, 2)
```

```
(4, 2)
```

Python overhead scales with the number of loop iterations, so the
rule is: **never iterate over elements; iterate over the outermost
logical unit (rows, batches, files), and vectorize every body.**
A 1M-row loop with vectorized bodies costs ~1M interpreter steps; a
1M-element doubly-nested loop costs ~1M×D steps.

---

## 6. `np.vectorize` Is NOT Fast

`np.vectorize` wraps a Python scalar function and calls it once per
element through the interpreter. It exists so that scalar functions
gain the *call signature* of a ufunc (broadcasting, `out=`); it gains
none of the speed.

```python
def f(x):
    return x * 2 if x > 0 else -x

f_vec = np.vectorize(f)
x = np.random.default_rng(7).normal(size=200_000)

import time
def timed(label, fn):
    t0 = time.perf_counter(); fn()
    print(f"{label:<14s} {time.perf_counter() - t0:.4f}s")

timed("vectorize",   lambda: f_vec(x))
timed("explicit loop", lambda: np.fromiter((f(v) for v in x), float))
timed("vectorized",  lambda: np.where(x > 0, x * 2, -x))
```

```
vectorize      0.0324s
explicit loop  0.0473s
vectorized     0.0019s
```

The vectorized rewrite is ~15× faster here and the gap grows with
size. Times vary by machine — the ordering does not.

---

## 7. Production Pattern: Masked Mean-Pooling

Sentence embeddings: tokens are padded to a fixed length, and the
sentence vector is the mean over the *real* tokens only. One
`np.where`, one sum, one broadcast divide — no batch loop.

```python
def mean_pool(embeddings, mask):
    """Mean-pool over the token axis, ignoring padding.

    embeddings: (B, T, D)   mask: (B, T) bool -> (B, D)
    """
    masked = np.where(mask[:, :, None], embeddings, 0.0)
    sums = masked.sum(axis=1)
    counts = mask.sum(axis=1, keepdims=True).astype(np.float64)
    return sums / np.maximum(counts, 1.0)

rng = np.random.default_rng(8)
emb = rng.normal(size=(16, 32, 64))
tok_mask = rng.integers(0, 2, size=(16, 32), dtype=bool)
pooled = mean_pool(emb, tok_mask)
print(pooled.shape)                                    # (16, 64)
print(np.allclose(pooled[0], emb[0][tok_mask[0]].mean(axis=0)))  # True
```

```
(16, 64)
True
```

`mask[:, :, None]` broadcasts the `(B, T)` mask over the `D` axis
(lecture 29), and `keepdims` keeps `(B, 1)` so the divide broadcasts
down rows. The whole batch pools in five compiled operations.

---

## 8. Common Mistakes to Avoid

### Mistake 1: Reaching for `np.vectorize` for speed
```
# WRONG — one Python call per element, still
fast = np.vectorize(slow_python_fn)(data)
# CORRECT — rewrite the math with ufuncs and np.where
fast = np.where(data > 0, data * 2, -data)
```

### Mistake 2: Chained filtering instead of one mask
```
# WRONG — three passes and fragile re-indexing
sub = vals[vals > 0][vals[vals > 0] < 10]
# CORRECT — one mask built from combined conditions
sub = vals[(vals > 0) & (vals < 10)]
```

### Mistake 3: Looping over the big axis
```
# WRONG — Python overhead scales with element count
for i in range(len(big)):
    big[i] = big[i] * 2
# CORRECT — one expression; or loop outer, vectorize inner
big = big * 2
```

### Mistake 4: `where` when a ufunc exists
```
# WRONG — slower than the dedicated ufunc
clipped = np.where(x < 0, 0.0, np.where(x > 1.0, 1.0, x))
# CORRECT
clipped = np.clip(x, 0.0, 1.0)
```

### Mistake 5: Assuming "vectorized" means "no temporaries"
```
# WRONG — three full-size temporaries for a simple update
y = (a * b) + (c * d)      # fine for clarity, but each op allocates
# BETTER at scale — reuse output buffers
np.multiply(a, b, out=tmp1); np.multiply(c, d, out=tmp2)
np.add(tmp1, tmp2, out=y)
```

---

## 9. Best Practices

1. **Write the loop reference first** in a comment or docstring, then
   replace it with the vectorized expression; keep both in `_verify()`.
2. **Use `np.where` for elementwise selection** and dedicated ufuncs
   (`np.clip`, `np.sign`, `np.maximum`) when they exist.
3. **Build one combined mask** with `&`, `|`, `~` instead of chaining
   filters.
4. **Reach for `einsum` when the operation has named axes**, and verify
   against `@` / `.T` in tests.
5. **Never loop over elements**; loop over rows/batches/files and
   vectorize every loop body.
6. **Do not use `np.vectorize` for performance** — only for ufunc-style
   API compatibility.
7. **Print timings, never assert them** — wall clock is not
   reproducible in CI; assert on values instead.
8. **Watch for hidden O(n·m) intermediates** when broadcasting meets
   reductions; use the matmul identity (lecture 29 Gold) to collapse
   them.
9. **Keep the number of passes low**: prefer `mask.sum()` over
   `len(mask[mask])`, one `where` over three nested ones.
10. **Document complexity** (O(B·T·D) etc.) on functions that process
    batches — it is the contract your reviewers check.

---

## 10. Complexity and Cost

Memory and allocation count, not just time. The Python loop's cost is
interpreter overhead per element; vectorized code moves the cost to
temporary buffers.

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Python loop over n elements | O(n) × ~50 ns/iter | O(n) | vectorized ufunc — 10–100× less wall time |
| `np.vectorize(f)` over n | O(n) × ~200 ns/iter | O(n) | `np.where` / ufunc rewrite |
| `np.where(cond, a, b)` | O(n) | O(n) output | `np.clip` for clip — fewer passes |
| mask `vals[mask]` | O(n) | O(k) result (k = True count) | — |
| `einsum("ij,jk->ik", A, B)` | O(n·m·k) | O(n·m) | `A @ B` — same math, BLAS-tuned |
| `mean_pool` batch | O(B·T·D) | O(B·T·D) + O(B·D) | fuse with in-place `out=` |

**Scale note:** at 10M embeddings × 768 dims, a Python loop is
hours; the vectorized pass is seconds. The dominant cost is memory
bandwidth — every full-size temporary is a pass over RAM.

---

## 11. AI Engineering Relevance

**Where this shows up:** embedding normalization, masked pooling,
attention score computation, token masking, gradient clipping,
thresholding — every hot loop in a training or inference pipeline.

| Concept here | Used for |
|---|---|
| ufunc rewrites | elementwise ops in preprocessing (tokenization stats, normalization) |
| `np.where` / masks | masked loss (ignore padding), thresholding, clipping |
| `einsum` | attention `softmax(Q K^T) V`, batched similarity, tensor contractions |
| loop-outer/vectorize-inner | ragged batches, per-sentence logic |
| masking + `keepdims` | mean/max pooling over variable-length sequences |

**Scale note:** the batch matmul `X @ X.T` for 10k embeddings is
10¹² multiply-adds — BLAS eats it in a second; a Python double loop
would take days. Vectorization is not an optimization here, it is the
difference between a service and a demo.

---

## 12. Practice Exercises

### Exercise 1: Rewrite the Loop (Difficulty: Easy)
Write `sigmoid(x)` both ways — Python loop and one vectorized
expression `1 / (1 + np.exp(-x))` — and assert they agree on
`rng.normal(size=10_000)` with `np.allclose`.

### Exercise 2: Where-Clip (Difficulty: Easy)
Implement `clamp(x, lo, hi)` with `np.where` only (no `np.clip`).
Verify against `np.clip` on arrays with values outside the range,
and on a zero-size array.

### Exercise 3: Einsum Menu (Difficulty: Medium)
Using `einsum`, express: trace of `A`; row sums of `A` (`"ij->i"`);
`A @ B` for 2-D; `X @ Y.T` for similarity; a batched product
`"bij,jk->bik"`. Verify each against the plain NumPy equivalent.

### Exercise 4: Ragged Loop Discipline (Difficulty: Medium)
Given `groups: list[np.ndarray]`, return the normalized (z-scored)
version of each group. Keep the loop over groups; vectorize the
inner math. Assert every returned group has mean ≈ 0.

### Exercise 5: Masked Embedding Mean (Difficulty: Hard)
Implement `mean_pool` from Section 7, then extend it: return both the
pooled vector and the token counts, and verify on a padded batch
where the first row has 3 real tokens and the second has 12.

---

## 13. Summary

| Concept | Description |
|---|---|
| Loop → vectorized | one expression replaces the per-element interpreter loop |
| `np.where` | vectorized if-else; both arms computed, then gathered |
| Masking | select/update/reduce with boolean arrays |
| `einsum` | named-axis algebra: dot, outer, trace, batch matmul |
| Loop exceptions | ragged data and data-dependent control flow; loop outer, vectorize inner |
| `np.vectorize` | API convenience only — a loop in disguise, never a speedup |

Vectorization is the skill that separates "I wrote it, it runs" from
"I wrote it, it runs at the speed of the hardware." The patterns are
few and mechanical; the discipline is reaching for them by default
and keeping the loop-reference version in your tests so the rewrite
can be proven equal.

---

## 14. Quick Reference

| Task | Idiom |
|---|---|
| Elementwise math | `x * 2 + 1`, `np.exp(x)` |
| Conditional select | `np.where(cond, a, b)` |
| Clip | `np.clip(x, lo, hi)` |
| Masked sum | `vals[mask].sum()` or `np.where(mask, vals, 0).sum()` |
| Masked update | `vals[mask] = value` |
| Matmul / batch matmul | `A @ B`, `batch @ B` |
| Named-axis math | `np.einsum("ij,jk->ik", A, B)` |
| Ragged stats | `np.array([row_stats(r) for r in rows])` |
| Timings | `time.perf_counter()` — print, never assert |

---

## Next Steps

Next: **[31 — Memory and Strides](31-memory-and-strides-lecture.md)** —
why the vectorized code you just wrote is fast (or suddenly slow):
strides, C vs Fortran order, views, and cache locality.
Continues in: **[Phase 3 — linear algebra](33-linear-algebra-lecture.md)**
for `@`, `solve`, decompositions, and cosine similarity as matmul.
Official docs: [NumPy einsum](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html),
[`np.where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html),
[NumPy ufuncs](https://numpy.org/doc/stable/reference/ufuncs.html).
