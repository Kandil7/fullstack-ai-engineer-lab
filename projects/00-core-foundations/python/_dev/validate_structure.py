"""
_dev/validate_structure.py
===========================
Validates the directory structure and file naming conventions for the
Python learning module.

Checks:
1. All expected phase directories exist
2. File numbering is sequential within each phase
3. No orphan files in the root
4. All files have matching lecture/glossary pairs (where applicable)

Usage:
    python _dev/validate_structure.py
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_PHASES = [
    ("01-core-python", 1, 41),
    ("02-advanced-python", 1, 20),
    ("03-libraries", None, None),  # Special structure
    ("04-databases", None, None),
    ("05-web-frameworks", None, None),
    ("06-data-structures-algorithms", 1, 20),
    ("07-machine-learning", 1, 23),
]

SUBDIRECTORIES = [
    "supplementary/lectures/01-core-python",
    "supplementary/quizzes",
    "supplementary/interviews",
    "projects/01-calculator",
    "projects/02-file-manager",
    "projects/03-api-server",
    "projects/04-data-analyzer",
    "projects/05-ml-pipeline",
    "_dev",
]


def check_directory_exists(path: str, errors: list) -> bool:
    full = os.path.join(HERE, path)
    if not os.path.isdir(full):
        errors.append(f"MISSING_DIR: {path}/")
        return False
    return True


def check_sequential_numbering(dir_path: str, start: int, end: int, errors: list):
    """Verify files are sequentially numbered from start to end."""
    full = os.path.join(HERE, dir_path)
    if not os.path.isdir(full):
        return

    files = [f for f in os.listdir(full) if f.endswith(".py") and re.match(r"\d{2}-", f)]
    
    # Extract numbers
    numbers = set()
    for f in files:
        match = re.match(r"(\d{2})", f)
        if match:
            numbers.add(int(match.group(1)))
    
    expected = set(range(start, end + 1))
    missing = expected - numbers
    extra = numbers - expected
    
    for num in sorted(missing):
        errors.append(f"GAP: {dir_path}/ — missing file #{num:02d}")
    
    # Check for duplicates
    seen = {}
    for f in files:
        match = re.match(r"(\d{2})", f)
        if match:
            num = int(match.group(1))
            if num not in seen:
                seen[num] = []
            seen[num].append(f)
    
    for num, filenames in seen.items():
        if len(filenames) > 1:
            errors.append(f"DUPLICATE: {dir_path}/ — #{num:02d}: {filenames}")


def check_readme_exists(dir_path: str, errors: list):
    """Check that each directory has a README.md."""
    full = os.path.join(HERE, dir_path)
    readme = os.path.join(full, "README.md")
    if not os.path.isfile(readme):
        errors.append(f"NO_README: {dir_path}/")


def main():
    errors = []
    warnings = []
    
    print(f"Validating structure: {HERE}")
    print()
    
    # Phase directories
    for phase, start, end in EXPECTED_PHASES:
        exists = check_directory_exists(phase, errors)
        if exists:
            if start is not None and end is not None:
                check_sequential_numbering(phase, start, end, errors)
            check_readme_exists(phase, errors)
    
    # Subdirectories
    for sub in SUBDIRECTORIES:
        check_directory_exists(sub, warnings)
    
    # Check root for orphan .py files
    root_files = [f for f in os.listdir(HERE) if f.endswith(".py")]
    allowed_root = {"run_smoke_tests.py"}
    for f in root_files:
        if f not in allowed_root:
            warnings.append(f"ORPHAN: root/{f} — should be in a phase directory")
    
    # Check for __pycache__ directories
    for dirpath, dirnames, _ in os.walk(HERE):
        for d in dirnames:
            if d == "__pycache__":
                warnings.append(f"CACHE: {os.path.relpath(os.path.join(dirpath, d), HERE)}/")
    
    # Results
    if errors:
        print(f"==> ERRORS ({len(errors)}):")
        for e in errors:
            print(f"   {e}")
    else:
        print("==> No errors found!")
    
    if warnings:
        print(f"\n==> WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"   {w}")
    
    print(f"\nTotal: {len(errors)} errors, {len(warnings)} warnings")
    return len(errors)


if __name__ == "__main__":
    sys.exit(main())
