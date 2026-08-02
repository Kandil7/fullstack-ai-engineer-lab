"""
Shared helpers for the Python module test suite.

The exercise files are flat, self-contained scripts (not importable packages),
so the tests discover files on disk and run them as subprocesses - the same
way a learner would. This keeps the suite resilient to restructuring.
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # python/

# Files that cannot (or should not) be executed in a test run.
DEFAULT_SKIP = {
    "practice_all.py",          # interactive
    "practice_no_solutions.py", # interactive
    "39-pip.py",                # runs pip commands
    "40-virtualenv.py",         # creates virtualenvs
    "__init__.py",
}

# Case studies that require optional deps (category_encoders) or are being
# reworked; compile-checked separately.
PANDAS_CASE_STUDY_SKIP = {
    "23-case-study-timeseries.py",
    "24-case-study-ml-prep.py",
}


def discover_phase_files(phase_dir: str, skip: set[str] | None = None) -> list[Path]:
    """Return sorted .py files in a phase directory (relative to module root)."""
    skip = DEFAULT_SKIP if skip is None else DEFAULT_SKIP | set(skip)
    phase_path = PROJECT_ROOT / phase_dir
    if not phase_path.is_dir():
        return []
    return sorted(
        f for f in phase_path.iterdir()
        if f.suffix == ".py" and f.name not in skip
    )


def compile_check(path: Path) -> bool:
    """True if the file parses (BOM-tolerant, like the tokenizer)."""
    try:
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        compile(raw, path.name, "exec")
        return True
    except SyntaxError:
        return False


def run_py_file(path: Path, timeout: int = 90) -> subprocess.CompletedProcess:
    """Run a python file from the module root (utf-8 output, Agg backend)."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"}
    return subprocess.run(
        [sys.executable, str(path)],
        capture_output=True, text=True, timeout=timeout,
        cwd=str(PROJECT_ROOT), env=env,
    )
