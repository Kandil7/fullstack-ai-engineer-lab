# Glossary: K-Nearest Neighbors (Lecture 23)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| KNN | Classifies based on K nearest neighbors | `KNeighborsClassifier()` |
| Instance-based | No training phase, stores all data | Lazy learning |
| K Value | Number of neighbors to consider | 5 (default) |
| Distance Metric | How to measure similarity | Euclidean, Manhattan |
| Euclidean Distance | √(Σ(xᵢ-yᵢ)²) | Default metric |
| Manhattan Distance | Σ\|xᵢ-yᵢ\| | L1 norm |
| Chebyshev Distance | max\|xᵢ-yᵢ\| | L∞ norm |
| Minkowski Distance | Generalized distance | p parameter |
| Uniform Weights | Equal voting from all neighbors | `weights='uniform'` |
| Distance Weights | Closer neighbors have more influence | `weights='distance'` |
| Majority Vote | Most common class among neighbors | Classification |
| KNN Regression | Average of K nearest neighbors | `KNeighborsRegressor()` |
| Curse of Dimensionality | Distance becomes meaningless in high dimensions | >10 features |
| Feature Scaling | Normalize features for KNN | `StandardScaler()` |
| Decision Boundary | Regions assigned to each class | Depends on K |

---

## Detailed Term Definitions

### K-Nearest Neighbors (KNN)

**Definition:** An instance-based learning algorithm that classifies new data points based on the majority vote of its K nearest neighbors in the training set.

**Algorithm:**
1. Store all training data
2. For a new point, calculate distances to all training points
3. Find K closest points
4. Classification: majority vote; Regression: average

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import numpy as np

X, y = make_classification(n_samples=300, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

accuracy = accuracy_score(y_test, knn.predict(X_test_scaled))
print(f"KNN Accuracy: {accuracy:.4f}")
```

**Related Terms:** Instance-based Learning, Lazy Learning, Distance Metric

---

### Instance-based Learning

**Definition:** A learning paradigm where the model stores training instances and classifies new points based on similarity to stored instances. No explicit training phase.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
import time

# KNN has no training phase - it just stores data
knn = KNeighborsClassifier(n_neighbors=5)

# "Training" is just storing data
start = time.time()
knn.fit(X_train, y_train)  # Very fast!
train_time = time.time() - start

# Prediction is slow (computes distances)
start = time.time()
predictions = knn.predict(X_test)  # Slower
predict_time = time.time() - start

print(f"Training time: {train_time:.6f}s (just storing)")
print(f"Prediction time: {predict_time:.4f}s (computing distances)")
```

**Related Terms:** Lazy Learning, Eager Learning, KNN

---

### K Value

**Definition:** The number of nearest neighbors used for classification or regression. Critical hyperparameter affecting model performance.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

print("Effect of K:")
for k in range(1, 16):
    pipeline.set_params(knn__n_neighbors=k)
    scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
    print(f"  K={k:2d}: {scores.mean():.4f}")
```

**Guidelines:**
- Small K (1-3): Low bias, high variance (overfitting)
- Medium K (5-10): Good balance
- Large K (>10): High bias, low variance (underfitting)
- Use odd K for binary classification (avoid ties)

**Related Terms:** Overfitting, Underfitting, Bias-Variance Tradeoff

---

### Distance Metric

**Definition:** A function that measures the similarity or dissimilarity between data points. KNN uses distances to find nearest neighbors.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

metrics = ['euclidean', 'manhattan', 'chebyshev', 'minkowski']

for metric in metrics:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=5, metric=metric))
    ])
    scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
    print(f"{metric:>12}: {scores.mean():.4f}")
```

**Related Terms:** Euclidean, Manhattan, Cosine Similarity

---

### Euclidean Distance

**Definition:** The straight-line distance between two points in Euclidean space. Most common metric for KNN.

**Formula:**
```
d(x, y) = √(Σ(xᵢ - yᵢ)²)
```

**Example:**
```python
import numpy as np
from sklearn.metrics import euclidean_distances

# Two points
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

# Manual calculation
dist_manual = np.sqrt(np.sum((x - y) ** 2))
print(f"Manual Euclidean distance: {dist_manual:.4f}")

# Sklearn
dist_sklearn = euclidean_distances([x], [y])[0, 0]
print(f"Sklearn Euclidean distance: {dist_sklearn:.4f}")
```

**Related Terms:** Manhattan Distance, Minkowski Distance

---

### Manhattan Distance

**Definition:** The sum of absolute differences between coordinates. Also known as L1 distance or city block distance.

**Formula:**
```
d(x, y) = Σ|xᵢ - yᵢ|
```

**Example:**
```python
import numpy as np
from sklearn.metrics import pairwise_distances

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

# Manual calculation
dist_manual = np.sum(np.abs(x - y))
print(f"Manual Manhattan distance: {dist_manual:.4f}")

# Sklearn
dist_sklearn = pairwise_distances([x], [y], metric='manhattan')[0, 0]
print(f"Sklearn Manhattan distance: {dist_sklearn:.4f}")
```

**When to use:**
- Sparse data
- High-dimensional data
- When outliers are present

**Related Terms:** Euclidean Distance, L1 Norm

---

### Chebyshev Distance

**Definition:** The maximum absolute difference between coordinates. Also known as L∞ distance.

**Formula:**
```
d(x, y) = max|xᵢ - yᵢ|
```

**Example:**
```python
import numpy as np

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

dist = np.max(np.abs(x - y))
print(f"Chebyshev distance: {dist:.4f}")
```

**Related Terms:** Manhattan Distance, L∞ Norm

---

### Uniform Weights

**Definition:** All K neighbors contribute equally to the prediction, regardless of distance. This is the default setting.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5, weights='uniform'))
])

scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"Uniform weights: {scores.mean():.4f}")
```

**Related Terms:** Distance Weights, Majority Vote

---

### Distance Weights

**Definition:** Closer neighbors have more influence on the prediction than farther neighbors. Weight is inversely proportional to distance.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5, weights='distance'))
])

scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"Distance weights: {scores.mean():.4f}")
```

**Benefits:**
- Reduces impact of outliers
- More robust than uniform weights
- Often improves accuracy

**Related Terms:** Uniform Weights, Inverse Distance Weighting

---

### Majority Vote

**Definition:** The final prediction in KNN classification is the class that appears most frequently among the K nearest neighbors.

**Example:**
```python
import numpy as np
from scipy import stats

# Example: 5 neighbors with labels
neighbor_labels = np.array([0, 0, 1, 0, 1])

# Majority vote
prediction = stats.mode(neighbor_labels, keepdims=False)[0]
print(f"Neighbor labels: {neighbor_labels}")
print(f"Majority vote prediction: {prediction}")

# Manual calculation
from collections import Counter
counts = Counter(neighbor_labels)
manual_prediction = counts.most_common(1)[0][0]
print(f"Manual majority vote: {manual_prediction}")
```

**Related Terms:** KNN Classification, Voting

---

### KNN Regression

**Definition:** KNN variant that predicts continuous values by averaging the values of K nearest neighbors.

**Example:**
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

knn_reg = KNeighborsRegressor(n_neighbors=5, weights='distance')
knn_reg.fit(X_train_scaled, y_train)

y_pred = knn_reg.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
print(f"KNN Regression R²: {r2:.4f}")
```

**Related Terms:** KNN Classification, Regression

---

### Curse of Dimensionality

**Definition:** In high-dimensional spaces, distance metrics become less meaningful as all points become approximately equidistant.

**Example:**
```python
import numpy as np

np.random.seed(42)

