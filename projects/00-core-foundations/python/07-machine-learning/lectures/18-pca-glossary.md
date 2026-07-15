# Glossary: Principal Component Analysis (Lecture 18)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| PCA | Reduces dimensions while preserving variance | `PCA(n_components=2)` |
| Principal Component | New orthogonal axis capturing variance | PC1, PC2, ... |
| Explained Variance | Proportion of variance captured by component | 0.73 (73%) |
| Eigenvalue | Variance explained by each component | `pca.explained_variance_` |
| Eigenvector | Direction of principal component | `pca.components_` |
| Dimensionality Reduction | Reducing number of features | 100D → 2D |
| Loadings | Contribution of each feature to component | `pca.components_` |
| Projection | Transform data to new coordinate system | `pca.transform(X)` |
| Reconstruction | Approximate original data from reduced | `pca.inverse_transform()` |
| Scree Plot | Plot of eigenvalues vs component number | Elbow method |
| Cumulative Variance | Running sum of explained variance | Choose components |
| Whitening | Normalizing components to unit variance | `whiten=True` |
| SVD | Singular Value Decomposition (PCA method) | Underlying math |
| Covariance Matrix | Matrix of feature covariances | PCA input |
| Transformed Data | Data in new coordinate system | `X_pca` |

---

## Detailed Term Definitions

### Principal Component Analysis (PCA)

**Definition:** A statistical technique that transforms high-dimensional data into a lower-dimensional space by finding orthogonal axes (principal components) that maximize variance.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Reduce from 4 to 2 dimensions
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"Original shape: {X_scaled.shape}")
print(f"PCA shape: {X_pca.shape}")
print(f"Variance explained: {pca.explained_variance_ratio_.sum():.2%}")
```

**Related Terms:** Dimensionality Reduction, Principal Components, Eigenvalues

---

### Principal Component

**Definition:** A new axis (direction) in the feature space that captures maximum variance. Components are ordered by importance and are orthogonal to each other.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA(n_components=2)
pca.fit(X_scaled)

print("Principal Components:")
for i, component in enumerate(pca.components_):
    print(f"  PC{i+1}: {component}")

print(f"\nExplained variance: {pca.explained_variance_ratio_}")
```

**Related Terms:** Eigenvector, Loadings, Orthogonal

---

### Explained Variance

**Definition:** The proportion of total variance in the data that is captured by each principal component.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_wine
import numpy as np

wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)

pca = PCA()
pca.fit(X_scaled)

# Individual explained variance
print("Explained variance by component:")
for i, var in enumerate(pca.explained_variance_ratio_):
    print(f"  PC{i+1}: {var:.4f} ({var:.1%})")

# Cumulative explained variance
cumvar = np.cumsum(pca.explained_variance_ratio_)
print(f"\nCumulative variance: {cumvar}")

# Components for 95% variance
n_95 = np.argmax(cumvar >= 0.95) + 1
print(f"Components for 95% variance: {n_95}")
```

**Related Terms:** Eigenvalue, Cumulative Variance, Scree Plot

---

### Eigenvalue

**Definition:** The variance explained by each principal component. Higher eigenvalue = more important component.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA()
pca.fit(X_scaled)

print("Eigenvalues (explained variance):")
for i, eigenval in enumerate(pca.explained_variance_):
    print(f"  λ{i+1} = {eigenval:.4f}")

# Eigenvalue ratio
print(f"\nRatio: λ1/λ2 = {pca.explained_variance_[0]/pca.explained_variance_[1]:.2f}")
```

**Related Terms:** Explained Variance, Eigenvector, Variance Ratio

---

### Eigenvector

**Definition:** The direction of a principal component. Shows how each original feature contributes to the component.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA(n_components=2)
pca.fit(X_scaled)

print("Eigenvectors (component loadings):")
print(f"Feature names: {iris.feature_names}")
print(f"\nPC1: {pca.components_[0]}")
print(f"PC2: {pca.components_[1]}")

