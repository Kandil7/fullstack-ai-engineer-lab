"""
NumPy -- 30: Vectorization
==============================================
Topics: loop -> vectorized rewrites (measured), np.where vs branches,
        masking, einsum, when a loop is unavoidable, np.vectorize
        is NOT fast

Why this matters for AI/backend engineering:
    Every embedding operation -- normalization, masking, distance,
    attention scores -- is a loop you must NOT write in Python. A
    Python-level loop over 1M embeddings is 10-100x slower than the
    same math vectorized, and it blocks the BLAS/GPU pipeline. This
    file teaches the rewrite patterns and the honest exceptions.

Run:      python 30-vectorization.py
Verify:   python 30-vectorization.py --verify
Reference: https://numpy.org/doc/stable/reference/generated/numpy.einsum.html
"""

from __future__ import annotations

import sys
import time

import numpy as np

rng = np.random.default_rng(42)


def timed(label: str, func) -> None:
    """Print wall time for a call -- informational, never asserted."""
    start = time.perf_counter()
    func()
    print(f"  {label:<28s} {time.perf_counter() - start:9.5f}s")


# ============================================================
# 1. Loop -> Vectorized: The Core Rewrite
# ============================================================
# A Python loop touches every element through the interpreter.
# A vectorized expression pushes the whole pass into compiled C.
# Complexity: both are O(n) work; the loop adds O(n) interpreter
# overhead -- that constant factor is the 10-100x.

# Example 1: elementwise transform, two spellings
def relu_loop(values: np.ndarray) -> np.ndarray:
    """ReLU via an explicit Python loop (slow reference)."""
    out = np.empty_like(values)
    for i in range(values.size):
        out[i] = values[i] if values[i] > 0 else 0.0
    return out


def relu_vec(values: np.ndarray) -> np.ndarray:
    """ReLU as one vectorized expression."""
    return np.maximum(values, 0.0)


x = rng.normal(size=1_000_000)
timed("relu_loop", lambda: relu_loop(x))
timed("relu_vec ", lambda: relu_vec(x))
print("loop == vectorized:",
      np.array_equal(relu_loop(x), relu_vec(x)))

# Output (times vary by machine -- the ORDER does not):
#   relu_loop                    0.09s
#   relu_vec                     0.00s
#   loop == vectorized: True


# ============================================================
# 2. np.where vs Branches: Vectorized If-Else
# ============================================================
# np.where(cond, a, b) selects elementwise without any Python
# branch. The scalar 'if' version cannot run on arrays at all.

