# Glossary: Logistic Regression (Lecture 15)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Logistic Regression | Classification algorithm using sigmoid function | `LogisticRegression()` |
| Sigmoid Function | Maps any value to probability (0-1) | σ(z) = 1/(1+e^(-z)) |
| Binary Classification | Two classes (0 or 1) | Spam/Not Spam |
| Multi-class Classification | More than two classes | Iris species |
| Decision Boundary | Threshold separating classes | P=0.5 |
| Log Loss | Cost function for logistic regression | Cross-entropy |
| Odds Ratio | Ratio of probability of event to non-event | p/(1-p) |
| Logit | Log of odds ratio | ln(p/(1-p)) |
| Softmax | Generalizes sigmoid to multi-class | For K classes |
| Class Weight | Adjusts for imbalanced datasets | `class_weight='balanced'` |
| Threshold | Cutoff probability for classification | 0.5 (default) |
| Precision | TP/(TP+FP) - accuracy of positive predictions | 0.95 |
| Recall | TP/(TP+FN) - ability to find all positives | 0.90 |
| F1 Score | Harmonic mean of precision and recall | 0.92 |
| Confusion Matrix | Table of TP, TN, FP, FN counts | 2x2 matrix |

---

## Detailed Term Definitions

### Logistic Regression

**Definition:** A statistical model that uses a logistic (sigmoid) function to model the probability of a binary outcome. Despite its name, it's a classification algorithm, not regression.

**Key Properties:**
- Output is a probability between 0 and 1
- Uses sigmoid function to map linear combination to probability
- Can be extended to multi-class problems

**Example:**
```python
from sklearn.linear_model import LogisticRegression
import numpy as np

# Binary classification
X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])
y = np.array([0, 0, 0, 1, 1])

model = LogisticRegression(random_state=42)
model.fit(X, y)

# Predict
X_new = np.array([[3.5, 4.5]])
prediction = model.predict(X_new)
probability = model.predict_proba(X_new)

print(f"Prediction: {prediction[0]}")
print(f"Probabilities: {probability[0]}")
```

**Related Terms:** Sigmoid Function, Binary Classification, Linear Classifier

---

### Sigmoid Function

**Definition:** A mathematical function that maps any real number to a value between 0 and 1, used as the activation function in logistic regression.

**Formula:**
```
σ(z) = 1 / (1 + e^(-z))
```

**Example:**
```python
import numpy as np

def sigmoid(z):
    """Sigmoid activation function."""
    return 1 / (1 + np.exp(-z))

# Test values
z_values = np.array([-10, -5, 0, 5, 10])
sigmoid_values = sigmoid(z_values)

for z, s in zip(z_values, sigmoid_values):
    print(f"σ({z:3d}) = {s:.6f}")

# Output:
# σ(-10) = 0.000045
# σ( -5) = 0.006693
# σ(  0) = 0.500000
# σ(  5) = 0.993307
# σ( 10) = 0.999955
```

**Properties:**
- Always outputs between 0 and 1
- σ(0) = 0.5 (decision boundary)
- Symmetric around z=0
- S-shaped curve

**Related Terms:** Logistic Regression, Decision Boundary, Logit Function

---

### Binary Classification

**Definition:** Classification with exactly two classes, typically labeled as 0 and 1 (negative and positive).

**Example:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Create binary classification data
X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Classes: {np.unique(y)}")
print(f"Accuracy: {accuracy:.4f}")
```

**Related Terms:** Multi-class Classification, Positive/Negative Class

---

### Multi-class Classification

**Definition:** Classification with more than two classes. Logistic regression extends to multi-class using One-vs-Rest or Softmax.

**Example:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Iris dataset (3 classes)
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Classes: {iris.target_names}")
print(f"Accuracy: {accuracy:.4f}")

# Predict probabilities for each class
probabilities = model.predict_proba(X_test[:5])
print(f"\nSample probabilities:\n{probabilities}")
```

**Related Terms:** One-vs-Rest, Softmax Regression, Iris Dataset

---

### Decision Boundary

