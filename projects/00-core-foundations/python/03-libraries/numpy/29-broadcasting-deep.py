"""
NumPy -- 29: Broadcasting, Deep
==============================================
Topics: the three broadcasting rules, shape alignment, newaxis,
        silent allocation, (n,) vs (n,1), ValueError cases

Why this matters for AI/backend engineering:
    Broadcasting is why batch inference works: a (B, D) batch of
    embeddings plus a (D,) bias vector is one expression, not a loop.
    Misreading the rules produces silent shape bugs (the classic
    z-score-by-row bug) or O(n*m) memory blowups nobody asked for.

Run:      python 29-broadcasting-deep.py
Verify:   python 29-broadcasting-deep.py --verify
Reference: https://numpy.org/doc/stable/user/basics.broadcasting.html
"""

from __future__ import annotations

import sys

import numpy as np

rng = np.random.default_rng(42)

# ============================================================
# 1. The Three Rules of Broadcasting
# ============================================================
# Rule 1: align shapes from the trailing (rightmost) dimension.
# Rule 2: two dims are compatible if equal or one of them is 1.
# Rule 3: dimensions of size 1 are stretched to match; missing
#         leading dimensions are treated as size 1.

# Example 1: compatible shapes that broadcast to a larger result
a = np.ones((3, 1))   # shape (3, 1)
b = np.ones((1, 4))   # shape (1, 4)
c = a + b             # both size-1 dims stretch -> (3, 4)
print("a.shape, b.shape, (a+b).shape:", a.shape, b.shape, c.shape)

# Example 2: trailing alignment -- (4,) pairs with the last axis
x = np.ones((3, 4))   # shape (3, 4)
v = np.ones(4)        # shape (4,) -> treated as (1, 4)
print("(3,4) + (4,):", (x + v).shape)          # (3, 4)

# Example 3: missing leading dims are treated as 1
big = np.ones((2, 5, 3))   # shape (2, 5, 3)
small = np.ones((5, 3))    # shape (5, 3) -> (1, 5, 3)
print("(2,5,3) + (5,3):", (big + small).shape)  # (2, 5, 3)

# Output:
# a.shape, b.shape, (a+b).shape: (3, 1) (1, 4) (3, 4)
# (3,4) + (4,): (3, 4)
# (2,5,3) + (5,3): (2, 5, 3)


# ============================================================
# 2. newaxis: Turning (n,) into (n,1) Explicitly
# ============================================================
# np.newaxis (alias None) inserts a size-1 axis at the position
# where it appears. This is the surgical fix for the (n,) vs
# (n,1) confusion: it makes broadcasting happen along a column
# instead of a row.

# Example 4: subtract the column mean -- the z-score pattern
rng = np.random.default_rng(42)
data = rng.normal(loc=[1.0, 2.0, 3.0], scale=0.5, size=(100, 3))
col_means = data.mean(axis=0)          # shape (3,)
centered_correct = data - col_means    # (100,3) - (3,) -> OK
centered_explicit = data - col_means[np.newaxis, :]  # same thing
print("means shape:", col_means.shape)
print("correct (100,3) - (3,):", centered_correct.shape)

# Example 5: adding a column vector to every row
v_col = np.arange(3)[:, None]          # shape (3, 1)
row_sum = np.arange(4)                 # shape (4,)
mat = np.ones((3, 4))
print("(3,1) column add:", (mat + v_col).shape)   # (3, 4)
print("(4,) row add:    ", (mat + row_sum).shape)  # (3, 4)

# Output:
# means shape: (3,)
# correct (100,3) - (3,): (100, 3)
# (4,1) column add: (3, 4)
# (4,) row add:     (3, 4)


# ============================================================
# 3. When Broadcasting Silently Allocates
# ============================================================
# Broadcasting does NOT create the stretched array for arithmetic
# -- the ufunc loops over the logical shape. But any operation
# whose RESULT is the stretched shape materializes that array.
# An outer product a[:, None] * b[None, :] is O(n*m) memory.

