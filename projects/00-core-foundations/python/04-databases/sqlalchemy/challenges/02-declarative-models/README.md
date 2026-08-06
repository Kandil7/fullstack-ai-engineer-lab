# Challenge 02: Declarative Models — Schema Contract Builder

## 🥉 Bronze — Build the Model (~15 min)

**Task:** Implement `build_model_versions_model(base)` which returns a mapped
class (SQLAlchemy 2.0 style) named `ModelVersion` with table name `model_versions`.

**Signature:**
```python
def build_model_versions_model(base: type) -> type:
```

**Requirements:**
- Columns: `id` (PK), `model_name` String(80) NOT NULL, `version` int NOT NULL,
  `artifact_uri` String(300) NOT NULL
- Use `Mapped[...]` / `mapped_column(...)`

| Check | Expected |
|---|---|
| `cls.__tablename__` | `"model_versions"` |
| create_all on sqlite | succeeds |

**Constraints:** Any correct approach passes.

---

## 🥈 Silver — Constrained Registry (~35 min)

**Task:** Same class, but with `__table_args__` adding a
`UniqueConstraint("model_name", "version")` so registering the same
(model_name, version) twice raises `IntegrityError`.

**Signature:**
```python
def build_model_versions_model(base: type) -> type:
```

| Scenario | Expected |
|---|---|
| Insert `("bert", 1)`, then `("bert", 1)` again | Second insert raises `IntegrityError` |
| Insert `("bert", 1)`, then `("bert", 2)` | Both succeed |

**Constraints:** duplicates must fail at the DATABASE layer, not in Python.

---

## 🥇 Gold — Versioned Checked Model (~75 min)

**Task:** Same class plus `CheckConstraint("version >= 1")` and a
`before_insert` ORM event (listened via `event.listen`) that rejects
`artifact_uri` values that do not start with `"s3://"` by raising `ValueError`.

**Signature:**
```python
def build_model_versions_model(base: type) -> type:
```

| Scenario | Expected |
|---|---|
| `version=0` | `IntegrityError` on insert |
| `artifact_uri="local/path"` | `ValueError` raised at insert time |
| `artifact_uri="s3://models/bert/v1"`, version 3 | succeeds |

**Follow-up:** why is the CHECK constraint better than Python-side validation?
(Answer: every writer must honor it — the ORM, raw SQL, and other services.)

---

## Running

```bash
pytest challenges/02-declarative-models/test_challenge.py -v
```
