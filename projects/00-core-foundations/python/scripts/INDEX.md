# Scripts Index

Utility scripts for maintaining the Python learning module.

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate_structure.py` | Validates directory structure, file naming conventions, and required files per phase | `python scripts/validate_structure.py` |
| `check_typos.py` | Scans markdown and Python files for common typos | `python scripts/check_typos.py` |
| `update_readmes.py` | Regenerates INDEX.md files for each phase folder | `python scripts/update_readmes.py` |

## Running All Checks

```powershell
python scripts/validate_structure.py
python scripts/check_typos.py
python scripts/update_readmes.py
```

## Adding New Scripts

1. Place the script in this directory
2. Add an entry to this INDEX.md
3. Ensure it has a `--help` flag and follows the existing patterns