# Tier 0 — Remediation Backlog

> **34 files fail or cannot run.** Every entry below was reproduced on 2026-07-29
> by executing the file and capturing the actual traceback. No guesses.
>
> **Rule: nothing new is written until this list is empty.** New content built on
> a broken baseline multiplies the debt and hides regressions.

---

## Summary

| Section | Fail | Total | Category |
|---|---|---|---|
| `01-core-python` | 0 | 41 | ✅ clean |
| `02-advanced-python` | 3 | 20 | logic, platform |
| `03-libraries/numpy` | 4 | 28 | API misuse, encoding |
| `03-libraries/pandas` | 14 | 45 | API drift, deps, syntax, **structural** |
| `03-libraries/matplotlib` | 0 | 20 | ✅ clean |
| `03-libraries/scipy` | 0 | 12 | ✅ clean |
| `04-databases/mysql` | 1 | 12 | SQL dialect |
| `04-databases/mongodb` | 2 | 11 | logic |
| `05-web-frameworks/django` | 20 | 20 | **dependency not installed** |
| `06-data-structures-algorithms` | 4 | 20 | logic, hang, encoding |
| `07-machine-learning` | 0 | 23 | ✅ clean |

**Root-cause distribution**

| Cause | Files | Note |
|---|---|---|
| Genuine logic bugs | 9 | Real defects that teach wrong behavior |
| Library API drift (pandas/numpy) | 8 | Written against older versions |
| Missing optional dependencies | 4 | `openpyxl`, `seaborn` |
| Windows console encoding (cp1252) | 4 | Unicode in `print()` |
| Platform/resource handling | 2 | Windows file locks, spawn semantics |
| SQL dialect mismatch | 1 | MySQL syntax on sqlite3 |
| Syntax error | 1 | File never ran |
| Infinite hang | 1 | Deadlock |
| Environment | 20 | Django absent |

---

## R1 — Blocking Bugs (fix first)

### R1.1 `06-data-structures-algorithms/04-queues.py` — hangs forever
**Measured:** `timeout 15` → exit code **124** (timeout). No traceback; never terminates.
**Cause:** `BoundedBuffer` (line ~463) is a condition-variable producer/consumer.
The demo at line ~505 calls it **sequentially on one thread**:
```python
for i in range(5):
    buffer.produce(i)      # capacity is 3 → 4th call blocks on not_full.wait()
```
With capacity 3, the 4th `produce` waits for a consumer that will never run,
because the consumer loop is *after* the producer loop on the same thread.
**Fix:** run producer and consumer in real `threading.Thread`s and `join()` them,
or size capacity ≥ item count for the sequential demo. The threaded version is
the better lesson — this file is *about* queues.
**Also:** the file's own comment admits `# Note: In real usage, these would run in
separate threads`, so the correct fix is the one the author intended.
**Blast radius:** blocks any CI run over this directory. Highest priority in the plan.

### R1.2 `03-libraries/pandas/20-performance.py` — `SyntaxError: unmatched ')'`
**Measured:** fails at parse time; the file has never executed.
**Fix:** repair the paren, then run. A syntax error surviving in the tree is the
clearest possible evidence that nothing gates this module (Gap A).

### R1.3 `06-data-structures-algorithms/09-binary-search-trees.py` — `AttributeError: 'BSTNode' object has no attribute 'val'`
**Cause:** two node classes coexist. `DLLNode` (line 353) defines `self.val`;
the BST's own node class defines `.data`. `bst_to_dll(bst.root)` (line 383) is
handed `BSTNode` objects, then line 389 reads `current.val`.
**Fix:** standardize on `.data` (matching the rest of the file and `08-binary-trees.py`),
or have `bst_to_dll` construct `DLLNode`s. Prefer the latter — converting a BST to
a DLL genuinely should produce DLL nodes, which is the real lesson.

### R1.4 `06-data-structures-algorithms/08-binary-trees.py` — `AttributeError: 'list' object has no attribute 'popleft'`
**Cause:** the file imports `deque` (line 18) and uses `deque([...])` correctly in
7 places, but lines **334**, **525**, **546** use a bare `queue = [root]` and then
call `.popleft()`.
**Fix:** `deque([root])` at those three lines.
**Teaching value:** worth a callout in the lecture — this is exactly the
`list`-vs-`deque` cost distinction from Gap B. `list.pop(0)` is O(n).

### R1.5 `02-advanced-python/17-multiprocessing.py` — `AttributeError: Can't get local object 'demo_basic_process.<locals>.worker'`
**Cause:** worker functions are defined *inside* another function. Windows uses
`spawn`, which re-imports and unpickles the target by qualified name; a closure
cannot be pickled. Also surfaces `PermissionError: [WinError 5]`.
**Fix:** move all worker callables to module top level; guard under
`if __name__ == "__main__":`.
**Teaching value:** this *is* the fork-vs-spawn lesson. The fix belongs in the
lecture as a named mistake, not just silently patched.

