# Lecture 06: Random Forests & Tabular

## Topic Overview

fast.ai lesson 6 steps away from deep learning for a while and builds one of
the most useful, most robust models in all of machine learning **from the
ground up**: the random forest. Using tabular datasets like Titanic and the
Blue Book for Bulldozers, we start with a single decision tree — a stack of
yes/no questions — then discover why *many* imperfect trees, trained on random
subsets of the data, beat one carefully tuned tree.

The guiding fast.ai philosophy for tabular data is refreshingly practical:
**start with a random forest.** It is nearly impossible to mess up, needs
almost no preprocessing, gives you free validation (OOB), tells you which
columns matter (feature importance), and rarely overfits catastrophically. You
reach for neural nets or gradient boosting only when you have a reason to.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Lectures 01-05

## Learning Objectives

By the end of this lecture you will be able to:

1. Explain how a decision tree makes a binary split and how the "best" split is
   chosen by minimizing impurity (Gini) or weighted standard deviation.
2. Build and visualize a single decision tree with scikit-learn, controlling
   its size with `max_leaf_nodes` and `min_samples_leaf`.
3. Diagnose overfitting in a deep tree and articulate the bias-variance
   tradeoff it exposes.
4. Describe **bagging** — bootstrap sampling plus random feature subsets — and
   explain *why* averaging uncorrelated errors reduces variance.
5. Train a `RandomForestRegressor` / `RandomForestClassifier`, tune
   `n_estimators`, and recognize the diminishing-returns curve.
6. Use **out-of-bag (OOB) error** as a free validation estimate.
7. Compute and interpret **feature importance** and **partial dependence**, and
   prune redundant or low-importance columns.
8. Decide when to use a random forest versus a neural net versus gradient
   boosting for tabular data.

## Key Concepts

### 1. A single decision tree

A decision tree predicts by asking a sequence of binary (yes/no) questions
about the features. Each internal node splits the data on one column at one
threshold; you follow the branch that matches your row until you land in a
**leaf**, whose prediction is just the average target (regression) or the
majority/probability of classes (classification) of the training rows that
reached it.

```python
# Conceptually, a tree is nested if/else on columns:
def predict_one(row):
    if row["Sex"] == "male":
        if row["Age"] <= 6.5:
            return 0.67  # young boys — higher survival
        return 0.17     # adult men — low survival
    else:
        if row["Pclass"] <= 2:
            return 0.95  # first/second class women
        return 0.50     # third class women
```

```text
                 [Sex == male?]
                /             \
             yes               no
              |                 |
        [Age <= 6.5?]      [Pclass <= 2?]
         /        \          /        \
      0.67       0.17      0.95       0.50   <- leaf predictions
```

### 2. How a split is chosen

At each node the tree tries every column and every candidate threshold and
picks the split that makes the two resulting groups as *pure* (homogeneous in
the target) as possible. For **classification** purity is measured by Gini
impurity or entropy; for **regression** it minimizes the weighted variance /
standard deviation of the two sides.

```python
import numpy as np

def gini(y: np.ndarray) -> float:
    """Gini impurity: 0.0 = perfectly pure node."""
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return 1.0 - np.sum(p ** 2)

def weighted_impurity(left: np.ndarray, right: np.ndarray) -> float:
    n = len(left) + len(right)
    return (len(left) / n) * gini(left) + (len(right) / n) * gini(right)

# The tree greedily chooses the (column, threshold) that MINIMIZES this.
```

### 3. Building a tree with scikit-learn

`DecisionTreeClassifier` / `DecisionTreeRegressor` implement the CART
algorithm. The single most useful knob is `max_leaf_nodes` (or
`min_samples_leaf`), which caps tree size and directly controls
overfitting.

```python
from sklearn.tree import DecisionTreeClassifier, export_text

tree = DecisionTreeClassifier(max_leaf_nodes=4, random_state=42)
tree.fit(X_train, y_train)

# A quick text view of the learned rules:
print(export_text(tree, feature_names=list(X_train.columns)))
```

### 4. Overfitting & the bias-variance tradeoff

A tree with no depth limit will keep splitting until each leaf holds a single
row — perfect on training data, terrible on new data. That is **high variance**
(the model memorizes noise). A tree with one split is **high bias** (too
simple). Between them sits the sweet spot.

```python
# Deep tree: train accuracy ~1.0, validation accuracy drops -> overfitting.
deep = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print(deep.score(X_train, y_train), deep.score(X_valid, y_valid))
# e.g. 1.000  0.76   <- big gap == overfit
```

```text
error
  |  \                         /  <- variance (validation)
  |   \                      /
  |    \___              ___/
  |        \___      ___/
  |            \____/         <- bias (train)
  +--------------------------- tree complexity
        sweet spot ^
```

### 5. Bagging → the random forest

