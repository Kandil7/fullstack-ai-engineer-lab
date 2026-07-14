# ML: Clustering - Quiz

## Topic Overview
Clustering is unsupervised learning that groups similar data points without predefined labels. This quiz covers K-Means, hierarchical clustering, DBSCAN, evaluation metrics, and practical clustering applications.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is clustering?
- **A)** A supervised learning technique for prediction
- **B)** An unsupervised learning technique that groups similar data points together
- **C)** A classification algorithm
- **D)** A regression technique

**Correct Answer: B** — Clustering groups unlabeled data into clusters where points within a cluster are more similar to each other than to points in other clusters.

---

### Q2. How does K-Means clustering work?
- **A)** It assigns each point to the nearest cluster center, then updates centers
- **B)** It builds a tree of clusters
- **C)** It uses density to find clusters
- **D)** It uses random assignment only

**Correct Answer: A** — K-Means iterates: (1) assign each point to the nearest centroid, (2) recalculate centroids as the mean of assigned points, repeat until convergence.

---

### Q3. How do you choose the optimal number of clusters (K) in K-Means?
- **A)** Always use K=2
- **B)** Use the Elbow Method or Silhouette Score
- **C)** Use the number of features
- **D)** Random choice

**Correct Answer: B** — The Elbow Method plots within-cluster sum of squares (WCSS) vs. K and looks for an "elbow." The Silhouette Score measures cluster cohesion vs. separation.

---

### Q4. What is the Elbow Method?
- **A)** A method to find outliers
- **B)** Plotting WCSS vs. K to find the point where adding more clusters gives diminishing returns
- **C)** A preprocessing technique
- **D)** A classification metric

**Correct Answer: B** — The Elbow Method plots the within-cluster sum of squares against K. The "elbow" point (where the rate of decrease sharply changes) suggests the optimal K.

---

### Q5. What is the Silhouette Score?
- **A)** A measure of how similar a point is to its own cluster vs. other clusters
- **B)** The size of clusters
- **C)** The number of clusters
- **D)** The distance between centroids

**Correct Answer: A** — Silhouette Score = (b - a) / max(a, b), where a = mean intra-cluster distance, b = mean nearest-cluster distance. Range: [-1, 1]. Higher is better.

---

### Q6. What is the main limitation of K-Means?
- **A)** It cannot handle numerical data
- **B)** It assumes clusters are spherical and equally sized
- **C)** It is too slow for large datasets
- **D)** It requires labeled data

**Correct Answer: B** — K-Means assumes convex, equally-sized clusters. It fails with non-spherical clusters, varying densities, or different-sized clusters.

---

### Q7. What is hierarchical clustering?
- **A)** A clustering method that builds a tree (dendrogram) of nested clusters
- **B)** A method that requires specifying K beforehand
- **C)** A density-based clustering method
- **D)** A classification algorithm

**Correct Answer: A** — Hierarchical clustering builds a dendrogram by either merging (agglomerative) or splitting (divisive) clusters iteratively without needing to pre-specify K.

---

### Q8. What is the difference between agglomerative and divisive hierarchical clustering?
- **A)** Agglomerative starts with one cluster; divisive starts with all points separate
- **B)** Agglomerative starts with each point as a cluster and merges; divisive starts with all points in one cluster and splits
- **C)** They are the same
- **D)** Agglomerative is faster

**Correct Answer: B** — Agglomerative (bottom-up): each point starts as its own cluster, then closest clusters are merged. Divisive (top-down): all points start in one cluster, then split.

---

### Q9. What is DBSCAN?
- **A)** A classification algorithm
- **B)** A density-based clustering algorithm that finds clusters of varying shapes
- **C)** A K-Means variant
- **D)** A regression method

**Correct Answer: B** — DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are closely packed and marks outliers in low-density regions.

---

### Q10. What are the two key parameters of DBSCAN?
- **A)** K and iterations
- **B)** eps (neighborhood radius) and min_samples (minimum points to form a dense region)
- **C)** Learning rate and epochs
- **D)** Alpha and beta

**Correct Answer: B** — `eps` defines the radius of the neighborhood, and `min_samples` defines the minimum number of points required to form a dense region (core point).

---

### Q11. What is an advantage of DBSCAN over K-Means?
- **A)** DBSCAN is always faster
- **B)** DBSCAN can find arbitrarily shaped clusters and doesn't need K specified
- **C)** DBSCAN works better with spherical clusters
- **D)** DBSCAN requires less memory

