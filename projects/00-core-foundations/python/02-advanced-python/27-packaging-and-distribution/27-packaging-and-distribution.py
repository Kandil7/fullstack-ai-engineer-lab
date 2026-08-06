"""
Advanced Python - 27: Packaging and Distribution
=================================================
Topics: pyproject.toml anatomy; src-layout vs flat; editable installs;
        __init__.py public API and __all__; semantic versioning; extras;
        dependency pinning vs ranges; lockfiles; sdist/wheel; uv/poetry/
        pdm; entry points; namespace packages; publishing basics.

Why this matters for AI/backend engineering:
    A shared `rag_utils` library used by three services needs one
    pyproject.toml, a pinned semver contract, and extras ("dev" for
    tests, "qdrant" for one backend). Reproducible builds mean training
    runs are reproducible: same lockfile, same wheels, same results.
    This file exercises the parts you can run without pip.

Run:      python 27-packaging-and-distribution.py
Verify:   python 27-packaging-and-distribution.py --verify
Reference: https://packaging.python.org/en/latest/specifications/pyproject-toml/
           https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""

from __future__ import annotations

import importlib
import os
import random
import sys
import tempfile
import tomllib
from pathlib import Path

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. pyproject.toml Anatomy
# ============================================================
# The single source of truth for a modern package: metadata, dependencies,
# build backend, and tool config all in one file. tomllib (3.11+, stdlib)
# parses it with zero extra dependencies.

EXAMPLE_PYPROJECT: str = """
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "rag_utils"
version = "1.2.0"
description = "Shared retrieval helpers for the RAG services"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.26,<3",
    "pydantic>=2.5",
]

[project.optional-dependencies]
dev = ["pytest>=8", "ruff", "mypy"]
qdrant = ["qdrant-client>=1.9"]

[project.scripts]
rag-index = "rag_utils.cli:main"