### R1.6 `02-advanced-python/19-logging.py` — `PermissionError: [WinError 32]`
**Measured:** `... file is being used by another process: 'C:\...\Temp\tmpi4xtpdf4.log'`
**Cause:** a `FileHandler` still holds the temp file open when the code tries to
delete it. POSIX permits unlinking an open file; Windows does not.
**Fix:** `logging.shutdown()` or `handler.close()` + `logger.removeHandler(...)`
before cleanup; wrap in `try/finally`.
**Note:** the `ZeroDivisionError` in this file's output is *intentional* (it demos
`logger.exception`) — do not "fix" that one.

### R1.7 `02-advanced-python/15-descriptors.py` — `TypeError: salary must be float, got int`
**Cause:** a validating descriptor with `expected_type=float` receives an `int`
literal. `isinstance(5, float)` is `False` — Python ints are not floats.
**Fix:** either pass `50000.0`, or accept `(int, float)` / use
`numbers.Real` in the descriptor.
**Teaching value:** genuine and worth keeping visible — the numeric tower is a
real trap. Demonstrate both the failure and the `numbers.Real` fix.

---

## R2 — Library API Drift

Written against older pandas/numpy; current versions reject them.

| File | Error | Fix |
|---|---|---|
`pandas/03-indexing-selection.py` | `ValueError: cannot set a row with mismatched columns` | `.loc[len(df)] = [...]` needs full-width row; use `pd.concat` or match column count |
`pandas/06-data-types.py` | `ValueError: Length of values (4) does not match length of index (20)` | Column assignment length mismatch; build with correct length or `Series` + index |
`pandas/07-string-methods.py` | `TypeError: StringMethods.replace() missing 1 required positional argument: 'repl'` | `.str.replace(pat, repl)` — `repl` no longer optional; add it and `regex=` explicitly |
`pandas/10-pivot-tables.py` | `ValueError: Index contains duplicate entries, cannot reshape` | `.pivot()` needs unique index/column pairs → use `.pivot_table(aggfunc=...)` |
`pandas/11-merging-joining.py` | `ValueError: Suffixes not supported when joining multiple DataFrames` | Drop `suffixes=` from multi-frame `.join()`, or chain pairwise merges |
`pandas/17-data-cleaning.py` | `ValueError: Bin edges must be unique` | `pd.qcut` on skewed data yields duplicate edges → `duplicates="drop"` |
`pandas/19-multiindex.py` | `TypeError: list keys are not supported in xs, pass a tuple instead` | `.xs(("a","b"))` not `.xs(["a","b"])` |
`pandas/21-styling.py` | `TypeError: Styler.highlight_null() got an unexpected keyword argument 'null_color'` | Renamed to `color=` |
`numpy/10-array-iterating.py` | `AttributeError: 'numpy.ndarray' object has no attribute 'index'` | `.index()` is a list method → `np.where(arr == v)[0][0]` |
`numpy/12-array-split.py` | `ValueError: array split does not result in an equal division` | `np.split` requires exact division → `np.array_split` |
`numpy/28-ufunc-set-operations.py` | `ValueError: truth value of an array ... is ambiguous` | `if arr:` on an array → `.any()` / `.all()` |

**Prevention:** pin minimum versions in `requirements.txt` and add a version-drift
CI job. These 11 failures are all "worked in 2023, broken in 2026" — a pinned
matrix would have caught each one.

---

## R3 — Windows Console Encoding (4 files)

**Measured errors**

| File | Character |
|---|---|
`numpy/27-ufunc-trigonometric.py` | `'\u03c0'` (π) |
`pandas/13-apply-map.py` | `'\U0001f34e'` (🍎) |
`06-dsa/07-trees.py` | box-drawing chars |
`+1 more` | emoji in output |