# Interpretation
print("\nInterpretation:")
print("PC1 loads heavily on petal features")
print("PC2 loads on sepal width")
```

**Related Terms:** Principal Component, Loadings, Orthogonal

---

### Dimensionality Reduction

**Definition:** The process of reducing the number of features while preserving important information. PCA is a common method.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import time

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Original (64 features)
start = time.time()
model_orig = LogisticRegression(max_iter=1000, random_state=42)
model_orig.fit(X_train_scaled, y_train)
time_orig = time.time() - start
acc_orig = accuracy_score(y_test, model_orig.predict(X_test_scaled))

# Reduced (32 features)
pca = PCA(n_components=32)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

start = time.time()
model_pca = LogisticRegression(max_iter=1000, random_state=42)
model_pca.fit(X_train_pca, y_train)
time_pca = time.time() - start
acc_pca = accuracy_score(y_test, model_pca.predict(X_test_pca))

print(f"Original: {X_train.shape[1]} features, Acc={acc_orig:.4f}, Time={time_orig:.4f}s")
print(f"Reduced:  {X_train_pca.shape[1]} features, Acc={acc_pca:.4f}, Time={time_pca:.4f}s")
```

**Related Terms:** PCA, Feature Selection, Compression

---

### Loadings

**Definition:** The coefficients that show how each original feature contributes to each principal component. Equal to eigenvectors.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA(n_components=2)
pca.fit(X_scaled)

# Create loadings DataFrame
loadings = pd.DataFrame(
    pca.components_.T,
    columns=['PC1', 'PC2'],
    index=iris.feature_names
)

print("Loadings:")
print(loadings.round(3))

# Visualize
import matplotlib.pyplot as plt
loadings.plot(kind='bar', figsize=(8, 4))
plt.title('PCA Loadings')
plt.ylabel('Loading')
plt.tight_layout()
plt.savefig('pca_loadings.png', dpi=100)
plt.show()
```

**Related Terms:** Eigenvector, Principal Component, Feature Importance

---

### Projection

**Definition:** The transformation of data points from the original coordinate system to the new coordinate system defined by principal components.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Project new point
new_point = np.array([[5.1, 3.5, 1.4, 0.2]])  # Original space
new_point_scaled = StandardScaler().fit_transform(iris.data).mean(axis=0) + new_point
new_projected = pca.transform(new_point_scaled)

print(f"Original point shape: {new_point.shape}")
print(f"Projected point shape: {new_projected.shape}")
print(f"Projected coordinates: {new_projected}")
```

**Related Terms:** Transform, Coordinate System, PCA

---

### Reconstruction

**Definition:** Approximating the original data from the reduced representation using `inverse_transform`.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Reduce to 2 dimensions
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)

# Reconstruct to original dimensions
X_reconstructed = pca.inverse_transform(X_reduced)

# Calculate reconstruction error
mse = np.mean((X_scaled - X_reconstructed) ** 2)
print(f"Original shape: {X_scaled.shape}")
print(f"Reconstructed shape: {X_reconstructed.shape}")
print(f"Reconstruction MSE: {mse:.4f}")

# Note: Some information is lost
# More components = less loss
```

**Related Terms:** Inverse Transform, Compression, Reconstruction Error

---

### Scree Plot

**Definition:** A plot of eigenvalues (or explained variance) vs component number, used to determine optimal number of components.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_wine
import matplotlib.pyplot as plt
import numpy as np

wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)

pca = PCA()
pca.fit(X_scaled)

# Create scree plot
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.bar(range(1, len(pca.explained_variance_) + 1),
        pca.explained_variance_, alpha=0.6)
plt.xlabel('Component')
plt.ylabel('Eigenvalue')
plt.title('Scree Plot')

plt.subplot(1, 2, 2)
cumvar = np.cumsum(pca.explained_variance_ratio_)
plt.plot(range(1, len(cumvar) + 1), cumvar, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--', label='95%')
plt.xlabel('Component')
plt.ylabel('Cumulative Variance')
plt.title('Cumulative Variance')
plt.legend()

plt.tight_layout()
plt.savefig('scree_plot.png', dpi=100)
plt.show()
```

**Related Terms:** Eigenvalue, Explained Variance, Elbow Method

---

### Cumulative Variance

