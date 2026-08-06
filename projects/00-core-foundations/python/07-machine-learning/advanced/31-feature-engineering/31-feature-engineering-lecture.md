# Feature Engineering — The Highest-Leverage Work

> **Topic 31 — Modeling depth.** Numeric transforms, encodings (one-hot,
> ordinal, target, hashing), interactions, binning, date and text features —
> and the rule that every encoder fits on train only.

Companion exercise: `31-feature-engineering.py`

---

## 1. Why It Wins

The model is the easy part. Feature engineering — turning raw logs into
informative columns — is where tabular ML is won. A strong feature can beat a
better model; the reverse rarely happens.

## 2. Numeric Transforms

- **Log transform** fixes right-skewed distributions (income, latency,
  revenue): `np.log1p(x)`.
- **Clip / winsorize** caps outliers learned from train quantiles.
- **Standardization** (z-score) for linear models; trees don't need it.

## 3. Encoding Strategies

| Strategy | Use for | Notes |
|---|---|---|
| **One-hot** | Nominal low-cardinality (city, channel) | `handle_unknown="ignore"` |
| **Ordinal** | Ranked categories (free < pro < enterprise) | explicit `categories=` |
| **Target encoding** | High-cardinality categories | mean target per group, **smoothed**, fit on train only |
| **Hashing** | Very high cardinality | fixed-size, collision-tolerant |

**Target encoding** — replace a category with the mean target of its rows —
is the single most powerful encoding for high-cardinality features, and the
easiest to leak: it must be computed from train data only, with smoothing.

## 4. Interactions & Polynomials

`age * salary` captures joint effects:

```python
PolynomialFeatures(degree=2, include_bias=False)
# [age, salary] -> [age, salary, age^2, age*salary, salary^2]
```

## 5. Binning

`KBinsDiscretizer` turns continuous values into ordinal buckets (quantile or
uniform) — adds robustness to skewed data and helps linear models.

## 6. Date Features

Extract the signal hidden in timestamps: hour, day-of-week, month, season,
weekend flag, lags and diffs for time series.

## 7. Text Features

`CountVectorizer` / `TfidfVectorizer` turn short text (bios, notes) into
numeric features. Fit on train only — the vocabulary is learned data.

## 8. The Golden Rule — Fit Encoders on Train Only

Every encoder (one-hot, ordinal, target, tf-idf, binner) has a `fit` step that
learns from data. Fit it on the **training set** and transform the rest —
putting encoders inside a `Pipeline`/`ColumnTransformer` makes this automatic.

## 9. Real-World Use Case — E-commerce Conversion

```python
features = [
    log(order_count + 1),                 # skew fix
    target_encoded(product_category),     # high-cardinality
    price / median_price_per_category,    # relative pricing
    hour_of_day, is_weekend,              # temporal signals
    tfidf(customer_bio)[:20],             # text signal
]
```

## Key Takeaways

1. Log for skew, clip for outliers, scale for linear models.
2. One-hot nominal, ordinal ranked, target-encoded high-cardinality.
3. Interactions capture joint effects; binning adds robustness.
4. Dates → hour/dow/month; text → TF-IDF.
5. Every encoder fits on train only — or it leaks.
