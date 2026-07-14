# Lecture 18: Principal Component Analysis (PCA)

## Topic Overview

Principal Component Analysis (PCA) is a dimensionality reduction technique that transforms high-dimensional data into a lower-dimensional space while preserving as much variance as possible. This lecture covers the mathematics behind PCA, practical implementation, choosing the number of components, and applications like visualization, speed improvement, and noise reduction.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what PCA does and why it's useful
2. Implement PCA with scikit-learn
3. Choose the number of components using explained variance
4. Use PCA for visualization of high-dimensional data
5. Apply PCA to speed up model training
6. Use PCA for noise reduction
7. Build complete pipelines with PCA

---

## Key Concepts

### 1. What is PCA?

PCA finds new axes (principal components) that capture the maximum variance in the data. Each component is a linear combination of original features.

**Key Properties:**
- Components are orthogonal (uncorrelated)
- First component captures most variance
- Second captures second most, etc.
- Components are ordered by importance

### 2. Explained Variance

The proportion of total variance captured by each component:

```
Explained Variance Ratio = λᵢ / Σλⱼ
```

Where:
- `λᵢ` = eigenvalue of component i
- `Σλⱼ` = sum of all eigenvalues

### 3. Dimensionality Reduction

- Reduce from n features to k components (k < n)
- Preserve maximum variance with fewer dimensions
- Trade-off: less interpretability for speed/visualization

### 4. When to Use PCA

| Use Case | Example |
|----------|---------|
| Visualization | Plot 100D data in 2D |
| Speed | Reduce features for faster training |
| Noise Reduction | Remove low-variance noise |
| Preprocessing | Before clustering or classification |

---

## Code Examples

### Example 1: Basic PCA

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# Load Iris dataset (4 features)
iris = load_iris()
X = iris.data
y = iris.target

print(f"Original shape: {X.shape}")
print(f"Features: {iris.feature_names}")
print(f"Classes: {iris.target_names}")

# Scale data first (important!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA (reduce to 2 components)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"\nPCA shape: {X_pca.shape}")
print(f"Reduced from {X.shape[1]} to {X_pca.shape[1]} dimensions")

# Check explained variance
print(f"\nExplained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {sum(pca.explained_variance_ratio_):.2%}")
```

**Output:**
```
Original shape: (150, 4)
PCA shape: (150, 2)
Explained variance ratio: [0.7296 0.2285]
Total variance explained: 95.81%
```

### Example 2: Choosing Number of Components

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Fit PCA with all components
pca_full = PCA()
pca_full.fit(X_scaled)

# Cumulative explained variance
cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

# Plot
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.bar(range(1, len(pca_full.explained_variance_ratio_) + 1),
        pca_full.explained_variance_ratio_, alpha=0.6, label='Individual')
plt.step(range(1, len(cumulative_variance) + 1),
         cumulative_variance, where='mid', label='Cumulative')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Explained Variance by Component')
plt.legend()
plt.grid(True, alpha=0.3)

# Print cumulative variance
print("Cumulative variance by component:")
for i, var in enumerate(cumulative_variance):
    print(f"  {i+1} components: {var:.2%}")

# Choose components to explain 95% of variance
n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1
print(f"\nComponents for 95% variance: {n_components_95}")
```

**Output:**
```
Cumulative variance by component:
  1 components: 72.96%
  2 components: 95.81%
  3 components: 99.48%
  4 components: 100.00%

Components for 95% variance: 2
```

### Example 3: PCA for Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# PCA to 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot
plt.figure(figsize=(8, 6))
colors = ['red', 'green', 'blue']
for i, target_name in enumerate(iris.target_names):
    mask = iris.target == i
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1],
                c=colors[i], label=target_name, alpha=0.7, edgecolors='black')

plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('PCA - Iris Dataset (2D)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('pca_visualization.png', dpi=100)
plt.show()
```

### Example 4: PCA for Speed

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
import time

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, iris.target, test_size=0.2, random_state=42
)

# Original data (4 features)
start = time.time()
model_orig = LogisticRegression(random_state=42, max_iter=200)
model_orig.fit(X_train, y_train)
time_orig = time.time() - start
acc_orig = accuracy_score(y_test, model_orig.predict(X_test))

# With PCA (2 features)
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

start = time.time()
model_pca = LogisticRegression(random_state=42, max_iter=200)
model_pca.fit(X_train_pca, y_train)
time_pca = time.time() - start
acc_pca = accuracy_score(y_test, model_pca.predict(X_test_pca))

print(f"Original ({X_train.shape[1]} features):")
print(f"  Accuracy: {acc_orig:.4f}")
print(f"  Training time: {time_orig:.4f}s")

print(f"\nPCA ({X_train_pca.shape[1]} features):")
print(f"  Accuracy: {acc_pca:.4f}")
print(f"  Training time: {time_pca:.4f}s")
```

### Example 5: Noise Reduction with PCA

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Add noise
np.random.seed(42)
X_noisy = X_scaled + np.random.randn(*X_scaled.shape) * 0.5

# Apply PCA (reconstruct with fewer components)
pca = PCA(n_components=3)
X_reduced = pca.fit_transform(X_noisy)
X_reconstructed = pca.inverse_transform(X_reduced)

# Calculate noise reduction
noise_original = np.mean((X_scaled - X_noisy) ** 2)
noise_removed = np.mean((X_scaled - X_reconstructed) ** 2)

print(f"MSE before PCA: {noise_original:.4f}")
print(f"MSE after PCA: {noise_removed:.4f}")
print(f"Noise reduction: {(noise_original - noise_removed) / noise_original:.1%}")
```

### Example 6: Understanding Principal Components

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Principal components (loadings)
print("Principal Components (loadings):")
print(f"  PC1: {pca.components_[0]}")
print(f"  PC2: {pca.components_[1]}")

# Interpret loadings
print("\nInterpretation:")
print("  PC1 is combination of all features (mostly petal features)")
print("  PC2 captures remaining variance (sepal width emphasis)")
```

### Example 7: PCA Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Create pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=2)),
    ('classifier', SVC(kernel='rbf'))
])

# Train
pipe.fit(X_train, y_train)

# Evaluate
y_pred = pipe.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Pipeline accuracy: {accuracy:.4f}")
print("Pipeline handles scaling, PCA, and classification")
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Scaling Before PCA

```python
# WRONG: Using unscaled data
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_unscaled)  # Features with larger ranges dominate

# CORRECT: Scale first
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_unscaled)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
```

### Mistake 2: Using PCA When Features Are Uncorrelated

```python
# If features are already uncorrelated, PCA won't help much
import numpy as np
import pandas as pd

# Create uncorrelated features
np.random.seed(42)
X = np.random.randn(100, 4)
df = pd.DataFrame(X, columns=['A', 'B', 'C', 'D'])
print("Correlation matrix (diagonal only):")
print(df.corr().round(2))
# PCA won't reduce dimensions effectively
```

### Mistake 3: Losing Interpretability

```python
# Principal components are combinations of original features
# Harder to interpret than original features

# Original: "petal length" is clear
# PC1: 0.5*sepal_length + 0.3*petal_length - 0.2*petal_width... (confusing)
```

---

## Best Practices

### 1. Always Scale Before PCA

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Use pipeline to ensure scaling
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=2))
])

X_pca = pipe.fit_transform(X)
```

### 2. Check Explained Variance

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

X_scaled = StandardScaler().fit_transform(X)

pca = PCA()
pca.fit(X_scaled)

cumvar = np.cumsum(pca.explained_variance_ratio_)
print(f"Components for 95% variance: {np.argmax(cumvar >= 0.95) + 1}")
```

### 3. Use for Visualization

```python
# Reduce high-dimensional data to 2D for plotting
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)

plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.show()
```

### 4. Preserve for Inverse Transform

