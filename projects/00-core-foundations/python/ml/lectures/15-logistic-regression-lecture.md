# Lecture 15: Logistic Regression

## Topic Overview

Logistic Regression is one of the most fundamental algorithms for classification tasks. Despite its name, it's used for predicting categorical outcomes (classes), not continuous values. This lecture covers the sigmoid function, binary and multi-class classification, model evaluation, and practical implementation with scikit-learn.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the difference between regression and classification
2. Explain the sigmoid function and how it maps outputs to probabilities
3. Implement binary classification with LogisticRegression
4. Interpret model coefficients and probabilities
5. Evaluate classifiers using accuracy, confusion matrix, and F1 score
6. Extend logistic regression to multi-class problems
7. Apply regularization to prevent overfitting

---

## Key Concepts

### 1. Regression vs Classification

| Aspect | Regression | Classification |
|--------|-----------|----------------|
| **Target** | Continuous value | Discrete class label |
| **Example** | Predict house price | Predict spam/not spam |
| **Output** | Any real number | Class label or probability |
| **Algorithm** | Linear Regression | Logistic Regression |

### 2. The Sigmoid Function

Logistic regression uses the sigmoid function to map any real number to a probability (0-1):

```
σ(z) = 1 / (1 + e^(-z))
```

Where `z = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ`

**Key Properties:**
- Output always between 0 and 1
- σ(0) = 0.5
- As z → +∞, σ(z) → 1
- As z → -∞, σ(z) → 0

### 3. Decision Boundary

The decision boundary is where the model switches between classes:
- If P(class=1) > 0.5 → Predict class 1
- If P(class=1) < 0.5 → Predict class 0

### 4. Cost Function (Log Loss)

```
J(β) = -(1/n) Σ[yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]
```

This cost function penalizes confident wrong predictions heavily.

---

## Code Examples

### Example 1: Sigmoid Function

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    """Sigmoid activation function."""
    return 1 / (1 + np.exp(-z))

# Sigmoid maps any value to 0-1
z_values = np.linspace(-10, 10, 100)
sigmoid_values = sigmoid(z_values)

# Key points
print("Sigmoid function properties:")
print(f"  σ(-10) = {sigmoid(-10):.6f}")
print(f"  σ(0) = {sigmoid(0):.4f}")
print(f"  σ(10) = {sigmoid(10):.6f}")

# Plot
plt.figure(figsize=(8, 4))
plt.plot(z_values, sigmoid_values, 'b-', linewidth=2)
plt.axhline(y=0.5, color='r', linestyle='--', label='Decision Boundary (0.5)')
plt.axvline(x=0, color='gray', linestyle='--')
plt.xlabel('z')
plt.ylabel('σ(z)')
plt.title('Sigmoid Function')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('sigmoid_function.png', dpi=100)
plt.show()
```

**Output:**
```
Sigmoid function properties:
  σ(-10) = 0.000045
  σ(0) = 0.5000
  σ(10) = 0.999955
```

### Example 2: Binary Classification

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Generate binary classification data
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=2, n_redundant=0,
    n_informative=2, random_state=42, n_clusters_per_class=1
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes: {np.unique(y)} (0 and 1)")
print(f"Class distribution: {np.bincount(y)}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train logistic regression
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

print(f"\nCoefficients: {model.coef_[0]}")
print(f"Intercept: {model.intercept_[0]:.4f}")
```

### Example 3: Predictions and Probabilities

```python
# Predict classes
y_pred = model.predict(X_test_scaled)

# Predict probabilities
y_prob = model.predict_proba(X_test_scaled)

print("First 5 predictions:")
for i in range(5):
    print(f"  Sample {i+1}: Predicted class={y_pred[i]}, "
          f"P(class 0)={y_prob[i, 0]:.3f}, "
          f"P(class 1)={y_prob[i, 1]:.3f}")

# How probabilities work
print("\nProbability interpretation:")
print(f"  P(class=0) + P(class=1) = {y_prob[0].sum():.4f} (always 1)")
print(f"  Prediction: {'class 1' if y_prob[0, 1] > 0.5 else 'class 0'}")
```

### Example 4: Model Evaluation

```python
# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:\n{cm}")

tn, fp, fn, tp = cm.ravel()
print(f"\nTrue Negatives: {tn} (correctly predicted 0)")
print(f"False Positives: {fp} (predicted 1, actually 0)")
print(f"False Negatives: {fn} (predicted 0, actually 1)")
print(f"True Positives: {tp} (correctly predicted 1)")

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

**Output:**
```
Accuracy: 0.9167

Confusion Matrix:
[[26  2]
 [ 3 29]]

True Negatives: 26 (correctly predicted 0)
False Positives: 2 (predicted 1, actually 0)
False Negatives: 3 (predicted 0, actually 1)
True Positives: 29 (correctly predicted 1)