**Bagging** (Bootstrap AGGregatING): train many trees, each on a *bootstrap
sample* (random rows drawn with replacement) and — crucially for a random
forest — each split only considering a *random subset of columns*
(`max_features`). Each tree is individually mediocre and overfit, but their
errors are only weakly correlated. Averaging many uncorrelated errors cancels
them out: the variance of the average shrinks while bias stays put.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,      # number of trees
    max_features="sqrt",   # random column subset per split -> decorrelation
    min_samples_leaf=5,
    n_jobs=-1,
    random_state=42,
)
rf.fit(X_train, y_train)
```

```text
  tree1  tree2  tree3 ... treeN
    \      |      |        /
     \     |      |       /
       average / vote
             |
        stable prediction  (variance ~ single-tree-variance / N, if uncorrelated)
```

### 6. n_estimators and diminishing returns

More trees never hurt accuracy (they only reduce variance), but the benefit
flattens quickly. Plot validation error against tree count and you get a curve
that drops steeply then plateaus — beyond ~100-200 trees you mostly pay compute
for little gain.

```python
import numpy as np

preds = np.stack([t.predict(X_valid) for t in rf.estimators_])
# Cumulative mean over trees shows the plateau:
for n in (1, 5, 20, 50, 100):
    avg = preds[:n].mean(axis=0)
    err = ((avg - y_valid) ** 2).mean()
    print(n, round(float(err), 4))
```

### 7. Out-of-bag (OOB) error — free validation

Each bootstrap sample leaves out ~37% of rows. Every row can be scored using
only the trees that did *not* see it, giving a validation estimate without a
held-out set — set `oob_score=True`.

```python
rf = RandomForestClassifier(
    n_estimators=200, oob_score=True, n_jobs=-1, random_state=42
).fit(X_train, y_train)
print("OOB score:", rf.oob_score_)   # ~ validation accuracy, for free
```

### 8. Feature importance & partial dependence

`feature_importances_` ranks columns by how much they reduced impurity across
all splits. **Partial dependence** shows *how* a feature moves the prediction
by averaging predictions as you sweep one column and hold the rest fixed.
Together they tell you which columns to keep, drop, or investigate.

```python
import pandas as pd

fi = pd.Series(rf.feature_importances_, index=X_train.columns)
print(fi.sort_values(ascending=False))

# Drop near-zero-importance and redundant columns, refit, and you often get a
# simpler model with the SAME accuracy — easier to explain and faster.
```

## Code Examples

### Example A: One tree, then overfit it, then rein it in

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def make_titanic_like(n: int = 800, seed: int = 0) -> pd.DataFrame:
    """Synthesize a small Titanic-flavored dataset (no download needed)."""
    rng = np.random.default_rng(seed)
    sex = rng.integers(0, 2, n)              # 0 female, 1 male
    pclass = rng.integers(1, 4, n)           # 1..3
    age = rng.normal(30, 14, n).clip(0.5, 80)
    fare = rng.gamma(2.0, 15.0, n)
    # Ground-truth survival probability (women & higher class survive more):
    logit = 1.6 - 2.3 * sex - 0.9 * (pclass - 1) - 0.02 * age + 0.01 * fare
    prob = 1 / (1 + np.exp(-logit))
    survived = (rng.random(n) < prob).astype(int)
    return pd.DataFrame(
        {"Sex": sex, "Pclass": pclass, "Age": age.round(1),
         "Fare": fare.round(2), "Survived": survived}
    )

df = make_titanic_like()
X = df.drop(columns="Survived")
y = df["Survived"]
X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.25, random_state=42)

# Unbounded tree -> overfits (train >> valid)
deep = DecisionTreeClassifier(random_state=42).fit(X_tr, y_tr)
print("deep :", round(deep.score(X_tr, y_tr), 3), round(deep.score(X_va, y_va), 3))

# Bounded tree -> generalizes better
small = DecisionTreeClassifier(max_leaf_nodes=8, random_state=42).fit(X_tr, y_tr)
print("small:", round(small.score(X_tr, y_tr), 3), round(small.score(X_va, y_va), 3))
```

### Example B: Random forest with OOB, importance, and prediction confidence

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200, min_samples_leaf=5, max_features="sqrt",
    oob_score=True, n_jobs=-1, random_state=42,
).fit(X_tr, y_tr)

print("valid acc:", round(rf.score(X_va, y_va), 3))
print("OOB  acc :", round(rf.oob_score_, 3))

# Feature importance
fi = pd.Series(rf.feature_importances_, index=X_tr.columns).sort_values(ascending=False)
print(fi.round(3))

