# NumPy 34 — Advanced Indexing: fancy, masks, take, top-k, searchsorted

## Topic Overview

Basic slicing (`x[1:5]`, `x[::2]`) covers contiguous or strided
access. Real pipelines need more: selecting arbitrary rows,
filtering by condition, shuffling batches, retrieving top-k
candidates, and bucketing continuous features. This lecture covers
the five tools that replace Python loops in those situations —
fancy indexing, boolean masks, `np.ix_`, `take`/`put`, and
`argpartition`/`searchsorted` — plus the view-vs-copy semantics
that decide whether your code corrupts the dataset or just reads
it.

## Learning Objectives

By the end of this lecture you will be able to:

1. Select and reorder rows with integer-array indexing and explain
   why it returns a copy.
2. Filter and write through boolean masks in one expression.
3. Build submatrix selections with `np.ix_` without the
   elementwise-pairing trap.
4. Use `np.take`/`np.put` with explicit boundary policies
   (`wrap`, `clip`).
5. Retrieve top-k elements in O(n) with `argpartition` instead of
   a full `argsort`.
6. Bucket values into bins with `searchsorted`/`digitize` and
   distinguish `side="left"` vs `"right"`.
7. Distinguish views from copies with `np.shares_memory`.

## Prerequisites

- NumPy 29 (broadcasting), 30 (vectorization), 33 (linear algebra
  — the top-k idea feeds cosine retrieval).
- Basic slicing and boolean comparisons.

---

## Key Concepts

### 1. Fancy indexing — integer arrays select, in order, as a copy

`x[[i0, i1, ...]]` builds a **new array** containing the rows at
those indices, in that order. Duplicates are allowed; the result
is always a copy.

```python
import numpy as np

scores = np.array([0.9, 0.4, 0.7, 0.2, 0.8])
print(scores[[3, 0, 4]])            # [0.2 0.9 0.8]
X = np.random.default_rng(42).normal(size=(6, 4))
shuffled = X[np.random.default_rng(0).permutation(X.shape[0])]
print(np.shares_memory(shuffled, X))  # False -- it's a copy
```

**Use it for:** batch shuffling, class-balanced sampling,
lookup-table construction, any reorder.

**Cost:** O(selected size); the copy dominates.

---

### 2. Boolean masks — filter with a condition, write with a mask

A boolean array of the same shape selects the True positions:

```python
data = np.random.default_rng(1).normal(size=12)
pos = data[data > 0.0]              # only positive entries
print(pos.shape)                    # (6,)
```

Masks also **write**: `data[data < -1.0] = -1.0` clamps in place,
no loop. Combine masks with `&`, `|`, `~` (parenthesize
conditions!).

**Common trap:** `mask` must match the *shape being indexed* —
`X[labels == 1]` works on the leading axis; filtering both axes
needs `np.ix_` or column-wise masks.

**Cost:** O(n) to build the mask, O(kept) for the copy.

---

### 3. `np.ix_` — submatrix selection without the pairing trap

`X[rows, cols]` with arrays pairs them elementwise (row i with
column i). To get the *grid* of all `rows × cols`, use `np.ix_`:

```python
M = np.arange(20.0).reshape(4, 5)
rows = np.array([0, 3])
cols = np.array([1, 2, 4])
grid = M[np.ix_(rows, cols)]        # (2, 3) submatrix
```

`M[np.ix_(rows, cols)]` ≡ `M[rows][:, cols]` — the grid, not the
diagonal pairing. This is the fix for the most common advanced-
indexing bug in the wild.

**Cost:** O(rows·cols) copy.

---

### 4. `take` / `put` — axis-aware selection with boundary policy

`np.take(a, idx, axis=..., mode=...)` is fancy indexing with an
explicit out-of-bounds policy:

| mode | Behavior |
|---|---|
| `"wrap"` | indices wrap modulo the axis length |
| `"clip"` | indices clamp to the valid range |
| `"raise"` (default) | error on out-of-bounds |

```python
x = np.arange(6)
print(np.take(x, [7, 8], mode="wrap"))   # [1 2]
print(np.take(x, [-3, 9], mode="clip"))  # [0 5]
```

`np.put(dst, idx, values)` writes values at indices (raises by
default) — the write counterpart. Both avoid Python loops for
batch gathers/scatters.

---

### 5. `argpartition` — top-k in O(n), no full sort

`np.argpartition(x, k)` reorders indices so the element at
position `k` is the (k+1)-th smallest and everything left of it
is ≤ it — but the left side is **not sorted**. Slice the first
`k` for the k smallest:

```python
x = np.random.default_rng(2).normal(size=100_000)
k = 5
idx = np.argpartition(x, k - 1)[:k]     # k smallest (unsorted)
top5 = np.sort(x[idx])                  # sort just the k winners
truth = np.sort(x)[:k]
print(np.array_equal(top5, truth))      # True
```

For the k **largest** (retrieval!), partition at `-k`:

```python
kidx = np.argpartition(x, -k)[-k:]
```

**Complexity:** O(n) average for `argpartition` vs O(n log n) for
`argsort`. For "top-10 of a million", that is ~100× less work.
Ties: the selected set is correct; which duplicate wins is not
specified.

**AI relevance:** candidate retrieval before ranking — cosine
scores (NumPy 33) → `argpartition` → rerank the survivors.

---

### 6. `searchsorted` — insertion points, log-time bucketing

`np.searchsorted(bins, v)` returns the index where each `v` would
insert to keep `bins` sorted: O(log n) per query, fully
vectorized.

- `side="left"`: first index where `bins[i] >= v`.
- `side="right"`: first index where `bins[i] > v` — i.e., the
  value lands *after* equal bin edges.

```python
bins = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
v = np.array([0.05, 0.25, 0.8, 2.0, -1.0])
print(np.searchsorted(bins, v, side="right"))   # [1 2 4 5 0]
print(np.digitize(v, bins))                     # same
```

`np.digitize` is `searchsorted` with `side="right"` on the bin
edges — the one-liner for feature bucketing and histogram
assignment.

**Requirement:** `bins` must be sorted ascending.

**AI relevance:** quantile bucketing (feed a model binned
features), score thresholds, and "which group does this row
belong to" lookups.

---

### 7. `unique` + `return_counts` — label statistics in one call

```python
labels = np.random.default_rng(3).integers(0, 4, size=1000)
uniq, counts = np.unique(labels, return_counts=True)
print(counts.sum() == labels.size)   # True
```

`np.unique` sorts and deduplicates; with `return_counts` you get
the categorical histogram — cardinality, class balance, and
missing-value counts for free.

**Cost:** O(n log n) (sort), O(unique) output.

---

### 8. Views vs copies — the memory semantics that bite

| Expression | Result | Memory |
|---|---|---|
| `x[1:5]`, `x[::2]`, `x.T` | view | shares memory with base |
| `x[[0, 2]]`, `x[mask]` | copy | new buffer |
| `x.reshape(...)` | view (when possible) | shares memory |
| `np.take(...)`, `np.copy` | copy | new buffer |

```python
base = np.arange(10.0)
view = base[::2]
view[:] = -1.0
print(base[0], base[2])            # -1.0 -1.0 -- wrote through!

fresh = np.arange(10.0)
copy_ = fresh[[0, 2, 4]]
copy_[:] = -1.0
print(fresh[0], fresh[2])          # 0.0 2.0 -- isolated
```

Writing through a view is often exactly what you want (in-place
clamping, zeroing, scaling); forgetting that a slice is a view
corrupts the base array silently. `np.shares_memory(a, b)` tells
you the truth before you debug for an hour.

---

## Common Mistakes to Avoid

1. **`X[rows, cols]` when you wanted the grid.** Pairing is
   elementwise; wrap with `np.ix_`.
2. **Mutating a "copy" that is actually a view.** Basic slices
   share memory; fancy/boolean indexing does not. Check with
   `np.shares_memory` before relying on isolation.
3. **Forgetting `side` on boundary values.** `searchsorted`
   defaults to `side="left"`; bucketing usually wants
   `side="right"` (or `digitize`) so values equal to an edge land
   in the *next* bucket.
4. **Full `argsort` when top-k suffices.** O(n log n) vs O(n) —
   at retrieval scale this is the difference between 50 ms and
   0.5 ms.
5. **Unparenthesized boolean combinations.** `data[x > 0 & x < 1]`
   parses as `x > (0 & x) < 1` — always write
   `data[(x > 0) & (x < 1)]`.
6. **Out-of-bounds fancy indices raise** by default (`IndexError`)
   — use `take` with `wrap`/`clip` when you *want* a boundary
   policy.
7. **`argpartition` output is not sorted.** It only guarantees
   the partition point; sort the winners yourself.

---

## Best Practices

- **Shuffle with `rng.permutation(n)` + fancy indexing** — one
  line, reproducible with a seed.
- **Filter with masks, not loops** — `X[mask]` is the idiomatic
  row filter; `X[(X[:, 0] > 0) & (X[:, 1] < 0)]` handles compound
  row predicates.
- **Clamp in place with masked assignment** — `a[a > hi] = hi`
  avoids allocating a copy.
- **Use `argpartition` for every "top-k" path** — retrieval,
  nearest-neighbor candidates, outlier detection.
