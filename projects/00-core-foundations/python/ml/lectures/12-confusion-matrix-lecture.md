# Lecture 12: Confusion Matrix

## Topic Overview

The Confusion Matrix is a fundamental tool for evaluating classification models. It provides a detailed breakdown of correct and incorrect predictions, enabling the calculation of metrics like accuracy, precision, recall, and F1 score. This lecture covers all these metrics, when to use each, and how to interpret multi-class confusion matrices.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Construct and interpret a confusion matrix
2. Calculate accuracy, precision, recall, and F1 score
3. Understand the components: TP, TN, FP, FN
4. Choose the right metric for different problems
5. Generate and interpret classification reports
6. Handle multi-class confusion matrices
7. Understand the tradeoff between precision and recall

---

## Key Concepts

### 1. Confusion Matrix Structure

For binary classification:

```
                    Predicted
                 0       1
Actual  0  │  TN    │   FP   │
       1   │  FN    │   TP   │
```

- **True Positives (TP):** Correctly predicted positive
- **True Negatives (TN):** Correctly predicted negative
- **False Positives (FP):** Incorrectly predicted positive (Type I error)
- **False Negatives (FN):** Incorrectly predicted negative (Type II error)

### 2. Metrics

**Accuracy:**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```
Overall correctness.

**Precision:**
```
Precision = TP / (TP + FP)
```
Of all predicted positives, how many are actually positive?

**Recall (Sensitivity):**
```
Recall = TP / (TP + FN)
```
Of all actual positives, how many did we catch?

**F1 Score:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Harmonic mean of precision and recall.

### 3. When to Use Each Metric

| Metric | Best For | Example |
|--------|----------|---------|
| **Accuracy** | Balanced classes | General classification |
| **Precision** | Cost of false positives is high | Spam detection |
| **Recall** | Cost of false negatives is high | Disease detection |
| **F1 Score** | Need balance, imbalanced classes | Information retrieval |

### 4. Precision-Recall Tradeoff

Increasing precision typically decreases recall, and vice versa. The optimal balance depends on the problem.

---

## Code Examples

### Example 1: Simple Confusion Matrix

```python
import numpy as np
from sklearn.metrics import confusion_matrix

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

cm = confusion_matrix(y_actual, y_predicted)
print("Confusion Matrix:")
print(cm)
```

### Example 2: Understanding Components

```python
tn, fp, fn, tp = cm.ravel()
print(f"True Negatives (TN): {tn}")
print(f"False Positives (FP): {fp}")
print(f"False Negatives (FN): {fn}")
print(f"True Positives (TP): {tp}")
```

### Example 3: Accuracy

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_actual, y_predicted)
print(f"Accuracy: {accuracy:.4f}")
print(f"Formula: (TP + TN) / Total = ({tp} + {tn}) / {tp+tn+fp+fn}")
```

### Example 4: Precision

```python
from sklearn.metrics import precision_score

precision = precision_score(y_actual, y_predicted)
print(f"Precision: {precision:.4f}")
print(f"Formula: TP / (TP + FP) = {tp} / ({tp} + {fp})")
```

### Example 5: Recall

```python
from sklearn.metrics import recall_score

recall = recall_score(y_actual, y_predicted)
print(f"Recall: {recall:.4f}")
print(f"Formula: TP / (TP + FN) = {tp} / ({tp} + {fn})")
```

### Example 6: F1 Score

```python
from sklearn.metrics import f1_score

f1 = f1_score(y_actual, y_predicted)
print(f"F1 Score: {f1:.4f}")
print(f"Formula: 2 × (Precision × Recall) / (Precision + Recall)")
```

### Example 7: Real Classification Model

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=10,
    n_informative=5, n_redundant=2,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)
```

### Example 8: Classification Report

```python
from sklearn.metrics import classification_report

print("Classification Report:")
print(classification_report(y_test, y_pred))
```

### Example 9: Multi-class Confusion Matrix

```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(f"3-class Confusion Matrix:\n{cm}")
print(f"\nClass names: {list(iris.target_names)}")
```

---

## Common Mistakes to Avoid

1. **Using accuracy with imbalanced classes** — 99% accuracy can be misleading
2. **Ignoring false negatives** — In medical diagnosis, FN are dangerous
3. **Ignoring false positives** — In spam detection, FP are annoying
4. **Not looking at the full matrix** — Accuracy hides the details
5. **Confusing precision and recall** — Know which matters for your problem

---

## Best Practices

1. **Always look at the confusion matrix** — Don't just report accuracy
2. **Choose metric based on business need** — FP vs FN cost
3. **Use classification_report** — Comprehensive view
4. **Consider class imbalance** — Use F1 or precision/recall instead of accuracy
5. **Threshold tuning** — Adjust decision threshold to balance precision/recall

---

## Summary

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| **Accuracy** | (TP+TN)/Total | Overall correctness |
| **Precision** | TP/(TP+FP) | Of predicted positives, how many correct |
| **Recall** | TP/(TP+FN) | Of actual positives, how many caught |
| **F1 Score** | 2×(P×R)/(P+R) | Balance of precision and recall |

| Scenario | Best Metric |
|----------|------------|
| Balanced classes | Accuracy |
| Spam detection | Precision |
| Disease screening | Recall |
| Imbalanced classes | F1 Score |

**Key Takeaway:** The confusion matrix reveals the full picture of classification performance. Accuracy alone is often misleading — use precision, recall, and F1 score to understand how your model performs on each class.

---

## Congratulations!

You've completed the first 12 lectures of the ML foundations course. You now have a solid understanding of:

- Machine Learning fundamentals and workflow
- Data mining and pattern discovery
- Dataset structure and train/test splitting
- Data cleaning and preprocessing
- Linear, polynomial, and multiple regression
- Model evaluation with R², confusion matrix, and classification metrics
- Decision trees and feature importance

**Next steps:** Continue with Lectures 13-23 for more advanced topics including correlation, logistic regression, clustering, PCA, and more.
