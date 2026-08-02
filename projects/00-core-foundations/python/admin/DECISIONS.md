# Admin Directory — Maintenance & Planning

This directory contains administrative and planning documents that are **off the learning path**. Learners should follow `learning_path.md` at the root instead.

## Contents

| File | Purpose |
|------|---------|
| `EXPANSION_PLAN.md` | Curriculum expansion plan for Phases 8 (MLOps) and 9 (GenAI) |
| `mastery-plan/` | 13 curriculum design documents from the original mastery plan |
| `DECISIONS.md` | This file — reorganization decisions log |
| `MAINTENANCE.md` | How to regenerate outputs/ and use scripts/ |

---

## Reorganization History

### August 2026 — Major Reorganization

**Trigger:** Two waves of work (Jul 29 bulk generation + Aug 2 live runs) left the directory messy with:
- 50+ stray PNGs at python/ root
- 3 SQLite DBs at python/ root
- Double-nested supplementary/interviews/interviews/ and supplementary/quizzes/quizzes/
- Pandas and Matplotlib with colliding numbered file series
- _dev/ with non-standard naming
- projects/ path clash with parent projects/
- Empty orphan dirs (downloads/, media/, uploads/)
- pyproject.toml ↔ pytest.ini conflict
- docs/mastery-plan/ arguably superseded by EXPANSION_PLAN.md

**Decisions Made:**

1. **Output Hygiene** → Created `outputs/` with subdirs `scipy/`, `matplotlib/`, `dbs/`. All exercise artifacts now land there. Updated SciPy and FastAPI exercises to write to these paths via `pathlib`.

2. **Pandas/Matplotlib Double-Sets** → Moved the "advanced" series (from EXPANSION_PLAN.md) into `pandas/advanced/` and `matplotlib/advanced/` with fresh sequential numbering (01–21 and 01–17). The original W3Schools-style series stays at the phase root as the canonical ladder.

3. **Supplementary Flattening** → Moved `supplementary/interviews/interviews/*` → `supplementary/interviews/` and `supplementary/quizzes/quizzes/*` → `supplementary/quizzes/`. Removed empty inner directories.

4. **Dev Utilities** → Renamed `_dev/` → `scripts/` (standard naming). Added `INDEX.md` and `README.md`.

5. **Capstones** → Renamed `projects/` → `capstones/` to avoid path clash with parent `projects/00-core-foundations/python/projects/`. Updated all references in `run_smoke_tests.py`, `README.md`, `learning_path.md`.

6. **Admin Docs** → Created `admin/` for off-path docs. Moved `EXPANSION_PLAN.md` and `docs/mastery-plan/` there. Added `DECISIONS.md` (this file) and `MAINTENANCE.md`.

7. **Pytest Config** → Picked `pytest.ini` as source of truth (points to `tests/`). Removed `[tool.pytest.ini_options]` from `pyproject.toml`. Removed `[tool.coverage.*]` (unused).

8. **Gitignore** → Extended with python-specific patterns for `outputs/`, `capstones/`.

9. **Cleanup** → Deleted `err.txt` (stale), `downloads/`, `media/`, `uploads/` (all empty).

**Verification:** All changes made in a single commit. Smoke tests pass for all 7 phases.

---

## Future Reorganizations

When adding Phase 8 (MLOps) and Phase 9 (GenAI):

1. Add `08-mlops/` and `09-genai/` as new phase directories
2. Update `run_smoke_tests.py` phases list
3. Update `README.md` quick navigation table
4. Update `learning_path.md` with new phases
5. Add new quizzes/interviews to `supplementary/`
6. Add new capstones to `capstones/`
7. Record decisions in this file