**Correct Answer: B** — DBSCAN discovers clusters of any shape, handles noise/outliers, and doesn't require pre-specifying the number of clusters.

---

### Q12. What is a core point in DBSCAN?
- **A)** A point on the edge of a cluster
- **B)** A point with at least min_samples points within its eps neighborhood
- **C)** The centroid of a cluster
- **D)** An outlier point

**Correct Answer: B** — A core point has ≥ min_samples neighbors within eps distance. Core points are the backbone of clusters in DBSCAN.

---

### Q13. What is the output of this code?
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(X)
print(kmeans.labels_)
```
- **A)** [0, 0, 0, 1, 1, 1]
- **B)** [1, 1, 1, 0, 0, 0]
- **C)** [0, 1, 0, 1, 0, 1]
- **D)** [0, 0, 1, 1, 0, 1]

**Correct Answer: A** — The data forms two clear groups: points at x=1 (cluster 0) and points at x=10 (cluster 1).

---

### Q14. What is the Within-Cluster Sum of Squares (WCSS)?
- **A)** The sum of distances between clusters
- **B)** The sum of squared distances of each point to its cluster centroid
- **C)** The sum of all feature values
- **D)** The number of clusters

**Correct Answer: B** — WCSS = Σ Σ ||xᵢ - μⱼ||² measures how compact clusters are. Lower WCSS means tighter clusters. Used in the Elbow Method.

---

### Q15. What is Gaussian Mixture Model (GMM) clustering?
- **A)** A hard clustering method like K-Means
- **B)** A probabilistic model that assigns soft probabilities of cluster membership
- **C)** A neural network for clustering
- **D)** A distance-based clustering method

**Correct Answer: B** — GMM assumes data is generated from a mixture of Gaussian distributions. Each point gets a probability of belonging to each cluster (soft clustering).

---

### Q16. What is the difference between hard and soft clustering?
- **A)** Hard is faster; soft is slower
- **B)** Hard assigns each point to exactly one cluster; soft assigns probabilities to multiple clusters
- **C)** They are the same
- **D)** Hard is for small data; soft is for big data

**Correct Answer: B** — Hard clustering (K-Means) assigns each point to one cluster. Soft clustering (GMM) gives each point a probability distribution over clusters.

---

### Q17. Why is feature scaling important for K-Means?
- **A)** It's not important
- **B)** K-Means uses distance metrics, so features with larger scales dominate
- **C)** Scaling makes the algorithm faster
- **D)** Scaling adds more features

**Correct Answer: B** — K-Means uses Euclidean distance. Without scaling, features with larger magnitudes dominate the distance calculation, biasing the clusters.

---

### Q18. What is the time complexity of K-Means?
- **A)** O(n)
- **B)** O(n × K × d × i) where n=samples, K=clusters, d=dimensions, i=iterations
- **C)** O(n²)
- **D)** O(n log n)

**Correct Answer: B** — K-Means runs in O(n × K × d × i) time: for each iteration, assign each of n points to one of K clusters in d dimensions.

---

### Q19. What is the Silhouette Score range and interpretation?
- **A)** [0, 1] where 1 is worst
- **B)** [-1, 1] where 1 is best (well-matched), 0 is borderline, -1 is worst (wrong cluster)
- **C)** [0, 100] where 100 is best
- **D)** [-∞, ∞] with no clear interpretation

**Correct Answer: B** — Silhouette ranges from -1 to 1. +1 = well-matched to own cluster. 0 = on cluster boundary. -1 = likely assigned to wrong cluster.

---

### Q20. When should you choose DBSCAN over K-Means?
- **A)** When clusters are spherical and equally sized
- **B)** When clusters have irregular shapes, varying sizes, or you want to detect noise
- **C)** When you know the exact number of clusters
- **D)** When the dataset is very small

**Correct Answer: B** — DBSCAN excels when clusters are non-spherical, have varying densities, or contain noise points. K-Means works best for spherical, equally-sized clusters.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | A | 12 | B |
| 3 | B | 13 | A |
| 4 | B | 14 | B |
| 5 | A | 15 | B |
| 6 | B | 16 | B |
| 7 | A | 17 | B |
| 8 | B | 18 | B |
| 9 | B | 19 | B |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong clustering knowledge
