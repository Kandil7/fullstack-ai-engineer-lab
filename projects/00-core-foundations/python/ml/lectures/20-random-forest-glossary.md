# Glossary: Random Forest (Lecture 20)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Random Forest | Ensemble of decision trees with bagging | `RandomForestClassifier()` |
| Ensemble Learning | Combining multiple models | Bagging, Boosting |
| Bagging | Bootstrap Aggregation | Train on random subsets |
| Decision Tree | Tree-based classifier | `DecisionTreeClassifier()` |
| Bootstrap Sample | Random sampling with replacement | ~63% unique samples |
| Feature Importance | Measures feature contribution | `rf.feature_importances_` |
| OOB Score | Out-of-Bag validation score | `oob_score=True` |
| n_estimators | Number of trees in forest | 100 (default) |
| max_depth | Maximum tree depth | None (unlimited) |
| min_samples_split | Min samples to split node | 2 (default) |
| min_samples_leaf | Min samples in leaf node | 1 (default) |
| max_features | Features considered at split | sqrt(n) (default) |
| Majority Vote | Final prediction (classification) | Most common class |
| Averaging | Final prediction (regression) | Mean of predictions |

---

## Detailed Term Definitions

### Random Forest

**Definition:** An ensemble learning method that constructs multiple decision trees during training and outputs the mode of the classes (classification) or mean prediction (regression).

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
```

**Related Terms:** Ensemble Learning, Bagging, Decision Tree

---

### Ensemble Learning

**Definition:** A machine learning paradigm where multiple models (weak learners) are combined to create a stronger predictor.

**Types:**
- **Bagging**: Train models in parallel on random subsets
- **Boosting**: Train models sequentially, each correcting errors
- **Stacking**: Combine different model types

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=500, n_features=10, random_state=42)

models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42)
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"{name:25s}: {scores.mean():.4f}")
```

**Related Terms:** Bagging, Boosting, Stacking, Weak Learner

---

### Bagging (Bootstrap Aggregation)

**Definition:** An ensemble technique where multiple models are trained on different random subsets of the training data (with replacement), then combined.

**Example:**
```python
import numpy as np
from sklearn.utils import resample

np.random.seed(42)
X = np.arange(10).reshape(-1, 1)
y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

print("Original data:", y)

# Bootstrap samples
for i in range(3):
    indices = resample(range(len(X)), n_samples=len(X), random_state=i)
    print(f"Bootstrap {i+1}: {y[indices]}")

# Each sample has ~63% unique points
# ~37% are duplicates (out-of-bag samples)
```

**Related Terms:** Bootstrap Sample, Out-of-Bag, Random Forest

---

### Decision Tree

**Definition:** A tree-based model that makes predictions by learning decision rules from features. Random Forest combines multiple decision trees.

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

# Single tree
dt = DecisionTreeClassifier(random_state=42)
dt_scores = cross_val_score(dt, X, y, cv=5, scoring='accuracy')

# Random Forest (many trees)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')

print(f"Single Tree: {dt_scores.mean():.4f} +/- {dt_scores.std():.4f}")
print(f"Random Forest: {rf_scores.mean():.4f} +/- {rf_scores.std():.4f}")
```

**Related Terms:** Random Forest, Overfitting, Gini Impurity

---

### Bootstrap Sample

**Definition:** A random sample drawn from the original dataset with replacement. Approximately 63% of original samples appear in each bootstrap.

**Example:**
```python
import numpy as np

np.random.seed(42)
original = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Bootstrap sample
bootstrap = np.random.choice(original, size=len(original), replace=True)
unique = np.unique(bootstrap)

print(f"Original: {original}")
print(f"Bootstrap: {bootstrap}")
print(f"Unique in bootstrap: {len(unique)}/{len(original)} ({len(unique)/len(original):.0%})")
# Expected: ~63% unique
```

**Related Terms:** Bagging, Out-of-Bag, Resampling

---

### Feature Importance

**Definition:** A measure of how much each feature contributes to the model's predictions. Calculated based on how much each feature decreases impurity across all trees.

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np
import pandas as pd

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

feature_names = [f"Feature_{i}" for i in range(10)]

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# Get importances
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

print("Feature Ranking:")
for i, idx in enumerate(indices):
    print(f"  {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")

# Select important features
threshold = 0.05
important = np.where(importances > threshold)[0]
print(f"\nImportant features (>{threshold}): {important}")
```

**Related Terms:** Gini Importance, Permutation Importance

---

### Out-of-Bag (OOB) Score

