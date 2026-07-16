# SciPy Lecture 10: Spatial Data — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| KD-Tree | Spatial data structure for NNS | `KDTree(points)` |
| Nearest Neighbor | Closest point in space | `tree.query(point, k=1)` |
| Delaunay | Triangulation maximizing min angle | `Delaunay(points)` |
| Voronoi | Partition of space by nearest point | `Voronoi(points)` |
| Convex Hull | Minimum convex polygon containing points | `ConvexHull(points)` |
| Pairwise Distance | All distances between points | `distance.pdist(points)` |
| Euclidean | Straight-line distance | `distance.euclidean(a, b)` |
| Manhattan | City-block distance | `distance.cityblock(a, b)` |
| Cosine | Angular distance | `distance.cosine(a, b)` |

### Distance Metrics

| Metric | `pdist` Method | Use Case |
|--------|---------------|----------|
| Euclidean | `'euclidean'` | General purpose |
| Manhattan | `'cityblock'` | Grid-based |
| Cosine | `'cosine'` | Text/vector similarity |
| Chebyshev | `'chebyshev'` | Maximum coordinate diff |
