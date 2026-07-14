# Lecture 16: K-Means Clustering

## Topic Overview

K-Means is one of the most popular unsupervised learning algorithms for clustering. It partitions data into K distinct clusters based on similarity, without requiring labeled data. This lecture covers the K-Means algorithm, the elbow method for choosing K, silhouette analysis, and practical applications like customer segmentation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the K-Means algorithm and how it works
2. Implement K-Means clustering with scikit-learn
3. Use the elbow method to find optimal K
4. Evaluate clustering quality with silhouette score
5. Apply K-Means to real-world problems like customer segmentation
6. Recognize limitations of K-Means and when to use alternatives

---

## Key Concepts

### 1. The K-Means Algorithm

K-Means partitions n observations into K clusters where each observation belongs to the cluster with the nearest centroid.

**Steps:**
1. **Initialize**: Randomly select K centroids
2. **Assign**: Assign each point to nearest centroid
3. **Update**: Recalculate centroids as mean of assigned points
4. **Repeat**: Steps 2-3 until convergence

### 2. Inertia (Within-Cluster Sum of Squares)

```
Inertia = Σ Σ ||xᵢ - μₖ||²
```

Where:
- `xᵢ` = data point
- `μₖ` = centroid of cluster k
- Lower inertia = tighter clusters

### 3. Elbow Method

A technique to find optimal K by plotting inertia vs K and looking for the "elbow" where adding more clusters provides diminishing returns.

### 4. Silhouette Score

Measures how similar a point is to its own cluster vs other clusters. Range: -1 to 1.

```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

Where:
- `a(i)` = average distance to same cluster
- `b(i)` = average distance to nearest other cluster

---

## Code Examples

### Example 1: Basic K-Means

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Generate clustered data
np.random.seed(42)
X, y = make_blobs(
    n_samples=300, centers=4, cluster_std=0.60, random_state=42
)

print(f"Generated {X.shape[0]} points in {X.shape[1]} dimensions")
print(f"True clusters: {len(np.unique(y))}")

# Apply K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X)

labels = kmeans.labels_
centers = kmeans.cluster_centers_

print(f"\nNumber of clusters: {kmeans.n_clusters}")
print(f"Cluster centers:\n{centers}")

# Count points per cluster
for i in range(4):
    cluster_size = np.sum(labels == i)
    print(f"Cluster {i}: {cluster_size} points")
```

### Example 2: Elbow Method

```python
import numpy as np
import matplotlib.pyplot as plt

# Calculate inertia for different K values
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(8, 4))
plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal K')
plt.xticks(K_range)
plt.grid(True, alpha=0.3)
plt.savefig('elbow_method.png', dpi=100)
plt.show()

print("K | Inertia")
print("-" * 20)
for k, inertia in zip(K_range, inertias):
    print(f"{k:2d} | {inertia:10.2f}")
```

**Interpretation:** The "elbow" (where inertia stops decreasing rapidly) suggests optimal K. For this data, K=4 is the elbow.

### Example 3: Silhouette Score

```python
from sklearn.metrics import silhouette_score

# Test different K values
results = []
for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    inertia = kmeans.inertia_
    sil = silhouette_score(X, labels)
    results.append({'k': k, 'inertia': inertia, 'silhouette': sil})
    print(f"K={k}: Inertia={inertia:.2f}, Silhouette={sil:.4f}")

# Find best K by silhouette
best_result = max(results, key=lambda x: x['silhouette'])
print(f"\nBest K by silhouette: {best_result['k']} (score={best_result['silhouette']:.4f})")
```

**Silhouette Score Interpretation:**
- Close to 1: Well-separated clusters
- Close to 0: Overlapping clusters
- Negative: Points may be in wrong clusters

### Example 4: Customer Segmentation

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n_customers = 200

# Features: annual_income, spending_score
annual_income = np.concatenate([
    np.random.normal(50000, 10000, 50),   # Low income
    np.random.normal(100000, 15000, 100), # Medium income
    np.random.normal(150000, 20000, 50)   # High income
])