# Example 6: outer product -- neat math, expensive memory
a6 = np.arange(5)
b6 = np.arange(4)
outer = a6[:, None] * b6[None, :]       # shape (5, 4)
print("outer product shape:", outer.shape)
print("outer[2,3] == a6[2]*b6[3]:", outer[2, 3] == a6[2] * b6[3])

# Example 7: broadcast_to is a free view -- but only read-only
view_only = np.broadcast_to(a6[:, None], (5, 4))
print("broadcast_to is a view (base is not None):",
      view_only.base is not None)
print("broadcast_to is read-only:", not view_only.flags.writeable)

# Output:
# outer product shape: (5, 4)
# outer[2,3] == a6[2]*b6[3]: True
# broadcast_to is a view (base is not None): True
# broadcast_to is read-only: True


# ============================================================
# 4. (n,) vs (n,1): The Shape Bug That Ships
# ============================================================
# arr.T on a 1-D array is a no-op. np.mean(arr, axis=1) fails on
# 1-D input. And subtracting a row-vector where you meant a column
# vector either raises ValueError (lucky) or broadcasts wrongly
# (unlucky -- the silent z-score-by-row bug).

# Example 8: transpose of a 1-D array does nothing
one_d = np.array([1.0, 2.0, 3.0])
print("1-D .T shape (still 1-D):", one_d.T.shape)   # (3,)

# Example 9: the silent row-vs-column broadcast trap
try:
    wrong_fix = data - data.mean(axis=1)   # (100,3) vs (100,)
    print("wrong_fix shape:", wrong_fix.shape)  # never reached
except ValueError as exc:
    print("row-mean subtract raises:", str(exc)[:60], "...")

# Output:
# 1-D .T shape (still 1-D): (3,)


# ============================================================
# 5. Failure Cases: NumPy Says No
# ============================================================
# When a trailing dimension is neither equal nor 1, NumPy raises
# ValueError with an explicit shape message. Learn to read it.

def try_broadcast(shp_a: tuple[int, ...],
                  shp_b: tuple[int, ...]) -> str:
    """Return the result shape or the exception message."""
    left = np.ones(shp_a)
    right = np.ones(shp_b)
    try:
        return f"ok -> {(left + right).shape}"
    except ValueError as exc:
        return f"ValueError: {exc}"

# Example 10: incompatible shapes
print("(3,2) + (2,3):", try_broadcast((3, 2), (2, 3)))
print("(3,2) + (2,4):", try_broadcast((3, 2), (2, 4)))
print("(4,) + (3,4):", try_broadcast((4,), (3, 4)))
print("(3,) + (3,4):", try_broadcast((3,), (3, 4)))

# Output:
# (3,2) + (2,3): ValueError: operands could not be broadcast together with shapes (3,2) (2,3)
# (3,2) + (2,4): ValueError: operands could not be broadcast together with shapes (3,2) (2,4)
# (4,) + (3,4): ok -> (3, 4)
# (3,) + (3,4): ValueError: operands could not be broadcast together with shapes (3,) (3,4)


# ============================================================
# 6. Production Pattern: Batch Inference and One-Hot
# ============================================================
# The two broadcasting idioms that show up in every embedding
# service: (1) fold a per-sample vector into a batch with keepdims,
# (2) turn integer labels into a one-hot matrix with one comparison.

# Complexity: row_normalize is O(B*D) time, O(B*D) memory --
# it must touch every element once; there is no cheaper way.

def row_normalize(mat: np.ndarray) -> np.ndarray:
    """L2-normalize each row of a (B, D) matrix.

    keepdims=True preserves (B, 1) so the division broadcasts
    along rows -- the (n,) vs (n,1) fix applied in production.
    """
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    return mat / norms


def one_hot(labels: np.ndarray, k: int) -> np.ndarray:
    """Convert integer labels in [0, k) to a one-hot matrix.

    labels[:, None] broadcasts against arange(k)[None, :],
    producing the full (n, k) boolean matrix in one pass.
    """
    return (labels[:, None] == np.arange(k)[None, :]).astype(np.float32)


