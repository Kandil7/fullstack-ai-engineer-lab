"""NumPy 34: Advanced Indexing — fancy, boolean, take, top-k, searchsorted.

Why this matters for AI/backend engineering:
Advanced indexing is how you slice datasets without Python loops:
masking filters rows, fancy indexing shuffles batches, argpartition
finds top-k candidates for retrievers in O(n), and searchsorted
buckets features for feature engineering. Understanding view vs
copy semantics here prevents the classic "my shuffle corrupted the
dataset" bug.

Docs: https://numpy.org/doc/stable/user/basics.indexing.html
"""

import numpy as np

rng = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Example 1: fancy indexing — integer arrays select arbitrary rows
# ---------------------------------------------------------------------------
# x[[i0, i1, ...]] returns a NEW array (a copy): rows in the given order.
# This is how you shuffle batches and build lookup tables.

scores = np.array([0.9, 0.4, 0.7, 0.2, 0.8])
pick = scores[[3, 0, 4]]
print("Example 1: fancy pick:", pick)          # [0.2 0.9 0.8]

X = rng.normal(size=(6, 4))
shuffled = X[rng.permutation(X.shape[0])]
print("Example 1: shuffled rows are a copy:",
      not np.shares_memory(shuffled, X))

# ---------------------------------------------------------------------------
# Example 2: boolean masks — filter by condition, then assign
# ---------------------------------------------------------------------------
# A boolean mask keeps True positions; masks also write: x[mask] = value.

data = rng.normal(size=12)
mask = data > 0.0
print("Example 2: positives kept:", data[mask].shape)
print("Example 2: mask counts:", mask.sum(), "/", data.size)

data[data < -1.0] = -1.0                        # clamp via mask assignment
print("Example 2: clamped min:", data.min())    # -1.0

# ---------------------------------------------------------------------------
# Example 3: np.ix_ — select a submatrix without broadcast traps
# ---------------------------------------------------------------------------
# X[np.ix_(rows, cols)] selects the rows x cols grid. Plain X[rows, cols]
# would pair them elementwise instead (the classic bug).

M = np.arange(20.0).reshape(4, 5)
rows = np.array([0, 3])
cols = np.array([1, 2, 4])
grid = M[np.ix_(rows, cols)]
print("Example 3: grid shape:", grid.shape)    # (2, 3)
print("Example 3: grid:\n", grid)

# ---------------------------------------------------------------------------
# Example 4: take / put — axis-aware selection with out-of-bounds modes
# ---------------------------------------------------------------------------
# np.take(a, idx, axis=..., mode="wrap"|"clip") is fancy indexing with
# explicit boundary policy; np.put writes into a copy-free manner.

x4 = np.arange(6)
print("Example 4: take wrap:", np.take(x4, [7, 8], mode="wrap"))    # [1 2]
print("Example 4: take clip:", np.take(x4, [-3, 9], mode="clip"))   # [0 5]

dst = np.zeros(6)
np.put(dst, [0, 2], [9.0, -9.0])
print("Example 4: put:", dst)                  # [ 9.  0. -9.  0.  0.  0.]

# ---------------------------------------------------------------------------
# Example 5: argsort and argpartition — top-k without a full sort
# ---------------------------------------------------------------------------
# np.argpartition(x, k) guarantees the k-th smallest is in place, left
# partition <= pivot: O(n) average. Full argsort is O(n log n).

x5 = rng.normal(size=100_000)
k = 5
idx = np.argpartition(x5, k - 1)[:k]           # k smallest
top5 = np.sort(x5[idx])
truth = np.sort(x5)[:k]
print("Example 5: argpartition top-k matches sort:",
      np.array_equal(top5, truth))

# Top-k by score for retrieval (largest k): partition at n-k.
kidx = np.argpartition(x5, -k)[-k:]
print("Example 5: largest k match:",
      np.array_equal(np.sort(x5[kidx]), np.sort(x5)[-k:]))

# ---------------------------------------------------------------------------
# Example 6: searchsorted — insertion points for sorted arrays
# ---------------------------------------------------------------------------
# np.searchsorted(bins, v) returns where v would insert to keep order:
# O(log n) per query, no Python loop. The backbone of bucketing.