**Cause:** Windows console defaults to cp1252; these appear in `print()`.
**Fix:** ASCII in program output — `pi`, `[OK]`, `->`, `+--`. Unicode stays fine in
comments and markdown. This is standard **E10** in
[01-content-standards.md](01-content-standards.md).
**Alternative considered and rejected:** forcing `PYTHONIOENCODING=utf-8`. It
papers over the issue and still breaks for a learner running the file directly.

---

## R4 — Missing Optional Dependencies (4 files)

| File | Missing |
|---|---|
`pandas/15-io-csv-json.py` | `openpyxl` |
`pandas/16-io-excel-sql.py` | `openpyxl` |
`pandas/18-visualization.py` | `seaborn` |
`pandas/22-case-study-eda.py` | `seaborn` |

**Fix (both halves):**
1. Add `openpyxl>=3.1` and `seaborn>=0.13` to `requirements.txt` — currently in
   neither `requirements.txt` nor `pyproject.toml`, though `EXPANSION_PLAN.md`
   lists `seaborn`.
2. Guard the import so the file degrades instead of crashing:
   ```python
   try:
       import seaborn as sns
       HAS_SEABORN = True
   except ImportError:
       HAS_SEABORN = False
       print("[skip] seaborn not installed — pip install seaborn")
   ```
Teaching files should never hard-crash on an optional extra.

---

## R5 — SQL Dialect

### `04-databases/mysql/08-delete.py` — `sqlite3.OperationalError: near "LIMIT": syntax error`
**Cause:** `DELETE ... LIMIT n` is MySQL-only. The module deliberately uses
`sqlite3` as a stand-in (documented in `README.md`), and sqlite3 rejects it
unless compiled with `SQLITE_ENABLE_UPDATE_DELETE_LIMIT`.
**Fix:** portable subquery —
```sql
DELETE FROM t WHERE rowid IN (SELECT rowid FROM t WHERE cond LIMIT 1);
```
**Teaching value:** a genuine portability lesson. Note both forms in the lecture.
**Related:** Phase 4 should move to real Postgres — see
[05-phase-4-databases.md](05-phase-4-databases.md).

---

## R6 — MongoDB Logic Bugs

| File | Error | Cause |
|---|---|---|
`mongodb/06-query.py` | `AttributeError: 'str' object has no attribute 'keys'` | Query helper assumes a dict operand but gets a bare string |
`mongodb/11-aggregation.py` | `AttributeError: 'int' object has no attribute 'get'` | Pipeline stage iterates documents but receives already-reduced scalars |

Both live in the dict-based MongoDB simulator. Fix the simulator's type handling
and add `assert`s covering the mixed-type paths that broke.
**Consider:** Phase 4 rework replaces the simulator with real MongoDB via Docker
(already in `infra/docker/`). The simulator hides exactly this class of bug.

---

## R7 — Django Cannot Run At All (20 files)

**Measured:** `python -c "import django"` → `ModuleNotFoundError`.
**Cause:** `django` is commented out in `requirements.txt`
(`# django>=5.0.0`) though `pyproject.toml` lists `django>=4.2` as a *core*
dependency. The two files contradict each other.
**Decision required — pick one:**

| Option | Consequence |
|---|---|
| **A. Install Django**, add to `requirements.txt`, make files runnable | +20 runnable files; Django is not central to AI engineering |
| **B. Mark Django reference-only**, exclude from smoke tests, state it in README | Honest; keeps CI green; `README.md` already calls it "(reference)" |

**Recommendation: B.** `README.md` already describes Django as reference and
FastAPI as runnable. Formalize that: exclude `django/` from the smoke runner and
say so. Invest the freed effort in production FastAPI
([06-phase-5-backend.md](06-phase-5-backend.md)), which matters far more for this
career target. Resolve the `pyproject.toml`/`requirements.txt` contradiction either way.

---

## R8 — Structural: pandas Double Series

**Not a crash — a curriculum defect.** `03-libraries/pandas/` holds **45**
exercises but only **24** lectures and **24** glossaries, because two series were
merged. Prefixes `02`–`13` are each duplicated:

| W3Schools series (has lectures) | EXPANSION_PLAN series (**no lectures**) |
|---|---|
`02-getting-started.py` | `02-inspecting-data.py` |
`03-series.py` | `03-indexing-selection.py` |
`04-dataframes.py` | `04-filtering.py` |
`05-load-data.py` | `05-missing-data.py` |
`06-reading-json.py` | `06-data-types.py` |
`07-data-viewing.py` | `07-string-methods.py` |
`08-data-selecting.py` | `08-datetime.py` |
`09-data-loc.py` | `09-groupby-aggregation.py` |
`10-data-drop.py` | `10-pivot-tables.py` |
`11-rename-columns.py` | `11-merging-joining.py` |
`12-iterating.py` | `12-window-functions.py` |
`13-clearing-data.py` | `13-apply-map.py` |

