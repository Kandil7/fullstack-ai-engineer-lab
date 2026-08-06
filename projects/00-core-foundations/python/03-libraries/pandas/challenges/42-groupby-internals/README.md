# Challenge 42: GroupBy Internals

`groupby` is split-apply-combine in one call. This challenge makes you
reimplement the machinery manually (split by key, apply a function, combine
back), then proves your manual version is *identical* to the native one —
and finishes with real-world groupby analysis patterns.

## 🥉 Bronze — Manual Split-Apply-Combine (~20 min)

**Task:** Implement `manual_group_mean(df, key)`: split `df` into groups by
`key`, compute the mean of the numeric columns for each group, and combine
into a result indexed by the key values. Reimplement the mechanics — do not
call `df.groupby().mean()`.

**Signature:**
```python
def manual_group_mean(df: pd.DataFrame, key: str) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| 3 rows a / 2 rows b, cols `x, y` | 2 rows indexed a, b; means per group |
| empty frame | empty result |
| missing key column | `KeyError` |

**Constraints:** `n <= 10^3`, one key column. A solution that calls
`groupby` directly fails the "no native groupby" guard (the test monkeypatches
`pd.DataFrame.groupby` to raise).

---

## 🥈 Silver — Group Metrics Panel (~30 min)

**Task:** Implement `group_metrics(df, key)`: for every **numeric** column,
compute `mean`, `max`, and `count` per group, returned as a MultiIndex
DataFrame with level 0 = column name, level 1 = metric.

**Signature:**
```python
def group_metrics(df: pd.DataFrame, key: str) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| teams `a`/`b`, cols `score`, `age` | 6 rows: (score, mean|max|count), (age, mean|max|count) |
| group with missing values | `mean` skips NaN; `count` counts non-NaN |
| single column | 3 rows |

**Constraints:** `n <= 10^4`. Values must match `df.groupby(key)[col].agg(...)`
within `1e-9`. The `count` of an all-NaN group must be **0** (not the group size).

---

## 🥇 Gold — Cohort Retention Builder (~75 min)

**Task:** Implement `cohort_retention(df)`. `df` has columns
`user_id`, `month` (e.g., `"2024-01"`). Build the standard retention matrix:
rows = first-purchase month, columns = months since first purchase (0, 1, 2, …),
values = fraction of that cohort's users still active in that month.

**Signature:**
```python
def cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| 2 users: u1 buys `2024-01`, `2024-02`; u2 buys `2024-01` only | row `2024-01`: [1.0, 0.5]; no other rows |
| all users single-month | diagonal-only matrix of 1.0s |
| empty frame | empty result |

**Constraints:** `n <= 10^4`. Hint: `groupby("user_id")["month"].min()` gives
each user's first month; then month index − first-month index = months since
first purchase.

**Follow-up:** which cell is the *retention red flag* for a monthly-subscription
product? (Answer: the (cohort, 1) column — the fraction that returns after the
first month. Column 0 is 1.0 by construction.)

---

## Running

```bash
pytest challenges/42-groupby-internals/test_challenge.py -v
```

## Test File Structure

```
challenges/42-groupby-internals/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