# Generate random points in different dimensions
for d in [2, 10, 50, 100]:
    X = np.random.randn(100, d)
    
    # Calculate distances
    from sklearn.metrics import pairwise_distances
    distances = pairwise_distances(X)
    
    # Get max and min distances (excluding diagonal)
    np.fill_diagonal(distances, np.inf)
    max_dist = distances.min(axis=1).max()
    min_dist = distances.min(axis=1).min()
    
    ratio = max_dist / min_dist
    print(f"Dimensions={d:3d}: Max/Min distance ratio={ratio:.2f}")
# As dimensions increase, ratio approaches 1
```

**Impact on KNN:**
- All neighbors become equally distant
- Distance-based classification becomes meaningless
- Solution: Use PCA or feature selection

**Related Terms:** High-Dimensional Data, Feature Selection, PCA

---

### Feature Scaling

**Definition:** Normalizing features to have similar scales. Critical for KNN because it's distance-based.

**Example:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=300, n_features=10, 
                           n_informative=5, random_state=42)

# Without scaling
knn_unscaled = KNeighborsClassifier(n_neighbors=5)
scores_unscaled = cross_val_score(knn_unscaled, X, y, cv=5, scoring='accuracy')

# With scaling
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5))
])
scores_scaled = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')

print(f"Without scaling: {scores_unscaled.mean():.4f}")
print(f"With scaling: {scores_scaled.mean():.4f}")
```

**Why scale?**
- Features with larger ranges dominate distance calculation
- E.g., income (10000-200000) dominates age (20-80)

**Related Terms:** StandardScaler, Normalization, Distance Metric

---

### Decision Boundary

**Definition:** The region in feature space where the classification changes from one class to another. KNN creates non-linear decision boundaries.

**Example:**
```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler

X, y = make_moons(n_samples=200, noise=0.1, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Different K values create different boundaries
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, k in zip(axes, [1, 5, 20]):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_scaled, y)
    
    # Create mesh grid
    h = 0.1
    x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
    y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.RdYlBu)
    ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolors='black')
    ax.set_title(f'K={k}')

plt.tight_layout()
plt.savefig('knn_decision_boundaries.png', dpi=100)
plt.show()
```

**Observations:**
- Small K: Complex, jagged boundaries (overfitting)
- Large K: Smooth, simple boundaries (underfitting)

**Related Terms:** K Value, Overfitting, Underfitting

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Euclidean Distance | √(Σ(xᵢ - yᵢ)²) |
| Manhattan Distance | Σ\|xᵢ - yᵢ\| |
| Chebyshev Distance | max\|xᵢ - yᵢ\| |
| Minkowski Distance | (Σ\|xᵢ - yᵢ\|^p)^(1/p) |
| Distance Weight | 1/d(x, neighbor) |

---

## Code Snippets Quick Reference

```python
# KNN Classification
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5, weights='distance', metric='euclidean')
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

# KNN Regression
from sklearn.neighbors import KNeighborsRegressor
knn_reg = KNeighborsRegressor(n_neighbors=5)
knn_reg.fit(X_train_scaled, y_train)

# Manual KNN (for understanding)
distances = np.sqrt(np.sum((X_train - X_new) ** 2, axis=1))
k_nearest = np.argsort(distances)[:K]
prediction = np.bincount(y_train[k_nearest]).argmax()

# Feature Scaling (ESSENTIAL)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Pipeline
from sklearn.pipeline import Pipeline
pipe = Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier())])
```

---

## Common Pitfalls

1. **Not scaling** — Features with larger ranges dominate
2. **Wrong K** — Too small = overfit, too large = underfit
3. **Irrelevant features** — Add noise to distance calculation
4. **High dimensions** — Curse of dimensionality
5. **Large datasets** — Slow prediction time

---

## Further Reading

- [Scikit-learn - Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html)
- [Wikipedia - KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)
- [Machine Learning Mastery - KNN](https://machinelearningmastery.com/k-nearest-neighbors-algorithm-for-machine-learning/)
