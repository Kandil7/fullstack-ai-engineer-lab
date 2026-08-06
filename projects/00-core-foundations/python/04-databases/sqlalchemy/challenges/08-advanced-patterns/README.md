# Challenge 08: Advanced Patterns — Hybrids, Vectors, Optimistic Locking

## 🥉 Bronze — Hybrid Promotable (~20 min)

**Task:** Implement `promotable_experiments(session)` which returns the names of
all experiments where the **SQL-side hybrid** `Experiment.is_leader` is true,
sorted by name.

**Signature:**
```python
def promotable_experiments(session: Session) -> list[str]:
```

**Requirements:**
- Filter with `Experiment.is_leader` **inside the WHERE clause** (the
  expression side of the hybrid) — not by loading everything into Python
- `is_leader` means `score >= 0.90` (already defined on the model)

| Input | Expected |
|---|---|
| "bert-run-1" score 0.92, "bert-run-2" score 0.85 | `["bert-run-1"]` |

---

## 🥈 Silver — Vector Round-Trip (~35 min)

**Task:** Implement `store_embedding(session, chunk_id, vector)` which stores an
embedding through the custom `VectorType` column and returns its id.

**Signature:**
```python
def store_embedding(session: Session, chunk_id: str, vector: list[float]) -> int:
```

**Requirements:**
- `Embedding.vector` stores `list[float]` as raw float32 bytes
- Reading the row back must return a `list[float]` equal to the input
  within float32 precision

| Input | Expected |
|---|---|
| `[0.25, 0.5, 0.75, 1.0]` | id; loaded vector `==` input (exact for these) |
| `[0.1, 0.2, 0.3]` | id; loaded vector ≈ input (float32, use approx) |

---

## 🥇 Gold — Ranked + Version-Guarded Update (~75 min)

**Task:** Implement two production functions:

1. `top_per_model(session, k)` — the top-k experiments **per model family**
   using `row_number() OVER (PARTITION BY model ORDER BY score DESC)` in one
   SQL query. Return `[(name, model, score)]` ordered by model, then rank.
2. `update_if_version(session, experiment_id, expected_version, new_score)` —
   optimistic update: only when the row's `version` still equals
   `expected_version`. The `before_update` event bumps `version` automatically;
   you just check, mutate, and commit.

**Signatures:**
```python
def top_per_model(session: Session, k: int = 1) -> list[tuple[str, str, float]]:
def update_if_version(session: Session, experiment_id: int, expected_version: int, new_score: float) -> bool:
```

**Requirements:**
- Window function in SQL — not Python sorting
- `update_if_version` returns `False` (no change) when the version is stale
- On success the version is bumped (1 → 2 → 3 …) and the score updated

| Input | Expected |
|---|---|
| bert: 0.92/0.85; gpt2: 0.93; `top_per_model(session, 1)` | `[("bert-run-1","bert",0.92), ("gpt-run-1","gpt2",0.93)]` |
| stale version `1` after a successful update | `False`, row unchanged |

**Follow-up:** why is the version check in `update_if_version` only as safe as
its concurrency? (Answer: check-then-write in Python has a race window — the
bulletproof version puts `WHERE version = :expected` in the UPDATE itself.)

---

## Running

```bash
pytest challenges/08-advanced-patterns/test_challenge.py -v
```

## Test File Structure

```
challenges/08-advanced-patterns/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
