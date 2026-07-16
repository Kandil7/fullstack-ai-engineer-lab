"""
W3Schools Python Tutorial - ML NN: Logistic Regression
=======================================================
Topics: LogisticRegression, Sigmoid Function, Binary Classification

Run: python 15-logistic-regression.py
Reference: https://www.w3schools.com/python/ml_logistic_regression.asp
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# ============================================================
# What is Logistic Regression?
# ============================================================

# Example 1: Logistic regression concept
print("Example 1: Logistic Regression Concept")
print("Logistic regression is used for classification (not regression!)")
print("It predicts probability of belonging to a class")
print("Output: 0 or 1 (binary) or probabilities")

# ============================================================
# The Sigmoid Function
# ============================================================

# Example 2: Sigmoid function
print("\nExample 2: Sigmoid Function")
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Sigmoid maps any value to 0-1
z_values = np.array([-10, -5, 0, 5, 10])
sigmoid_values = sigmoid(z_values)

print("z values:", z_values)
print("Sigmoid(z):", sigmoid_values)
print("\nSigmoid properties:")
print("  - Output always between 0 and 1")
print("  - Output 0.5 when z = 0")
print("  - Approaches 0 as z -> -inf")
print("  - Approaches 1 as z -> +inf")

# ============================================================
# Binary Classification
# ============================================================

# Example 3: Generate binary classification data
print("\nExample 3: Binary Classification Data")
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=2, n_redundant=0,
    n_informative=2, random_state=42, n_clusters_per_class=1
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes: {np.unique(y)} (0 and 1)")
print(f"Class distribution: {np.bincount(y)}")

# ============================================================
# Logistic Regression Model
# ============================================================

# Example 4: Train/test split
print("\nExample 4: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Example 5: Fit logistic regression
print("\nExample 5: Logistic Regression Model")
# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

print("Model trained successfully")
print(f"Coefficients: {model.coef_[0]}")
print(f"Intercept: {model.intercept_[0]}")

# ============================================================
# Predictions and Probabilities
# ============================================================

# Example 6: Predictions
print("\nExample 6: Predictions")
# Predict classes
y_pred = model.predict(X_test_scaled)

# Predict probabilities
y_prob = model.predict_proba(X_test_scaled)

print("First 5 predictions:")
for i in range(5):
    print(f"  Sample {i+1}: Predicted class={y_pred[i]}, "
          f"Probability(class 0)={y_prob[i, 0]:.3f}, "
          f"Probability(class 1)={y_prob[i, 1]:.3f}")

# ============================================================
# Model Evaluation
# ============================================================

# Example 7: Accuracy
print("\nExample 7: Model Evaluation")
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Example 8: Confusion matrix
print("\nExample 8: Confusion Matrix")
cm = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{cm}")

tn, fp, fn, tp = cm.ravel()
print(f"\nTrue Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives: {tp}")

# Example 9: Classification report
print("\nExample 9: Classification Report")
print(classification_report(y_test, y_pred))

# ============================================================
# Decision Boundary
# ============================================================

# Example 10: Decision boundary concept
print("\nExample 10: Decision Boundary")
print("Logistic regression creates a linear decision boundary")
print("The boundary is where probability = 0.5")
print("Points on one side predicted as class 0, other side as class 1")

# ============================================================
# Multi-class Logistic Regression
# ============================================================

# Example 11: Multi-class classification
print("\nExample 11: Multi-class Logistic Regression")
from sklearn.datasets import load_iris

iris = load_iris()
X_multi = iris.data
y_multi = iris.target

X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
    X_multi, y_multi, test_size=0.2, random_state=42
)

# Scale features
scaler_multi = StandardScaler()
X_train_multi_scaled = scaler_multi.fit_transform(X_train_multi)
X_test_multi_scaled = scaler_multi.transform(X_test_multi)

# Train multi-class model
model_multi = LogisticRegression(max_iter=200, random_state=42)
model_multi.fit(X_train_multi_scaled, y_train_multi)

# Evaluate
y_pred_multi = model_multi.predict(X_test_multi_scaled)
accuracy_multi = accuracy_score(y_test_multi, y_pred_multi)

print(f"Iris dataset: {len(X_multi)} samples, {len(np.unique(y_multi))} classes")
print(f"Multi-class accuracy: {accuracy_multi:.4f}")

# ============================================================
# Logistic Regression Parameters
# ============================================================

# Example 12: Model parameters
print("\nExample 12: Logistic Regression Parameters")
print("Key parameters:")
print("  - C: Inverse regularization strength (smaller = stronger)")
print("  - penalty: 'l1', 'l2', 'elasticnet', or 'none'")
print("  - solver: Algorithm to use ('lbfgs', 'liblinear', etc.)")

# Example with L1 regularization
model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=42)
model_l1.fit(X_train_scaled, y_train)
acc_l1 = accuracy_score(y_test, model_l1.predict(X_test_scaled))

print(f"\nL1 regularization (C=0.1) accuracy: {acc_l1:.4f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Logistic regression is for classification, not regression")
print("- Uses sigmoid function to map outputs to probabilities")
print("- Binary classification: predict 0 or 1")
print("- Multi-class: extends to multiple classes")
print("- Evaluate with accuracy, confusion matrix, F1 score")
print("- Use regularization to prevent overfitting")
print("="*60)