# Example 2: clip with branches vs np.where vs np.clip
def clip_where(values: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Clip via np.where -- vectorized, reads as an if-else."""
    return np.where(values < lo, lo, np.where(values > hi, hi, values))


data = rng.normal(size=100_000)
print("clip_where == np.clip:",
      np.array_equal(clip_where(data, -1.0, 1.0),
                     np.clip(data, -1.0, 1.0)))

# Example 3: sign function via where
signed = np.where(data > 0, 1.0, np.where(data < 0, -1.0, 0.0))
print("sign via where == np.sign:",
      np.array_equal(signed, np.sign(data)))

# Output:
# clip_where == np.clip: True
# sign via where == np.sign: True


# ============================================================
# 3. Masking: Selecting and Updating Subsets
# ============================================================
# A boolean mask selects positions; combined with fancy indexing
# it replaces filter-then-update loops. Complexity: O(n) per mask
# operation; each pass is compiled.

# Example 4: zero out negative values -- the masking idiom
scores = rng.normal(size=1_000_000)
mask = scores < 0
scores[mask] = 0.0                      # vectorized scatter
print("masked update:", bool((scores >= 0).all()))

# Example 5: masked reductions -- counts and conditional sums
vals = rng.normal(size=1_000_000)
print("count > 0:", int((vals > 0).sum()))
print("sum of positives:", round(float(vals[vals > 0].sum()), 3))
print("same via where:", np.allclose(vals[vals > 0].sum(),
                                     np.where(vals > 0, vals, 0.0).sum()))

# Output:
# masked update: True
# count > 0: 500236
# sum of positives: 399172.853
# same via where: True


# ============================================================
# 4. einsum: Explicit Einstein Notation
# ============================================================
# einsum names each axis and the output axis layout, so the same
# string notation expresses dot, outer, trace, transpose, and
# batch products. Slower than dedicated BLAS calls at large size,
# but unbeatable for clarity and for fused small ops.

# Example 6: the five classic einsums
A = rng.normal(size=(4, 5))
B = rng.normal(size=(5, 6))
print("matmul einsum == @:",
      np.allclose(np.einsum("ij,jk->ik", A, B), A @ B))
print("trace einsum:", np.einsum("ii->", np.ones((5, 5))) == 5.0)
print("outer einsum shape:",
      np.einsum("i,j->ij", np.ones(3), np.ones(4)).shape)
print("transpose einsum == .T:",
      np.array_equal(np.einsum("ij->ji", A), A.T))

# Example 7: batch matmul with einsum vs @
batches = rng.normal(size=(8, 4, 5))
print("batch einsum == @:",
      np.allclose(np.einsum("bij,jk->bik", batches, B),
                  batches @ B))

# Output:
# matmul einsum == @: True
# trace einsum: True
# outer einsum shape: (3, 4)
# transpose einsum == .T: True
# batch einsum == @: True


# ============================================================
# 5. When a Loop Is Unavoidable -- and How to Shrink It
# ============================================================
# Ragged data (variable-length rows) cannot be a dense 2-D array,
# and per-row control flow that depends on row content cannot be
# vectorized directly. The honest pattern: loop over the SMALL
# outer axis, vectorize the inner work. Complexity: O(rows) loop
# iterations, each O(row work) compiled -- far better than a
# doubly-nested Python loop.

# Example 8: ragged rows -- loop outer, vectorize inner
def row_stats_ragged(rows: list[np.ndarray]) -> np.ndarray:
    """Per-row mean and std for ragged data.

    The loop is unavoidable (rows differ in length); each body is
    fully vectorized, so the Python overhead is O(#rows), not
    O(#elements).
    """
    return np.array([(r.mean(), r.std()) for r in rows])


ragged = [rng.normal(size=n) for n in (3, 7, 2, 5)]
print("ragged stats shape:", row_stats_ragged(ragged).shape)  # (4, 2)

# Output:
# ragged stats shape: (4, 2)


# ============================================================
# 6. np.vectorize Is NOT Fast
# ============================================================
# np.vectorize wraps a Python function and calls it once per
# element -- it is a for loop in disguise, usually SLOWER than
# the explicit loop. It exists for API convenience (matching the
# ufunc call signature), not for speed.

# Example 9: np.vectorize vs the explicit loop vs vectorized
def f(x: float) -> float:
    """A scalar piecewise function."""
    return x * 2 if x > 0 else -x


f_vec = np.vectorize(f)
small = rng.normal(size=200_000)

timed("np.vectorize", lambda: f_vec(small))
timed("explicit loop", lambda: np.fromiter((f(v) for v in small),
                                           dtype=float))
timed("vectorized   ", lambda: np.where(small > 0, small * 2, -small))
print("all three agree:",
      bool(np.allclose(f_vec(small),
                       np.where(small > 0, small * 2, -small))))

# Output (times vary -- np.vectorize is NEVER fastest):
#   np.vectorize                  0.19s
#   explicit loop                 0.15s
#   vectorized                    0.00s
#   all three agree: True


# ============================================================
# 7. Production Pattern: Batch Embedding Math
# ============================================================
# Everything above composes into one line of batch math. Here:
# masked mean-pooling of embeddings (used for sentence embeddings
# when tokens are padded).

# Complexity: all ops are O(B * T * D); no Python loop over the
# batch. Memory: one (B, T, D) batch plus (B, D) output.

def mean_pool(embeddings: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Mean-pool embeddings over the token axis, ignoring padding.

    embeddings: (B, T, D) float
    mask:       (B, T) bool -- True for real tokens
    Returns:    (B, D) pooled vectors
    """
    masked = np.where(mask[:, :, None], embeddings, 0.0)
    sums = masked.sum(axis=1)
    counts = mask.sum(axis=1, keepdims=True).astype(np.float64)
    return sums / np.maximum(counts, 1.0)


emb = rng.normal(size=(16, 32, 64))           # 16 sentences x 32 tokens
tok_mask = rng.integers(0, 2, size=(16, 32), dtype=bool)
pooled = mean_pool(emb, tok_mask)
print("pooled shape:", pooled.shape)          # (16, 64)

# Sanity: pooling a single padded row equals mean of its tokens.
row = emb[0]
m = tok_mask[0]
manual = row[m].mean(axis=0)
print("matches manual mean:",
      np.allclose(pooled[0], manual))

# Output:
# pooled shape: (16, 64)
# matches manual mean: True


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: reaching for np.vectorize to "speed up" a function
#   bad = np.vectorize(slow_python_fn)   # still one call per item
# CORRECT: rewrite the math with ufuncs / np.where
#   good = np.where(cond, a, b)
#
# MISTAKE: filtering twice instead of one mask
#   bad = vals[vals > 0][vals[vals > 0] < 10]   # 3 passes, re-index
# CORRECT:
#   good = vals[(vals > 0) & (vals < 10)]        # 1 pass, one mask
#
# MISTAKE: looping over the big axis
#   Always loop over the SMALL axis and vectorize the inner work;
#   Python overhead scales with the loop count, not element count.


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Loop and vectorized rewrites must agree exactly.
    rng = np.random.default_rng(42)
    x = rng.normal(size=10_000)
    assert np.array_equal(relu_loop(x), relu_vec(x)), \
        "loop and vectorized ReLU must agree"

    # np.where equivalence with branches for scalar logic.
    assert np.allclose(clip_where(x, -1.0, 1.0), np.clip(x, -1.0, 1.0)), \
        "np.where clip must match np.clip"

    # Masking: update and reduction agree with np.where.
    vals = rng.normal(size=10_000)
    mask = vals > 0
    assert np.allclose(vals[mask].sum(), np.where(vals > 0, vals, 0).sum()), \
        "masked sum must match where-sum"

    # einsum correctness against @, .T, and batch matmul.
    A = rng.normal(size=(4, 5))
    B = rng.normal(size=(5, 6))
    assert np.allclose(np.einsum("ij,jk->ik", A, B), A @ B), \
        "einsum matmul must equal @"
    assert np.array_equal(np.einsum("ij->ji", A), A.T), \
        "einsum transpose must equal .T"
    batch = rng.normal(size=(8, 4, 5))
    assert np.allclose(np.einsum("bij,jk->bik", batch, B), batch @ B), \
        "einsum batch matmul must equal batched @"

    # np.vectorize agrees with the vectorized rewrite (values only;
    # speed is printed, never asserted -- wall clock is not CI-safe).
    assert np.allclose(f_vec(x), np.where(x > 0, x * 2, -x)), \
        "np.vectorize must agree numerically with the ufunc version"

    # Mean-pooling matches a manual token-mean.
    emb = rng.normal(size=(16, 32, 64))
    tok_mask = rng.integers(0, 2, size=(16, 32), dtype=bool)
    pooled = mean_pool(emb, tok_mask)
    assert pooled.shape == (16, 64), "pooled shape must be (B, D)"
    assert np.allclose(pooled[0], emb[0][tok_mask[0]].mean(axis=0)), \
        "pooling must equal manual masked mean"

    print("[OK] 30-vectorization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Rewrite loops as ufuncs / np.where / masks.")
        print("2. einsum names axes explicitly; check with @ and .T.")
        print("3. np.vectorize is a loop in disguise -- never for speed.")
        _verify()          # always runs, so plain execution is also a test