# Prediction confidence = agreement across trees (low std == confident)
per_tree = np.stack([t.predict_proba(X_va)[:, 1] for t in rf.estimators_])
conf_std = per_tree.std(axis=0)
print("mean tree-to-tree std:", round(float(conf_std.mean()), 3))
```

### Example C: Pruning redundant features without losing accuracy

```python
# Keep only columns above a small importance threshold, refit, compare.
keep = fi[fi > 0.05].index.tolist()
rf_small = RandomForestClassifier(
    n_estimators=200, min_samples_leaf=5, n_jobs=-1, random_state=42
).fit(X_tr[keep], y_tr)

print("kept columns:", keep)
print("full  acc:", round(rf.score(X_va, y_va), 3))
print("slim  acc:", round(rf_small.score(X_va[keep], y_va), 3))
# Often equal accuracy with fewer columns -> simpler, faster, more explainable.
```

## Common Mistakes to Avoid

**Mistake 1: One-hot encoding high-cardinality columns for trees.**

```python
# BAD: explodes a 500-category column into 500 sparse columns; trees split
# poorly on them and importance gets diluted.
X_enc = pd.get_dummies(df, columns=["Ticket"])  # hundreds of columns

# GOOD: use ordinal/label encoding for trees — order is arbitrary but trees
# only care about split points, and the column stays compact.
from sklearn.preprocessing import OrdinalEncoder
df["Ticket"] = OrdinalEncoder().fit_transform(df[["Ticket"]])
```

**Mistake 2: Judging a forest by training accuracy.**

```python
# BAD: training accuracy is near-perfect and tells you nothing about
# generalization.
print(rf.score(X_tr, y_tr))  # ~0.99 always -> meaningless

# GOOD: use OOB score or a validation set.
rf = RandomForestClassifier(oob_score=True, n_jobs=-1, random_state=42).fit(X_tr, y_tr)
print(rf.oob_score_)         # honest estimate
```

**Mistake 3: Cranking `n_estimators` to fight overfitting.**

```python
# BAD: more trees do NOT reduce bias or fix a leaky feature; they only reduce
# variance and waste compute past the plateau.
rf = RandomForestClassifier(n_estimators=5000).fit(X_tr, y_tr)  # slow, no gain

# GOOD: ~100-200 trees, then control fit with min_samples_leaf / max_features.
rf = RandomForestClassifier(
    n_estimators=200, min_samples_leaf=5, max_features="sqrt", n_jobs=-1
).fit(X_tr, y_tr)
```

## Best Practices

1. **Start with a random forest** for any tabular problem — it is the hardest
   model to get badly wrong.
2. Use **ordinal/label encoding** for categoricals with trees; reserve one-hot
   for linear models and neural nets.
3. Don't scale or normalize features for tree models — splits are
   scale-invariant.
4. Turn on `oob_score=True` to get free validation, and still keep a real
   held-out set for the final estimate.
5. Set `n_estimators` to ~100-200; increase only if the OOB curve is still
   dropping.
6. Control fit with `min_samples_leaf` (try 1, 5, 25) rather than tree count.
7. Keep `max_features="sqrt"` (classification) or `~0.5` (regression) to
   decorrelate trees — this is what makes bagging work.
8. Read `feature_importances_` early; drop low-importance and redundant columns
   and refit to simplify.
9. Use **partial dependence** to understand *direction and shape*, not just
   *which* features matter.
10. Use tree-to-tree prediction variance as a confidence signal — flag
    low-agreement rows for review.

## Practice Exercises

1. Build a `DecisionTreeClassifier` with `max_leaf_nodes` in {2, 4, 8, 32,
   None}. Plot train vs. validation accuracy and mark the overfitting point.
2. Implement the `gini` and `weighted_impurity` helpers above and, for a single
   column, find the threshold that minimizes weighted impurity. Confirm it
   matches sklearn's first split.
3. Train random forests with `n_estimators` in {1, 5, 20, 50, 100, 200} and
   plot OOB error to observe the diminishing-returns curve.
4. Compute `feature_importances_`, drop everything below 0.05, refit, and
   verify accuracy is unchanged. Report which columns you removed.
5. For the two most important features, compute a simple partial-dependence
   curve (sweep the column over its range, average predictions) and describe
   the relationship.

## Summary

A decision tree is a greedy stack of binary splits chosen to minimize impurity;
alone it overfits (high variance) or underfits (high bias). A **random forest**
fixes this by **bagging** — training many trees on bootstrapped rows and random
column subsets — then averaging. Because their errors are only weakly
correlated, averaging cancels the noise and slashes variance without adding
bias. You get free validation via **OOB error**, interpretability via **feature
importance** and **partial dependence**, and confidence estimates from
tree-to-tree variance — all with almost no preprocessing. For tabular data,
reach for a random forest first; consider gradient boosting when you need to
squeeze out more accuracy, and neural nets when you have high-cardinality
categoricals or want to combine tabular data with text/images.

**Next lecture:** Lecture 07 — Collaborative Filtering.