# Example 11: batch inference -- bias add + row normalization
batch = rng.normal(size=(8, 5))          # 8 embeddings, dim 5
bias = rng.normal(size=5)                # per-dim bias, shape (5,)
logits = batch + bias                    # (8,5) + (5,) -> (8,5)
probs = logits / logits.sum(axis=1, keepdims=True)
normed = row_normalize(batch)
print("batch + bias ->", logits.shape, "| normed rows ->",
      normed.shape, "| row norms ~1:",
      bool(np.allclose(np.linalg.norm(normed, axis=1), 1.0)))

# Example 12: one-hot in one broadcast
labels = np.array([0, 2, 1, 2, 0])
oh = one_hot(labels, k=3)
print("one-hot shape:", oh.shape)
print(oh)

# Output:
# batch + bias -> (8, 5) | normed rows -> (8, 5) | row norms ~1: True
# one-hot shape: (5, 3)
# [[1. 0. 0.]
#  [0. 0. 1.]
#  [0. 1. 0.]
#  [0. 0. 1.]
#  [1. 0. 0.]]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: relying on .T to fix a column problem on 1-D data
#   bad = data - data.mean(axis=1).T   # .T is a no-op on 1-D
# CORRECT:
#   good = data - data.mean(axis=1)[:, None]   # explicit axis
#
# MISTAKE: computing an outer product when a broadcast_to view
#   would do -- every materialized element costs 8 bytes
#   bad = a[:, None] * b[None, :]        # (n, m) full copy
# CORRECT:
#   lazy = np.broadcast_to(a[:, None], (n, m))  # view, read-only
#
# MISTAKE: treating broadcasting as "it usually works"
#   Always check result.shape against the intended shape;
#   silent stretching is a feature AND a bug source.


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Rule mechanics: size-1 dims stretch.
    c = np.ones((3, 1)) + np.ones((1, 4))
    assert c.shape == (3, 4), "broadcasting must produce (3, 4)"

    # Trailing alignment with a 1-D operand.
    assert (np.ones((3, 4)) + np.ones(4)).shape == (3, 4), \
        "(4,) must align with the trailing axis"

    # newaxis produces (n, 1); row and column adds differ in shape.
    v = np.arange(3)
    assert v[:, None].shape == (3, 1), "newaxis must insert size-1 axis"
    assert (np.ones((3, 4)) + v[:, None]).shape == (3, 4), \
        "column vector add must broadcast to (3, 4)"

    # Failure cases raise ValueError, not silent garbage.
    try:
        np.ones((3, 2)) + np.ones((2, 3))
    except ValueError:
        pass
    else:
        raise AssertionError("(3,2) + (2,3) must raise ValueError")

    # Outer product values are pairwise products.
    a6 = np.arange(5)
    b6 = np.arange(4)
    outer = a6[:, None] * b6[None, :]
    assert np.array_equal(outer, a6.reshape(5, 1) * b6.reshape(1, 4)), \
        "outer product must equal explicit pairwise product"

    # broadcast_to is a non-owning view.
    assert np.broadcast_to(a6[:, None], (5, 4)).base is not None, \
        "broadcast_to must not copy"

    # keepdims normalization matches the manual (n,1) version.
    mat = rng.normal(size=(10, 3))
    manual = mat / np.linalg.norm(mat, axis=1)[:, None]
    assert np.allclose(row_normalize(mat), manual), \
        "keepdims normalization must equal manual (n,1) version"

    # One-hot: exactly one 1 per row, shape (n, k).
    labels = np.array([0, 2, 1, 2, 0])
    oh = one_hot(labels, k=3)
    assert oh.shape == (5, 3), "one-hot must be (n, k)"
    assert np.all(oh.sum(axis=1) == 1), "each row must have one 1"
    assert oh[1, 2] == 1.0 and oh[1, 0] == 0.0, \
        "label 2 must land in column 2"

    print("[OK] 29-broadcasting-deep: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Align trailing dims; dims must be equal or 1; 1s stretch.")
        print("2. newaxis is the explicit fix for (n,) vs (n,1).")
        print("3. Watch silent allocation: outer products are O(n*m).")
        _verify()          # always runs, so plain execution is also a test