**Definition:** The threshold where the model switches between class predictions. For binary logistic regression, typically P(class=1) > 0.5.

**Example:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Simple 2D data
X = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5],
              [1, 5], [2, 4], [3, 3], [4, 2], [5, 1]])
y = np.array([0, 0, 0, 1, 1, 1, 1, 0, 0, 0])

model = LogisticRegression(random_state=42)
model.fit(X, y)

# Create mesh grid
h = 0.1
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# Predict on mesh
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.RdYlBu)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolors='black')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Decision Boundary')
plt.savefig('decision_boundary.png', dpi=100)
plt.show()
```

**Related Terms:** Threshold, Class Separation, Linear Boundary

---

### Log Loss (Cross-Entropy)

**Definition:** The cost function used in logistic regression, penalizing confident wrong predictions more heavily than correct ones.

**Formula:**
```
J(β) = -(1/n) Σ[yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]
```

**Example:**
```python
import numpy as np
from sklearn.metrics import log_loss

y_true = np.array([0, 1, 1, 0, 1])
y_prob = np.array([0.1, 0.9, 0.8, 0.2, 0.7])

loss = log_loss(y_true, y_prob)
print(f"Log Loss: {loss:.4f}")

# Manual calculation
eps = 1e-15  # Small value to avoid log(0)
y_prob = np.clip(y_prob, eps, 1 - eps)
manual_loss = -np.mean(y_true * np.log(y_prob) + (1 - y_true) * np.log(1 - y_prob))
print(f"Manual Log Loss: {manual_loss:.4f}")
```

**Properties:**
- Always non-negative
- 0 when predictions are perfect
- Penalizes confident wrong predictions heavily

**Related Terms:** Cross-Entropy, Cost Function, Binary Cross-Entropy

---

### Odds Ratio

**Definition:** The ratio of the probability of an event occurring to the probability of it not occurring. Odds = p / (1-p).

**Example:**
```python
import numpy as np

def odds(p):
    """Calculate odds from probability."""
    return p / (1 - p)

def log_odds(p):
    """Calculate log-odds (logit) from probability."""
    return np.log(odds(p))

# Example: Disease probability
p_disease = 0.1
odds_disease = odds(p_disease)
log_odds_disease = log_odds(p_disease)

print(f"Probability: {p_disease}")
print(f"Odds: {odds_disease:.4f}")
print(f"Log-odds: {log_odds_disease:.4f}")

# Interpretation
print(f"\nIf probability = 0.1 (10%):")
print(f"  Odds = {odds_disease:.4f} (1 in {1/odds_disease:.1f})")
```

**Related Terms:** Logit Function, Probability, Sigmoid Function

---

### Logit Function

**Definition:** The inverse of the sigmoid function. Maps probabilities (0-1) to real numbers (-∞ to +∞). Also called the log-odds.

**Formula:**
```
logit(p) = ln(p / (1-p))
```

**Example:**
```python
import numpy as np

def logit(p):
    """Logit function (inverse sigmoid)."""
    return np.log(p / (1 - p))

def sigmoid(z):
    """Sigmoid function."""
    return 1 / (1 + np.exp(-z))

# Test: logit and sigmoid are inverses
p = 0.7
z = logit(p)
p_back = sigmoid(z)

print(f"Original probability: {p}")
print(f"Logit (z): {z:.4f}")
print(f"Back to probability: {p_back:.4f}")

# Verify they're inverses
print(f"\nSigmoid(logit(p)) = p? {np.isclose(p, p_back)}")
```

**Related Terms:** Sigmoid Function, Odds Ratio, Inverse Link Function

---

### Softmax Function

**Definition:** Generalization of the sigmoid function to multi-class problems. Converts raw scores (logits) to probabilities that sum to 1.

**Formula:**
```
softmax(zₖ) = e^(zₖ) / Σⱼ e^(zⱼ)
```

**Example:**
```python
import numpy as np

def softmax(z):
    """Softmax function."""
    exp_z = np.exp(z - np.max(z))  # Subtract max for numerical stability
    return exp_z / exp_z.sum()

