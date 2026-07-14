# Lecture 23: K-Nearest Neighbors (KNN)

## Topic Overview

K-Nearest Neighbors (KNN) is a simple, instance-based learning algorithm that classifies new data points based on the majority vote of its K nearest neighbors. Despite its simplicity, KNN is effective for many problems. This lecture covers how KNN works, choosing K, distance metrics, and practical applications.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand how KNN classifies data points
2. Implement KNN with scikit-learn
3. Choose the optimal K value
4. Select appropriate distance metrics
5. Use weighted voting for better performance
6. Apply KNN to classification and regression
7. Recognize KNN limitations

---

## Key Concepts

### 1. How KNN Works

1. Store all training data
2. For a new point, calculate distances to all training points
3. Find K nearest neighbors
4. Classification: majority vote; Regression: average

### 2. Choosing K

| K Value | Effect |
|---------|--------|
| Small K (1-3) | Low bias, high variance (overfitting) |
| Medium K (5-10) | Good balance |
| Large K (>10) | High bias, low variance (underfitting) |

### 3. Distance Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| Euclidean | √(Σ(xᵢ-yᵢ)²) | Default, continuous data |
| Manhattan | Σ\|xᵢ-yᵢ\| | Sparse data, outliers |
| Chebyshev | max\|xᵢ-yᵢ\| | High-dimensional |

### 4. Weighted KNN

Closer neighbors have more influence on the prediction than farther ones.

---

## Code Examples

### Example 1: How KNN Works

```python
import numpy as np

# Simple dataset
X_train = np.array([[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]])
y_train = np.array([0, 0, 0, 1, 1, 1])

# New point to classify
X_new = np.array([[4, 4]])

print("Training data:")
for i, (x, y) in enumerate(zip(X_train, y_train)):
    print(f"  Point {i}: {x} -> Class {y}")

# Calculate distances
distances = np.sqrt(np.sum((X_train - X_new) ** 2, axis=1))
print(f"\nDistances from {X_new[0]}: {distances}")

# Find K nearest neighbors
K = 3
nearest_indices = np.argsort(distances)[:K]
nearest_labels = y_train[nearest_indices]
print(f"K={K} nearest neighbors: {nearest_indices}")
print(f"Neighbor labels: {nearest_labels}")

# Majority vote
prediction = np.bincount(nearest_labels).argmax()
print(f"Prediction: Class {prediction}")
```

### Example 2: KNN Classifier

```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# Generate data
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=2, n_redundant=0,
    n_informative=2, random_state=42, n_clusters_per_class=1
)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features (IMPORTANT for KNN!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# Evaluate
y_pred = knn.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"K=5, Accuracy: {accuracy:.4f}")
```

### Example 3: Choosing K

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
X, y = make_classification(n_samples=300, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Test different K values
results = []
for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, knn.predict(X_test_scaled))
    results.append({'k': k, 'accuracy': acc})

# Find best K
best = max(results, key=lambda x: x['accuracy'])
print(f"Best K: {best['k']} (Accuracy: {best['accuracy']:.4f})")

# Plot
plt.figure(figsize=(8, 4))
plt.plot([r['k'] for r in results], [r['accuracy'] for r in results], 'bo-')
plt.axvline(x=best['k'], color='r', linestyle='--', label=f"Best K={best['k']}")
plt.xlabel('K')
plt.ylabel('Accuracy')
plt.title('KNN: Accuracy vs K')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('knn_k_selection.png', dpi=100)
plt.show()
```

### Example 4: Distance Metrics

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=300, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Test different metrics
metrics = ['euclidean', 'manhattan', 'chebyshev', 'minkowski']
print("Distance Metric Comparison:")
print("-" * 35)

for metric in metrics:
    knn = KNeighborsClassifier(n_neighbors=5, metric=metric)
    knn.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, knn.predict(X_test_scaled))
    print(f"{metric:>12}: {acc:.4f}")
```

### Example 5: KNN Regression

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X = np.random.rand(200, 1) * 10
y = np.sin(X.squeeze()) + np.random.randn(200) * 0.2

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_reg = KNeighborsRegressor(n_neighbors=5)
knn_reg.fit(X_train_scaled, y_train)

y_pred = knn_reg.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
print(f"KNN Regression R²: {r2:.4f}")
```

### Example 6: Weighted KNN

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=300, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Uniform weights (default)
knn_uniform = KNeighborsClassifier(n_neighbors=5, weights='uniform')
knn_uniform.fit(X_train_scaled, y_train)
acc_uniform = accuracy_score(y_test, knn_uniform.predict(X_test_scaled))

# Distance weights
knn_distance = KNeighborsClassifier(n_neighbors=5, weights='distance')
knn_distance.fit(X_train_scaled, y_train)
acc_distance = accuracy_score(y_test, knn_distance.predict(X_test_scaled))

print(f"Uniform weights: {acc_uniform:.4f}")
print(f"Distance weights: {acc_distance:.4f}")
```

### Example 7: KNN Limitations

