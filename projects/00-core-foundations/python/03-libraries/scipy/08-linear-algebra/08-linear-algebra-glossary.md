# SciPy Lecture 08: Linear Algebra — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| LU Decomposition | A = PLU | `linalg.lu(A)` |
| QR Decomposition | A = QR | `linalg.qr(A)` |
| SVD | A = UΣV^T | `linalg.svd(A)` |
| Cholesky | A = LL^T | `linalg.cholesky(A)` |
| Eigenvalue | λ where Av = λv | `linalg.eig(A)` |
| Eigenvector | v in Av = λv | `linalg.eig(A)` |
| Sparse Matrix | Mostly zero entries | `csr_matrix(A)` |
| `spsolve()` | Solve sparse system | `spsolve(A, b)` |
| `eigsh()` | Sparse eigenvalues | `eigsh(A, k=3)` |
| Condition Number | Matrix sensitivity | `linalg.cond(A)` |
| Norm | Matrix/vector magnitude | `linalg.norm(A)` |

### NumPy vs SciPy Linear Algebra

| Operation | NumPy | SciPy | When SciPy Better |
|-----------|-------|-------|-------------------|
| Solve | `np.linalg.solve()` | `linalg.solve()` | More methods, sparse |
| SVD | `np.linalg.svd()` | `linalg.svd()` | SciPy has sparse SVD |
| LU | ✗ | `linalg.lu()` | SciPy only |
| Sparse | ✗ | `scipy.sparse` | SciPy only |