**Definition:** The running total of explained variance across components, used to determine how many components to keep.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA()
pca.fit(X_scaled)

cumvar = np.cumsum(pca.explained_variance_ratio_)

print("Cumulative variance:")
for i, var in enumerate(cumvar):
    print(f"  {i+1} components: {var:.2%}")

# Find components for target variance
for target in [0.90, 0.95, 0.99]:
    n = np.argmax(cumvar >= target) + 1
    print(f"\nFor {target:.0%} variance: {n} components needed")
```

**Related Terms:** Explained Variance, Scree Plot, Component Selection

---

### Whitening

**Definition:** A preprocessing step that normalizes principal components to have unit variance. Useful for algorithms that assume isotropic noise.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Without whitening
pca = PCA(n_components=2, whiten=False)
X_pca = pca.fit_transform(X_scaled)
print(f"Without whitening - Std: {X_pca.std(axis=0)}")

# With whitening
pca_whiten = PCA(n_components=2, whiten=True)
X_pca_whiten = pca_whiten.fit_transform(X_scaled)
print(f"With whitening - Std: {X_pca_whiten.std(axis=0)}")
# With whitening, all components have unit variance
```

**Related Terms:** PCA, Standardization, Isotropic Noise

---

### SVD (Singular Value Decomposition)

**Definition:** The mathematical method underlying PCA. Decomposes the data matrix into U, Σ, and Vᵀ matrices.

**Example:**
```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Manual SVD
U, S, Vt = np.linalg.svd(X_scaled, full_matrices=False)

# Compare with PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Manual projection
X_manual = X_scaled @ Vt[:2].T

print("SVD components match PCA components:")
print(f"  Match: {np.allclose(pca.components_, Vt[:2])}")

print(f"\nSingular values: {S}")
print(f"Explained variance: {pca.explained_variance_ratio_}")
```

**Related Terms:** PCA, Eigendecomposition, Linear Algebra

---

### Covariance Matrix

**Definition:** A matrix showing how features vary together. PCA diagonalizes this matrix to find principal components.

**Example:**
```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Calculate covariance matrix
cov_matrix = np.cov(X_scaled.T)
print("Covariance Matrix:")
print(cov_matrix.round(3))

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
print(f"\nEigenvalues: {eigenvalues}")
print(f"Explained variance: {eigenvalues / eigenvalues.sum()}")
```

**Related Terms:** Eigenvalue, Eigenvector, Correlation Matrix

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Explained Variance Ratio | λᵢ / Σλⱼ |
| PCA Projection | X_pca = X @ W (where W is eigenvector matrix) |
| Reconstruction | X_approx = X_pca @ Wᵀ + mean |
| Covariance Matrix | C = (1/n) XᵀX |
| Eigenvalue Equation | Cv = λv |

---

## Code Snippets Quick Reference

```python
# Basic PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Choose components by variance
pca = PCA()
pca.fit(X_scaled)
cumvar = np.cumsum(pca.explained_variance_ratio_)
n_components = np.argmax(cumvar >= 0.95) + 1

# Explained variance
print(pca.explained_variance_ratio_)
print(pca.explained_variance_)

# Components (loadings)
print(pca.components_)

# Transform and inverse transform
X_reduced = pca.transform(X_scaled)
X_reconstructed = pca.inverse_transform(X_reduced)

# With whitening
pca = PCA(n_components=2, whiten=True)

# In pipeline
from sklearn.pipeline import Pipeline
pipe = Pipeline([('scaler', StandardScaler()), ('pca', PCA(n_components=2))])
```

---

## Common Pitfalls

1. **Not scaling** — PCA is variance-based, scale matters
2. **Too few components** — Loses important information
3. **Too many components** — Doesn't reduce dimensions
4. **Losing interpretability** — PCs are combinations of features
5. **Using on uncorrelated features** — PCA won't help

---

## Further Reading

- [Scikit-learn - PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca)
- [Wikipedia - PCA](https://en.wikipedia.org/wiki/Principal_component_analysis)
- [StatQuest - PCA](https://www.youtube.com/watch?v=FgakZw6K1QQ)