```python
print("KNN Limitations:")
print("1. Slow prediction (computes distances to all points)")
print("2. Memory intensive (stores all training data)")
print("3. Sensitive to irrelevant features")
print("4. Sensitive to feature scaling")
print("5. Struggles with high dimensions (curse of dimensionality)")

print("\nWhen to use KNN:")
print("  ✓ Small to medium datasets")
print("  ✓ Low-dimensional data")
print("  ✓ Simple, interpretable model needed")
print("  ✓ No training phase required")

print("\nWhen to avoid KNN:")
print("  ✗ Large datasets (slow prediction)")
print("  ✗ High-dimensional data")
print("  ✗ Real-time predictions needed")
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Scaling Features

```python
# WRONG: Using features with different scales
knn_unscaled = KNeighborsClassifier(n_neighbors=5)
knn_unscaled.fit(X_train, y_train)  # Bad results

# CORRECT: Always scale for KNN
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_scaled = KNeighborsClassifier(n_neighbors=5)
knn_scaled.fit(X_train_scaled, y_train)  # Good results
```

### Mistake 2: Using Too Small K

```python
# K=1 is very sensitive to noise
knn_1 = KNeighborsClassifier(n_neighbors=1)
# May overfit

# Use odd K to avoid ties
knn_5 = KNeighborsClassifier(n_neighbors=5)
```

### Mistake 3: Ignoring Irrelevant Features

```python
# KNN is sensitive to irrelevant features
# They add noise to distance calculations

# SOLUTION: Feature selection or dimensionality reduction
from sklearn.decomposition import PCA

pca = PCA(n_components=5)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)
```

---

## Best Practices

### 1. Always Scale Features

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5))
])

pipeline.fit(X_train, y_train)
```

### 2. Use Odd K to Avoid Ties

```python
# For binary classification, use odd K
knn = KNeighborsClassifier(n_neighbors=5)  # Odd
```

### 3. Use Weighted Voting

```python
# Distance weights give closer neighbors more influence
knn = KNeighborsClassifier(n_neighbors=5, weights='distance')
```

### 4. Tune K with Cross-Validation

```python
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

for k in range(1, 11):
    pipeline.set_params(knn__n_neighbors=k)
    scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
    print(f"K={k:2d}: {scores.mean():.4f}")
```

---

## Practice Exercises

### Exercise 1: Find Optimal K

```python
"""
Find the optimal K value for KNN.
1. Test K from 1 to 20
2. Use cross-validation
3. Plot results
4. Choose best K
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

# Your code here
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

k_range = range(1, 21)
scores = []

for k in k_range:
    pipeline.set_params(knn__n_neighbors=k)
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
    scores.append(cv_scores.mean())

best_k = list(k_range)[np.argmax(scores)]
print(f"Best K: {best_k}")

plt.figure(figsize=(8, 4))
plt.plot(k_range, scores, 'bo-')
plt.axvline(x=best_k, color='r', linestyle='--')
plt.xlabel('K')
plt.ylabel('CV Accuracy')
plt.title('KNN: K Selection')
plt.grid(True)
plt.savefig('knn_optimal_k.png', dpi=100)
plt.show()
```

### Exercise 2: Distance Metrics Comparison

```python
"""
Compare different distance metrics for KNN.
1. Generate data
2. Test euclidean, manhattan, chebyshev
3. Compare accuracy
4. Recommend best metric
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

# Your code here
metrics = ['euclidean', 'manhattan', 'chebyshev', 'minkowski']

for metric in metrics:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=5, metric=metric))
    ])
    scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
    print(f"{metric:>12}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

### Exercise 3: Weighted vs Uniform KNN

```python
"""
Compare uniform and distance-weighted KNN.
1. Create dataset
2. Test both weighting methods
3. Compare across different K values
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

# Your code here
for k in [3, 5, 7, 11]:
    for weights in ['uniform', 'distance']:
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k, weights=weights))
        ])
        scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
        print(f"K={k:2d}, {weights:8s}: {scores.mean():.4f}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **KNN** | Classifies based on K nearest neighbors |
| **Instance-based** | No training phase, stores all data |
| **Distance Metrics** | Euclidean, Manhattan, Chebyshev |
| **Weighted KNN** | Closer neighbors have more influence |
| **K Value** | Small K = overfit, Large K = underfit |
| **Scaling** | Always scale features for KNN |

### Key Takeaways

1. **Always scale features** for KNN
2. Use **odd K** to avoid ties
3. **Distance weights** often improve performance
4. **Tune K** with cross-validation
5. **Slow on large datasets** — consider alternatives

---

## Next Steps

- **Review all lectures** with proper cross-validation
- **Try different algorithms** on the same dataset
- **Build complete ML pipelines**

---

## References

- [W3Schools - KNN](https://www.w3schools.com/python/ml_knn.asp)
- [Scikit-learn Documentation - KNN](https://scikit-learn.org/stable/modules/neighbors.html)
- [Wikipedia - KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)
