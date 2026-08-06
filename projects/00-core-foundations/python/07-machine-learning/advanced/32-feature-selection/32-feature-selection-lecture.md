# Feature Selection — Fewer, Better Features

> **Topic 32 — Modeling depth.** Filter, wrapper, and embedded methods; RFE,
> `SelectFromModel`, L1, multicollinearity and VIF, permutation importance,
> and selection stability.

Companion exercise: `32-feature-selection.py`

---

## 1. Why Select Features

Fewer features = cheaper pipelines, faster training, less overfitting, easier
deployment and monitoring. Selection also removes noise that silently
degrades models.

## 2. Filter Methods — Fast, Model-Agnostic

Score each feature independently and keep the top k:

- **VarianceThreshold**: drop near-constant columns.
- **f_classif / ANOVA F**: univariate association with the target.
- **mutual_info_classif**: non-linear association, robust but slower.

Cheap enough to run on every pipeline; ignores feature interactions.

## 3. Wrapper Methods — Model-Aware

**RFE** (Recursive Feature Elimination) trains the model, drops the least
important feature, repeats. Model-aware and powerful, but expensive — each
iteration refits.

## 4. Embedded Methods — Selection During Training

- **L1 regularization** zeroes out coefficients — the remaining non-zero
  features are selected.
- **Tree importance** — `SelectFromModel(RandomForest, threshold="median")`
  keeps features above the median importance.

Fast, model-aware, built into training.

## 5. Multicollinearity & VIF

**VIF** (Variance Inflation Factor) measures how well a column is predicted
from the others. VIF > 10 indicates harmful collinearity — the column is
redundant and destabilizes linear models:

```python
vif = 1 / (1 - R²_of_column_vs_rest)
```

## 6. Permutation Importance

Shuffle a feature's values and measure the score drop — the honest measure of
"how much does this feature matter". Model-agnostic, but collinear features
share credit, so interpret with care.

## 7. Stability — Selection Must Not Flip

Resample the data a few times; if selection keeps picking the same features,
it's stable. If the chosen set churns wildly, the signal is weak — don't ship
a selection that depends on the seed.

## Key Takeaways

1. Filter: fast, model-agnostic — variance, F, mutual info.
2. Wrapper (RFE): model-aware but expensive.
3. Embedded: L1 zeros weights; trees rank by importance.
4. VIF > 10 → drop collinear columns.
5. Verify selection stability across resamples before shipping.
