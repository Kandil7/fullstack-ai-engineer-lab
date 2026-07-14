# Glossary: Confusion Matrix

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Confusion Matrix | Table showing TP, TN, FP, FN counts | Tool |
| True Positives (TP) | Correctly predicted positive | Count |
| True Negatives (TN) | Correctly predicted negative | Count |
| False Positives (FP) | Incorrectly predicted positive | Count |
| False Negatives (FN) | Incorrectly predicted negative | Count |
| Accuracy | Overall correctness | Metric |
| Precision | Of predicted positives, how many correct | Metric |
| Recall | Of actual positives, how many caught | Metric |
| Sensitivity | Same as recall | Alias |
| Specificity | Of actual negatives, how many correct | Metric |
| F1 Score | Harmonic mean of precision and recall | Metric |
| Type I Error | False Positive | Error |
| Type II Error | False Negative | Error |
| Classification Report | Detailed metrics per class | Tool |
| Threshold | Decision boundary for classification | Parameter |
| ROC Curve | Receiver Operating Characteristic | Plot |
| AUC | Area Under ROC Curve | Metric |
| Binary Classification | Two classes | Type |
| Multi-class Classification | More than two classes | Type |
| Class Imbalance | Unequal class distribution | Problem |

---

## Detailed Definitions

### A

#### Accuracy
**Definition:** The proportion of all predictions that were correct. The most intuitive metric, but can be misleading with imbalanced classes.

**Formula:**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**Example:**
```python
from sklearn.metrics import accuracy_score
import numpy as np

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

accuracy = accuracy_score(y_actual, y_predicted)
print(f"Accuracy: {accuracy:.4f}")  # 0.8
# 8 correct out of 10
```

**Limitations:**
- Misleading with imbalanced classes (99% accuracy possible with 99% majority class)
- Doesn't distinguish between FP and FN

**Related Terms:** Precision, Recall, F1 Score

---

### C

#### Classification Report
**Definition:** A comprehensive summary of classification metrics including precision, recall, F1 score, and support for each class.

**Example:**
```python
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
# Output includes precision, recall, f1-score, support for each class
```

**Output columns:**
- **precision**: TP / (TP + FP)
- **recall**: TP / (TP + FN)
- **f1-score**: 2 × (precision × recall) / (precision + recall)
- **support**: Number of actual samples per class

**Related Terms:** Precision, Recall, F1 Score, Confusion Matrix

#### Confusion Matrix
**Definition:** A table that compares predicted labels against actual labels, showing the counts of true positives, true negatives, false positives, and false negatives.

**Example:**
```python
from sklearn.metrics import confusion_matrix
import numpy as np

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

cm = confusion_matrix(y_actual, y_predicted)
print("Confusion Matrix:")
print(cm)
# [[4 1]    TN=4, FP=1
#  [1 4]]   FN=1, TP=4

# With labels
cm = confusion_matrix(y_actual, y_predicted, labels=[0, 1])
print("\nWith labels:")
print(cm)
```

**For multi-class:**
```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(f"3×3 Confusion Matrix:\n{cm}")
# Rows = actual, Columns = predicted
```

**Related Terms:** TP, TN, FP, FN, Accuracy, Precision, Recall

---

### F

#### False Negative (FN)
**Definition:** A case where the actual value is positive but the model predicted negative. Also called a Type II error.

**Example:**
```python
import numpy as np
from sklearn.metrics import confusion_matrix

# Actual: Patient has disease (1)
# Predicted: Patient doesn't have disease (0)
y_actual = np.array([1, 1, 1, 0, 0])
y_predicted = np.array([0, 1, 0, 0, 1])

cm = confusion_matrix(y_actual, y_predicted)
tn, fp, fn, tp = cm.ravel()

print(f"False Negatives: {fn}")
# FN = 2: Two patients with disease were told they're healthy
# This is DANGEROUS in medical diagnosis!
```

**Impact:** Missed detections, delayed treatment, safety risks

**Related Terms:** False Positive, Type II Error, Recall

#### False Positive (FP)
**Definition:** A case where the actual value is negative but the model predicted positive. Also called a Type I error.

**Example:**
```python
import numpy as np
from sklearn.metrics import confusion_matrix

# Actual: Email is not spam (0)
# Predicted: Email is spam (1)
y_actual = np.array([0, 0, 0, 1, 1])
y_predicted = np.array([1, 0, 1, 1, 0])

cm = confusion_matrix(y_actual, y_predicted)
tn, fp, fn, tp = cm.ravel()

print(f"False Positives: {fp}")
# FP = 2: Two legitimate emails marked as spam
# This is ANNOYING in spam detection
```

**Impact:** False alarms, wasted resources, user frustration

**Related Terms:** False Negative, Type I Error, Precision

#### F1 Score
**Definition:** The harmonic mean of precision and recall. Provides a single score that balances both metrics. Useful when you need to balance precision and recall.

