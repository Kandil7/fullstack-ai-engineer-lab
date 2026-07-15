# Lecture 17: Hierarchical Clustering

## Topic Overview

Hierarchical clustering builds a hierarchy of clusters by either merging small clusters (agglomerative/bottom-up) or splitting large clusters (divisive/top-down). Unlike K-Means, it doesn't require pre-specifying K and produces a dendrogram showing the cluster structure. This lecture covers both approaches, linkage methods, and practical applications.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand agglomerative and divisive clustering approaches
2. Implement hierarchical clustering with scikit-learn
3. Create and interpret dendrograms
4. Choose appropriate linkage methods (ward, complete, average, single)
5. Determine optimal number of clusters from dendrograms
6. Compare hierarchical clustering with K-Means
7. Apply to real-world scenarios

---

## Key Concepts

### 1. Agglomerative (Bottom-Up)

Starts with each point as its own cluster, then repeatedly merges the closest pairs until only one cluster remains.

**Steps:**
1. Start with N clusters (one per point)
2. Find two closest clusters
3. Merge them
4. Repeat until K clusters remain

### 2. Divisive (Top-Down)

Starts with all points in one cluster, then recursively splits until each point is its own cluster.

### 3. Linkage Methods

| Method | Description | Pros/Cons |
|--------|-------------|-----------|
| **Ward** | Minimizes variance within clusters | Balanced, often best |
| **Complete** | Maximum distance between points | Compact clusters |
| **Average** | Average distance between points | Compromise |
| **Single** | Minimum distance between points | Can handle non-convex |

### 4. Dendrogram

A tree diagram showing the hierarchy of clusters and the distances at which merges occurred.

---

## Code Examples

### Example 1: Basic Agglomerative Clustering

```python
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs

# Generate data
np.random.seed(42)
X, y = make_blobs(
    n_samples=100, centers=3, cluster_std=1.0, random_state=42
)

print(f"Generated {X.shape[0]} points in {X.shape[1]} dimensions")

# Apply agglomerative clustering
clustering = AgglomerativeClustering(n_clusters=3)
labels = clustering.fit_predict(X)

print(f"Number of clusters: {clustering.n_clusters_}")
print(f"Labels: {np.unique(labels)}")

# Count points per cluster
for i in range(3):
    count = np.sum(labels == i)
    print(f"Cluster {i}: {count} points")
```

### Example 2: Linkage Methods

```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import numpy as np

# Test different linkage methods
linkage_methods = ['ward', 'complete', 'average', 'single']
results = []

for method in linkage_methods:
    clustering = AgglomerativeClustering(n_clusters=3, linkage=method)
    labels = clustering.fit_predict(X)
    sil_score = silhouette_score(X, labels)
    results.append({'method': method, 'silhouette': sil_score})
    print(f"{method:>10}: Silhouette Score = {sil_score:.4f}")

# Find best method
best = max(results, key=lambda x: x['silhouette'])
print(f"\nBest linkage: {best['method']} (score={best['silhouette']:.4f})")
```

### Example 3: Dendrogram

```python
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Create linkage matrix
Z = linkage(X, method='ward')

print("Linkage matrix shape:", Z.shape)
print("\nFirst 5 rows of linkage matrix:")
print("  [cluster1, cluster2, distance, count]")
print(Z[:5])

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90,
           leaf_font_size=10, show_contracted=True)
plt.title('Hierarchical Clustering Dendrogram (Ward)')
plt.xlabel('Cluster Size')
plt.ylabel('Distance')
plt.axhline(y=7, color='r', linestyle='--', label='Cut for 3 clusters')
plt.legend()
plt.tight_layout()
plt.savefig('dendrogram.png', dpi=100)
plt.show()
```

**Interpreting Dendrogram:**
- Height = distance at which merge occurred
- Longer vertical lines = more distinct clusters
- Cut horizontally to get desired number of clusters