# Raw scores (logits) for 3 classes
logits = np.array([2.0, 1.0, 0.1])

probs = softmax(logits)
print(f"Logits: {logits}")
print(f"Softmax probabilities: {probs}")
print(f"Sum of probabilities: {probs.sum():.4f}")  # Always 1.0

# Interpretation
print(f"\nClass 0: {probs[0]*100:.1f}%")
print(f"Class 1: {probs[1]*100:.1f}%")
print(f"Class 2: {probs[2]*100:.1f}%")
```

**Related Terms:** Sigmoid Function, Multi-class Classification, Logits

---

### Class Weight

**Definition:** Parameters that adjust the importance of each class during training, useful for imbalanced datasets.

**Example:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report
import numpy as np

# Create imbalanced dataset
X, y = make_classification(n_samples=1000, n_features=10,
                           weights=[0.9, 0.1], random_state=42)

print(f"Class distribution: {np.bincount(y)}")

# Without class weighting
model_unweighted = LogisticRegression(random_state=42)
model_unweighted.fit(X, y)
y_pred_unweighted = model_unweighted.predict(X)

print("\nWithout class weighting:")
print(classification_report(y, y_pred_unweighted))

# With class weighting
model_weighted = LogisticRegression(class_weight='balanced', random_state=42)
model_weighted.fit(X, y)
y_pred_weighted = model_weighted.predict(X)

print("\nWith class weighting:")
print(classification_report(y, y_pred_weighted))
```

**Related Terms:** Imbalanced Data, Resampling, F1 Score

---

### Threshold

**Definition:** The probability cutoff for classifying a sample as positive. Default is 0.5 but can be adjusted for different business needs.

**Example:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score

