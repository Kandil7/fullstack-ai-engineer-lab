# Challenge 07: Async SQLAlchemy — Async Prediction Ingest

## 🥉 Bronze — Async Count (~20 min)

**Task:** Implement `async def count_models(engine)` which returns the distinct
model names stored in `predictions`, sorted ascending.

**Signature:**
```python
async def count_models(engine) -> list[str]:
```

**Requirements:**
- Open an `AsyncSession` from an `async_sessionmaker(engine)` (your own)
- `await` every DB operation — never call sync methods on an async session
- Return `[]` on an empty table

| Input | Expected |
|---|---|
| models "bert", "gpt2", "bert" | `["bert", "gpt2"]` |

---

## 🥈 Silver — Batch Ingest (~35 min)

**Task:** Implement `async def ingest_batch(engine, rows)` which inserts a list
of `{model, input_hash, latency_ms}` dicts in one transaction and returns the
row count.

**Signature:**
```python
async def ingest_batch(engine, rows: list[dict]) -> int:
```

**Requirements:**
- One `add_all` + one `await session.commit()`
- Rows are visible to a later `count_models` call
- Duplicate `input_hash` (unique) → `IntegrityError` raised, and the session
  must be closed so the engine stays usable afterwards

| Input | Expected |
|---|---|
| 3 rows | `3`, then `count_models` sees all 3 |

---

## 🥇 Gold — Request + Greenlet Bridge (~75 min)

**Task:** Implement two functions:

1. `async def simulate_async_request(engine, model, input_hash)` — the
   simulated endpoint body: write one prediction row and return
   `f"stored {input_hash}"`.
2. `async def run_sync_count(engine)` — count all rows using the **greenlet
   bridge**: a sync helper executed via `session.run_sync(...)`.

**Signatures:**
```python
async def simulate_async_request(engine, model: str, input_hash: str) -> str:
async def run_sync_count(engine) -> int:
```

**Requirements:**
- `simulate_async_request` uses `async_sessionmaker` + commit, exactly like a
  FastAPI endpoint body
- `run_sync_count` must call a plain **sync** function through `run_sync`
  (the helper does the `select().all()` inside)
- After a duplicate-hash `IntegrityError`, a fresh request must still work

| Input | Expected |
|---|---|
| `simulate_async_request(engine, "bert", "h1")` | `"stored h1"`; row persisted |
| after 2 stored rows | `run_sync_count(engine) == 2` |

**Follow-up:** why can't you just call `session.scalars()` directly in
`run_sync_count`? (Answer: the sync helper runs inside a greenlet — it must
stay fully synchronous; the *bridge* is what converts it.)

---

## Running

```bash
pytest challenges/07-async-sqlalchemy/test_challenge.py -v
```

## Test File Structure

```
challenges/07-async-sqlalchemy/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
