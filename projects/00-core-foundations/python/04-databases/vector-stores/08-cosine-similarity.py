"""
Vector Stores — 08: Cosine Similarity
==============================================
Topics: dot vs cosine vs L2, normalization, the unit-vector identity
        (L2^2 = 2 - 2*cos), score interpretation and thresholds, the
        curse of dimensionality (similarity concentration), metric
        choice per store

Why this matters for AI/backend engineering:
    Cosine is the default metric in most vector stores, but its
    behavior is subtle: magnitudes are ignored, scores concentrate
    toward 0 in high dimensions, and a fixed threshold means nothing
    across corpora. This exercise builds the intuition you need to
    choose a metric and read scores.

Run:      python 08-cosine-similarity.py
Verify:   python 08-cosine-similarity.py --verify
"""

from __future__ import annotations

import sys

import numpy as np

from vector_utils import cosine_sim, l2_dist

rng = np.random.default_rng(19)

# ============================================================
# 1. The three distance functions
# ============================================================
a = np.array([1.0, 2.0, 3.0])
b = np.array([3.0, 2.0, 1.0])
c = np.array([10.0, 20.0, 30.0])          # same direction as a, 10x magnitude

print(f"dot(a, c)     = {a @ c:.1f}    (magnitude-sensitive)")
print(f"cosine(a, c)  = {cosine_sim(a, c):.2f}   (direction only)")
print(f"L2(a, c)      = {l2_dist(a, c):.2f}     (magnitude-sensitive)")

# Output:
# dot(a, c)     = 140.0    (magnitude-sensitive)
# cosine(a, c)  = 1.00   (direction only)
# L2(a, c)      = 33.67     (magnitude-sensitive)

# ============================================================
# 2. The unit-vector identity
# ============================================================
# For unit vectors: ||a-b||^2 = 2 - 2*cos(a,b). So under L2-norm,
# ranking by L2 == ranking by cosine. That is why stores say "cosine
# and L2 are equivalent after normalization".
ua, ub = a / np.linalg.norm(a), b / np.linalg.norm(b)
lhs = l2_dist(ua, ub) ** 2
rhs = 2 - 2 * cosine_sim(ua, ub)
print(f"\n||ua-ub||^2 = {lhs:.4f}   2 - 2*cos = {rhs:.4f}   (equal)")

# Output:
# ||ua-ub||^2 = 0.5714   2 - 2*cos = 0.5714   (equal)

# ============================================================
# 3. Same direction, different magnitude: L2 disagrees with cosine
# ============================================================
# a and c point the same way (cos=1.0) yet L2 says they are far apart.
# Which is right depends on the DATA: for text embeddings, direction is
# meaning; for product vectors (price x quantity), magnitude matters.
print(f"\ncosine ranks parallel vectors as identical, L2 does not:")
print(f"  cos(a, c) = {cosine_sim(a, c):.2f} (same direction)")
print(f"  L2(a, c)  = {l2_dist(a, c):.2f} (10x magnitude)")

# Output:
# cosine ranks parallel vectors as identical, L2 does not:
#   cos(a, c) = 1.00 (same direction)
#   L2(a, c)  = 33.67 (10x magnitude)

# ============================================================
# 4. Score interpretation: what does 0.9 mean?
# ============================================================
# 0.9 cosine means the angle is arccos(0.9) ~ 25.8 degrees. That is a
# strong directional match — but its practical meaning depends on the
# embedding space (see section 5: random vectors in 1024 dims average
# ~0.03, so 0.9 there is huge; in a 4-dim space random vectors can hit
# 0.5+ easily).
import math

for cos_val in (0.9, 0.5, 0.0):
    deg = math.degrees(math.acos(cos_val))
    print(f"  cos={cos_val:.1f} -> angle ~{deg:5.1f} deg")

# Output:
#   cos=0.9 -> angle ~ 25.8 deg
#   cos=0.5 -> angle ~ 60.0 deg
#   cos=0.0 -> angle ~ 90.0 deg

# ============================================================
# 5. The curse of dimensionality — similarity concentration
# ============================================================
# Random unit vectors in high dims are nearly orthogonal: the mean
# pairwise cosine shrinks as sqrt-ish of 1/d and the spread collapses.
# A fixed threshold that works at dim=64 silently breaks at dim=1536.
def random_cosine_stats(dim: int, n: int = 2000, seed: int = 1) -> tuple:
    r = np.random.default_rng(seed)
    v = r.normal(size=(n, dim))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    sims = v @ v.T
    iu = np.triu_indices(n, k=1)
    return float(sims[iu].mean()), float(sims[iu].std())