Classification Report:
              precision    recall  f1-score   support

           0       0.90      0.93      0.91        28
           1       0.94      0.91      0.92        32

    accuracy                           0.92        60
   macro avg       0.92      0.92      0.92        60
weighted avg       0.92      0.92      0.92        60
```

### Example 5: Multi-class Classification

```python
from sklearn.datasets import load_iris

# Iris dataset (3 classes)
iris = load_iris()
X_multi = iris.data
y_multi = iris.target

print(f"Iris dataset: {len(X_multi)} samples, {len(np.unique(y_multi))} classes")
print(f"Feature names: {iris.feature_names}")
print(f"Target names: {iris.target_names}")

# Split and scale
X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(
    X_multi, y_multi, test_size=0.2, random_state=42
)

scaler_m = StandardScaler()
X_train_m_scaled = scaler_m.fit_transform(X_train_m)
X_test_m_scaled = scaler_m.transform(X_test_m)

# Train multi-class model
model_multi = LogisticRegression(max_iter=200, random_state=42)
model_multi.fit(X_train_m_scaled, y_train_m)

# Evaluate
y_pred_m = model_multi.predict(X_test_m_scaled)
accuracy_m = accuracy_score(y_test_m, y_pred_m)

print(f"\nMulti-class accuracy: {accuracy_m:.4f}")
print("\nClassification Report:")
print(classification_report(y_test_m, y_pred_m, target_names=iris.target_names))
```

### Example 6: Regularization

```python
print("Logistic Regression Parameters:")
print("  C: Inverse regularization strength (smaller = stronger)")
print("  penalty: 'l1', 'l2', 'elasticnet', or 'none'")

# L2 regularization (default)
model_l2 = LogisticRegression(penalty='l2', C=1.0, random_state=42)
model_l2.fit(X_train_scaled, y_train)
acc_l2 = accuracy_score(y_test, model_l2.predict(X_test_scaled))
print(f"\nL2 regularization (C=1.0) accuracy: {acc_l2:.4f}")

# L1 regularization (sparse solutions)
model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=42)
model_l1.fit(X_train_scaled, y_train)
acc_l1 = accuracy_score(y_test, model_l1.predict(X_test_scaled))
print(f"L1 regularization (C=0.1) accuracy: {acc_l1:.4f}")

# Compare coefficients
print("\nCoefficient comparison:")
print(f"  L2 coefficients: {model_l2.coef_[0]}")
print(f"  L1 coefficients: {model_l1.coef_[0]}")
```

### Example 7: Decision Boundary Visualization

```python
import numpy as np
import matplotlib.pyplot as plt

def plot_decision_boundary(model, X, y, scaler=None):
    """Plot decision boundary for 2D data."""
    h = 0.02  # Step size
    
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    if scaler:
        mesh_points = scaler.transform(np.c_[xx.ravel(), yy.ravel()])
    else:
        mesh_points = np.c_[xx.ravel(), yy.ravel()]
    
    Z = model.predict(mesh_points)
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.RdYlBu)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolors='black')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Logistic Regression Decision Boundary')
    plt.savefig('decision_boundary.png', dpi=100)
    plt.show()

# Plot for our model
plot_decision_boundary(model, X_test_scaled, y_test, scaler)
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Linear Regression for Classification

```python
# WRONG: Using LinearRegression for classification
from sklearn.linear_model import LinearRegression

model_wrong = LinearRegression()
model_wrong.fit(X_train, y_train)
y_pred_wrong = model_wrong.predict(X_test)
# Outputs can be < 0 or > 1, meaningless for classification

# CORRECT: Use LogisticRegression
from sklearn.linear_model import LogisticRegression

model_correct = LogisticRegression()
model_correct.fit(X_train_scaled, y_train)
y_pred_correct = model_correct.predict(X_test_scaled)
# Always outputs class labels (0 or 1)
```

### Mistake 2: Not Scaling Features

```python
# Logistic regression is sensitive to feature scales
# Features with larger ranges dominate

# WRONG
model_unscaled = LogisticRegression()
model_unscaled.fit(X_train, y_train)  # Bad results

# CORRECT
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model_scaled = LogisticRegression()
model_scaled.fit(X_train_scaled, y_train)  # Good results
```

### Mistake 3: Ignoring Class Imbalance

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Create imbalanced dataset
X_imb, y_imb = make_classification(
    n_samples=1000, n_features=10, weights=[0.9, 0.1],
    random_state=42
)

print(f"Class distribution: {np.bincount(y_imb)}")

# WRONG: Not handling imbalance
model_wrong = LogisticRegression(random_state=42)
model_wrong.fit(X_train, y_train)
print("\nWithout class weighting:")
print(classification_report(y_test, model_wrong.predict(X_test)))

# CORRECT: Use class_weight='balanced'
model_correct = LogisticRegression(class_weight='balanced', random_state=42)
model_correct.fit(X_train, y_train)
print("\nWith class weighting:")
print(classification_report(y_test, model_correct.predict(X_test)))
```

### Mistake 4: Only Looking at Accuracy

```python
# Accuracy can be misleading with imbalanced classes
# If 90% are class 0, a model predicting all 0s has 90% accuracy!