spending_score = np.concatenate([
    np.random.normal(30, 10, 50),    # Low spenders
    np.random.normal(70, 15, 100),   # Medium spenders
    np.random.normal(50, 20, 50)     # Mixed spenders
])

X_customers = np.column_stack([annual_income, spending_score])

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_customers)

# Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

# Analyze segments
print(f"Segmented {len(X_customers)} customers into 3 groups\n")
for i in range(3):
    mask = labels == i
    avg_income = annual_income[mask].mean()
    avg_spending = spending_score[mask].mean()
    count = mask.sum()
    print(f"Segment {i+1}: {count} customers")
    print(f"  Avg Income: ${avg_income:,.0f}")
    print(f"  Avg Spending Score: {avg_spending:.0f}\n")
```

### Example 5: Limitations of K-Means

```python
print("K-Means assumes:")
print("  1. Spherical clusters (isotropic)")
print("  2. Similar cluster sizes")
print("  3. Similar cluster densities")

print("\nK-Means may fail with:")
print("  - Non-convex shapes (moons, rings)")
print("  - Different cluster densities")
print("  - Outliers")

print("\nAlternatives for these cases:")
print("  - DBSCAN (density-based)")
print("  - Gaussian Mixture Models")
print("  - Spectral Clustering")
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Scaling Features

```python
# WRONG: Using features with different scales
# Income (10000-200000) will dominate spending (1-100)

# CORRECT: Always scale before K-Means
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)
```

### Mistake 2: Assuming K-Means Finds Optimal K

```python
# K-Means requires you to specify K
# It doesn't find optimal K automatically

# SOLUTION: Use elbow method or silhouette analysis
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
```

### Mistake 3: Using K-Means on Non-Numeric Data

```python
# K-Means only works with numeric features
# For categorical data, use:
# - K-Modes (categorical data)
# - K-Prototypes (mixed data)
# - One-hot encoding + K-Means
```

### Mistake 4: Ignoring Initialization

```python
# Default: 10 random initializations (n_init=10)
# For reproducibility, always set random_state

kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)

# K-Means++ (default) provides better initialization
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
```

---

## Best Practices

### 1. Always Scale Features

```python
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Use pipeline for reproducibility
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('kmeans', KMeans(n_clusters=3, random_state=42))
])

labels = pipeline.fit_predict(X)
```

### 2. Use Multiple Evaluation Methods

```python
# Combine elbow method and silhouette analysis
from sklearn.metrics import silhouette_score

results = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    
    results.append({
        'k': k,
        'inertia': kmeans.inertia_,
        'silhouette': silhouette_score(X, labels)
    })

# Find K with highest silhouette
best_k = max(results, key=lambda x: x['silhouette'])['k']
print(f"Optimal K: {best_k}")
```

### 3. Analyze Cluster Characteristics

```python
# After clustering, analyze what makes each cluster unique
import pandas as pd

df = pd.DataFrame(X, columns=['feature1', 'feature2'])
df['cluster'] = labels

# Cluster statistics
print(df.groupby('cluster').mean())
print("\nCluster sizes:")
print(df['cluster'].value_counts().sort_index())
```

### 4. Handle Outliers

```python
# K-Means is sensitive to outliers
# Consider removing outliers before clustering

from sklearn.ensemble import IsolationForest

# Identify outliers
iso_forest = IsolationForest(contamination=0.1, random_state=42)
outliers = iso_forest.fit_predict(X)

# Remove outliers
X_clean = X[outliers == 1]
print(f"Removed {np.sum(outliers == -1)} outliers")
```

---

## Practice Exercises

### Exercise 1: Find Optimal K

```python
"""
Use elbow method and silhouette analysis to find optimal K.
1. Test K from 2 to 10
2. Plot inertia vs K
3. Calculate silhouette scores
4. Determine best K
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

np.random.seed(42)
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=42)

# Your code here
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X, labels))

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(K_range, inertias, 'bo-', linewidth=2)
ax1.set_xlabel('K')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method')

ax2.plot(K_range, silhouette_scores, 'ro-', linewidth=2)
ax2.set_xlabel('K')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Analysis')

plt.tight_layout()
plt.savefig('optimal_k_analysis.png', dpi=100)
plt.show()

best_k = list(K_range)[np.argmax(silhouette_scores)]
print(f"Optimal K by silhouette: {best_k}")
```

