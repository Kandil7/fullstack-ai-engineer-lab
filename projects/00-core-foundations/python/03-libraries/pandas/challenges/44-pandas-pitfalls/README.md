# Challenge 44: Pandas Pitfalls — The Bug Hunt

Every item below is a real bug report from production pandas code. Your job:
write the functions that handle the edge cases *correctly* — and prove the
"wrong" versions are wrong.

## 🥉 Bronze — NaN-Aware Filter (~15 min)

**Task:** Implement `filter_below(df, col, threshold)`: rows where
`col < threshold`, keeping **NaN rows out** of the result — but *return the
kept rows and the dropped rows separately* as a tuple.

**Signature:**
```python
def filter_below(df: pd.DataFrame, col: str, threshold: float) -> tuple[pd.DataFrame, pd.DataFrame]:
```

| Input | Expected |
|---|---|
| `[1, NaN, 5]`, threshold 4 | kept = rows 0 only; dropped = NaN row + 5 row |
| all NaN | kept empty, dropped all |
| no NaN | normal comparison |

**Constraints:** `n <= 10^3`. The naive `df[df[col] < threshold]` *silently
drops NaN rows* — correct here, but the test verifies you KNOW which rows
went where.

---

## 🥈 Silver — Duplicate-Key Merge Guard (~35 min)

**Task:** Implement `merge_check_duplicates(left, right, on)`: perform an
inner merge on `on`, but **raise `ValueError` if either input has duplicate
keys** — the classic "why did my rows multiply?" bug.

**Signature:**
```python
def merge_check_duplicates(left: pd.DataFrame, right: pd.DataFrame, on: str) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| unique keys both sides | normal merge |
| duplicate key in left | `ValueError` |
| duplicate key in right | `ValueError` |
| both unique but different key sets | normal merge (inner semantics) |

**Constraints:** `n <= 10^4`. A merge with duplicates is a silent
row-multiplication bug (1 `a`-row × 2 `a`-rows = 2 rows out). The guard
must check *before* merging.

---

## 🥇 Gold — Three-Way NaN Detection (~75 min)

**Task:** Implement `count_nan_mismatches(a: pd.Series, b: pd.Series) -> int`:
count positions where exactly **one** of the two series is NaN.

Then implement `safe_pct_change(series)`: `pct_change` that does **not**
silently ffill gaps — every NaN window surfaces as NaN instead of a
fabricated delta.

**Signature:**
```python
def count_nan_mismatches(a: pd.Series, b: pd.Series) -> int:
def safe_pct_change(series: pd.Series) -> pd.Series:
```

| Input | Expected |
|---|---|
| `a=[1, NaN, NaN]`, `b=[1, 2, NaN]` | 1 (position 1) |
| identical NaN patterns | 0 |
| `series=[10, NaN, 20]` | `[NaN, NaN, NaN]` (default `pct_change` gives `[NaN, 0.0, 1.0]`!) |
| `series=[10, 20, 30]` | `[NaN, 1.0, 0.5]` |

**Constraints:** `n <= 10^4`. The `pct_change` pitfall: the **default**
`pct_change()` calls `fill_method='pad'` — it ffill-replaces missing values
*before* computing deltas. `[10, NaN, 20]` silently becomes
`[NaN, 0.0, 1.0]`: a fabricated "no change" at the gap, and a 100% growth
computed from a value that never existed. The safe version passes
`fill_method=None` so gaps surface as NaN — and sidesteps the deprecation
warning (the default fill is being removed).

**Follow-up:** why is the default `pct_change` result dangerous for a
financial dashboard? (Answer: `[10, NaN, 20]` reports `0.0` for the missing
week — a real analyst reading "no change" when the data simply disappeared —
and `1.0` for a jump that was computed against a filled value. Missing data
must surface as NaN; the human decides how to treat gaps.)

---

## Running

```bash
pytest challenges/44-pandas-pitfalls/test_challenge.py -v
```

## Test File Structure

```
challenges/44-pandas-pitfalls/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