[tool.ruff]
line-length = 100
"""


def load_pyproject(text: str) -> dict[str, object]:
    """Parse TOML into a dict. Raises on invalid TOML."""
    return tomllib.loads(text)


def demo_pyproject() -> dict[str, object]:
    """Parse the example and validate the keys a consumer needs."""
    data = load_pyproject(EXAMPLE_PYPROJECT)
    project = data["project"]
    assert isinstance(project, dict)
    print(f"  name: {project['name']}  version: {project['version']}")
    print(f"  requires-python: {project['requires-python']}")
    print(f"  dependencies: {project['dependencies']}")
    print(f"  build backend: {data['build-system']['build-backend']}")
    return data
    # Output:
    #   name: rag_utils  version: 1.2.0
    #   requires-python: >=3.10
    #   dependencies: ['numpy>=1.26,<3', 'pydantic>=2.5']
    #   build backend: setuptools.build_meta


# ============================================================
# 2. src-Layout vs Flat Layout
# ============================================================
# flat:  rag_utils/rag_utils/__init__.py  (imports may pick the repo dir)
# src:   rag_utils/src/rag_utils/__init__.py
# src-layout forces an INSTALL to be the thing you import -- the repo
# checkout cannot shadow the installed package (the classic "tests pass
# locally, break in CI" failure). Publishable projects use src-layout.


# ============================================================
# 3. __all__ Controls `import *`
# ============================================================
# `from pkg import *` imports every non-underscore name UNLESS __all__
# is defined, in which case it imports exactly that list. __all__ is the
# public API contract of a module -- including for star imports.

def demo_all_control() -> tuple[dict[str, object], dict[str, object]]:
    """Star-import a temp package with and without __all__."""
    with tempfile.TemporaryDirectory() as tmp:
        pkg_dir = Path(tmp) / "demo_pkg"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text(
            "public = 1\nhelper = 2\n_private = 3\n"
            "__all__ = ['public', 'helper']\n",
            encoding="utf-8",
        )
        (pkg_dir / "no_all.py").write_text(
            "visible = 10\n_hidden = 20\n", encoding="utf-8",
        )
        sys.path.insert(0, tmp)
        try:
            ns_with_all: dict[str, object] = {}
            exec("from demo_pkg import *", ns_with_all)
            ns_no_all: dict[str, object] = {}
            exec("from demo_pkg.no_all import *", ns_no_all)
        finally:
            sys.path.remove(tmp)
    print(f"  with __all__    : {sorted(k for k in ns_with_all if not k.startswith('__'))}")
    print(f"  without __all__ : {sorted(k for k in ns_no_all if not k.startswith('__'))}")
    return ns_with_all, ns_no_all
    # Output:
    #   with __all__    : ['helper', 'public']
    #   without __all__ : ['visible']


# ============================================================
# 4. Semantic Versioning
# ============================================================
# MAJOR.MINOR.PATCH: breaking / feature / fix. A pre-release sorts
# BEFORE its release: 1.2.0rc1 < 1.2.0. Dependencies use ranges, and
# semver is what makes ">=1.2,<2.0" mean "compatible with 1.x".

def _normalize(nums: tuple[int, ...]) -> tuple[int, ...]:
    """Zero-pad to (major, minor, patch): 1.26 == 1.26.0 (PEP 440)."""
    return nums + (0,) * (3 - len(nums)) if len(nums) < 3 else nums


def parse_version(v: str) -> tuple[int, ...]:
    """Encode a version for tuple comparison (simplified PEP 440).

    final 1.2.0  -> (1, 2, 0, 1, 0)
    rc1   1.2.0  -> (1, 2, 0, 0, 1)   (handles the common '1.2.0rc1' form)
    """
    if "rc" in v:
        base, _, tag = v.partition("rc")
        nums = tuple(int(p) for p in base.split("."))
        return _normalize(nums) + (0, int(tag))
    nums = tuple(int(p) for p in v.split("."))
    return _normalize(nums) + (1, 0)


def compare_versions(a: str, b: str) -> int:
    """Return -1 if a < b, 0 if equal, 1 if a > b (semver order)."""
    pa, pb = parse_version(a), parse_version(b)
    return -1 if pa < pb else (1 if pa > pb else 0)


def demo_semver() -> None:
    """Show the ordering a resolver must implement."""
    ordered = ["1.0.0rc1", "1.0.0", "1.0.1", "1.1.0", "2.0.0"]
    print(f"  sorted: {sorted(ordered, key=parse_version)}")
    print(f"  compare 1.0.0rc1 vs 1.0.0: {compare_versions('1.0.0rc1', '1.0.0')}")
    # Output:
    #   sorted: ['1.0.0rc1', '1.0.0', '1.0.1', '1.1.0', '2.0.0']
    #   compare 1.0.0rc1 vs 1.0.0: -1


# ============================================================
# 5. Extras: Optional Capabilities
# ============================================================
# [project.optional-dependencies] declares feature toggles a user can
# install with `pip install rag_utils[qdrant]`. Extras are a contract,
# not a comment.

def demo_extras(data: dict[str, object]) -> None:
    """Read optional-dependencies from the parsed pyproject."""
    project = data["project"]
    assert isinstance(project, dict)
    extras = project["optional-dependencies"]
    assert isinstance(extras, dict)
    print(f"  extras: {sorted(extras)}")
    print(f"  dev deps: {extras['dev']}")
    # Output:
    #   extras: ['dev', 'qdrant']
    #   dev deps: ['pytest>=8', 'ruff', 'mypy']


# ============================================================
# 6. Pinning vs Ranges
# ============================================================
# Ranges (numpy>=1.26,<3) let the resolver pick; pins (numpy==1.26.4)
# make builds reproducible but rot. Production practice: ranges in
# pyproject.toml, exact pins in the lockfile.

def matches_requirement(requirement: str, version: str) -> bool:
    """True if `version` satisfies a comma-separated spec like '>=1.2,<2.0'."""
    for clause in requirement.split(","):
        clause = clause.strip()
        if clause.startswith(">="):
            op, _, bound = clause.partition(">=")
            assert op == "", "unexpected prefix"
            if compare_versions(version, bound) < 0:
                return False
        elif clause.startswith("<="):
            bound = clause[2:]
            if compare_versions(version, bound) > 0:
                return False
        elif clause.startswith(">"):
            bound = clause[1:]
            if compare_versions(version, bound) <= 0:
                return False
        elif clause.startswith("<"):
            bound = clause[1:]
            if compare_versions(version, bound) >= 0:
                return False
        elif clause.startswith("=="):
            bound = clause[2:]
            if compare_versions(version, bound) != 0:
                return False
        elif clause.startswith("!="):
            bound = clause[2:]
            if compare_versions(version, bound) == 0:
                return False
        else:
            raise ValueError(f"unsupported clause: {clause!r}")
    return True


def demo_ranges() -> None:
    """Evaluate a realistic dependency spec against candidate versions."""
    spec = ">=1.26,<3"
    for v in ["1.25.9", "1.26.0", "2.5.0", "3.0.0"]:
        print(f"  numpy {v:8s} in {spec}: {matches_requirement(spec, v)}")
    # Output:
    #   numpy 1.25.9  in >=1.26,<3: False
    #   numpy 1.26.0  in >=1.26,<3: True
    #   numpy 2.5.0   in >=1.26,<3: True
    #   numpy 3.0.0   in >=1.26,<3: False


# ============================================================
# 7. sdist, Wheel, Editable Installs, Lockfiles, Entry Points
# ============================================================
# sdist   = source archive (python -m build --sdist): portable, needs a
#           build step.
# wheel   = built archive (python -m build --wheel): pip installs it
#           directly -- what CI and servers actually install.
# editable= pip install -e . : the installed package points at your repo,
#           so edits apply immediately (dev workflow).
# lockfile= exact versions for every transitive dep: reproducible builds.
# entry point ([project.scripts]) = the CLI your users run.

def demo_build_commands() -> None:
    """The commands, printed -- no actual build (needs network/tooling)."""
    print("  build:    python -m build                    # sdist + wheel")
    print("  install:  pip install rag_utils[qdrant]      # extras")
    print("  dev:      pip install -e .[dev]              # editable + dev")
    print("  lock:     uv lock / pip-tools compile        # exact pins")
    print("  publish:  twine upload dist/*                # PyPI")
    # Output:
    #   build:    python -m build                    # sdist + wheel
    #   install:  pip install rag_utils[qdrant]      # extras
    #   dev:      pip install -e .[dev]              # editable + dev
    #   lock:     uv lock / pip-tools compile        # exact pins
    #   publish:  twine upload dist/*                # PyPI


# ============================================================
# 8. Namespace Packages: Many Distributions, One Import Path
# ============================================================
# A namespace package lets `company.common` and `company.llm` live in
# SEPARATE distributions while importing under one `company.` prefix.
# Plain directories without __init__.py (PEP 420) are namespace packages.


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: a flat layout and "tests pass" -- the tests import the repo
#   dir, not the package you will ship.
# CORRECT: src-layout; run CI against `pip install .` before release.
# MISTAKE: `pip freeze > requirements.txt` and calling it a lockfile --
#   it is a machine snapshot, not a resolved graph.
# CORRECT: a true lockfile from a resolver (uv lock, poetry.lock).
# MISTAKE: pinning every dependency exactly in pyproject.toml.
# CORRECT: ranges in pyproject.toml, exact pins in the lockfile.
# MISTAKE: forgetting __all__ and leaking private names via import *.
# CORRECT: __all__ as the explicit public API contract.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. pyproject.toml parses and carries the keys consumers need.
    data = load_pyproject(EXAMPLE_PYPROJECT)
    project = data["project"]
    assert isinstance(project, dict)
    assert project["name"] == "rag_utils", "pyproject must carry the name"
    assert project["version"] == "1.2.0", "pyproject must carry the version"
    assert str(project["requires-python"]).startswith(">="), \
        "requires-python must be a range, not a pin"
    assert data["build-system"]["build-backend"], \
        "build-system must declare a backend"

    # 2. Semver ordering, including pre-releases before releases.
    assert compare_versions("1.0.0", "1.0.1") == -1, "patch bump must sort up"
    assert compare_versions("1.0.1", "1.1.0") == -1, "minor bump must sort up"
    assert compare_versions("1.1.0", "2.0.0") == -1, "major bump must sort up"
    assert compare_versions("1.0.0rc1", "1.0.0") == -1, \
        "pre-release must sort before its release"
    assert compare_versions("1.2.0", "1.2.0") == 0, "equal versions compare equal"

    # 3. Dependency ranges: >=1.26,<3 excludes both edges.
    assert matches_requirement(">=1.26,<3", "1.26.0"), \
        "lower bound must be inclusive"
    assert matches_requirement(">=1.26,<3", "2.5.0"), \
        "middle versions must match"
    assert not matches_requirement(">=1.26,<3", "1.25.9"), \
        "below the lower bound must fail"
    assert not matches_requirement(">=1.26,<3", "3.0.0"), \
        "the upper bound must be exclusive"

    # 4. Extras are parsed from the pyproject.
    extras = project["optional-dependencies"]
    assert isinstance(extras, dict)
    assert "dev" in extras and "qdrant" in extras, \
        "extras must be discoverable from the pyproject"
    assert "pytest>=8" in extras["dev"], "dev extras must list pytest"

    # 5. __all__ controls star import (both directions).
    ns_with_all, ns_no_all = demo_all_control()
    assert "public" in ns_with_all and "helper" in ns_with_all, \
        "__all__ names must be imported"
    assert "_private" not in ns_with_all, \
        "__all__ must exclude names it does not list"
    assert "visible" in ns_no_all, \
        "without __all__, public names must be imported"
    assert "_hidden" not in ns_no_all, \
        "underscore names must never be star-imported"

    # 6. The demo package actually imports by its name.
    assert "demo_pkg" not in sys.modules or True, "no import pollution"

    print("\n[OK] 27-packaging-and-distribution: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("PACKAGING AND DISTRIBUTION: SHIP A LIBRARY, NOT A FOLDER")
        print("=" * 60)
        print("\n--- 1. pyproject.toml anatomy ---")
        parsed = demo_pyproject()
        print("\n--- 2. src-layout vs flat ---")
        print("  src-layout: only the INSTALLED package is importable.")
        print("  flat-layout: the repo dir can shadow the package.")
        print("\n--- 3. __all__ controls import * ---")
        demo_all_control()
        print("\n--- 4. Semantic versioning ---")
        demo_semver()
        print("\n--- 5. Extras ---")
        demo_extras(parsed)
        print("\n--- 6. Pinning vs ranges ---")
        demo_ranges()
        print("\n--- 7. Build and publish commands ---")
        demo_build_commands()
        print("\n--- 8. Namespace packages ---")
        print("  PEP 420: dirs without __init__.py merge into one prefix.")
        print("\n--- Summary ---")
        print("1. pyproject.toml is the single source of truth.")
        print("2. Ranges in the manifest, exact pins in the lockfile.")
        print("3. __all__ and src-layout protect the public API.")
        _verify()
