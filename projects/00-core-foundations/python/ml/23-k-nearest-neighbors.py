"""
W3Schools Python Tutorial - ML NN: K-Nearest Neighbors
=======================================================
Topics: KNeighborsClassifier, Distance Metrics, Choosing K

Run: python 23-k-nearest-neighbors.py
Reference: https://www.w3schools.com/python/ml_knn.asp
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.datasets import make_classification, make_regression
from sklearn.preprocessing import StandardScaler

# ============================================================
# What is K-Nearest Neighbors?
# ============================================================

# Example 1: KNN concept
print("Example 1: KNN Concept")
print("KNN classifies based on majority vote of K nearest neighbors")
print("Simple but effective for many problems")
print("No training phase - stores all training data")

# ============================================================
# How KNN Works
# ============================================================

# Example 2: Manual KNN
print("\nExample 2: How KNN Works")
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

# ============================================================
# KNN Classifier
# ============================================================

# Example 3: Generate data
print("\nExample 3: Classification Data")
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=2, n_redundant=0,
    n_informative=2, random_state=42, n_clusters_per_class=1
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")

# Example 4: Train/test split
print("\nExample 4: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features (important for KNN!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Example 5: KNN classifier
print("\nExample 5: KNN Classifier")
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

y_pred = knn.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"K=5, Accuracy: {accuracy:.4f}")

# ============================================================
# Choosing K
# ============================================================

# Example 6: Different K values
print("\nExample 6: Choosing K")
results = []
for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, knn.predict(X_test_scaled))
    results.append({'k': k, 'accuracy': acc})

# Find best K
best = max(results, key=lambda x: x['accuracy'])
print(f"Best K: {best['k']} (Accuracy: {best['accuracy']:.4f})")

# Show trend
print("\nAccuracy vs K:")
for r in results[:10]:
    print(f"  K={r['k']:2d}: {r['accuracy']:.4f}")

# ============================================================
# Distance Metrics
# ============================================================

# Example 7: Different distance metrics
print("\nExample 7: Distance Metrics")
metrics = ['euclidean', 'manhattan', 'chebyshev', 'minkowski']
results = []

for metric in metrics:
    knn = KNeighborsClassifier(n_neighbors=5, metric=metric)
    knn.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, knn.predict(X_test_scaled))
    results.append({'metric': metric, 'accuracy': acc})
    print(f"{metric:>12}: {acc:.4f}")

# ============================================================
# KNN Regression
# ============================================================

# Example 8: KNN regression
print("\nExample 8: KNN Regression")
np.random.seed(42)
X_reg = np.random.rand(200, 1) * 10
y_reg = np.sin(X_reg.squeeze()) + np.random.randn(200) * 0.2

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

scaler_reg = StandardScaler()
X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_reg.transform(X_test_reg)

knn_reg = KNeighborsRegressor(n_neighbors=5)
knn_reg.fit(X_train_reg_scaled, y_train_reg)

r2 = r2_score(y_test_reg, knn_reg.predict(X_test_reg_scaled))
print(f"KNN Regression R^2: {r2:.4f}")

# ============================================================
# Weighted KNN
# ============================================================

# Example 9: Weighted voting
print("\nExample 9: Weighted KNN")
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

# ============================================================
# KNN Limitations
# ============================================================

# Example 10: Limitations
print("\nExample 10: KNN Limitations")
print("1. Slow prediction (computes distances to all points)")
print("2. Memory intensive (stores all training data)")
print("3. Sensitive to irrelevant features")
print("4. Sensitive to feature scaling")
print("5. Struggles with high dimensions")

# ============================================================
# When to Use KNN
# ============================================================

# Example 11: Use cases
print("\nExample 11: When to Use KNN")
print("Advantages:")
print("  - Simple and intuitive")
print("  - No training phase")
print("  - Works with any number of classes")
print("  - Naturally handles multi-class")

print("\nDisadvantages:")
print("  - Slow on large datasets")
print("  - Memory intensive")
print("  - Sensitive to feature scaling")
print("  - Struggles with high dimensions")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- KNN classifies based on K nearest neighbors")
print("- Choose K based on validation performance")
print("- Scale features before using KNN")
print("- Distance metrics affect performance")
print("- Weighted voting can improve results")
print("- Simple but slow on large datasets")
print("="*60)