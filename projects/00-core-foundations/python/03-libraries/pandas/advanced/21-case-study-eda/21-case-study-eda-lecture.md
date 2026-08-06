# Pandas Case Study: Exploratory Data Analysis (EDA)

> **Topic 21 — Advanced pandas series (capstone).** An end-to-end EDA on a
> realistic dataset, tying together every technique from the series: loading,
> cleaning, aggregation, visualization, and insight.

Companion exercise: `advanced/21-case-study-eda.py`

---

## 1. What EDA Is For

Before any model or report, EDA answers: *what is in this data, what's wrong
with it, and what stands out?* It is the discipline that turns a raw dump into
a defensible analysis — and it is exactly what you'll be asked to do in
interviews and on the job.

The standard loop:

1. **Load & orient** — shape, columns, dtypes, sample rows.
2. **Audit** — missing values, duplicates, cardinality.
3. **Clean** — fix dtypes, dedupe, handle missing.
4. **Profile** — univariate stats, distributions.
5. **Explore relationships** — groupbys, correlations, cross-tabs.
6. **Visualize** — trends, distributions, comparisons.
7. **Report** — capture findings as concrete, actionable statements.

## 2. Load & Orient

```python
import pandas as pd
import numpy as np

df = pd.read_csv("sales.csv", parse_dates=["date"])
df.info()          # dtypes + non-null counts — always first
df.head(), df.tail()
df.describe()      # numeric summaries: count, mean, std, quartiles
df.describe(include="object")  # categorical summary
df.shape           # (rows, columns)
```

`df.info()` in 3 seconds tells you the dtypes and where the missing values
are — the highest-value line in EDA.

## 3. Audit & Clean

```python
# Missing value audit
missing = df.isna().sum()
missing[missing > 0].sort_values(ascending=False)

# Duplicate check
df.duplicated(subset=["order_id"]).sum()

# Cardinality (unique counts) per column
df.nunique()

# Clean pass
df = df.drop_duplicates(subset=["order_id"])
df["price"] = df["price"].fillna(df["price"].median())
df["region"] = df["region"].fillna("unknown")
```

## 4. Profile the Target & Key Columns

```python
# Distribution of the main numeric column
df["revenue"].describe()
df["revenue"].hist(bins=40)

# Categorical breakdown
df["region"].value_counts(normalize=True)

# Time range
df["date"].min(), df["date"].max()
```

Watch for: skewed distributions (log-transform before models), unexpected
zeros/negatives, and rare categories that should be grouped into "other".

## 5. Explore Relationships

```python
# Grouped summaries — the heart of EDA
df.groupby("region")["revenue"].agg(["sum", "mean", "count"])

# Cross-tabulation
pd.crosstab(df["region"], df["channel"], normalize="index")

# Numeric correlation
df[["revenue", "units", "discount", "rating"]].corr().round(2)

# Trend over time
df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().plot()
```

Correlation only captures **linear** relationships — always pair it with
scatter plots. Groupbys reveal the story behind the aggregate numbers.

## 6. Iterate & Document

EDA is iterative: an anomaly in the by-region table sends you back to the raw
rows; a weird histogram sends you to `df[df["revenue"] > 1e6]` to inspect
outliers. Capture each finding:

```python
FINDINGS = [
    "Revenue is right-skewed; median ($82) far below mean ($214) — log-scale before modeling.",
    "3.2% of orders are missing region; filled with 'unknown' (not imputed).",
    "Discount > 30% correlates with higher return rate (r = 0.41).",
    "South region shows flat growth while others grew ~15% MoM.",
]
```

## 7. Deliverable Checklist

A professional EDA deliverable includes:

1. **Data dictionary** — every column, dtype, meaning, allowed values.
2. **Quality report** — missing/duplicate/outlier counts and decisions.
3. **Univariate profiles** — key distributions with charts.
4. **Bivariate analysis** — correlations, groupbys, cross-tabs.
5. **Clear findings** — 3–5 bullet insights, each with the evidence behind it.
6. **Next steps** — which features to engineer, which data to collect.

## Key Takeaways

1. `info()` + `describe()` + `isna().sum()` are the 10-second triage.
2. Clean deliberately: dedupe, fix dtypes, fill/drop with justification.
3. Groupbys + cross-tabs + corr reveal relationships; always verify with charts.
4. Document findings — EDA's value is the *interpretation*, not the code.
5. EDA is the foundation of every model and every report you'll ever build.
