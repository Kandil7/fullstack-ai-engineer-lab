# EDA Case Study — Glossary

> Companion reference for the **EDA Case Study** lecture. Reach for it while
> working through `advanced/21-case-study-eda.py`.

## Orientation

- **EDA (Exploratory Data Analysis)**: The systematic investigation of a dataset — shape, quality, distributions, relationships — before modeling or reporting.
- **`df.info()`**: One-line-per-column: dtype + non-null counts.
- **`df.describe()`**: Numeric summary — count, mean, std, min, quartiles, max.
- **`df.describe(include="object")`**: Categorical summary (unique, top, freq).
- **`df.shape`**: (rows, columns).
- **`df.head()` / `df.tail()`**: First/last rows.
- **`df.nunique()`**: Unique count per column (cardinality).
- **Data dictionary**: A table of every column — name, dtype, meaning, allowed values.

## Audit

- **`df.isna().sum()`**: Missing count per column.
- **`df.duplicated(subset=[...]).sum()`**: Duplicate-row count.
- **`df.dtypes`**: Current column types.
- **Cardinality**: Number of distinct values; high-cardinality columns need special handling.
- **Skewness**: Asymmetric distribution (right-skew = long tail of big values); often log-transformed.

## Analysis

- **`df.groupby(cols).agg([...])`**: Grouped summaries — sum/mean/count per group.
- **`pd.crosstab(a, b, normalize="index")`**: Frequency cross-tabulation (row % by default).
- **`df[cols].corr().round(2)`**: Pearson correlation matrix.
- **`df.groupby(df["date"].dt.to_period("M")).sum()`**: Monthly/period aggregation.
- **`value_counts(normalize=True)`**: Category shares.
- **Univariate**: one variable at a time (histogram, describe).
- **Bivariate**: two variables (scatter, crosstab, groupby).

## Process

- **Triage**: `info()` + `describe()` + `isna().sum()` first.
- **Iterate**: anomalies in aggregates send you back to raw rows.
- **Findings**: 3–5 evidence-backed insights; EDA value is the interpretation.
- **Deliverable**: data dictionary + quality report + profiles + relationships + findings + next steps.