# ALWAYS check precision, recall, and F1
from sklearn.metrics import classification_report

print("Always use classification_report for complete picture:")
print(classification_report(y_test, y_pred))
```

---

## Best Practices

### 1. Start with Simple Models

```python
# Logistic regression is a great baseline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)
baseline_score = accuracy_score(y_test, model.predict(X_test_scaled))

print(f"Logistic Regression baseline: {baseline_score:.4f}")
# Try more complex models only if needed
```

### 2. Use Cross-Validation

```python
from sklearn.model_selection import cross_val_score

model = LogisticRegression(random_state=42)
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')

print(f"CV Accuracy: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
```

### 3. Tune Hyperparameters

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}

grid_search = GridSearchCV(
    LogisticRegression(random_state=42),
    param_grid, cv=5, scoring='accuracy', n_jobs=-1
)
grid_search.fit(X_train_scaled, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV accuracy: {grid_search.best_score_:.4f}")
```

### 4. Interpret Probabilities

```python
# Use predict_proba for uncertainty estimation
y_prob = model.predict_proba(X_test)

# Low confidence predictions
low_confidence = np.max(y_prob, axis=1) < 0.6
print(f"Low confidence predictions: {low_confidence.sum()}")

# Use threshold tuning for specific needs
threshold = 0.3  # Lower threshold = more recall
y_pred_custom = (y_prob[:, 1] >= threshold).astype(int)
```

---

## Practice Exercises

### Exercise 1: Email Spam Classification

```python
"""
Build a logistic regression model for email spam detection.
1. Generate synthetic email data
2. Train logistic regression
3. Evaluate with appropriate metrics
4. Interpret which features are most predictive
"""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

np.random.seed(42)

# Features: word_count, has_link, has_attachment, capital_ratio, exclamation_count
X, y = make_classification(n_samples=500, n_features=5, n_informative=4,
                          weights=[0.7, 0.3], random_state=42)

# Your code here
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

# Feature importance
feature_names = ['word_count', 'has_link', 'has_attachment', 'capital_ratio', 'exclamation_count']
for name, coef in zip(feature_names, model.coef_[0]):
    print(f"{name}: {coef:.4f}")
```

### Exercise 2: Threshold Tuning

```python
"""
Experiment with different classification thresholds.
1. Train a logistic regression model
2. Test thresholds from 0.3 to 0.7
3. Plot precision-recall tradeoff
4. Choose threshold for business requirement
"""
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

# Your code here
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

y_prob = model.predict_proba(X_test_scaled)[:, 1]

precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)

# Find threshold for 90% recall
target_recall = 0.9
idx = np.argmin(np.abs(recalls - target_recall))
optimal_threshold = thresholds[idx]

print(f"For 90% recall, use threshold: {optimal_threshold:.3f}")
print(f"Precision at this threshold: {precisions[idx]:.3f}")

# Plot
plt.figure(figsize=(8, 6))
plt.plot(thresholds, precisions[:-1], label='Precision')
plt.plot(thresholds, recalls[:-1], label='Recall')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Precision-Recall vs Threshold')
plt.legend()
plt.grid(True)
plt.savefig('precision_recall_threshold.png', dpi=100)
plt.show()
```

### Exercise 3: Multi-class Problem

```python
"""
Solve a multi-class classification problem.
1. Use Iris dataset
2. Train logistic regression
3. Create confusion matrix
4. Identify which classes are hardest to classify
"""
from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Your code here
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=iris.target_names,
            yticklabels=iris.target_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.savefig('iris_confusion_matrix.png', dpi=100)
plt.show()

# Classification report
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Logistic Regression** | Classification algorithm using sigmoid function |
| **Sigmoid Function** | Maps any value to probability (0-1) |
| **Decision Boundary** | Threshold where class prediction changes |
| **Binary Classification** | Two classes (0 or 1) |
| **Multi-class** | Extends to multiple classes |
| **Regularization** | L1 (sparse) or L2 (default) to prevent overfitting |
| **Evaluation Metrics** | Accuracy, Precision, Recall, F1 Score |

### Key Takeaways

1. Logistic regression is for **classification**, not regression
2. The **sigmoid function** maps outputs to probabilities
3. Always **scale features** for logistic regression
4. Use **precision/recall/F1** for imbalanced datasets
5. **Regularization** (L1/L2) prevents overfitting

---

## Next Steps

- **Lecture 16**: K-Means Clustering — Unsupervised learning
- **Lecture 20**: Random Forest — Ensemble methods
- **Lecture 21**: SVM — Another powerful classifier

---

## References

- [W3Schools - Logistic Regression](https://www.w3schools.com/python/ml_logistic_regression.asp)
- [Scikit-learn Documentation - LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [Wikipedia - Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression)