**Definition:** A validation estimate using samples not included in each bootstrap sample. About 37% of samples are OOB for each tree.

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

# With OOB score
rf_oob = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)
rf_oob.fit(X, y)

print(f"OOB Score: {rf_oob.oob_score_:.4f}")

# Compare with cross-validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(rf_oob, X, y, cv=5, scoring='accuracy')
print(f"CV Score: {scores.mean():.4f}")
# OOB is a good approximation of CV score
```

**Related Terms:** Bootstrap, Cross-Validation, Validation

---

### n_estimators

**Definition:** The number of decision trees in the forest. More trees generally improve performance but increase computation.

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import time

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

print("Effect of n_estimators:")
for n in [10, 50, 100, 200, 500]:
    start = time.time()
    rf = RandomForestClassifier(n_estimators=n, random_state=42)
    scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    time_taken = time.time() - start
    print(f"  {n:3d} trees: {scores.mean():.4f} ({time_taken:.2f}s)")
```

**Related Terms:** Ensemble Size, Computational Cost

---

### max_depth

**Definition:** Maximum depth of each decision tree. None means unlimited depth. Deeper trees can overfit.

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

print("Effect of max_depth:")
for depth in [3, 5, 10, 20, None]:
    rf = RandomForestClassifier(n_estimators=100, max_depth=depth, random_state=42)
    scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    print(f"  depth={str(depth):5s}: {scores.mean():.4f}")
```

**Related Terms:** Tree Depth, Overfitting, Regularization

---

### min_samples_split

**Definition:** The minimum number of samples required to split an internal node. Higher values prevent overfitting.

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

print("Effect of min_samples_split:")
for split in [2, 5, 10, 20]:
    rf = RandomForestClassifier(n_estimators=100, min_samples_split=split, 
                                random_state=42)
    scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    print(f"  split={split:2d}: {scores.mean():.4f}")
```

**Related Terms:** min_samples_leaf, Regularization, Overfitting

---

### max_features

**Definition:** The number of features to consider when looking for the best split. Default is sqrt(n_features) for classification.

**Example:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

print("Effect of max_features:")
for features in ['sqrt', 'log2', 0.5, 0.8, 1.0]:
    rf = RandomForestClassifier(n_estimators=100, max_features=features, 
                                random_state=42)
    scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    print(f"  features={str(features):5s}: {scores.mean():.4f}")
```

**Related Terms:** Feature Randomness, Decorrelation

---

### Majority Vote

**Definition:** The final prediction in Random Forest classification is the class that appears most often across all trees.

**Example:**
```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

rf = RandomForestClassifier(n_estimators=10, random_state=42)
rf.fit(X, y)

# Get individual tree predictions
X_test = X[:5]
tree_predictions = np.array([tree.predict(X_test) for tree in rf.estimators_])

print("Individual tree predictions (first 5 samples):")
print(tree_predictions[:5, :])

# Final prediction (majority vote)
final_predictions = rf.predict(X_test)
print(f"\nFinal predictions: {final_predictions}")

# Manual majority vote
from scipy import stats
manual_vote = stats.mode(tree_predictions, axis=0)[0]
print(f"Manual majority vote: {manual_vote}")
```

**Related Terms:** Ensemble Prediction, Voting Classifier

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Bootstrap Sample | Sample n with replacement |
| OOB Samples | ~37% of original per tree |
| Feature Randomness | sqrt(n) features at each split |
| Gini Impurity | 1 - Σpᵢ² |
| Feature Importance | Decrease in impurity |

---

## Code Snippets Quick Reference

```python
# Basic Random Forest
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# Feature Importance
importances = rf.feature_importances_

# OOB Score
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)

# Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)

# Parameter Tuning
from sklearn.model_selection import GridSearchCV
param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, None]}
grid = GridSearchCV(rf, param_grid, cv=5)
grid.fit(X, y)

# Parallel Training
rf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
```

---

## Common Pitfalls

1. **Too few trees** — High variance, unstable predictions
2. **Ignoring overfitting** — Check train vs test scores
3. **Not using OOB** — Free validation, always enable
4. **Ignoring feature importance** — Use for feature selection
5. **Not tuning** — Default parameters may not be optimal

---

## Further Reading

- [Scikit-learn - Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees)
- [Wikipedia - Random Forest](https://en.wikipedia.org/wiki/Random_forest)
- [Towards Data Science - Random Forest](https://towardsdatascience.com/understanding-random-forest-584037908c26)
