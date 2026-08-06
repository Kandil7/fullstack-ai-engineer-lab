# Challenge 05: Querying with select() — Registry Queries

## 🥉 Bronze — Done Experiments (~15 min)

**Task:** Implement `done_experiments(session)` which returns the **names** of all
experiments with `status == "done"`, sorted ascending.

**Signature:**
```python
def done_experiments(session: Session) -> list[str]:
```

**Requirements:**
- Use `select()` + `session.scalars()` — never legacy `.query()`
- Sort by name; exclude non-done statuses

| Input | Expected |
|---|---|
| done: "bert-finetune-1", "gpt-finetune-1"; running: "bert-finetune-2" | `["bert-finetune-1", "gpt-finetune-1"]` |

---

## 🥈 Silver — Best F1 per Model (~35 min)

**Task:** Implement `best_f1_per_model(session)` which returns `(model, best_f1)`
pairs for every model that has at least one `f1` metric, ordered by model.

**Signature:**
```python
def best_f1_per_model(session: Session) -> list[tuple[str, float]]:
```

**Requirements:**
- `JOIN` experiments to metrics and **filter to `metric == "f1"`** *before* grouping
- Aggregate with `func.max(EvalMetric.value)`; group by model
- Return models in ascending order

| Input | Expected |
|---|---|
| bert: f1 0.89, f1 0.81; gpt2: f1 0.93 | `[("bert", 0.89), ("gpt2", 0.93)]` |

**Watch out:** joining before filtering multiplies rows — the `max()` is only
meaningful when the join is narrowed to one metric.

---

## 🥇 Gold — Leaderboard (~75 min)

**Task:** Implement `metric_leaderboard(session, metric, min_value, limit)` which
returns `(experiment_name, value)` pairs for rows where the metric value is
**>= min_value**, sorted by value **descending**, limited to `limit`.

**Signature:**
```python
def metric_leaderboard(session: Session, metric: str, min_value: float, limit: int) -> list[tuple[str, float]]:
```

**Requirements:**
- Explicit join + filter — never expose a row without its metric
- Order by value DESC, then limit

| Input | Expected |
|---|---|
| f1 values 0.89/0.93/0.81, min 0.90 | `[("gpt-finetune-1", 0.93)]` |
| f1, min 0.80, limit 2 | top 2 by f1: `[("gpt-finetune-1", 0.93), ("bert-finetune-1", 0.89)]` |

**Follow-up:** how would you make the leaderboard deep-pageable without OFFSET?
(Answer: keyset — `WHERE (value, id) < (last_value, last_id) ORDER BY value DESC, id DESC`.)

---

## Running

```bash
pytest challenges/05-querying-2.0/test_challenge.py -v
```

## Test File Structure

```
challenges/05-querying-2.0/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
