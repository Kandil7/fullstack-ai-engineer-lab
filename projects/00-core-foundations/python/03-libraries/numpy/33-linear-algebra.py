"""NumPy 33: Linear Algebra — matmul, solve, decompositions, eigen, norms.

Why this matters for AI/backend engineering:
Matrix multiplication is the engine of every neural net and of
embedding similarity search; solve/lstsq power recommenders and
feature fitting; SVD is PCA and low-rank compression; condition
numbers tell you when your feature scales or your model weights
will blow up. This module builds the vocabulary — @ vs dot vs
solve vs inv — you will use daily in ML pipelines.

Docs: https://numpy.org/doc/stable/reference/routines.linalg.html
"""

import numpy as np

rng = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Example 1: @, np.matmul, and np.dot — shape rules
# ---------------------------------------------------------------------------
# (n,) @ (n,)  -> scalar       inner product
# (m,k) @ (k,n) -> (m,n)       matrix product
# np.dot flattens 2-D cases identically but differs on higher dims.

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])
print("Example 1: inner product:", a @ b)          # 32.0

A = np.arange(6.0).reshape(2, 3)
B = np.arange(12.0).reshape(3, 4)
print("Example 1: matmul shape:", (A @ B).shape)   # (2, 4)

# ---------------------------------------------------------------------------
# Example 2: batched matmul — many queries against one weight matrix
# ---------------------------------------------------------------------------
# np.matmul broadcasts leading dimensions: (batch, m, k) @ (k, n) -> (batch, m, n).

X = rng.normal(size=(5, 8, 4))      # 5 batches of (8, 4) inputs
W = rng.normal(size=(4, 3))         # shared weight (4, 3)
out = X @ W                         # (5, 8, 3)
print("Example 2: batched out shape:", out.shape)

# ---------------------------------------------------------------------------
# Example 3: cosine similarity as one matmul (embedding search)
# ---------------------------------------------------------------------------
# Normalize rows, then S = Xn @ Xn.T. S[i, j] is the cosine between rows i, j.
# This is how embedding lookups / RAG retrievers score candidates fast.

emb = rng.normal(size=(6, 8))                       # 6 documents, 8-dim embeddings
norms = np.linalg.norm(emb, axis=1, keepdims=True)
Xn = emb / norms
S = Xn @ Xn.T
print("Example 3: cosine diag (should be ~1):", np.round(np.diag(S), 6))
print("Example 3: symmetric:", np.allclose(S, S.T, atol=1e-12))

# ---------------------------------------------------------------------------
# Example 4: solve over inv — never invert to solve
# ---------------------------------------------------------------------------
# np.linalg.solve(A, b) uses LU factorization with partial pivoting:
# O(n^3) like inv, but far more stable. inv(A) @ b does the same work
# plus a full inverse — two solves, more rounding.

A4 = rng.normal(size=(5, 5))
x_true = rng.normal(size=5)
b4 = A4 @ x_true
x_solved = np.linalg.solve(A4, b4)
print("Example 4: solve recovers x:", np.allclose(x_solved, x_true, atol=1e-10))

# ---------------------------------------------------------------------------
# Example 5: least squares — fit a line through noisy points
# ---------------------------------------------------------------------------
# Design matrix with a column of ones; lstsq minimizes ||A x - y||_2.

t = np.linspace(0.0, 1.0, 20)
A5 = np.column_stack([np.ones_like(t), t])          # intercept + slope
y = 3.0 + 2.0 * t + rng.normal(scale=0.05, size=t.size)
(coef, *_rest) = np.linalg.lstsq(A5, y, rcond=None)
print("Example 5: fitted [intercept, slope]:", np.round(coef, 4))  # ~[3.0, 2.0]

# ---------------------------------------------------------------------------
# Example 6: QR decomposition — orthonormal basis
# ---------------------------------------------------------------------------
# A = Q R with Q.T Q = I and R upper triangular. QR is the stable workhorse
# behind solve and lstsq.

A6 = rng.normal(size=(6, 4))
Q, R = np.linalg.qr(A6)
print("Example 6: Q orthonormal:", np.allclose(Q.T @ Q, np.eye(4), atol=1e-12))
print("Example 6: Q R reconstructs A:", np.allclose(Q @ R, A6, atol=1e-12))

# ---------------------------------------------------------------------------
# Example 7: SVD — reconstruction and low-rank approximation
# ---------------------------------------------------------------------------
# A = U diag(s) Vh. Keeping the top k singular vectors gives the best
# rank-k approximation (Eckart-Young); error = sqrt(sum of s[k:]^2).

A7 = rng.normal(size=(6, 5))
U, s, Vh = np.linalg.svd(A7)
print("Example 7: U shape:", U.shape, "| Vh shape:", Vh.shape)  # (6,6) (5,5)
recon = (U[:, :s.size] * s) @ Vh      # U's extra columns pair with zero singular values
print("Example 7: SVD reconstructs A:", np.allclose(recon, A7, atol=1e-12))

k = 2
approx = U[:, :k] @ np.diag(s[:k]) @ Vh[:k, :]
pred_err = np.linalg.norm(A7 - approx)
true_err = np.sqrt(np.sum(s[k:] ** 2))
print("Example 7: rank-2 error == tail singular values:",
      np.allclose(pred_err, true_err, rtol=1e-6))

