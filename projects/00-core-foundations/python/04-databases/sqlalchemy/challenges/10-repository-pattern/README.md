# Challenge 10: Repository Pattern — Storage Behind a Contract

## 🥉 Bronze — Pure Domain Rules (~15 min)

**Task:** Implement two pure functions — no session, no SQL:

1. `should_promote(score)` — `True` when the run is good enough to promote
   (`score >= 0.9`).
2. `best_model_name(experiments)` — the model name of the highest-scoring
   experiment, or `None` for an empty list.

**Signatures:**
```python
def should_promote(score: float) -> bool:
def best_model_name(experiments: list[Experiment]) -> str | None:
```

| Input | Expected |
|---|---|
| `should_promote(0.9)` / `should_promote(0.89)` | `True` / `False` |
| two experiments, scores 0.7 vs 0.95 | model of the 0.95 one |
| `[]` | `None` |

---

## 🥈 Silver — In-Memory Repository (~35 min)

**Task:** Implement `InMemoryExperimentRepository` honoring the
`ExperimentRepository` **Protocol** (add / get / list_all / count / delete).

**Requirements:**
- `add(exp)` → returns the id; **duplicate name raises `ValueError`**
- `get(name)` → the experiment or `None`; `delete(name)` → `True`/`False`
- It must pass `isinstance(repo, ExperimentRepository)` (structural typing)

| Operation | Expected |
|---|---|
| `add` then `get("x")` | same experiment |
| `add` with an existing name | `ValueError` |
| `delete("missing")` | `False` |

---

## 🥇 Gold — SQL Repository + Unit of Work (~75 min)

**Task:** Implement two pieces:

1. `SqlExperimentRepository(session)` — the same Protocol backed by
   SQLAlchemy: `add` flushes (assigns the PK) but **never commits** (the
   caller owns the transaction); `get`/`list_all`/`count`/`delete` query the
   session.
2. `register_batch_with_transaction(session, experiments)` — **all-or-nothing**
   registration: add every experiment, commit once, return the ids. If any
   name is a duplicate, roll back and raise `ValueError` — **no partial rows
   may survive**.

**Signatures:**
```python
class SqlExperimentRepository:
    def __init__(self, session: Session) -> None: ...
    def add(self, experiment: Experiment) -> int: ...
    def get(self, name: str) -> Experiment | None: ...
    def list_all(self) -> list[Experiment]: ...
    def count(self) -> int: ...
    def delete(self, name: str) -> bool: ...

def register_batch_with_transaction(session: Session, experiments: list[Experiment]) -> list[int]:
```

**Requirements:**
- After `repo.add(exp)`, `exp.id` is assigned but **not visible to a fresh
  session** until the caller commits
- A failing batch leaves the table exactly as it was (count unchanged)

| Input | Expected |
|---|---|
| clean batch of 3 | `[id1, id2, id3]`, all rows persisted |
| batch containing a duplicate name | `ValueError`, table unchanged |

**Follow-up:** why does the repository never commit? (Answer: transaction
ownership — the service above it decides commit vs rollback, so several
repositories can share ONE transaction.)

---

## Running

```bash
pytest challenges/10-repository-pattern/test_challenge.py -v
```

## Test File Structure

```
challenges/10-repository-pattern/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
