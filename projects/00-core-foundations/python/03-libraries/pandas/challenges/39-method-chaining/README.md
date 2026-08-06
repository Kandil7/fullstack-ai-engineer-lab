# Challenge 39: Method Chaining

Chains turn a feature pipeline into one reviewable expression — but only if
each link returns a new frame and callables see the *filtered* state. This
challenge builds the three levels of chain discipline.

## 🥉 Bronze — Filter + Assign Chain (~15 min)

**Task:** Implement `chain_filter_assign(frame, min_spend)`, which returns a
**new** frame containing only rows with `spend > min_spend`, plus a
`log_spend` column computed with `np.log1p`. The input frame must not be
modified.

**Signature:**
```python
def chain_filter_assign(frame: pd.DataFrame, min_spend: float) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| `spend=[50, 120, 300], min=100` | 2 rows, `log_spend = log1p([120, 300])` |
| `spend=[10, 20], min=100` | 0 rows (empty frame, same columns) |
| `spend=[50, 120], min=50` | 1 row (`120` only — strict `>`) |

**Constraints:** `n <= 10^3`. Any correct approach passes.

---

## 🥈 Silver — Callable vs Precomputed Rank (~35 min)

**Task:** Implement `feature_chain(frame)`, the production chain from lecture
39: copy -> drop missing rows -> keep `plan == "free"` and `spend > 0` -> add
`log_spend` (`np.log1p`), `rank` (descending, **computed on the filtered
frame**), and `is_power_user` (spend >= 80th percentile of the filtered
frame) -> sort by spend descending.

**Signature:**
```python
def feature_chain(frame: pd.DataFrame) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| `spend=[400, 350, 200, 50, 300], plan=[pro, pro, free, free, free]` (filter `plan == "free"` first) | rank = `[2.0, 3.0, 1.0]` (free users only) |
| frame with a NaN row | NaN row dropped, 4 rows remain |
| all spends `<= 0` | empty frame, all columns present |

**Constraints:** `n <= 10^4`. The rank test **fails** if the rank was
computed on the full frame (the precomputed-Series bug) — the filter step
must come first and the callable must see the filtered state.

---

## 🥇 Gold — Pipe-able Transform Library (~75 min)

**Task:** Implement `add_rank_after_filter(frame, filter_expr, col)` which
applies `frame.query(filter_expr)`, then adds a `rank` column computed on
the **filtered** frame only (descending), returning the filtered frame. Also
implement `pipe_through(frame, *transforms)` which applies a sequence of
callables `(frame) -> frame` with `functools.reduce`/a loop — the pipe
mechanism — and returns the final frame.

**Signature:**
```python
def add_rank_after_filter(frame: pd.DataFrame, filter_expr: str, col: str) -> pd.DataFrame:
def pipe_through(frame: pd.DataFrame, *transforms) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| `spend=[400, 350, 200, 50, 300]`, `"plan == 'free'"`, `"spend"` | rank `[2.0, 3.0, 1.0]` — NOT `[4.0, 5.0, 3.0]` |
| `spend=[400, 350, 200, 50, 300]`, `"spend > 100"`, `"spend"` | rank `[1.0, 2.0, 4.0, 3.0]` |
| `pipe_through(df, add_a, add_b)` | both transforms applied in order |
| `pipe_through(df)` | identity — frame returned unchanged |

**Constraints:** `n <= 10^5`. The rank must be computed **after** the query —
a solution that ranks first and filters second produces wrong values and
fails.

**Follow-up:** what breaks if a transform in `pipe_through` returns `None`
(as `dropna(inplace=True)` does)? (Answer: the next call fails on
`'NoneType'` — chains require every link to return a frame.)

---

## Running

```bash
pytest challenges/39-method-chaining/test_challenge.py -v
```

## Test File Structure

```
challenges/39-method-chaining/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
