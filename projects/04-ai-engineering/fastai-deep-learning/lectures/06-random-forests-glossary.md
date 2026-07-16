# Glossary: Random Forests & Tabular

## Quick Reference Table

| Term | One-line definition |
|------|---------------------|
| Decision tree | A model that predicts by following a chain of binary yes/no splits to a leaf. |
| Binary split | A single node's rule: `column <= threshold` sends rows left or right. |
| Impurity / Gini | Measure of how mixed the target is in a node; 0 = pure. |
| Leaf node | A terminal node whose prediction is the mean/majority of its training rows. |
| Overfitting | Model memorizes training noise; great on train, poor on new data. |
| Bias-variance tradeoff | Balance between too-simple (bias) and too-sensitive (variance) models. |
| Bagging | Bootstrap AGGregatING: train many models on random samples and average. |
| Bootstrap | Sampling rows with replacement to build each tree's training set. |
| Random forest | An ensemble of bagged decision trees with random feature subsets. |
| n_estimators | Number of trees in the forest. |
| Out-of-bag (OOB) error | Validation estimate from rows each tree didn't see (~37%). |
| Feature importance | Ranking of columns by total impurity reduction across splits. |
| Partial dependence | How predictions change as one feature is swept, others fixed. |
| Ensemble | Any model that combines multiple base models' predictions. |
| Gradient boosting | Ensemble that adds trees sequentially, each fixing prior errors. |
| One-hot / ordinal encoding | Two ways to turn categorical columns into numbers. |

## Detailed Definitions

### Decision tree
A supervised model that recursively partitions the feature space with binary
splits. To predict, you route a row from the root through internal nodes to a
leaf. It handles mixed feature types, needs no scaling, and is fully
interpretable, but a single deep tree overfits badly. Implemented in sklearn as
`DecisionTreeClassifier` and `DecisionTreeRegressor`.

### Binary split
The rule at an internal node, of the form `feature <= threshold`. Rows
satisfying it go one way, the rest go the other. The tree evaluates every
column and candidate threshold and greedily keeps the split that most reduces
impurity.

### Impurity / Gini
A number quantifying how mixed the target values are in a node. **Gini
impurity** for classification is `1 - Σ p_k²`, minimized (0) when all rows share
one class. For regression, "impurity" is variance / standard deviation. The
tree chooses splits that minimize the weighted impurity of the two children.

### Leaf node
A terminal node with no further splits. Its prediction is the mean target
(regression) or class distribution / majority vote (classification) of the
training rows that landed there. Fewer rows per leaf → more complex, more
overfit tree; `min_samples_leaf` sets a floor.

### Overfitting
When a model fits training-set noise instead of the underlying signal, shown by
a large gap between training and validation performance. Deep unbounded trees
overfit almost by construction (each leaf can isolate a single row).

### Bias-variance tradeoff
Total error decomposes into bias (error from over-simplified assumptions) and
variance (error from sensitivity to the particular training sample). Simple
trees are high-bias; deep trees are high-variance. Random forests attack the
variance term specifically, leaving bias roughly unchanged.

### Bagging
**B**ootstrap **agg**regat**ing**: train each base model on its own bootstrap
sample and combine by averaging (regression) or voting (classification). It
reduces variance without increasing bias, provided the base models are diverse.
Random forests are bagging applied to decision trees, plus random feature
subsetting.

### Bootstrap
A resampling technique: draw N rows *with replacement* from an N-row dataset.
Each bootstrap sample contains roughly 63% of the unique rows; the ~37% left out
are that tree's out-of-bag rows.

### Random forest
An ensemble of decision trees where (1) each tree trains on a bootstrap sample
and (2) each split considers only a random subset of columns (`max_features`).
Both sources of randomness decorrelate the trees so that averaging cancels their
independent errors. Robust, low-maintenance, and strong on tabular data.
sklearn: `RandomForestClassifier` / `RandomForestRegressor`.

### n_estimators
The number of trees. More trees monotonically reduce variance (never increase
error) but with sharply diminishing returns and linear cost; ~100-200 is the
usual practical range. It is *not* a knob for fixing bias or leaky features.

### Out-of-bag (OOB) error
Since each tree omits ~37% of rows, every row can be predicted by only the trees
that never saw it. Aggregating these gives a validation-quality estimate with no
separate held-out set. Enable with `oob_score=True`; read via `oob_score_`.

### Feature importance
`feature_importances_` measures how much each column reduced impurity, summed
over all splits in all trees and normalized to sum to 1. Great for ranking and
pruning columns, but biased toward high-cardinality features and can split
credit across correlated columns — corroborate with partial dependence or
permutation importance.

### Partial dependence
The average model prediction as a single feature is swept across its range while
all other features are held at their actual values (then averaged). It reveals
the *shape and direction* of a feature's effect, complementing the magnitude
given by feature importance. See sklearn `PartialDependenceDisplay`.

### Ensemble
Any technique that combines multiple base models to produce a stronger
prediction than any one alone. Bagging (random forests) and boosting (gradient
boosting) are the two dominant families for trees.

### Gradient boosting
An ensemble that builds trees *sequentially*, each new (shallow) tree fitting
the residual errors of the current ensemble. Often more accurate than random
forests on tabular data but more sensitive to hyperparameters and easier to
overfit. Popular libraries: XGBoost, LightGBM, CatBoost.

### One-hot / ordinal encoding
Two ways to numericize categoricals. **One-hot** creates a 0/1 column per
category (good for linear models and neural nets, bad for high cardinality).
**Ordinal/label** maps each category to an integer (compact; ideal for trees,
which only care about split points, not the arbitrary ordering).

## Summary

Random forests turn a fragile, overfitting decision tree into a robust,
low-maintenance predictor by bagging many decorrelated trees and averaging their
errors away. The surrounding vocabulary — impurity and splits (how a tree
learns), bootstrap and OOB (how the ensemble is trained and validated for free),
feature importance and partial dependence (how you interpret it) — is the
practical toolkit for tabular machine learning.

**Next:** See Lecture 07 — Collaborative Filtering.
