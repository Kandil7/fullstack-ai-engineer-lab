# Maintenance Scripts

This directory contains utility scripts for maintaining the Python learning module.

## Scripts

- **[validate_structure.py](validate_structure.py)** — Validates the directory structure, file naming conventions, and required files per phase. Run after any reorganization.
- **[check_typos.py](check_typos.py)** — Scans markdown and Python files for common typos.
- **[update_readmes.py](update_readmes.py)** — Regenerates INDEX.md files for each phase folder with current file listings.

## Quick Start

```powershell
# Run all maintenance checks
python scripts/validate_structure.py
python scripts/check_typos.py
python scripts/update_readmes.py
```

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

See [INDEX.md](INDEX.md) for detailed usage of each script.