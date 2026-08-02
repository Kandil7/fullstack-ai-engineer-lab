# Maintenance Guide

This document explains how the `outputs/` and `scripts/` directories work and how to maintain them.

---

## outputs/ — Exercise Artifacts

All exercise-generated artifacts (PNG plots, SQLite databases) are written to `outputs/` instead of the python/ root. This keeps the module clean and predictable.

### Structure

```
outputs/
├── scipy/          # 43 PNGs from SciPy exercises (plt.savefig)
├── matplotlib/     # PNGs from Matplotlib exercises
└── dbs/            # SQLite DBs from FastAPI exercises (3 files)
    └── README.md   # Explains these are runtime artifacts
```

### How It Works

1. **SciPy exercises** (`03-libraries/scipy/0X-*.py`):
   - Use `pathlib.Path(__file__).parent.parent.parent / "outputs" / "scipy" / filename`
   - This resolves to `python/outputs/scipy/` regardless of where the script is run from

2. **FastAPI exercises** (`05-web-frameworks/fastapi/18-database.py`, `19-orm.py`, `exercises/19-orm.py`):
   - Use `sqlite:///../../../outputs/dbs/filename.db` for SQLAlchemy
   - Or `pathlib.Path(__file__).parent.parent.parent / "outputs" / "dbs" / filename` for raw sqlite3

3. **Matplotlib exercises** (any phase):
   - Use `outputs/matplotlib/` via relative path from project root

### Regenerating Outputs

```bash
# From python/ directory
python run_smoke_tests.py --clean-outputs

# Or just run the exercises normally — they recreate outputs/ on each run
cd 03-libraries/scipy
python 01-introduction.py
# PNG appears in ../../outputs/scipy/
```

### Cleaning Outputs

```bash
# Remove all generated artifacts
Remove-Item -Path outputs\scipy\*, outputs\matplotlib\*, outputs\dbs\* -Force

# Or use the smoke test flag
python run_smoke_tests.py --clean-outputs
```

---

## scripts/ — Maintenance Utilities

Three utility scripts for module maintenance:

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate_structure.py` | Validates directory structure, file naming, required files per phase | `python scripts/validate_structure.py` |
| `check_typos.py` | Scans markdown and Python files for common typos | `python scripts/check_typos.py` |
| `update_readmes.py` | Regenerates INDEX.md files for each phase folder | `python scripts/update_readmes.py` |

### Running All Checks

```powershell
python scripts/validate_structure.py
python scripts/check_typos.py
python scripts/update_readmes.py
```

### Adding New Scripts

1. Place the script in `scripts/`
2. Add an entry to `scripts/INDEX.md`
3. Ensure it has a `--help` flag and follows existing patterns

---

## Adding New Phases (8, 9, etc.)

When adding Phase 8 (MLOps) and Phase 9 (GenAI):

1. Create `08-mlops/` and `09-genai/` directories with same internal structure
2. Update `run_smoke_tests.py` — add to `phases` list
3. Update `README.md` — add row to Quick Navigation table
4. Update `learning_path.md` — add new phase section
5. Add quizzes to `supplementary/quizzes/`
6. Add interviews to `supplementary/interviews/`
7. Add capstones to `capstones/`
6. Record decisions in `admin/DECISIONS.md`

---

## Gitignore Notes

The following patterns are in `.gitignore`:

```
# Python learning module
python/outputs/**
python/scipy_*.png
python/*.db
capstones/**/.venv
capstones/**/__pycache__
```

The `outputs/` directory is fully gitignored — fresh clones won't have artifacts, but exercises regenerate them on first run.