bins = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
v = np.array([0.05, 0.25, 0.8, 2.0, -1.0])
b = np.searchsorted(bins, v, side="right")
print("Example 6: bucket indices:", b)         # [1 2 4 5 0]
print("Example 6: digitize agrees:",
      np.array_equal(b, np.digitize(v, bins)))

# ---------------------------------------------------------------------------
# Example 7: unique + return_counts — label distribution in one call
# ---------------------------------------------------------------------------
# np.unique with return_counts is the histogram of categorical labels.

labels = rng.integers(0, 4, size=1000)
uniq, counts = np.unique(labels, return_counts=True)
print("Example 7: labels:", uniq)
print("Example 7: counts:", counts)
print("Example 7: counts sum to n:", counts.sum() == labels.size)

# ---------------------------------------------------------------------------
# Example 8: view vs copy — basic slices share memory, advanced don't
# ---------------------------------------------------------------------------
# base[::2] is a VIEW: writing through it changes the base. Fancy and
# boolean indexing always COPY. Mixing the two silently is the classic bug.

base = np.arange(10.0)
view = base[::2]
view[:] = -1.0
print("Example 8: view wrote through:", base[0], base[2])   # -1.0 -1.0

fresh = np.arange(10.0)
copy_ = fresh[[0, 2, 4]]
copy_[:] = -1.0
print("Example 8: fancy copy isolated:", fresh[0], fresh[2])  # 0.0 2.0


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def _verify() -> None:
    rng_v = np.random.default_rng(1)

    # 1. fancy indexing returns a copy, not a view
    a = np.arange(10.0)
    b = a[[1, 3, 5]]
    b[:] = 0.0
    assert a[1] == 1.0 and not np.shares_memory(a, b)

    # 2. boolean mask filters correctly and counts match
    x = rng_v.normal(size=100)
    kept = x[x > 0.0]
    assert kept.size == int((x > 0.0).sum())
    assert np.all(kept > 0.0)

    # 3. ix_ grid equals manual double indexing
    M = rng_v.normal(size=(6, 7))
    rows = np.array([0, 4, 5])
    cols = np.array([2, 6])
    assert np.array_equal(M[np.ix_(rows, cols)], M[rows][:, cols])

    # 4. take modes behave
    assert np.array_equal(np.take(np.arange(6), [7, 8], mode="wrap"), [1, 2])
    assert np.array_equal(np.take(np.arange(6), [-3, 9], mode="clip"), [0, 5])

    # 5. argpartition top-k equals full-sort top-k
    y = rng_v.normal(size=50_000)
    idx5 = np.argpartition(y, 4)[:5]
    assert np.array_equal(np.sort(y[idx5]), np.sort(y)[:5])
    kidx5 = np.argpartition(y, -5)[-5:]
    assert np.array_equal(np.sort(y[kidx5]), np.sort(y)[-5:])

    # 6. searchsorted bucket assignment is correct on boundaries
    bins6 = np.array([0.0, 0.5, 1.0])
    assert np.array_equal(np.searchsorted(bins6, [0.0, 0.5, 0.75], side="right"),
                          [1, 2, 2])
    assert np.array_equal(np.searchsorted(bins6, [0.0, 0.5, 0.75], side="left"),
                          [0, 1, 2])

    # 7. unique counts partition the data
    lab = rng_v.integers(0, 5, size=2000)
    _, cnt = np.unique(lab, return_counts=True)
    assert cnt.sum() == lab.size and cnt.size == 5

    # 8. basic slices share memory; advanced indexing does not
    base8 = np.arange(8.0)
    v8 = base8[::2]
    assert np.shares_memory(base8, v8)
    f8 = base8[[0, 2, 4]]
    assert not np.shares_memory(base8, f8)

    # 9. np.ix_ with a single index behaves like fancy indexing
    M9 = rng_v.normal(size=(4, 4))
    assert np.array_equal(M9[np.ix_([0, 2])], M9[[0, 2]])

    print("[OK] NumPy 34: Advanced Indexing")


if __name__ == "__main__":
    _verify()