```python
# Keep scaler and PCA for reconstruction
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)

# Reconstruct (approximate)
X_reconstructed = pca.inverse_transform(X_reduced)
X_original_approx = scaler.inverse_transform(X_reconstructed)
```

---

## Practice Exercises

### Exercise 1: Choose Optimal Components

```python
"""
Find the number of PCA components needed for 95% variance.
1. Load Wine dataset
2. Scale features
3. Fit PCA with all components
4. Plot cumulative variance
5. Determine optimal number
"""
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)

# Your code here
pca = PCA()
pca.fit(X_scaled)

cumvar = np.cumsum(pca.explained_variance_ratio_)

plt.figure(figsize=(8, 4))
plt.plot(range(1, len(cumvar) + 1), cumvar, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% threshold')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Explained Variance')
plt.legend()
plt.grid(True)
plt.savefig('wine_pca_variance.png', dpi=100)
plt.show()

n_95 = np.argmax(cumvar >= 0.95) + 1
print(f"Components for 95% variance: {n_95}")
```

### Exercise 2: PCA for Classification

```python
"""
Compare classification performance with and without PCA.
1. Use digits dataset (64 features)
2. Train classifier on original data
3. Train classifier on PCA-reduced data
4. Compare accuracy and speed
"""
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
import time

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.2, random_state=42
)

# Your code here
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Original
start = time.time()
model_orig = LogisticRegression(max_iter=1000, random_state=42)
model_orig.fit(X_train_scaled, y_train)
time_orig = time.time() - start
acc_orig = accuracy_score(y_test, model_orig.predict(X_test_scaled))

# PCA (32 components)
pca = PCA(n_components=32)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

start = time.time()
model_pca = LogisticRegression(max_iter=1000, random_state=42)
model_pca.fit(X_train_pca, y_train)
time_pca = time.time() - start
acc_pca = accuracy_score(y_test, model_pca.predict(X_test_pca))

print(f"Original: Acc={acc_orig:.4f}, Time={time_orig:.4f}s")
print(f"PCA:      Acc={acc_pca:.4f}, Time={time_pca:.4f}s")
```

### Exercise 3: Noise Reduction

```python
"""
Use PCA for noise reduction.
1. Generate noisy data
2. Apply PCA
3. Reconstruct
4. Compare MSE before and after
"""
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

np.random.seed(42)
X_noisy = X_scaled + np.random.randn(*X_scaled.shape) * 0.5

# Your code here
pca = PCA(n_components=3)
X_reduced = pca.fit_transform(X_noisy)
X_reconstructed = pca.inverse_transform(X_reduced)

mse_before = np.mean((X_scaled - X_noisy) ** 2)
mse_after = np.mean((X_scaled - X_reconstructed) ** 2)

print(f"MSE before: {mse_before:.4f}")
print(f"MSE after:  {mse_after:.4f}")
print(f"Improvement: {(mse_before - mse_after) / mse_before:.1%}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **PCA** | Reduces dimensions while preserving variance |
| **Principal Components** | New orthogonal axes |
| **Explained Variance** | Proportion of variance captured |
| **Scaling** | Always scale before PCA |
| **Visualization** | Reduce to 2D/3D for plotting |
| **Speed** | Fewer features = faster training |
| **Noise Reduction** | Remove low-variance noise |

### Key Takeaways

1. **Always scale** before PCA
2. Use **explained variance** to choose components
3. Great for **visualization** of high-dimensional data
4. **Trade-off**: less interpretability for speed
5. Use **pipelines** for reproducible workflows

---

## Next Steps

- **Lecture 19**: Naive Bayes — Classification with probabilities
- **Lecture 21**: SVM — Another powerful classifier
- **Lecture 22**: Cross-Validation — Proper model evaluation

---

## References

- [W3Schools - PCA](https://www.w3schools.com/python/ml_pca.asp)
- [Scikit-learn Documentation - PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- [Wikipedia - PCA](https://en.wikipedia.org/wiki/Principal_component_analysis)
