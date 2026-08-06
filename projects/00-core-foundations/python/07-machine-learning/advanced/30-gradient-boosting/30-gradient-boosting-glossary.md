# Gradient Boosting — Glossary

> Companion reference for the **Gradient Boosting** lecture.

## Concepts

- **Gradient boosting**: Sequentially train shallow trees on the *residuals* of the ensemble; final prediction = weighted sum.
- **`GradientBoostingClassifier/Regressor`**: Classic sklearn boosting (medium data).
- **`HistGradientBoostingClassifier/Regressor`**: Histogram-binned fast boosting; native NaN + categorical support.
- **`learning_rate`**: Step size per tree; lower → need more trees.
- **`n_estimators` / `max_iter`**: Tree budget / capacity.
- **`max_depth`**: Per-tree depth; controls interaction order.
- **`subsample`**: Row subsampling → variance reduction.
- **`min_samples_leaf`**: Regularization via leaf minimums.
- **Early stopping**: `n_iter_no_change` + validation fraction stops training when val loss plateaus.
- **`categorical_features`**: Column indices/names treated as categorical natively.

## Tradeoffs

- **Tabular → GBDT**: No scaling, handles NaN/categoricals, wins on small-medium tabular.
- **Text/image/audio → NN**: High-dimensional structured data favors deep nets.
- **Loss functions**: deviance/log-loss for classification, squared error for regression.

## Real-World Patterns

- **Churn/fraud/credit**: HistGradientBoosting with early stopping.
- **Feature mix**: numeric + categorical + missing all in one fit.
- **Interpretability**: tree feature importances are free.
