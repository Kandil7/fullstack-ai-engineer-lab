"""
W3Schools Python Tutorial - ML NN: Decision Trees
==================================================
Topics: DecisionTreeClassifier, Tree Visualization, Gini/Entropy

Run: python 11-decision-tree.py
Reference: https://www.w3schools.com/python/ml_decision_tree.asp
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification

# ============================================================
# What is a Decision Tree?
# ============================================================

# Example 1: Decision tree concept
print("Example 1: Decision Tree Concept")
print("A decision tree splits data based on feature values")
print("Each node tests a feature, each branch is an outcome")
print("Leaves make the final prediction")

# ============================================================
# Creating a Decision Tree
# ============================================================

# Example 2: Generate classification data
print("\nExample 2: Generate Classification Data")
np.random.seed(42)
X, y = make_classification(
    n_samples=200, n_features=4, n_informative=3,
    n_redundant=1, n_classes=2, random_state=42
)

print(f"Features: {X.shape[1]}")
print(f"Samples: {X.shape[0]}")
print(f"Classes: {np.unique(y)}")

# Example 3: Train/test split
print("\nExample 3: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# ============================================================
# DecisionTreeClassifier
# ============================================================

# Example 4: Basic decision tree
print("\nExample 4: Basic Decision Tree")
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predictions
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Example 5: Tree structure
print("\nExample 5: Tree Structure")
print(f"Number of nodes: {clf.tree_.node_count}")
print(f"Number of leaves: {clf.get_n_leaves()}")
print(f"Tree depth: {clf.get_depth()}")

# ============================================================
# Gini Impurity vs Entropy
# ============================================================

# Example 6: Different criteria
print("\nExample 6: Gini vs Entropy")
# Gini impurity (default)
clf_gini = DecisionTreeClassifier(criterion='gini', random_state=42)
clf_gini.fit(X_train, y_train)
acc_gini = accuracy_score(y_test, clf_gini.predict(X_test))

# Entropy
clf_entropy = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf_entropy.fit(X_train, y_train)
acc_entropy = accuracy_score(y_test, clf_entropy.predict(X_test))

print(f"Gini impurity accuracy: {acc_gini:.4f}")
print(f"Entropy accuracy: {acc_entropy:.4f}")

# ============================================================
# Tree Parameters
# ============================================================

# Example 7: Controlling tree size
print("\nExample 7: Controlling Tree Size")
# Max depth
clf_depth3 = DecisionTreeClassifier(max_depth=3, random_state=42)
clf_depth3.fit(X_train, y_train)
acc_depth3 = accuracy_score(y_test, clf_depth3.predict(X_test))

# Min samples split
clf_split10 = DecisionTreeClassifier(min_samples_split=10, random_state=42)
clf_split10.fit(X_train, y_train)
acc_split10 = accuracy_score(y_test, clf_split10.predict(X_test))

# Min samples leaf
clf_leaf5 = DecisionTreeClassifier(min_samples_leaf=5, random_state=42)
clf_leaf5.fit(X_train, y_train)
acc_leaf5 = accuracy_score(y_test, clf_leaf5.predict(X_test))

print(f"max_depth=3: Accuracy={acc_depth3:.4f}, Depth={clf_depth3.get_depth()}")
print(f"min_samples_split=10: Accuracy={acc_split10:.4f}")
print(f"min_samples_leaf=5: Accuracy={acc_leaf5:.4f}")

# ============================================================
# Feature Importance
# ============================================================

# Example 8: Feature importance
print("\nExample 8: Feature Importance")
importances = clf.feature_importances_
feature_names = [f"Feature {i}" for i in range(X.shape[1])]

print("Feature importances:")
for name, importance in sorted(zip(feature_names, importances), 
                              key=lambda x: x[1], reverse=True):
    print(f"  {name}: {importance:.4f}")

# ============================================================
# Overfitting in Decision Trees
# ============================================================

# Example 9: Overfitting demonstration
print("\nExample 9: Overfitting")
# No constraints (will overfit)
clf_unlimited = DecisionTreeClassifier(random_state=42)
clf_unlimited.fit(X_train, y_train)

acc_train_unlimited = accuracy_score(y_train, clf_unlimited.predict(X_train))
acc_test_unlimited = accuracy_score(y_test, clf_unlimited.predict(X_test))

print(f"Unconstrained tree:")
print(f"  Training accuracy: {acc_train_unlimited:.4f}")
print(f"  Test accuracy: {acc_test_unlimited:.4f}")
print(f"  Gap: {acc_train_unlimited - acc_test_unlimited:.4f}")

# With pruning
clf_pruned = DecisionTreeClassifier(max_depth=5, random_state=42)
clf_pruned.fit(X_train, y_train)

acc_train_pruned = accuracy_score(y_train, clf_pruned.predict(X_train))
acc_test_pruned = accuracy_score(y_test, clf_pruned.predict(X_test))

print(f"\nPruned tree (max_depth=5):")
print(f"  Training accuracy: {acc_train_pruned:.4f}")
print(f"  Test accuracy: {acc_test_pruned:.4f}")
print(f"  Gap: {acc_train_pruned - acc_test_pruned:.4f}")

# ============================================================
# Classification Report
# ============================================================

# Example 10: Detailed evaluation
print("\nExample 10: Classification Report")
y_pred = clf_pruned.predict(X_test)
print(classification_report(y_test, y_pred))

# ============================================================
# Decision Tree for Regression
# ============================================================

# Example 11: Regression trees
print("\nExample 11: Decision Tree for Regression")
from sklearn.tree import DecisionTreeRegressor

np.random.seed(42)
X_reg = np.random.rand(100, 1) * 10
y_reg = np.sin(X_reg.squeeze()) + np.random.randn(100) * 0.2

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

reg = DecisionTreeRegressor(max_depth=3, random_state=42)
reg.fit(X_train_reg, y_train_reg)

r2_train = reg.score(X_train_reg, y_train_reg)
r2_test = reg.score(X_test_reg, y_test_reg)

print(f"Regression tree R^2 (train): {r2_train:.4f}")
print(f"Regression tree R^2 (test): {r2_test:.4f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Decision trees split data based on feature values")
print("- Use Gini or Entropy for split criterion")
print("- Control tree size to prevent overfitting")
print("- Feature importance shows which features matter most")
print("- Works for both classification and regression")
print("- Simple to interpret but prone to overfitting")
print("="*60)