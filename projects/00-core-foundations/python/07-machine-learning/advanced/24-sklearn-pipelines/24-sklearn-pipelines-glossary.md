# sklearn Pipelines — Glossary

> Companion reference for the **sklearn Pipelines** lecture.

## Pipeline Core

- **`Pipeline(steps)`**: Chain of `(name, transformer/estimator)` steps ending in an estimator; one `fit`/`predict` interface.
- **`make_pipeline(*steps)`**: Quick constructor without explicit step names.
- **`named_steps`**: Access steps by name (`pipe.named_steps["clf"]`).
- **Double-underscore params**: `clf__n_estimators` addresses nested step params during tuning.
- **Leakage prevention**: transforms are fit on train folds only because they live inside the pipeline.

## Column Routing

- **`ColumnTransformer(transformers)`**: List of `(name, transformer, columns)` routing different column groups to different recipes.
- **`remainder`**: What happens to unlisted columns — `"drop"` (default) or `"passthrough"`.
- **`handle_unknown="ignore"`**: OneHotEncoder keeps unknown test categories from crashing.
- **`SimpleImputer(strategy=...)`**: Fill missing values (`median`, `mean`, `most_frequent`, `constant`).

## Composability

- **`FeatureUnion(transformer_list)`**: Run extractors in parallel, concatenate outputs.
- **`FunctionTransformer(func)`**: Wrap a plain function as a transformer.
- **`BaseEstimator, TransformerMixin`**: Base classes for custom transformers (give `get_params`/`set_params` and `fit_transform`).
- **`fit(X, y)` / `transform(X)` / `fit_transform(X, y)`**: The transformer contract.

## Real-World Patterns

- **Heterogeneous data**: numerics impute+scale, categoricals one-hot — via ColumnTransformer.
- **Custom rules**: ClipOutliers-style transformers encapsulate business logic with train-only bounds.
- **Tuning**: `GridSearchCV(pipeline, {"step__param": [...]})` tunes the whole chain safely.
