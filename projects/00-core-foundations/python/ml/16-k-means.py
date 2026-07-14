"""
W3Schools Python Tutorial - ML NN: K-Means Clustering
======================================================
Topics: KMeans Clustering, Elbow Method, Inertia

Run: python 16-k-means.py
Reference: https://www.w3schools.com/python/ml_k-means.asp
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ============================================================
# What is K-Means Clustering?
# ============================================================

# Example 1: K-means concept
print("Example 1: K-Means Concept")
print("K-means groups data into K clusters based on similarity")
print("It minimizes within-cluster sum of squares (inertia)")
print("Unsupervised: no labels needed!")

# ============================================================
# Creating Clusters
# ============================================================

# Example 2: Generate clustered data
print("\nExample 2: Generate Clustered Data")
np.random.seed(42)
X, y = make_blobs(
    n_samples=300, centers=4, cluster_std=0.60, random_state=42
)

print(f"Generated {X.shape[0]} points in {X.shape[1]} dimensions")
print(f"True clusters: {len(np.unique(y))}")

# ============================================================
# K-Means Algorithm
# ============================================================

# Example 3: Basic K-means
print("\nExample 3: Basic K-Means")
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X)

labels = kmeans.labels_
centers = kmeans.cluster_centers_

print(f"Number of clusters: {kmeans.n_clusters}")
print(f"Cluster centers:\n{centers}")
print(f"Labels: {np.unique(labels)}")

# Example 4: Cluster assignments
print("\nExample 4: Cluster Assignments")
for i in range(4):
    cluster_size = np.sum(labels == i)
    print(f"Cluster {i}: {cluster_size} points")

# ============================================================
# Elbow Method
# ============================================================

# Example 5: Finding optimal K
print("\nExample 5: Elbow Method")
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

print("K | Inertia")
print("-" * 20)
for k, inertia in zip(K_range, inertias):
    print(f"{k:2d} | {inertia:10.2f}")

print("\nThe 'elbow' in the plot suggests the optimal K")
print("Where adding more clusters doesn't significantly reduce inertia")

# ============================================================
# Inertia and Silhouette Score
# ============================================================

# Example 6: Inertia interpretation
print("\nExample 6: Inertia Interpretation")
print("Inertia = Sum of squared distances to nearest cluster center")
print("Lower inertia = tighter clusters")
print("But too low K gives high inertia, too high K gives low inertia")

# Example 7: Silhouette Score
print("\nExample 7: Silhouette Score")
kmeans_4 = KMeans(n_clusters=4, random_state=42, n_init=10)
labels_4 = kmeans_4.fit_predict(X)
sil_score = silhouette_score(X, labels_4)

print(f"Silhouette Score for K=4: {sil_score:.4f}")
print("Score range: -1 to 1 (higher is better)")
print("  - Close to 1: well-separated clusters")
print("  - Close to 0: overlapping clusters")
print("  - Negative: points may be in wrong clusters")

# ============================================================
# Choosing K
# ============================================================

# Example 8: Testing different K values
print("\nExample 8: Testing Different K Values")
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

# ============================================================
# K-Means with Different Data
# ============================================================

# Example 9: Non-spherical clusters
print("\nExample 9: Limitations of K-Means")
print("K-means assumes spherical clusters of similar size")
print("It may fail with:")
print("  - Non-convex shapes")
print("  - Different cluster densities")
print("  - Outliers")

# ============================================================
# Practical Example
# ============================================================

# Example 10: Customer segmentation
print("\nExample 10: Customer Segmentation Example")
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

# Find optimal K
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

print(f"Segmented {len(X_customers)} customers into 3 groups")
for i in range(3):
    mask = labels == i
    avg_income = annual_income[mask].mean()
    avg_spending = spending_score[mask].mean()
    count = mask.sum()
    print(f"  Segment {i+1}: {count} customers, "
          f"Avg Income: ${avg_income:,.0f}, Avg Spending: {avg_spending:.0f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- K-means groups data into K clusters")
print("- Use elbow method to find optimal K")
print("- Inertia measures cluster compactness")
print("- Silhouette score measures cluster separation")
print("- Assumes spherical, equally-sized clusters")
print("- Scale features before clustering")
print("="*60)