X, y = make_classification(n_samples=200, n_features=10,
                           weights=[0.7, 0.3], random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

y_prob = model.predict_proba(X_test)[:, 1]

# Test different thresholds
for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
    y_pred = (y_prob >= threshold).astype(int)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    print(f"Threshold {threshold}: Precision={precision:.3f}, Recall={recall:.3f}")
```

**Related Terms:** Decision Boundary, Precision, Recall, Tradeoff

---

### Precision

**Definition:** The fraction of positive predictions that are actually positive. Measures exactness.

**Formula:**
```
Precision = TP / (TP + FP)
```

**Example:**
```python
from sklearn.metrics import precision_score
import numpy as np

y_true = np.array([1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([1, 0, 0, 1, 0, 1, 1, 0, 1, 0])

precision = precision_score(y_true, y_pred)
print(f"Precision: {precision:.4f}")

# Manual calculation
tp = np.sum((y_pred == 1) & (y_true == 1))
fp = np.sum((y_pred == 1) & (y_true == 0))
precision_manual = tp / (tp + fp)
print(f"Manual Precision: {precision_manual:.4f}")
```

**Interpretation:**
- Precision = 0.95 means 95% of positive predictions are correct
- High precision = few false positives

**Related Terms:** Recall, F1 Score, Confusion Matrix

---

### Recall (Sensitivity)

**Definition:** The fraction of actual positive cases that are correctly identified. Measures completeness.

**Formula:**
```
Recall = TP / (TP + FN)
```

**Example:**
```python
from sklearn.metrics import recall_score
import numpy as np

y_true = np.array([1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([1, 0, 0, 1, 0, 1, 1, 0, 1, 0])

recall = recall_score(y_true, y_pred)
print(f"Recall: {recall:.4f}")

# Manual calculation
tp = np.sum((y_pred == 1) & (y_true == 1))
fn = np.sum((y_pred == 0) & (y_true == 1))
recall_manual = tp / (tp + fn)
print(f"Manual Recall: {recall_manual:.4f}")
```

**Interpretation:**
- Recall = 0.90 means 90% of actual positives are found
- High recall = few false negatives

**Related Terms:** Precision, F1 Score, Sensitivity, True Positive Rate

---

### F1 Score

**Definition:** The harmonic mean of precision and recall, balancing both metrics. Useful when you need a single metric.

**Formula:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Example:**
```python
from sklearn.metrics import f1_score
import numpy as np

y_true = np.array([1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([1, 0, 0, 1, 0, 1, 1, 0, 1, 0])

f1 = f1_score(y_true, y_pred)
print(f"F1 Score: {f1:.4f}")

# Manual calculation
from sklearn.metrics import precision_score, recall_score
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1_manual = 2 * (precision * recall) / (precision + recall)
print(f"Manual F1: {f1_manual:.4f}")
```

**Properties:**
- Ranges from 0 to 1
- 1 = perfect precision and recall
- Harmonic mean penalizes extreme values

**Related Terms:** Precision, Recall, Accuracy

---

### Confusion Matrix

**Definition:** A table showing the counts of true positives, true negatives, false positives, and false negatives.

**Example:**
```python
from sklearn.metrics import confusion_matrix
import numpy as np

y_true = np.array([1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([1, 0, 0, 1, 0, 1, 1, 0, 1, 0])

cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)

tn, fp, fn, tp = cm.ravel()
print(f"\nTrue Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives: {tp}")
```

**Visual Interpretation:**
```
              Predicted
              0    1
Actual  0  [TN]  [FP]
        1  [FN]  [TP]
```

**Related Terms:** True Positive, False Positive, True Negative, False Negative

---

### Regularization (L1/L2)

**Definition:** Techniques to prevent overfitting by adding penalty terms to the cost function.

**Example:**
```python
from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.random.randn(100, 10)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# L2 regularization (default, Ridge)
model_l2 = LogisticRegression(penalty='l2', C=1.0, random_state=42)
model_l2.fit(X, y)
print(f"L2 coefficients: {model_l2.coef_[0][:3]}...")

# L1 regularization (Lasso, sparse solutions)
model_l1 = LogisticRegression(penalty='l1', solver='liblinear', 
                               C=0.1, random_state=42)
model_l1.fit(X, y)
print(f"L1 coefficients: {model_l1.coef_[0][:3]}...")

# L1 produces sparse solutions (many zeros)
print(f"\nL1 zero coefficients: {np.sum(model_l1.coef_ == 0)}")
```

**Parameters:**
- `C`: Inverse regularization strength (smaller = stronger)
- `penalty`: 'l1', 'l2', 'elasticnet', or 'none'

**Related Terms:** Ridge, Lasso, Overfitting, Sparse Solutions

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Sigmoid | σ(z) = 1 / (1 + e^(-z)) |
| Logit | logit(p) = ln(p / (1-p)) |
| Odds | odds(p) = p / (1-p) |
| Log Loss | J = -(1/n) Σ[y log(ŷ) + (1-y) log(1-ŷ)] |
| Softmax | softmax(zₖ) = e^(zₖ) / Σⱼ e^(zⱼ) |
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1 Score | 2 × (Precision × Recall) / (Precision + Recall) |

---

## Code Snippets Quick Reference

```python
# Binary Classification
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

# Multi-class Classification
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)  # y_train has 3+ classes

# Sigmoid Function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Softmax Function
def softmax(z):
    exp_z = np.exp(z - np.max(z))
    return exp_z / exp_z.sum()

# Evaluation
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, log_loss

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Regularization
model = LogisticRegression(penalty='l1', C=0.1, solver='liblinear')

# Class Weighting
model = LogisticRegression(class_weight='balanced')

# Threshold Tuning
y_prob = model.predict_proba(X_test)[:, 1]
y_pred_custom = (y_prob >= 0.3).astype(int)
```

---

## Common Pitfalls

1. **Using for regression** — Logistic regression is for classification
2. **Not scaling features** — Affects convergence and coefficients
3. **Ignoring class imbalance** — Use class_weight='balanced'
4. **Only looking at accuracy** — Check precision, recall, F1
5. **Wrong threshold** — Adjust based on business needs

---

## Further Reading

- [Scikit-learn - Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [Wikipedia - Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression)
- [STATSmodels - Logit](https://www.statsmodels.org/stable/discrete.html#logit)
