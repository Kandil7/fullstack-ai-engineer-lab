# SciPy Lecture 08: Linear Algebra

## 🎯 Topic Overview

SciPy's `linalg` module extends NumPy's linear algebra with more advanced routines for matrix decompositions, solving complex systems, and specialized matrix operations.

## 📚 Learning Objectives

1. Solve linear systems with `solve()`
2. Perform matrix decompositions (LU, QR, SVD, Cholesky)
3. Compute eigenvalues and eigenvectors
4. Work with sparse matrices

---

## 1. Solving Linear Systems

```python
import numpy as np
from scipy import linalg

# Solve Ax = b
A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]])
b = np.array([1, -2, 0])

x = linalg.solve(A, b)
print(f"Solution: x = {x}")

# Verify
print(f"Verification: A·x = {A @ x}")
print(f"b = {b}")
```

---

## 2. Matrix Decompositions

```python
from scipy import linalg

# LU Decomposition
A = np.array([[2, 1, 1], [1, 3, 2], [1, 0, 4]])
P, L, U = linalg.lu(A)
print("LU Decomposition:")
print(f"L:\n{L}")
print(f"U:\n{U}")

# QR Decomposition
Q, R = linalg.qr(A)
print(f"QR: Q shape {Q.shape}, R shape {R.shape}")

# Singular Value Decomposition (SVD)
U, s, Vh = linalg.svd(A)
print(f"SVD singular values: {s}")

# Cholesky Decomposition (for positive definite)
A_pd = np.array([[4, 1], [1, 3]])
L = linalg.cholesky(A_pd, lower=True)
print(f"Cholesky L:\n{L}")
print(f"Verification: L·L^T:\n{L @ L.T}")
```

---

## 3. Eigenvalues and Eigenvectors

```python
A = np.array([[4, -2], [1, 1]])
eigenvalues, eigenvectors = linalg.eig(A)

print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")

# For symmetric matrices (real eigenvalues)
A_sym = np.array([[3, 1], [1, 2]])
eigvals, eigvecs = linalg.eigh(A_sym)
print(f"Real eigenvalues: {eigvals}")
```

---

## 4. Sparse Matrices

```python
from scipy.sparse import csr_matrix, eye, diags
from scipy.sparse.linalg import spsolve, eigsh

# Create sparse matrix
n = 1000
diagonals = [[1] * n, [-2] * n, [1] * n]  # 1D Laplacian
A_sparse = diags(diagonals, offsets=[-1, 0, 1], shape=(n, n))

# Solve sparse system
b = np.ones(n)
x = spsolve(A_sparse, b)
print(f"Sparse solution (first 5): {x[:5]}")

# Sparse eigenvalues
eigenvalues_sparse = eigsh(A_sparse, k=3, which='SM')[0]
print(f"Smallest 3 eigenvalues: {eigenvalues_sparse}")
```

---

## Summary

| Function | Purpose | Use Case |
|----------|---------|----------|
| `solve()` | Linear system Ax=b | Dense systems |
| `lu()` | LU decomposition | General matrices |
| `qr()` | QR decomposition | Least-squares |
| `svd()` | SVD | Dimensionality reduction |
| `eig()` / `eigh()` | Eigenvalues | Spectral analysis |
| `spsolve()` | Sparse system | Large sparse systems |
| `diags()` | Sparse diagonal | Structured matrices |