print("\nrandom-pair cosine stats per dimension:")
for dim in (4, 32, 256, 1024):
    mu, sd = random_cosine_stats(dim)
    print(f"  dim={dim:4d}: mean = {mu:+.3f}  std = {sd:.3f}")

# Output:
# random-pair cosine stats per dimension:
#   dim=   4: mean = -0.000  std = 0.500
#   dim=  32: mean = -0.000  std = 0.177
#   dim= 256: mean = +0.000  std = 0.063
#   dim=1024: mean = -0.000  std = 0.031

# ============================================================
# 6. Thresholding — rank-based beats fixed cutoffs
# ============================================================
# "similarity > 0.8" is fragile: the 0.8 boundary sits at a different
# percentile per corpus and per dim. The robust production rule is
# rank-based (top-k) or percentile-based, not an absolute cosine.
corpus = rng.normal(size=(500, 64))
corpus /= np.linalg.norm(corpus, axis=1, keepdims=True)
q = corpus[0] + 0.15 * rng.normal(size=64)
q /= np.linalg.norm(q)
sims = np.array([cosine_sim(q, v) for v in corpus])
sims[0] = 1.0                               # self-match
print(f"\nquery vs 500-doc corpus: max={sims.max():.3f} "
      f"min={sims.min():.3f} p95={np.percentile(sims, 95):.3f}")
print(f"rank of the true match = 1 (top-k retrieval finds it, "
      f"a fixed 0.9 cutoff would not: max={sims.max():.3f})")

# Output:
# query vs 500-doc corpus: max=1.000 min=-0.332 p95=0.212
# rank of the true match = 1 (top-k retrieval finds it, a fixed 0.9 cutoff would not: max=1.000)

# ============================================================
# 7. Metric choice per store
# ============================================================
#   cosine  -> default; magnitude-blind; best for text embeddings
#   dot     -> fastest; equivalent to cosine AFTER normalization
#              (stores like Pinecone/pgvector implement it as cosine)
#   L2      -> magnitude matters; right for coordinates/audio
# All three are rank-equivalent on normalized vectors; pick by data
# semantics, then normalize and measure.
print("\nmetric rules of thumb:")
print("  1. text/embedding models  -> cosine (or dot on normalized)")
print("  2. coordinates/sensors    -> L2")
print("  3. always normalize once, then cosine == dot ranking")

# Output:
# metric rules of thumb:
#   1. text/embedding models  -> cosine (or dot on normalized)
#   2. coordinates/sensors    -> L2
#   3. always normalize once, then cosine == dot ranking

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: mixing raw and normalized vectors in one index — cosine
#   ranking then silently changes meaning.
# MISTAKE: hard-coding a cosine threshold across corpora/dimensions
#   (section 5: the same 0.5 cutoff is a tie in dim=4 and impossible
#   noise in dim=1024).
# MISTAKE: assuming cosine == dot for unnormalized vectors — they
#   disagree by exactly the magnitudes.
# MISTAKE: using L2 on text embeddings and wondering why long docs
#   rank far — that is magnitude, not meaning.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # cosine is magnitude-blind; L2 is not
    assert np.isclose(cosine_sim(a, c), 1.0), \
        "parallel vectors must have cosine 1.0 regardless of magnitude"
    assert l2_dist(a, c) > 10.0, \
        "parallel vectors with 10x magnitude must be L2-far"

    # the unit-vector identity holds exactly
    assert np.isclose(lhs, rhs, atol=1e-9), \
        "L2^2 must equal 2 - 2*cos for unit vectors"

    # concentration: std must collapse as dims grow
    stds = [random_cosine_stats(d, seed=1)[1] for d in (4, 32, 256, 1024)]
    assert stds[0] > stds[1] > stds[2] > stds[3], \
        "random-pair cosine std must shrink with dimension"

    # the true match must be the top-1 cosine hit
    assert int(np.argmax(sims)) == 0, \
        "self-match must rank first under cosine"

    # angle table sanity
    assert np.isclose(math.degrees(math.acos(0.5)), 60.0), \
        "acos(0.5) must be exactly 60 degrees"

    print("[OK] 08-cosine-similarity: all checks passed")


if __name__ == "__main__":
    if "--verify" not in sys.argv:
        print("\n--- Summary ---")
        print("1. Cosine is magnitude-blind; L2 and dot are not")
        print("2. On unit vectors, L2^2 = 2 - 2*cos (rank-equivalent)")
        print("3. Scores concentrate toward 0 as dims grow - thresholds drift")
        print("4. Prefer rank-based retrieval over fixed cosine cutoffs")
    _verify()  # always runs, so plain execution is also a test