- **Bucket with `searchsorted(bins, v, side="right")`** or
  `digitize`; keep `bins` sorted and boundary semantics explicit.
- **Prefer `np.take` with explicit `mode`** when indices may come
  from user input — turn silent `IndexError`s into defined
  behavior.
- **Verify memory semantics once per pattern** with
  `np.shares_memory` when writing libraries that mutate data.

---

## Complexity and Cost

| Operation | Time | Memory | Notes |
|---|---|---|---|
| `x[idx]` fancy | O(selected) | O(selected) copy | duplicates allowed |
| `x[mask]` | O(n) | O(kept) copy | mask build is O(n) |
| `np.ix_` grid | O(rows·cols) | O(rows·cols) | equivalent to `[rows][:, cols]` |
| `np.take` / `np.put` | O(k) | O(k) | `mode` handles bounds |
| `np.argpartition` | O(n) average | O(n) index array | partial sort only |
| `np.argsort` | O(n log n) | O(n) | full order |
| `np.searchsorted` | O(k log n) | O(k) | bins must be sorted |
| `np.unique(return_counts)` | O(n log n) | O(unique) | sorts first |
| basic slice / reshape | O(1) | 0 (view) | shares memory |

---

## AI Engineering Relevance

- **Batch shuffling** for training loops: `X[rng.permutation(n)]`
  — no Python loop, reproducible seeds.
- **Class-balanced sampling**: boolean masks per label +
  `rng.choice` on the mask indices.
- **Retrieval pipelines**: cosine scores (NumPy 33) →
  `argpartition` top-k → rerank the k survivors — the standard
  retrieve-then-rerank pattern in RAG and search.
- **Feature engineering**: `searchsorted`/`digitize` turns
  continuous features into quantile buckets; `np.unique(
  return_counts=True)` gives class balance reports.
- **Data cleaning**: mask-based clamps, outlier replacement, and
  `take(mode="clip")` guards for ragged user input.
- **Memory discipline**: knowing views from copies prevents
  accidental dataset corruption and avoids needless copies in
  memory-bound serving paths.

---

## Practice Exercises

1. Shuffle a `(1000, 32)` matrix with a seeded permutation;
   assert `np.shares_memory` is False and the row multiset is
   preserved (`np.unique` on an `np.lexsort`-style fingerprint).
2. Filter rows where column 0 > 0 and column 1 < 0; assert the
   boolean counts match the filter size and that the result is a
   copy.
3. From a `(10, 8)` matrix, select the `(3, 4)` submatrix at rows
   `[0, 5, 9]` and cols `[1, 3, 6, 7]` via `np.ix_`; assert it
   equals the double-indexed version.
4. Find the 10 largest values of a `1e6`-element array with
   `argpartition`, assert set-equality with the full sort, and
   time-benchmark (informally) against `argsort`.
5. Bucket 10,000 uniform values into 5 quantile bins using
   `np.quantile` edges + `searchsorted`; assert every bin has
   within 10% of n/5 members and that boundary values land
   deterministically.

---

## Summary

- **Fancy indexing** selects/reorders rows as a copy;
  **boolean masks** filter and write in place.
- **`np.ix_`** builds grids without the elementwise-pairing trap.
- **`take`/`put`** gather/scatter with explicit boundary modes.
- **`argpartition`** gives top-k in O(n) — retrieval's default
  tool; sort the winners yourself.
- **`searchsorted`/`digitize`** bucket sorted data in O(log n)
  per element, with `side` deciding edge ownership.
- **Views share memory; advanced indexing copies** — check with
  `np.shares_memory` when the semantics decide correctness.

## Quick Reference

```python
import numpy as np

# select / reorder / filter
rows = X[[0, 4, 7]]                    # copy, in order
kept = X[X[:, 0] > 0.0]                # boolean filter
grid = M[np.ix_(rows, cols)]           # submatrix grid
X[X > 1.0] = 1.0                       # in-place clamp

# gather / scatter with policies
np.take(x, idx, mode="wrap")           # wrap | clip | raise
np.put(dst, idx, vals)                 # write at indices

# top-k and bucketing
idx = np.argpartition(scores, -k)[-k:] # k largest, O(n)
b = np.searchsorted(bins, v, side="right")   # bucket ids
b = np.digitize(v, bins)               # same as side="right"

# memory semantics
np.shares_memory(a, b)                 # True => view
```

## Next Steps

- Combine with NumPy 33: cosine scores via matmul, then
  `argpartition` top-k — you have built a retrieval pipeline in
  two NumPy calls.
- In SciPy 16 (distance and similarity) the same top-k pattern
  reappears with `cdist`/`pdist` and KD-trees.
- In SciPy 13 (statistical tests) you will use masks for group
  splits before running hypothesis tests.
