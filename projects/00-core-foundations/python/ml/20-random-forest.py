"""
W3Schools Python Tutorial - ML NN: Random Forest
==================================================
Topics: RandomForestClassifier, Ensemble Methods, Feature Importance

Run: python 20-random-forest.py
Reference: https://www.w3schools.com/python/ml_random_forest.asp
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

# ============================================================
# What is Random Forest?
# ============================================================

# Example 1: Random forest concept
print("Example 1: Random Forest Concept")
print("Random forest is an ensemble of decision trees")
print("Each tree is trained on a random subset of data")
print("Final prediction is the majority vote (classification) or average (regression)")

# ============================================================
# Creating Random Forest
# ============================================================

# Example 2: Generate data
print("\nExample 2: Generate Data")
np.random.seed(42)
X, y = make_classification(
    n_samples=500, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes: {np.unique(y)}")

# Example 3: Train/test split
print("\nExample 3: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# ============================================================
# RandomForestClassifier
# ============================================================

# Example 4: Basic random forest
print("\nExample 4: RandomForestClassifier")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Number of trees: {rf.n_estimators}")
print(f"Accuracy: {accuracy:.4f}")

# Example 5: Ensemble methods
print("\nExample 5: Ensemble Methods")
print("Random forest uses:")
print("  - Bagging: Training on random subsets")
print("  - Feature randomness: Random feature subsets at each split")
print("  - Majority voting: Combining tree predictions")

# ============================================================
# Comparing with Single Decision Tree
# ============================================================

# Example 6: Random forest vs single tree
print("\nExample 6: Random Forest vs Single Tree")
# Single decision tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
acc_dt = accuracy_score(y_test, dt.predict(X_test))

# Random forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
acc_rf = accuracy_score(y_test, rf.predict(X_test))

print(f"Single Decision Tree: {acc_dt:.4f}")
print(f"Random Forest: {acc_rf:.4f}")
print(f"Improvement: {(acc_rf - acc_dt)*100:.2f}%")

# ============================================================
# Feature Importance
# ============================================================

# Example 7: Feature importance
print("\nExample 7: Feature Importance")
importances = rf.feature_importances_
feature_names = [f"Feature {i}" for i in range(X.shape[1])]

print("Feature importances:")
for name, importance in sorted(zip(feature_names, importances), 
                              key=lambda x: x[1], reverse=True):
    print(f"  {name}: {importance:.4f}")

# ============================================================
# Random Forest Parameters
# ============================================================

# Example 8: Key parameters
print("\nExample 8: Key Parameters")
print("n_estimators: Number of trees (more = better but slower)")
print("max_depth: Maximum tree depth (None = unlimited)")
print("min_samples_split: Minimum samples to split a node")
print("min_samples_leaf: Minimum samples in a leaf")
print("max_features: Number of features to consider for best split")

# Example 9: Parameter tuning
print("\nExample 9: Parameter Tuning")
results = []
for n_trees in [10, 50, 100, 200]:
    rf = RandomForestClassifier(n_estimators=n_trees, random_state=42)
    rf.fit(X_train, y_train)
    acc = accuracy_score(y_test, rf.predict(X_test))
    results.append({'n_trees': n_trees, 'accuracy': acc})
    print(f"  {n_trees:3d} trees: Accuracy = {acc:.4f}")

# ============================================================
# Random Forest for Regression
# ============================================================

# Example 10: Regression
print("\nExample 10: Random Forest for Regression")
np.random.seed(42)
X_reg = np.random.rand(200, 5)
y_reg = 3 * X_reg[:, 0] + 2 * X_reg[:, 1] + np.random.randn(200) * 0.5

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train_reg, y_train_reg)

r2_train = r2_score(y_train_reg, rf_reg.predict(X_train_reg))
r2_test = r2_score(y_test_reg, rf_reg.predict(X_test_reg))

print(f"R^2 (train): {r2_train:.4f}")
print(f"R^2 (test): {r2_test:.4f}")

# ============================================================
# OOB Score
# ============================================================

# Example 11: Out-of-bag score
print("\nExample 11: Out-of-Bag Score")
rf_oob = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)
rf_oob.fit(X_train, y_train)

print(f"OOB Score: {rf_oob.oob_score_:.4f}")
print("OOB score uses unused samples for validation (free validation!)")

# ============================================================
# When to Use Random Forest
# ============================================================

# Example 12: Use cases
print("\nExample 12: When to Use Random Forest")
print("Advantages:")
print("  - Robust to overfitting")
print("  - Handles high-dimensional data")
print("  - Provides feature importance")
print("  - Works with missing values")

print("\nDisadvantages:")
print("  - Less interpretable than single tree")
print("  - Slower prediction than single tree")
print("  - Can overfit with very noisy data")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Random forest combines multiple decision trees")
print("- Each tree trained on random data/feature subsets")
print("- More accurate and robust than single trees")
print("- Provides feature importance")
print("- Use for classification and regression")
print("- Tune n_estimators for performance")
print("="*60)