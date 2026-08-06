# Challenge 04: Polars pandas Comparison

## 🥉 Bronze — Filter Translation (~15 min)

**Task:** Translate a pandas boolean-mask filter into the equivalent
Polars expression and prove both select the same rows.

**Signature:**
```python
def polars_filter_equivalent(pdf: pd.DataFrame, campaign: str, min_rev: float) -> pl.DataFrame:
```

**Requirements:**
- Translate `pdf[(pdf["campaign"] == campaign) & (pdf["revenue"] >= min_rev)]`
- Keep the pandas row order (Polars preserves input order for filters)
- Return the Polars frame (call it `pl.from_pandas` at the entry)

| Input | Expected |
|-------|----------|
| 5-row frame, `campaign="a", min_rev=10.0` | rows matching the pandas mask, same order |

**Constraints:** n <= 10^3. Any correct approach passes.

---

## 🥈 Silver — Grouped Aggregation Parity (~35 min)

**Task:** Reproduce a pandas `groupby().agg({...})` result exactly with
Polars expressions.

**Signature:**
```python
def polars_groupby_equivalent(pdf: pd.DataFrame) -> pl.DataFrame:
```

**Requirements:**
- Reproduce: `groupby("campaign").agg(conversions=("converted", "sum"), revenue=("revenue", "mean"))` then `reset_index()`
- Sort both results by `campaign` before comparing
- Numeric equality to 1e-9, column-for-column

| Input | Expected |
|-------|----------|
| 100-row seeded frame | identical per-campaign sums/means |

**Constraints:** n <= 10^6. No `.apply()`, no row loops.

---

## 🥇 Gold — Three-Step Parity Suite (~75 min)

**Task:** Build a parity harness that runs a 3-step pipeline in both
engines and reports exact agreement.

**Signature:**
```python
def parity_suite(pdf: pd.DataFrame) -> dict[str, object]:
```

**Requirements:**
- Step 1: filter `revenue >= 5`; Step 2: join campaign budgets (left);
  Step 3: group by campaign, mean revenue
- Return `{"verdict": bool, "pandas_rows": list, "polars_rows": list}`
  where the row lists are the final aggregated rows sorted by campaign
- `verdict` is True iff the two final tables match exactly (1e-9)

| Input (200k seeded rows) | Expected |
|-------|----------|
| any frame | `verdict` True; both row lists identical |

**Constraints:** n <= 10^6. Polars side must be expression-only
(no `.apply()`), and it must handle the `budget` column arriving via
join, not by manual assignment.
**Follow-up:** what breaks first at 10^8 rows? (Answer: pandas
materializes intermediates; the Polars side streams.)

---

## Running

```bash
python -m pytest 03-libraries/polars/challenges/04-pandas-comparison/test_challenge.py -v
```

## Test File Structure

```
challenges/04-pandas-comparison/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
