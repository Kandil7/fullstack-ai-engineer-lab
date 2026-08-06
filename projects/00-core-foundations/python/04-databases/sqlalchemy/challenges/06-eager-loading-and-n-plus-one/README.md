# Challenge 06: Eager Loading and the N+1 Problem (STAR)

> The star challenge: the tests **count SQL statements** — a lazy solution
> cannot pass. You must fix the N+1, not just return the right rows.

## 🥉 Bronze — Selectin Load (~20 min)

**Task:** Implement `load_projects(session)` which returns
`[(project_name, [run_names...])]` for every project, ordered by project id,
with **exactly 2 SQL queries** total (1 for projects, 1 `IN (...)` for runs).

**Signature:**
```python
def load_projects(session: Session) -> list[tuple[str, list[str]]]:
```

**Requirements:**
- Use `selectinload(Project.experiments)` — the lazy default is **wrong** here
- Tests assert `counter.count() == 2` right after your call

| Input | Expected |
|---|---|
| 3 projects × 2 experiments | `[("campaign-0", ["campaign-0-run-0", ...]), ...]` |

---

## 🥈 Silver — Joined Load (~35 min)

**Task:** Implement `load_projects_joined(session)` with the same return shape
using `joinedload`, and remember the de-duplication rule.

**Signature:**
```python
def load_projects_joined(session: Session) -> list[tuple[str, list[str]]]:
```

**Requirements:**
- **Exactly 1 query** (a single LEFT OUTER JOIN)
- No duplicate projects in the result — apply `.unique()` on the result
  (2.0 `scalars()` does not do it automatically for joined collections)

| Input | Expected |
|---|---|
| 3 projects × 2 experiments | 3 project entries, 6 runs total, 1 query |

---

## 🥇 Gold — Fail Loudly, Not Slowly (~75 min)

**Task:** Implement `fetch_projects_with_runs(session)` — the production listing
function — with **at most 2 queries**, returning `[(name, [runs])]`; and
`lazy_access_raises(session)` which loads a project from the strict table and
returns the exception **name** raised when its unloaded `experiments`
collection is touched.

**Signatures:**
```python
def fetch_projects_with_runs(session: Session) -> list[tuple[str, list[str]]]:
def lazy_access_raises(session: Session) -> str:
```

**Requirements:**
- `fetch_projects_with_runs` uses `selectinload`; ≤ 2 queries, exact same shape
- `StrictProject.experiments` is declared `lazy="raise"` — touching it must
  raise `InvalidRequestError`; return `"InvalidRequestError"` from the helper
- Seed rows in `strict_projects` before testing it

| Input | Expected |
|---|---|
| strict project with 1 run | `"InvalidRequestError"` |

**Follow-up:** why does `lazy="raise"` belong in the *model*, not just in the
query? (Answer: it turns an accidental N+1 into a loud test failure anywhere in
the codebase — the ORM equivalent of a canary.)

---

## Running

```bash
pytest challenges/06-eager-loading-and-n-plus-one/test_challenge.py -v
```

## Test File Structure

```
challenges/06-eager-loading-and-n-plus-one/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests (they count queries!)
```
