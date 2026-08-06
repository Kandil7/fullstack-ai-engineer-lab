# Feature Engineering — Glossary

> Companion reference for the **Feature Engineering** lecture.

## Numeric Transforms

- **Log transform**: `np.log1p(x)` fixes right skew (income, latency, revenue).
- **Clip/winsorize**: Cap values at train-learned quantiles.
- **StandardScaler**: z-score; needed for linear/neural models, not trees.
- **`KBinsDiscretizer`**: Quantile/uniform binning into ordinal buckets.

## Encodings

- **One-hot**: `OneHotEncoder(handle_unknown="ignore")` — nominal, low-cardinality.
- **Ordinal**: `OrdinalEncoder(categories=[...])` — ranked categories.
- **Target encoding**: Replace category with smoothed mean target — fit on train only; powerful for high-cardinality.
- **Hashing**: `HashingEncoder`-style fixed-size encoding for very high cardinality.
- **`LabelEncoder`**: integer labels — usually for the *target*, not features.

## Interactions & Text

- **`PolynomialFeatures(degree=2)`**: Adds squares and cross-products.
- **Interaction term**: `a * b` captures joint effects.
- **`CountVectorizer`**: Word-count text features.
- **`TfidfVectorizer(max_features=...)`**: Term-frequency-inverse-document-frequency text features.
- **Vocabulary as data**: Text encoders must fit on train only.

## Date Features

- **`dt.hour` / `dt.dayofweek` / `dt.month` / `dt.is_weekend`**: Temporal signals.
- **Lag/diff**: Previous-value features for time series.

## Rules

- **Fit on train only**: every encoder has a fit step — use pipelines to enforce.
- **`ColumnTransformer`**: Routes columns to their encoders leak-free.
- **Feature store**: reusable, versioned feature definitions (Phase 8).
