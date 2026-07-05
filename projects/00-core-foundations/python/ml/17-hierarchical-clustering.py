"""
W3Schools Python Tutorial - ML NN: Hierarchical Clustering
===========================================================
Topics: AgglomerativeClustering, Linkage Concepts

Run: python 17-hierarchical-clustering.py
Reference: https://www.w3schools.com/python/ml_hierarchical_clustering.asp
"""

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# ============================================================
# What is Hierarchical Clustering?
# ============================================================

# Example 1: Hierarchical clustering concept
print("Example 1: Hierarchical Clustering Concept")
print("Builds a hierarchy of clusters (tree/dendrogram)")
print("Two approaches:")
print("  - Agglomerative (bottom-up): Start with individual points, merge")
print("  - Divisive (top-down): Start with one cluster, split")

# ============================================================
# Generating Data
# ============================================================

# Example 2: Generate data
print("\nExample 2: Generate Clustered Data")
np.random.seed(42)
X, y = make_blobs(
    n_samples=100, centers=3, cluster_std=1.0, random_state=42
)

print(f"Generated {X.shape[0]} points in {X.shape[1]} dimensions")
print(f"True clusters: {len(np.unique(y))}")

# ============================================================
# Agglomerative Clustering
# ============================================================

# Example 3: Basic agglomerative clustering
print("\nExample 3: Basic Agglomerative Clustering")
clustering = AgglomerativeClustering(n_clusters=3)
labels = clustering.fit_predict(X)

print(f"Number of clusters: {clustering.n_clusters}")
print(f"Labels: {np.unique(labels)}")

# Count points per cluster
for i in range(3):
    count = np.sum(labels == i)
    print(f"Cluster {i}: {count} points")

# ============================================================
# Linkage Methods
# ============================================================

# Example 4: Different linkage methods
print("\nExample 4: Linkage Methods")
print("Linkage defines how to measure distance between clusters:")
print("  - ward: Minimizes variance within clusters")
print("  - complete: Maximum distance between points")
print("  - average: Average distance between points")
print("  - single: Minimum distance between points")

# Test different linkage methods
linkage_methods = ['ward', 'complete', 'average', 'single']
results = []

for method in linkage_methods:
    clustering = AgglomerativeClustering(n_clusters=3, linkage=method)
    labels = clustering.fit_predict(X)
    sil_score = silhouette_score(X, labels)
    results.append({'method': method, 'silhouette': sil_score})
    print(f"{method:>10}: Silhouette Score = {sil_score:.4f}")

# ============================================================
# Dendrogram
# ============================================================

# Example 5: Creating dendrogram
print("\nExample 5: Dendrogram")
# Create linkage matrix
Z = linkage(X, method='ward')

print("Linkage matrix shape:", Z.shape)
print("First 5 rows of linkage matrix:")
print(Z[:5])

# ============================================================
# Choosing Number of Clusters
# ============================================================

# Example 6: Finding optimal clusters
print("\nExample 6: Finding Optimal Clusters")
results = []
for n_clusters in range(2, 8):
    clustering = AgglomerativeClustering(n_clusters=n_clusters)
    labels = clustering.fit_predict(X)
    sil_score = silhouette_score(X, labels)
    results.append({'n_clusters': n_clusters, 'silhouette': sil_score})
    print(f"K={n_clusters}: Silhouette Score = {sil_score:.4f}")

best = max(results, key=lambda x: x['silhouette'])
print(f"\nBest K: {best['n_clusters']} (Silhouette={best['silhouette']:.4f})")

# ============================================================
# Distance Metrics
# ============================================================

# Example 7: Distance metrics
print("\nExample 7: Distance Metrics")
print("Common distance metrics:")
print("  - Euclidean: sqrt(sum((x-y)^2))")
print("  - Manhattan: sum(|x-y|)")
print("  - Cosine: 1 - cos(angle)")

# ============================================================
# Practical Example
# ============================================================

# Example 8: Customer segmentation
print("\nExample 8: Customer Segmentation")
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

# ============================================================
# Comparison with K-Means
# ============================================================

# Example 9: Hierarchical vs K-Means
print("\nExample 9: Hierarchical vs K-Means")
print("Hierarchical clustering:")
print("  - Does not require pre-specifying K")
print("  - Produces dendrogram for visualization")
print("  - More computationally expensive")
print("  - Not suitable for large datasets")

print("\nK-Means:")
print("  - Requires pre-specifying K")
print("  - Faster for large datasets")
print("  - Assumes spherical clusters")
print("  - More scalable")

# ============================================================
# When to Use Hierarchical
# ============================================================

# Example 10: Use cases
print("\nExample 10: When to Use Hierarchical Clustering")
print("Use hierarchical clustering when:")
print("  - You want to see cluster hierarchy")
print("  - Dataset is small to medium size")
print("  - You're not sure how many clusters to use")
print("  - You need interpretable cluster structure")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Hierarchical clustering builds a hierarchy of clusters")
print("- Agglomerative: bottom-up approach")
print("- Use dendrogram to visualize cluster structure")
print("- Linkage method affects cluster formation")
print("- More interpretable but less scalable than K-means")
print("- Good for small to medium datasets")
print("="*60)