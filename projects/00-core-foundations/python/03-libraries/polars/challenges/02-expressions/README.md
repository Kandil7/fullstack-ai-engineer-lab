# Challenge 02: Polars Expressions

## 🥉 Bronze — Filter and Project (~15 min)

**Task:** Write the row-selection + column-projection stage of a feature
pipeline using expressions only.

**Signature:**
```python
def filter_and_project(df: pl.DataFrame, min_score: float, min_spend: float) -> pl.DataFrame:
```

**Requirements:**
- Keep rows where `score >= min_score` AND `spend >= min_spend`
- Output exactly two columns: `user`, `score`
- Predicates must use `&` with full parentheses — no `and`

| Input | Expected |
|-------|----------|
| 4-row frame (below) with `min_score=0.5, min_spend=15` | `[("c", 0.7)]` |

**Constraints:** n <= 10^3. Any correct approach passes.

---

## 🥈 Silver — Feature Derivation (~35 min)

**Task:** Derive three features in a single `with_columns` call.

**Signature:**
```python
def derive_features(df: pl.DataFrame) -> pl.DataFrame:
```

**Requirements:**
- `band`: `"high"` when `score >= 0.5` else `"low"` (via `pl.when/then/otherwise`)
- `score_rank`: rank of `score`, descending (highest score -> rank 1)
- `spend_norm`: `spend / 100`
- One `with_columns` call; all original columns preserved

| Input `score` | Expected `band` | Expected `score_rank` |
|---------------|-----------------|------------------------|
| `[0.9, 0.4, 0.7, 0.2]` | `["high", "low", "high", "low"]` | `[1.0, 3.0, 2.0, 4.0]` |

**Constraints:** n <= 10^6. No `.apply()`, no Python loops over rows.

---

## 🥇 Gold — Window Features at Scale (~75 min)

**Task:** Build a per-user ranked feature pipeline on a large frame,
combining window computations and grouped aggregates.

**Signature:**
```python
def group_ranked_features(df: pl.DataFrame) -> pl.DataFrame:
```

**Requirements:**
- Add `spend_rank_in_user` = `spend.rank()` over `user`
- Add `share_of_user` = `spend / sum(spend)` over `user`
- Then aggregate per user: `n_events` (pl.len), `max_share`
  (max of `share_of_user`), `spend_total` (sum of spend)
- Return one row per user, sorted by `user`

| Input user `[a, a, b]`, spend `[10, 30, 20]` | Expected |
|------|----------|
| `a`: n_events 2, max_share 0.75, spend_total 40; `b`: n_events 1, max_share 1.0, spend_total 20 | rows sorted by user |

**Constraints:** n <= 10^6 (test uses 200k rows). Must be pure
expressions — `.apply()` and `iter_rows` are forbidden.
**Follow-up:** why does `share_of_user` need `.over()` instead of a
`group_by` + join? (Answer: `.over()` aligns the aggregate back to the
original rows in one pass; a join would re-key and re-sort.)

---

## Running

```bash
python -m pytest 03-libraries/polars/challenges/02-expressions/test_challenge.py -v
```

## Test File Structure

```
challenges/02-expressions/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
