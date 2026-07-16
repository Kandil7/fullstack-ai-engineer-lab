# SciPy Lecture 10: Spatial Data

## 🎯 Topic Overview

SciPy's `spatial` module provides algorithms for spatial data analysis — KD-trees for nearest neighbor search, Delaunay triangulation, Voronoi diagrams, and convex hulls.

## 📚 Learning Objectives

1. Use KD-Trees for efficient nearest neighbor search
2. Compute spatial distance metrics
3. Generate Delaunay triangulations and Voronoi diagrams

---

## 1. KD-Tree for Nearest Neighbors

```python
import numpy as np
from scipy.spatial import KDTree
from scipy.spatial import distance

# Generate data points
np.random.seed(42)
points = np.random.randn(100, 2)

# Build KD-Tree
tree = KDTree(points)

# Query nearest neighbor
query_point = [0, 0]
dist, idx = tree.query(query_point, k=5)  # 5 nearest neighbors
print(f"5 nearest neighbors indices: {idx}")
print(f"Distances to neighbors: {dist}")

# Query all points within radius
indices = tree.query_ball_point(query_point, r=2.0)
print(f"Points within radius 2.0: {len(indices)}")

# Distance matrix
dist_matrix = distance.pdist(points)  # Pairwise distances
dist_square = distance.squareform(dist_matrix)  # Square matrix
print(f"Distance matrix shape: {dist_square.shape}")
```

---

## 2. Triangulation and Convex Hull

```python
from scipy.spatial import Delaunay, ConvexHull, Voronoi

# Delaunay triangulation
tri = Delaunay(points)
print(f"Number of simplices (triangles): {tri.simplices.shape[0]}")

# Convex hull
hull = ConvexHull(points)
print(f"Hull vertices: {hull.vertices}")
print(f"Hull area: {hull.area:.3f}")
print(f"Hull volume (area): {hull.volume:.3f}")

# Voronoi diagram
vor = Voronoi(points)
print(f"Number of Voronoi regions: {len(vor.regions)}")
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `KDTree()` | Spatial indexing for nearest neighbors |
| `distance.pdist()` | Pairwise distances |
| `Delaunay()` | Delaunay triangulation |
| `ConvexHull()` | Convex hull computation |
| `Voronoi()` | Voronoi diagram |
