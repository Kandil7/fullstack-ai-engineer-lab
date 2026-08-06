# Challenge 03: Session Lifecycle — Request-Scoped Service

## 🥉 Bronze — Save User (~15 min)

**Task:** Implement `save_user(session, name)` which adds a `User`, **commits**,
and returns the new primary key.

**Signature:**
```python
def save_user(session: Session, name: str) -> int:
```

**Requirements:**
- Add the user and commit (flush alone is not enough)
- Return the PK — it must be readable **after** commit (expiry keeps PKs)
- Do not create your own session; use the one you are given

| Input | Expected |
|---|---|
| `save_user(session, "ada")` | an `int > 0` |
| `save_user(session, "ada")` again | raises `IntegrityError` (name is unique) |

**Constraints:** The table is `users(id, name UNIQUE, role DEFAULT 'annotator')`.

---

## 🥈 Silver — Get or Create (~35 min)

**Task:** Implement `get_or_create(session, name)` which returns
`(user, created: bool)` — the classic registry write path.

**Signature:**
```python
def get_or_create(session: Session, name: str) -> tuple[User, bool]:
```

**Requirements:**
- Return `(existing_user, False)` when the name already exists
- Return `(new_user, True)` when this call inserted the row
- Load an existing user through the session — the second call in the same
  session must return **the same object** (identity map), not a copy

| Input | Expected |
|---|---|
| first call, fresh name | `(user, True)`, row persisted |
| second call, same name | `(user, False)` where `user is` the first result |

---

## 🥇 Gold — Transaction Boundary (~75 min)

**Task:** Implement `guarded_commit(session, name, fail)` which commits a new
user **unless** `fail=True`, in which case it rolls back and returns `None`.

**Signature:**
```python
def guarded_commit(session: Session, name: str, fail: bool) -> int | None:
```

**Requirements:**
- `fail=False` → commit, return the new id
- `fail=True` → rollback, return `None`, and leave the database **exactly**
  as it was (no ghost rows)
- A failed call must not disturb rows committed by earlier calls on the
  same session

| Input | Expected |
|---|---|
| `guarded_commit(s, "good", False)` | id, row exists |
| `guarded_commit(s, "bad", True)` | `None`, zero rows named "bad" |

**Follow-up:** why is a rollback that *silently swallows* a real exception
dangerous in a request handler? (Answer: the session is left mid-transaction —
the next request reuses a poisoned session; close and recreate it instead.)

---

## Running

```bash
pytest challenges/03-session-lifecycle/test_challenge.py -v
```

## Test File Structure

```
challenges/03-session-lifecycle/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
