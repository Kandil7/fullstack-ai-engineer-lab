# Feature Selection — Glossary

> Companion reference for the **Feature Selection** lecture.

## Filter Methods

- **`VarianceThreshold(threshold)`**: Drop near-constant features.
- **`SelectKBest(score_func, k)`**: Keep top-k by univariate score.
- **`f_classif`**: ANOVA F-score (linear association).
- **`mutual_info_classif`**: Non-linear association measure.
- **Pros/cons**: fast, model-agnostic, ignores interactions.

## Wrapper Methods

- **`RFE(estimator, n_features_to_select)`**: Recursive elimination — fit, drop least important, repeat.
- **`RFECV`**: RFE with CV to choose the count automatically.
- **Pros/cons**: model-aware, expensive (refits per iteration).

## Embedded Methods

- **L1 regularization**: `penalty="l1"` zeroes coefficients → implicit selection.
- **`SelectFromModel(estimator, threshold="median")`**: Keep features above a threshold of model importance.
- **Tree feature_importances_**: impurity-based importance (biased toward high-cardinality features).

## Diagnostics

- **VIF (Variance Inflation Factor)**: `1/(1-R²)` of regressing a column on the rest; >10 → collinear.
- **Permutation importance**: score drop when shuffling a feature — model-agnostic importance.
- **Stability**: overlap of selected sets across resamples; low overlap = unreliable selection.
- **Multicollinearity**: correlated predictors that destabilize linear models.

## Real-World Patterns

- **Cheap first pass**: VarianceThreshold + SelectKBest(mutual_info).
- **Model-aware**: SelectFromModel with trees or L1.
- **Interpretability**: permutation importance on the final model.