### Exercise 2: Customer Segmentation

```python
"""
Perform customer segmentation with K-Means.
1. Generate customer data
2. Find optimal K
3. Interpret segments
4. Make business recommendations
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# Generate customer data
n_customers = 500
annual_income = np.concatenate([
    np.random.normal(30000, 8000, 150),
    np.random.normal(60000, 12000, 200),
    np.random.normal(100000, 20000, 100),
    np.random.normal(150000, 25000, 50)
])

spending_score = np.concatenate([
    np.random.normal(20, 8, 150),
    np.random.normal(50, 15, 200),
    np.random.normal(80, 10, 100),
    np.random.normal(60, 20, 50)
])

age = np.concatenate([
    np.random.normal(55, 10, 150),
    np.random.normal(35, 8, 200),
    np.random.normal(28, 5, 100),
    np.random.normal(45, 12, 50)
])

X = np.column_stack([annual_income, spending_score, age])

# Your code here
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal K
silhouette_scores = []
for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores.append(silhouette_score(X_scaled, labels))

best_k = np.argmax(silhouette_scores) + 2
print(f"Optimal K: {best_k}")

# Apply K-Means with best K
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

# Analyze segments
df = pd.DataFrame({
    'income': annual_income,
    'spending': spending_score,
    'age': age,
    'segment': labels
})

print("\nSegment Analysis:")
print(df.groupby('segment').mean().round(0))
print("\nSegment Sizes:")
print(df['segment'].value_counts().sort_index())
```

### Exercise 3: Compare K-Means with Other Methods

```python
"""
Compare K-Means with other clustering algorithms.
1. Apply K-Means
2. Apply DBSCAN
3. Compare results
"""
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np

np.random.seed(42)
from sklearn.datasets import make_moons

# Non-convex data
X_moons, y_moons = make_moons(n_samples=200, noise=0.1, random_state=42)

# K-Means
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_moons)
sil_kmeans = silhouette_score(X_moons, labels_kmeans)

# DBSCAN
dbscan = DBSCAN(eps=0.2, min_samples=5)
labels_dbscan = dbscan.fit_predict(X_moons)
sil_dbscan = silhouette_score(X_moons, labels_dbscan) if len(np.unique(labels_dbscan)) > 1 else -1

print(f"K-Means Silhouette: {sil_kmeans:.4f}")
print(f"DBSCAN Silhouette: {sil_dbscan:.4f}")

# Note: K-Means struggles with non-convex shapes
# DBSCAN can find arbitrary-shaped clusters
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **K-Means** | Partitions data into K clusters based on centroid proximity |
| **Inertia** | Sum of squared distances to cluster centers (lower = tighter) |
| **Elbow Method** | Plot inertia vs K to find optimal K |
| **Silhouette Score** | Measures cluster separation (-1 to 1, higher = better) |
| **Centroids** | Center points of each cluster |
| **n_init** | Number of random initializations (default 10) |

### Key Takeaways

1. K-Means is **unsupervised** — no labels needed
2. Always **scale features** before clustering
3. Use **elbow method** and **silhouette analysis** to find K
4. K-Means assumes **spherical clusters** of similar size
5. **Analyze clusters** to extract business insights

---

## Next Steps

- **Lecture 17**: Hierarchical Clustering — Alternative clustering method
- **Lecture 18**: PCA — Dimensionality reduction for better clustering
- **Lecture 19**: Naive Bayes — Another unsupervised/supervised hybrid

---

## References

- [W3Schools - K-Means](https://www.w3schools.com/python/ml_k-means.asp)
- [Scikit-learn Documentation - KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [Wikipedia - K-means Clustering](https://en.wikipedia.org/wiki/K-means_clustering)
