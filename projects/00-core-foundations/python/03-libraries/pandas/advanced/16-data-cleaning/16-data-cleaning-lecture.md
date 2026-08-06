# Pandas Data Cleaning: Real-World ETL Patterns

> **Topic 16 — Advanced pandas series.** The messy, essential work: fixing
> dtypes, handling duplicates, outliers, malformed values, and building a
> reusable cleaning pipeline for production ML.

Companion exercise: `advanced/16-data-cleaning.py`

---

## 1. The Reality of Dirty Data

Real datasets arrive with:

- Wrong dtypes (dates as strings, numbers with commas, zips as ints).
- Duplicate rows and near-duplicates.
- Outliers that skew statistics.
- Malformed values (`"N/A"`, `"unknown"`, `"$1,234.56"`, mixed units).
- Inconsistent casing/whitespace (`"  New York "` vs `"new york"`).

Cleaning is not glamorous — it is **most** of an ML engineer's job. A reusable
`clean_*` pipeline is the deliverable that matters.

## 2. dtype Repair — The Foundation

```python
df = pd.DataFrame({
    "price": ["$1,234.56", "$99.99", "n/a"],
    "joined": ["2026-01-05", "2026-02-14", "2025-12-30"],
    "zip": ["02134", "10001", "94016"],
})

# String money -> float (strip $ and commas, coerce junk to NaN)
df["price"] = (
    df["price"].str.replace(r"[\$,]", "", regex=True)
               .astype(float)
)

# ISO date strings -> datetime64
df["joined"] = pd.to_datetime(df["joined"], errors="coerce")

# Leading zeros must stay strings
df["zip"] = df["zip"].astype(str).str.zfill(5)
```

`errors="coerce"` turns unparseable values into `NaN` instead of crashing —
then you decide what to do with the missing values.

## 3. Duplicates — Exact and Near

```python
# Exact duplicates
dupes = df[df.duplicated(subset=["email"], keep="first")]
df = df.drop_duplicates(subset=["email"], keep="first")

# Normalize before de-duping (casing/whitespace make "real" dupes)
df["email_key"] = df["email"].str.strip().str.lower()
df = df.drop_duplicates(subset=["email_key"])

# Fuzzy near-duplicates (e.g. "ACME Inc." vs "ACME Inc")
import pandas as pd  # (use rapidfuzz in production)
```

A common ETL trick: create a **dedup key** column (normalized email / phone /
company), dedupe on it, then drop it.

## 4. Outliers — Detect, Decide, Document

```python
# IQR rule
q1, q3 = df["amount"].quantile([0.25, 0.75])
iqr = q3 - q1
outlier_mask = (df["amount"] < q1 - 1.5 * iqr) | (df["amount"] > q3 + 1.5 * iqr)

# Decide, don't delete blindly:
#  - cap/winsorize extreme-but-real values
df["amount_capped"] = df["amount"].clip(lower=q1 - 1.5 * iqr, upper=q3 + 1.5 * iqr)
#  - or keep and flag them for the model
df["is_outlier"] = outlier_mask.astype(int)
```

Outliers are frequently **signal** (fraud, spikes) — flag and keep rather than
silently drop.

## 5. Malformed Values & Inconsistent Text

```python
# Strip whitespace + normalize case
df["city"] = df["city"].str.strip().str.title()

# Unify synonyms
df["status"] = df["status"].replace({
    "active": "active", "ACTIVE": "active", "Active ": "active",
    "closed": "inactive", "disabled": "inactive",
})

# Split a combined field
df[["first", "last"]] = df["full_name"].str.split(" ", n=1, expand=True)

# Categorical cleanup via CategoricalDtype catches typos at assignment
df["status"] = pd.Categorical(df["status"],
                              categories=["active", "inactive"])
```

## 6. Missing Values — Strategy by Column

```python
# Inspect first
print(df.isna().sum(), df.isna().mean())

# Column-dependent strategy:
#  - numeric: median (robust) or mean
df["amount"] = df["amount"].fillna(df["amount"].median())
#  - categorical: mode or a dedicated "unknown" bucket
df["region"] = df["region"].fillna("unknown")
#  - time series: forward-fill
df["daily_users"] = df["daily_users"].ffill()
#  - rows that can't be repaired: drop
df = df.dropna(subset=["order_id"])
```

Rule of thumb: **fill with a justifiable value** (median, mode, ffill) or
**drop rows** — never leave `NaN` in a column a model will consume.

## 7. Reusable Cleaning Pipeline

```python
def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """One idempotent, documented cleaning pass."""
    df = df.copy()

    # 1. dtypes
    df["price"] = df["price"].str.replace(r"[\$,]", "", regex=True).astype(float)
    df["ordered_at"] = pd.to_datetime(df["ordered_at"], errors="coerce")

    # 2. dedupe on a normalized key
    df["_key"] = df["email"].str.strip().str.lower()
    df = df.drop_duplicates(subset=["_key"]).drop(columns="_key")

    # 3. text normalization
    df["city"] = df["city"].str.strip().str.title()

    # 4. missing values
    df["price"] = df["price"].fillna(df["price"].median())
    df = df.dropna(subset=["email"])

    return df


clean = clean_orders(raw)
```

Idempotent (running twice gives the same result), single-purpose, and
documented — exactly what a production ETL step looks like.

## Key Takeaways

1. Fix **dtypes first** — everything else is easier on well-typed data.
2. Dedupe on a **normalized key**, not the raw column.
3. Outliers: flag or cap, don't silently delete.
4. Missing data: median/mode/ffill with justification, or drop.
5. Wrap the whole pass in an idempotent, documented function.
