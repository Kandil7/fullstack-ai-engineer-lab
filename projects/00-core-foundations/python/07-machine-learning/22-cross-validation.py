"""
W3Schools Python Tutorial - ML NN: Cross Validation
====================================================
Topics: KFold, cross_val_score, Stratified Split

Run: python 22-cross-validation.py
Reference: https://www.w3schools.com/python/ml_cross_validation.asp
"""

import numpy as np
from sklearn.model_selection import (KFold, cross_val_score, 
                                   StratifiedKFold, train_test_split)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, r2_score
from sklearn.datasets import make_classification, make_regression

# ============================================================
# Why Cross Validation?
# ============================================================

# Example 1: Problem with single split
print("Example 1: Problem with Single Split")
np.random.seed(42)
X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Multiple random splits give different results
print("Different random splits give different accuracy scores:")
for i in range(5):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"  Split {i+1}: {acc:.4f}")

print("\nCross-validation gives more reliable estimates!")

# ============================================================
# K-Fold Cross Validation
# ============================================================

# Example 2: K-Fold concept
print("\nExample 2: K-Fold Concept")
print("K-Fold splits data into K equal folds")
print("Train on K-1 folds, test on remaining fold")
print("Repeat K times, each fold gets to be test set once")

# Example 3: Manual K-Fold
print("\nExample 3: Manual K-Fold")
kf = KFold(n_splits=5, shuffle=True, random_state=42)

scores = []
for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    score = accuracy_score(y_val, model.predict(X_val))
    scores.append(score)

print(f"Fold scores: {[f'{s:.4f}' for s in scores]}")
print(f"Mean: {np.mean(scores):.4f} +/- {np.std(scores):.4f}")

# ============================================================
# cross_val_score
# ============================================================

# Example 4: Using cross_val_score
print("\nExample 4: cross_val_score")
model = LogisticRegression(random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"CV scores: {[f'{s:.4f}' for s in cv_scores]}")
print(f"Mean: {cv_scores.mean():.4f}")
print(f"Std: {cv_scores.std():.4f}")

# ============================================================
# Stratified K-Fold
# ============================================================

# Example 5: Stratified split
print("\nExample 5: Stratified K-Fold")
print("Stratified ensures each fold has same class distribution")

# Check class distribution
print(f"Original class distribution: {np.bincount(y)}")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
stratified_scores = []

for train_idx, val_idx in skf.split(X, y):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    # Check distribution
    train_dist = np.bincount(y_train)
    val_dist = np.bincount(y_val)
    
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    score = accuracy_score(y_val, model.predict(X_val))
    stratified_scores.append(score)

print(f"Stratified CV scores: {[f'{s:.4f}' for s in stratified_scores]}")
print(f"Mean: {np.mean(stratified_scores):.4f}")

# ============================================================
# Different Scoring Metrics
# ============================================================

# Example 6: Different metrics
print("\nExample 6: Different Scoring Metrics")
model = LogisticRegression(random_state=42)

# Accuracy
scores_acc = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores_acc.mean():.4f}")

# F1
scores_f1 = cross_val_score(model, X, y, cv=5, scoring='f1')
print(f"F1 Score: {scores_f1.mean():.4f}")

# Precision
scores_prec = cross_val_score(model, X, y, cv=5, scoring='precision')
print(f"Precision: {scores_prec.mean():.4f}")

# Recall
scores_rec = cross_val_score(model, X, y, cv=5, scoring='recall')
print(f"Recall: {scores_rec.mean():.4f}")

# ============================================================
# Cross Validation for Regression
# ============================================================

# Example 7: Regression CV
print("\nExample 7: Cross Validation for Regression")
X_reg, y_reg = make_regression(n_samples=200, n_features=5, noise=0.5, random_state=42)

model_reg = LinearRegression()
cv_scores_r2 = cross_val_score(model_reg, X_reg, y_reg, cv=5, scoring='r2')
cv_scores_neg_mse = cross_val_score(model_reg, X_reg, y_reg, cv=5, scoring='neg_mean_squared_error')

print(f"R^2 scores: {[f'{s:.4f}' for s in cv_scores_r2]}")
print(f"Mean R^2: {cv_scores_r2.mean():.4f}")
print(f"Mean MSE: {-cv_scores_neg_mse.mean():.4f}")

# ============================================================
# Choosing Number of Folds
# ============================================================

# Example 8: Different K values
print("\nExample 8: Choosing K")
model = LogisticRegression(random_state=42)
results = []

for k in [3, 5, 10, 15, 20]:
    scores = cross_val_score(model, X, y, cv=k, scoring='accuracy')
    results.append({'k': k, 'mean': scores.mean(), 'std': scores.std()})
    print(f"K={k:2d}: Mean={scores.mean():.4f} +/- {scores.std():.4f}")

# ============================================================
# Cross Validation vs Holdout
# ============================================================

# Example 9: Comparison
print("\nExample 9: CV vs Holdout")
print("Holdout (single split):")
print("  - Fast")
print("  - Simple")
print("  - Less reliable")
print("  - Wastes data")

print("\nCross-validation:")
print("  - More reliable")
print("  - Uses all data for training")
print("  - Slower")
print("  - Better for model selection")

# ============================================================
# Practical Tips
# ============================================================

# Example 10: Tips
print("\nExample 10: Practical Tips")
print("1. Use 5 or 10 folds (good balance)")
print("2. Use stratified for classification")
print("3. Shuffle data before splitting")
print("4. Use cross-validation for model selection")
print("5. Report mean +/- std of CV scores")
print("6. Don't use CV for final evaluation (use test set)")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Cross-validation gives more reliable performance estimates")
print("- K-Fold splits data into K folds")
print("- Stratified K-Fold preserves class distribution")
print("- Use cross_val_score for easy implementation")
print("- Use 5 or 10 folds for good balance")
print("- Always report mean +/- std of CV scores")
print("="*60)