**Formula:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Example:**
```python
from sklearn.metrics import f1_score
import numpy as np

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

f1 = f1_score(y_actual, y_predicted)
print(f"F1 Score: {f1:.4f}")
```

**Interpretation:**
- F1 = 1.0: Perfect precision and recall
- F1 = 0.5: Balanced but not great
- F1 = 0.0: Either precision or recall is 0

**When to use:**
- Imbalanced classes
- Need to balance FP and FN costs
- Comparing models

**Related Terms:** Precision, Recall, Harmonic Mean

---

### P

#### Precision
**Definition:** Of all the samples predicted as positive, what proportion were actually positive. Also called Positive Predictive Value.

**Formula:**
```
Precision = TP / (TP + FP)
```

**Example:**
```python
from sklearn.metrics import precision_score
import numpy as np

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

precision = precision_score(y_actual, y_predicted)
print(f"Precision: {precision:.4f}")
```

**Interpretation:**
- High precision = few false positives
- When FP is costly: spam detection, fraud alerts

**Related Terms:** Recall, F1 Score, False Positive

---

### R

#### Recall (Sensitivity)
**Definition:** Of all the actual positive samples, what proportion did the model correctly identify. Also called Sensitivity or True Positive Rate.

**Formula:**
```
Recall = TP / (TP + FN)
```

**Example:**
```python
from sklearn.metrics import recall_score
import numpy as np

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

recall = recall_score(y_actual, y_predicted)
print(f"Recall: {recall:.4f}")
```

**Interpretation:**
- High recall = few false negatives
- When FN is costly: disease detection, safety systems

**Related Terms:** Precision, F1 Score, Sensitivity, True Positive Rate

---

### S

#### Specificity
**Definition:** Of all the actual negative samples, what proportion did the model correctly identify. The complement of the False Positive Rate.

**Formula:**
```
Specificity = TN / (TN + FP)
```

**Example:**
```python
from sklearn.metrics import confusion_matrix
import numpy as np

y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

cm = confusion_matrix(y_actual, y_predicted)
tn, fp, fn, tp = cm.ravel()
specificity = tn / (tn + fp)
print(f"Specificity: {specificity:.4f}")
```

**Related Terms:** Sensitivity, Recall, True Negative Rate

---

### T

#### True Negative (TN)
**Definition:** A case where the actual value is negative and the model correctly predicted negative.

**Example:**
```python
import numpy as np
from sklearn.metrics import confusion_matrix

y_actual = np.array([0, 0, 1, 1, 0])
y_predicted = np.array([0, 1, 1, 0, 0])

cm = confusion_matrix(y_actual, y_predicted)
tn, fp, fn, tp = cm.ravel()
print(f"True Negatives: {tn}")  # 2
```

**Related Terms:** True Positive, False Positive, False Negative

#### True Positive (TP)
**Definition:** A case where the actual value is positive and the model correctly predicted positive.

**Example:**
```python
import numpy as np
from sklearn.metrics import confusion_matrix

y_actual = np.array([1, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1])

cm = confusion_matrix(y_actual, y_predicted)
tn, fp, fn, tp = cm.ravel()
print(f"True Positives: {tp}")  # 2
```

**Related Terms:** True Negative, False Positive, False Negative

#### Type I Error
**Definition:** Incorrectly rejecting a true null hypothesis. In classification, this is a False Positive — predicting positive when the actual is negative.

**Example:**
```python
# Type I Error (False Positive):
# Actual: Email is NOT spam
# Predicted: Email IS spam
# Result: Legitimate email goes to spam folder
```

**Related Terms:** Type II Error, False Positive, Precision

#### Type II Error
**Definition:** Incorrectly failing to reject a false null hypothesis. In classification, this is a False Negative — predicting negative when the actual is positive.

**Example:**
```python
# Type II Error (False Negative):
# Actual: Patient HAS disease
# Predicted: Patient DOES NOT have disease
# Result: Disease goes untreated
```

**Related Terms:** Type I Error, False Negative, Recall

---

## Key Formulas

| Metric | Formula | Range |
|--------|---------|-------|
| Accuracy | `(TP+TN)/(TP+TN+FP+FN)` | [0, 1] |
| Precision | `TP/(TP+FP)` | [0, 1] |
| Recall | `TP/(TP+FN)` | [0, 1] |
| F1 Score | `2×(P×R)/(P+R)` | [0, 1] |
| Specificity | `TN/(TN+FP)` | [0, 1] |

---

## Python Import Cheat Sheet

```python
# Confusion Matrix
from sklearn.metrics import confusion_matrix

# Individual metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Comprehensive report
from sklearn.metrics import classification_report

# Complete workflow
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

# All metrics
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall: {recall_score(y_test, y_pred):.4f}")
print(f"F1: {f1_score(y_test, y_pred):.4f}")

# Full report
print(classification_report(y_test, y_pred))
```