### Example 4: Choosing Number of Clusters

```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import numpy as np

results = []
for n_clusters in range(2, 8):
    clustering = AgglomerativeClustering(n_clusters=n_clusters)
    labels = clustering.fit_predict(X)
    sil_score = silhouette_score(X, labels)
    results.append({'n_clusters': n_clusters, 'silhouette': sil_score})
    print(f"K={n_clusters}: Silhouette Score = {sil_score:.4f}")

best = max(results, key=lambda x: x['silhouette'])
print(f"\nBest K: {best['n_clusters']} (Silhouette={best['silhouette']:.4f})")
```

### Example 5: Customer Segmentation

```python
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

np.random.seed(42)

# Generate customer data
n_customers = 150
X_customers = np.random.randn(n_customers, 2) * 2
X_customers[:50] += [3, 3]   # Cluster 1
X_customers[50:100] += [-3, -3]  # Cluster 2
X_customers[100:] += [3, -3]   # Cluster 3

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_customers)

# Apply clustering
clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = clustering.fit_predict(X_scaled)

print(f"Segmented {n_customers} customers into 3 groups")
for i in range(3):
    count = np.sum(labels == i)
    print(f"  Segment {i+1}: {count} customers")

# Evaluate
sil = silhouette_score(X_scaled, labels)
print(f"\nSilhouette Score: {sil:.4f}")
```

### Example 6: Hierarchical vs K-Means

```python
print("Hierarchical Clustering:")
print("  ✓ Does not require pre-specifying K")
print("  ✓ Produces dendrogram for visualization")
print("  ✓ More interpretable cluster structure")
print("  ✗ More computationally expensive O(n³)")
print("  ✗ Not suitable for large datasets")

print("\nK-Means:")
print("  ✓ Faster for large datasets O(n)")
print("  ✓ More scalable")
print("  ✗ Requires pre-specifying K")
print("  ✗ Assumes spherical clusters")
```

---

## Common Mistakes to Avoid

### Mistake 1: Using on Large Datasets

```python
# Hierarchical clustering is O(n³) complexity
# Not suitable for datasets with > 10,000 samples

# WRONG
# clustering = AgglomerativeClustering(n_clusters=3)
# labels = clustering.fit_predict(X_large)  # 100,000 points!

# CORRECT: Use K-Means for large datasets
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_large)  # Much faster
```

### Mistake 2: Ignoring Linkage Method

```python
# Different linkage methods produce different results
# Always compare multiple methods

for method in ['ward', 'complete', 'average', 'single']:
    clustering = AgglomerativeClustering(n_clusters=3, linkage=method)
    labels = clustering.fit_predict(X)
    sil = silhouette_score(X, labels)
    print(f"{method}: {sil:.4f}")
```

### Mistake 3: Not Scaling Features

```python
# Hierarchical clustering is distance-based
# Features must be on same scale

# WRONG
clustering = AgglomerativeClustering(n_clusters=3)
labels = clustering.fit_predict(X_unscaled)

# CORRECT
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
clustering = AgglomerativeClustering(n_clusters=3)
labels = clustering.fit_predict(X_scaled)
```

---

## Best Practices

### 1. Use Ward Linkage by Default

```python
# Ward linkage usually produces best results
clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = clustering.fit_predict(X)
```

### 2. Visualize with Dendrogram

```python
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

Z = linkage(X, method='ward')
plt.figure(figsize=(10, 6))
dendrogram(Z)
plt.title('Dendrogram')
plt.show()
```

### 3. Use for Small to Medium Datasets

```python
# Hierarchical: < 10,000 samples
# K-Means: > 10,000 samples

if len(X) < 10000:
    from sklearn.cluster import AgglomerativeClustering
    model = AgglomerativeClustering(n_clusters=3)
else:
    from sklearn.cluster import KMeans
    model = KMeans(n_clusters=3, random_state=42)
```