# ---------------------------------------------------------------------------
# Example 8: eigenvalues — symmetric matrices stay real
# ---------------------------------------------------------------------------
# eigh is specialized for symmetric/Hermitian: real eigenvalues, O(n^3),
# and guaranteed orthonormal eigenvectors.

A8 = rng.normal(size=(5, 5))
A_sym = A8 + A8.T                                    # symmetric by construction
w, V = np.linalg.eigh(A_sym)
resid = A_sym @ V - V @ np.diag(w)
print("Example 8: eigenvalues real:", np.isrealobj(w))
print("Example 8: A v == lambda v:", np.allclose(resid, 0.0, atol=1e-10))

# ---------------------------------------------------------------------------
# Example 9: norms — L1, L2, Frobenius, infinity
# ---------------------------------------------------------------------------
# np.linalg.norm default (no axis/ord) is the Frobenius norm for matrices:
# sqrt(sum of squared entries) — the root-mean magnitude of all elements.

x = np.array([3.0, -4.0])
print("Example 9: L2:", np.linalg.norm(x))          # 5.0
print("Example 9: L1:", np.linalg.norm(x, 1))       # 7.0
print("Example 9: Linf:", np.linalg.norm(x, np.inf))  # 4.0
M = np.array([[1.0, 2.0], [3.0, 4.0]])
print("Example 9: Frobenius:", np.linalg.norm(M))   # sqrt(30)
print("Example 9: Frobenius formula:",
      np.allclose(np.linalg.norm(M), np.sqrt(np.sum(M ** 2))))

# ---------------------------------------------------------------------------
# Example 10: condition number — how sensitive is your system?
# ---------------------------------------------------------------------------
# cond(A) = s_max / s_min. Hilbert matrices are famously ill-conditioned:
# tiny input perturbations become huge output errors.

def hilbert(n):
    """n x n Hilbert matrix: H[i, j] = 1 / (i + j + 1)."""
    i, j = np.indices((n, n))
    return 1.0 / (i + j + 1.0)


H6 = hilbert(6)
print("Example 10: cond(Hilbert 6):", f"{np.linalg.cond(H6):.2e}")  # ~1.5e7
b10 = np.ones(6)
x_pert = np.linalg.solve(H6, b10 + 1e-8 * rng.normal(size=6))
x_base = np.linalg.solve(H6, b10)
rel_err = np.linalg.norm(x_pert - x_base) / np.linalg.norm(x_base)
print("Example 10: relative error from 1e-8 perturbation:",
      f"{rel_err:.2e}")  # amplified to ~1e-1


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def _verify() -> None:
    # 1. solve recovers the exact right-hand side
    A = rng.normal(size=(5, 5))
    x_true = rng.normal(size=5)
    assert np.allclose(A @ np.linalg.solve(A, A @ x_true), A @ x_true, atol=1e-10)

    # 2. solve and inv agree on a well-conditioned problem
    A2 = rng.normal(size=(4, 4))
    b2 = rng.normal(size=4)
    assert np.allclose(np.linalg.solve(A2, b2),
                       np.linalg.inv(A2) @ b2, atol=1e-10)

    # 3. SVD reconstruction is exact
    M = rng.normal(size=(7, 4))
    U3, s3, Vh3 = np.linalg.svd(M)
    assert np.allclose((U3[:, :s3.size] * s3) @ Vh3, M, atol=1e-12)

    # 4. Eckart-Young: rank-k error equals the tail singular-value norm
    k = 3
    M3 = rng.normal(size=(8, 6))
    U4, s4, Vh4 = np.linalg.svd(M3)
    rank_k = U4[:, :k] @ np.diag(s4[:k]) @ Vh4[:k, :]
    assert np.allclose(np.linalg.norm(M3 - rank_k),
                       np.sqrt(np.sum(s4[k:] ** 2)), rtol=1e-6)

    # 5. QR gives an orthonormal Q and triangular R
    M5 = rng.normal(size=(6, 3))
    Q5, R5 = np.linalg.qr(M5)
    assert np.allclose(Q5.T @ Q5, np.eye(3), atol=1e-12)
    assert np.allclose(Q5 @ R5, M5, atol=1e-12)

    # 6. eigh eigenvectors satisfy A v = lambda v
    M6 = rng.normal(size=(5, 5))
    S6 = M6 + M6.T
    w6, V6 = np.linalg.eigh(S6)
    assert np.allclose(S6 @ V6, V6 @ np.diag(w6), atol=1e-10)

    # 7. norms obey their definitions
    v = np.array([3.0, -4.0])
    assert np.allclose(np.linalg.norm(v), 5.0)
    assert np.allclose(np.linalg.norm(v, 1), 7.0)
    assert np.allclose(np.linalg.norm(v, np.inf), 4.0)

    # 8. cosine similarity matrix from normalized rows is symmetric, diag ~ 1
    E = rng.normal(size=(10, 12))
    En = E / np.linalg.norm(E, axis=1, keepdims=True)
    C = En @ En.T
    assert np.allclose(C, C.T, atol=1e-12)
    assert np.allclose(np.diag(C), 1.0, atol=1e-6)

    # 9. condition number equals the singular value ratio
    M9 = rng.normal(size=(6, 6))
    s9 = np.linalg.svd(M9, compute_uv=False)
    assert np.allclose(np.linalg.cond(M9), s9[0] / s9[-1], rtol=1e-10)

    print("[OK] NumPy 33: Linear Algebra")


if __name__ == "__main__":
    _verify()
