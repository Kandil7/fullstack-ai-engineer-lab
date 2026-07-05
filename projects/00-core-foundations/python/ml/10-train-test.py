"""
W3Schools Python Tutorial - ML NN: Train/Test Split
====================================================
Topics: train_test_split, Why Split Data, Test Size, Random State

Run: python 10-train-test.py
Reference: https://www.w3schools.com/python/ml_train_test_split.asp
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ============================================================
# Why Split Data?
# ============================================================

# Example 1: Overfitting problem
print("Example 1: Why Split Data?")
print("If we train and test on the same data, we get overly optimistic results")
print("The model might memorize the data instead of learning patterns")

# Simulate overfitting
np.random.seed(42)
X = np.random.rand(50, 1) * 10
y = 2 * X.squeeze() + 3 + np.random.randn(50) * 0.5

# Train on all data
model = LinearRegression()
model.fit(X, y)
r2_all = r2_score(y, model.predict(X))
print(f"R^2 when training and testing on same data: {r2_all:.4f}")
print("(This is misleadingly high!)")

# ============================================================
# Basic Train/Test Split
# ============================================================

# Example 2: Simple split
print("\nExample 2: Basic Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Original dataset size: {len(X)}")
print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Example 3: Proper evaluation
print("\nExample 3: Proper Model Evaluation")
model = LinearRegression()
model.fit(X_train, y_train)

r2_train = r2_score(y_train, model.predict(X_train))
r2_test = r2_score(y_test, model.predict(X_test))

print(f"R^2 on training set: {r2_train:.4f}")
print(f"R^2 on test set: {r2_test:.4f}")
print("(Test R^2 is more realistic)")

# ============================================================
# Test Size Parameter
# ============================================================

# Example 4: Different test sizes
print("\nExample 4: Test Size Effects")
test_sizes = [0.1, 0.2, 0.3, 0.4]
results = []

for test_size in test_sizes:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    
    results.append({
        'test_size': test_size,
        'train_size': len(X_train),
        'test_size_n': len(X_test),
        'r2': r2
    })
    
    print(f"Test size {test_size:.0%}: Train={len(X_train)}, Test={len(X_test)}, R^2={r2:.4f}")

# ============================================================
# Random State
# ============================================================

# Example 5: Reproducibility
print("\nExample 5: Random State for Reproducibility")
print("Without random_state, each split is different:")
for i in range(3):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )
    print(f"  Split {i+1}: Test indices = {X_test[:3].flatten()}")

print("\nWith random_state=42, splits are always the same:")
for i in range(3):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"  Split {i+1}: Test indices = {X_test[:3].flatten()}")

# ============================================================
# Stratified Split
# ============================================================

# Example 6: Classification with stratify
print("\nExample 6: Stratified Split for Classification")
from sklearn.datasets import make_classification

X_clf, y_clf = make_classification(
    n_samples=200, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)

print(f"Original class distribution: {np.bincount(y_clf)}")

# Without stratify
X_train, X_test, y_train, y_test = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42
)
print(f"Without stratify: Train {np.bincount(y_train)}, Test {np.bincount(y_test)}")

# With stratify
X_train, X_test, y_train, y_test = train_test_split(
    X_clf, y_clf, test_size=0.2, stratify=y_clf, random_state=42
)
print(f"With stratify: Train {np.bincount(y_train)}, Test {np.bincount(y_test)}")

# ============================================================
# Splitting Multiple Arrays
# ============================================================

# Example 7: Splitting X and y together
print("\nExample 7: Splitting Multiple Arrays")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")

# ============================================================
# Cross-Validation Preview
# ============================================================

# Example 8: Why cross-validation?
print("\nExample 8: Cross-Validation Preview")
print("Single train/test split can be unstable")
print("Cross-validation splits data multiple times")
print("Gives more reliable performance estimate")

from sklearn.model_selection import cross_val_score

model = LinearRegression()
scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"5-fold CV R^2 scores: {scores}")
print(f"Mean R^2: {scores.mean():.4f} +/- {scores.std():.4f}")

# ============================================================
# Common Mistakes
# ============================================================

# Example 9: Data leakage
print("\nExample 9: Common Mistakes")
print("1. Scaling before split (use pipeline instead)")
print("2. Using too small test set (unreliable estimates)")
print("3. Not using random_state (non-reproducible)")
print("4. Not stratifying for imbalanced classes")
print("5. Tuning hyperparameters on test set")

# ============================================================
# Best Practices
# ============================================================

# Example 10: Recommended approach
print("\nExample 10: Best Practices")
print("1. Use 20-30% for test set")
print("2. Always set random_state for reproducibility")
print("3. Use stratify for classification")
print("4. Never look at test set during training")
print("5. Use cross-validation for model selection")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Always split data into train/test sets")
print("- Use 20-30% for test set")
print("- Set random_state for reproducibility")
print("- Use stratify for imbalanced classes")
print("- Cross-validation gives more reliable estimates")
print("- Never use test set for training decisions")
print("="*60)