### 4. Combine with PCA for High Dimensions

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Scale and reduce dimensions
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Cluster in reduced space
clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = clustering.fit_predict(X_pca)
```

---

## Practice Exercises

### Exercise 1: Dendrogram Analysis

```python
"""
Create and analyze a dendrogram.
1. Generate data with 3 natural clusters
2. Create dendrogram
3. Determine optimal K from dendrogram
4. Compare with silhouette analysis
"""
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

np.random.seed(42)
from sklearn.datasets import make_blobs
X, _ = make_blobs(n_samples=100, centers=3, random_state=42)

# Your code here
Z = linkage(X, method='ward')

plt.figure(figsize=(10, 6))
dendrogram(Z, truncate_mode='lastp', p=30)
plt.title('Dendrogram')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.axhline(y=7, color='r', linestyle='--', label='Cut line')
plt.legend()
plt.savefig('exercise_dendrogram.png', dpi=100)
plt.show()

# Compare with silhouette
for k in range(2, 6):
    clustering = AgglomerativeClustering(n_clusters=k)
    labels = clustering.fit_predict(X)
    sil = silhouette_score(X, labels)
    print(f"K={k}: Silhouette = {sil:.4f}")
```

### Exercise 2: Compare Linkage Methods

```python
"""
Compare all linkage methods on the same dataset.
1. Generate non-convex data (moons)
2. Apply each linkage method
3. Evaluate with silhouette score
4. Visualize results
"""
from sklearn.datasets import make_moons
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import numpy as np

X, y = make_moons(n_samples=200, noise=0.1, random_state=42)

# Your code here
methods = ['ward', 'complete', 'average', 'single']
for method in methods:
    clustering = AgglomerativeClustering(n_clusters=2, linkage=method)
    labels = clustering.fit_predict(X)
    sil = silhouette_score(X, labels)
    print(f"{method:>10}: Silhouette = {sil:.4f}")
```

### Exercise 3: Real-World Application

```python
"""
Apply hierarchical clustering to a real-world scenario.
1. Generate multi-dimensional data (e.g., 5 features)
2. Apply PCA to reduce to 2D
3. Cluster with hierarchical clustering
4. Analyze cluster characteristics
"""
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import numpy as np

np.random.seed(42)
X = np.random.randn(200, 5)
X[:50] += [2, 2, 0, 0, 0]
X[50:100] += [-2, -2, 0, 0, 0]
X[100:150] += [0, 0, 2, 2, 0]
X[150:] += [0, 0, -2, -2, 0]

# Your code here
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

clustering = AgglomerativeClustering(n_clusters=4, linkage='ward')
labels = clustering.fit_predict(X_pca)

print(f"Clusters: {len(np.unique(labels))}")
print(f"Cluster sizes: {np.bincount(labels)}")
print(f"Variance explained: {pca.explained_variance_ratio_.sum():.2%}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Agglomerative** | Bottom-up: merge closest clusters |
| **Divisive** | Top-down: split largest cluster |
| **Linkage** | Method to measure inter-cluster distance |
| **Ward** | Minimizes variance (usually best) |
| **Dendrogram** | Tree showing merge hierarchy |
| **No K Required** | Determine K from dendrogram |

### Key Takeaways

1. Hierarchical clustering produces a **dendrogram**
2. Use **Ward linkage** by default
3. **No need to specify K** in advance
4. **Slower than K-Means** — use for small/medium datasets
5. Great for **visualizing cluster structure**

---

## Next Steps

- **Lecture 16**: K-Means — Faster alternative for large datasets
- **Lecture 18**: PCA — Dimensionality reduction for better clustering
- **Lecture 20**: Random Forest — Supervised learning alternative

---

## References

- [W3Schools - Hierarchical Clustering](https://www.w3schools.com/python/ml_hierarchical_clustering.asp)
- [Scikit-learn Documentation - AgglomerativeClustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html)
- [SciPy Documentation - Dendrogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html)