**21 files have no lecture and no glossary** (`14-categorical-data` through
`22-case-study-eda`, plus the twelve above).

**Recommended resolution:** keep **both**, renumbered into one 34-topic
progression — basics first (W3Schools set), then the professional set
(groupby/pivot/window/performance), which is genuinely more advanced and is what
an AI engineer actually uses. Then author the 21 missing lecture/glossary pairs.
Full renumbering table: [04-phase-3-libraries.md](04-phase-3-libraries.md).

**Do not** delete the EXPANSION_PLAN series — `20-performance`, `19-multiindex`,
and `12-window-functions` are the highest-value pandas content in the module.

---

## R9 — Documentation Corrections

| File | Claim | Reality |
|---|---|---|
`python/README.md` | "405+ files" | **1128** |
`python/README.md` | `01-core-python` = 43 files | 41 numbered + 2 practice |
`python/README.md` | `pandas/ (24 files)` | **45** |
`python/README.md` | `supplementary/lectures/01-core-python/` = 82 files | Lectures live at `<section>/lectures/` |
`python/README.md` | quizzes "29" / interviews "16" | 29 ✅ / **15** |
`EXPANSION_PLAN.md` | pandas `0 files ❌ MISSING` | 45 exist |
`EXPANSION_PLAN.md` | matplotlib `0 files ❌ MISSING` | 20 exist |
`EXPANSION_PLAN.md` | "Plan created: July 2024" | inconsistent with July 2026 content |
`01-core-python/README.md` | "43 exercise files" | 41 + 2 |
`01-core-python/lectures/README.md` | "consistent format" | drifts after file 14 |
`learning_path.md` | lectures at `supplementary/lectures/01-core-python/` | wrong path |
`pyproject.toml` vs `requirements.txt` | django core vs commented out | contradiction (R7) |
`pyproject.toml` | `[tool.pytestini_options]` typo | dead section; `asyncio_mode` never applied |

Also: `pyproject.toml` has both `[tool.pytest.ini_options]` and a separate
`pytest.ini` — two competing configs with different `testpaths`. Consolidate.

---

## R10 — CI Gate (the fix that prevents recurrence)

None of the 34 failures would have survived a gate. Establish one.

**Extend `run_smoke_tests.py`:**
- `--all` runs every numbered exercise per section
- `--verify` passes `--verify` to invoke each `_verify()`
- Per-file timeout (30s) so an R1.1-style hang fails instead of hanging forever
- Skip list with *reasons*: `33-user-input.py` (stdin), `django/*` (R7)
- Sets `MPLBACKEND=Agg`, `PYTHONHASHSEED=0`, seeds RNGs
- Exit non-zero on any failure; print a summary table

**GitHub Actions:**
```yaml
strategy:
  matrix:
    python: ["3.10", "3.12"]
    os: [ubuntu-latest, windows-latest]   # windows-latest catches R3 encoding
```
Windows in the matrix is essential — all four encoding failures and both platform
failures are Windows-only, and this is a Windows development machine.

---

## Execution Order

| Step | Work | Rationale |
|---|---|---|
| 1 | R1.1 (hang), R1.2 (syntax) | Block all CI |
| 2 | R1.3–R1.7 (logic bugs) | Teach wrong behavior |
| 3 | R3 (encoding), R4 (deps) | Mechanical, unblocks 8 files |
| 4 | R2 (API drift) | Mechanical, unblocks 11 files |
| 5 | R5, R6 (SQL, Mongo) | Isolated |
| 6 | R7 decision (Django) | Needs your call — see recommendation |
| 7 | R8 (pandas restructure) | Largest; touches 45 files + 21 new lecture pairs |
| 8 | R9 (docs), R10 (CI) | Locks in correctness |

**Exit criteria for Tier 0:**
- `python run_smoke_tests.py --all --verify` exits 0
- `pytest tests/ -q` green
- Green on Ubuntu + Windows, Python 3.10 + 3.12
- Every documented count matches reality

---

*Backlog measured 2026-07-29 against commit `c4a4eec`. Reproduce any entry by running the named file.*
