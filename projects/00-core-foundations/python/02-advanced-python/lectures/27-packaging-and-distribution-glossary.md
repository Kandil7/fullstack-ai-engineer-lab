# Packaging and Distribution — Glossary 27

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| build backend | Component | The tool that turns source into artifacts (setuptools, hatchling) |
| console script | Feature | A CLI command installed from a `[project.scripts]` entry point |
| dependency resolution | Process | Choosing versions satisfying all requirement specifiers |
| distribution | Concept | A package as a shippable, installable product |
| extras | Feature | Optional dependency sets: `rag_utils[dev]`, `rag_utils[qdrant]` |
| lockfile | File | Pins exact resolved versions for reproducible installs |
| metadata | Data | The manifest's name, version, description, requires |
| PEP 440 | Standard | Version scheme: normalization, ordering, pre-releases |
| pre-release | Version | `1.3.0rc1` — sorts before its final `1.3.0` |
| pyproject.toml | File | The single source of truth for a Python package |
| requires-python | Metadata | Declares the supported interpreter range (`>=3.10`) |
| requirement specifier | Syntax | A bounded version promise: `numpy>=1.26,<3` |
| semantic versioning | Scheme | major.minor.patch with contractual bump meanings |
| tomllib | Module | Standard-library TOML parser (3.11+), reads pyproject.toml |
| wheel | Artifact | A pre-built, pip-installable package format (`.whl`) |

## Detailed Definitions

### build backend
**Definition**: The tool that consumes `pyproject.toml` and produces distributable artifacts. `setuptools.build_meta` (the default) compiles wheels and sdists; hatchling and flit are lighter alternatives. Declared in `[build-system]`.
**Example**:
```python
import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

print(data["build-system"]["build-backend"])
```
```text
setuptools.build_meta
```
**Related**: pyproject.toml, wheel

### console script
**Definition**: A command-line entry point created by `[project.scripts]`: `rag-index = "rag_utils.indexer:main"` makes `rag-index` call `main()` after install. The standard way Python projects ship CLIs — no shell wrappers, works on every OS.
**Example**:
```python
def main(argv: list[str] | None = None) -> str:
    args = list(argv if argv is not None else [])
    if "--version" in args:
        return "rag_utils 1.2.0"
    return f"indexing {len(args)} sources"

print(main(["--version"]))
print(main(["docs/"]))
```
```text
rag_utils 1.2.0
indexing 1 sources
```
**Related**: metadata, distribution

### dependency resolution
**Definition**: The installer's job of picking concrete versions that satisfy every package's specifiers simultaneously. Resolution fails on conflicts (`numpy<2` vs `numpy>=2`); lockfiles record a successful resolution so it never has to be redone.
**Example**:
```python
from packaging.specifiers import SpecifierSet
from packaging.version import Version

def matches(req: str, version: str) -> bool:
    return Version(version) in SpecifierSet(req)

print(matches("numpy>=1.26,<3", "1.26.4"), matches("numpy>=1.26,<3", "3.0.0"))
```
```text
True False
```
**Related**: requirement specifier, lockfile

### distribution
**Definition**: A package in shippable form — the line between "code on my machine" and "a product others can depend on". A distribution has metadata, a build backend, versioning, and optionally extras and entry points.
**Example**:
```python
dist = {"name": "rag_utils", "version": "1.2.0", "entry": "rag-index"}
print(dist["name"], dist["version"], dist["entry"])
```
```text
rag_utils 1.2.0 rag-index
```
**Related**: pyproject.toml, metadata, wheel

### extras
**Definition**: Optional dependency sets declared under `[project.optional-dependencies]`. Installing `rag_utils[qdrant]` adds the vector-store client only where needed; `rag_utils[dev]` adds test tooling. Keeps base installs lean and vendor coupling opt-in.
**Example**:
```python
import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

extras = data["project"]["optional-dependencies"]
print(sorted(extras), extras["dev"][0])
```
```text
['dev', 'qdrant'] pytest>=8.0
```
**Related**: requirement specifier, dependency resolution

### lockfile
**Definition**: A file recording the *exact* resolved versions — `numpy==1.26.4` — produced by `uv lock` / `pip freeze`. The manifest allows a range; the lockfile records the present. CI and prod install from the lockfile so every environment is byte-identical.
**Example**:
```python
manifest = "numpy>=1.26,<3"        # what we allow
lockfile = {"numpy": "1.26.4"}     # what we got

from packaging.specifiers import SpecifierSet
print(Version_ok := SpecifierSet(manifest).contains(lockfile["numpy"], prereleases=True))
```
```text
True
```
**Related**: dependency resolution, requirement specifier

### metadata
**Definition**: The machine-readable facts about a package: name, version, description, `requires-python`, dependencies. Declared in `[project]`; exposed by `importlib.metadata`; used by pip for resolution and display.
**Example**:
```python
import tomllib

with open("pyproject.toml", "rb") as f:
    proj = tomllib.load(f)["project"]

print(proj["name"], proj["version"], proj["requires-python"])
```
```text
rag_utils 1.2.0 >=3.10
```
**Related**: pyproject.toml, distribution

### PEP 440
**Definition**: The specification defining Python's version scheme: how versions normalize (`1.26 == 1.26.0`), how they order, and what suffixes mean (`rc1`, `a1`, `post1`). Every requirement check and comparison must follow it.
**Example**:
```python
def normalize(v: str) -> tuple[int, ...]:
    parts = [int(p) for p in v.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)

print(normalize("1.26") == normalize("1.26.0"))
```
```text
True
```
**Related**: semantic versioning, pre-release, requirement specifier

### pre-release
**Definition**: A version with a pre-release suffix — `1.3.0rc1`, `2.0.0a1`, `1.4.0b2` — which sorts **before** its final version (`1.3.0rc1 < 1.3.0`). Parsing requires splitting the suffix first: `"1.2.0rc1".split(".")` yields `int("0rc1")` — a `ValueError` trap.
**Example**:
```python
def parse(v: str) -> tuple[int, int, int, int]:
    core, _, rc = v.partition("rc")
    parts = [int(p) for p in core.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return (parts[0], parts[1], parts[2], int(rc) if rc else 2**63)

print(parse("1.2.0rc1") < parse("1.2.0"))
```
```text
True
```
**Related**: PEP 440, semantic versioning

### pyproject.toml
**Definition**: The single source of truth for a Python package (PEP 621): `[project]` holds metadata and dependencies, `[project.optional-dependencies]` holds extras, `[project.scripts]` holds entry points, `[build-system]` names the backend. Readable with `tomllib`.
**Example**:
```python
import tomllib, io

text = """
[project]
name = "rag_utils"
version = "1.2.0"
"""
data = tomllib.load(io.StringIO(text))
print(data["project"]["name"], data["project"]["version"])
```
```text
rag_utils 1.2.0
```
**Related**: metadata, build backend, extras

### requires-python
**Definition**: The manifest's declaration of supported interpreter versions (`requires-python = ">=3.10"`). Installers refuse incompatible interpreters; it is a contract between the package and the Python version — the phase's exercise asserts `>=3.10` parses and matches `3.11.9`.
**Example**:
```python
from packaging.specifiers import SpecifierSet

print(SpecifierSet(">=3.10").contains("3.11.9"))
```
```text
True
```
**Related**: requirement specifier, metadata

### requirement specifier
**Definition**: The syntax for version constraints — `numpy>=1.26,<3` means "at least 1.26, strictly below 3". Specifiers are ranges, not pins; combined with exact pins they form the manifest-plus-lockfile pairing. Evaluated correctly by `packaging.specifiers`.
**Example**:
```python
from packaging.specifiers import SpecifierSet

s = SpecifierSet(">=1.26,<3")
print(s.contains("1.26.0", prereleases=True), s.contains("3.0.0", prereleases=True))
```
```text
True False
```
**Related**: dependency resolution, lockfile, requires-python

### semantic versioning
**Definition**: The scheme `major.minor.patch`: bump patch for fixes, minor for backward-compatible features, major for breaking changes. Consumers read the bump to know whether upgrade is safe; pre-releases announce what is coming. Version numbers are promises.
**Example**:
```python
def bump(v: str, kind: str) -> str:
    major, minor, patch = (int(p) for p in v.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"

print(bump("1.2.0", "major"), bump("1.2.0", "minor"), bump("1.2.0", "patch"))
```
```text
2.0.0 1.3.0 1.2.1
```
**Related**: PEP 440, pre-release

### tomllib
**Definition**: The standard-library TOML parser (3.11+), used to read `pyproject.toml` without any dependency: `tomllib.load(open(path, "rb"))`. The exercise parses the package manifest with it and asserts every field.
**Example**:
```python
import tomllib, io

data = tomllib.load(io.StringIO("[project]\nname = 'rag_utils'\n"))
print(data["project"]["name"])
```
```text
rag_utils
```
**Related**: pyproject.toml, metadata

### wheel
**Definition**: The binary distribution format (`.whl`) — a pre-built zip that pip extracts and installs without running the build step. Wheels are what most users install; sdists (source archives) are the fallback when no wheel exists for the platform.
**Example**:
```python
wheel = "rag_utils-1.2.0-py3-none-any.whl"
parts = wheel.split("-")
print(parts[0], parts[1], parts[2])
```
```text
rag_utils 1.2.0 py3
```
**Related**: build backend, distribution

## Key Concepts Summary

### The Manifest Is a Contract
- `pyproject.toml` holds everything: metadata, deps, extras, scripts, backend.
- `requires-python` promises supported interpreters; specifiers bound versions.
- `tomllib` reads it with zero dependencies.

### Versions Are Promises
- Semver: patch = fixes, minor = features, major = breaking.
- PEP 440 normalizes (`1.26 == 1.26.0`) and orders pre-releases before finals.
- Compare as int tuples, never as strings; split suffixes before parsing.

### Reproducibility Is Correctness
- Manifest = what you allow; lockfile = what you got.
- Install from the lockfile everywhere: CI, prod, teammates.
- Extras keep installs lean; console scripts ship CLIs; wheels ship fast.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. PEP 440 — ___
2. semantic versioning — ___
3. extras — ___
4. lockfile — ___
5. console script — ___
6. pyproject.toml — ___
7. pre-release — ___
8. requirement specifier — ___
9. requires-python — ___
10. wheel — ___

A. Normalization + ordering rules for versions
B. major.minor.patch with contractual bumps
C. Optional dependency sets
D. Exact pinned versions for reproducible installs
E. CLI command from [project.scripts]
F. The single source of truth for a package
G. 1.3.0rc1 sorts before 1.3.0
H. Bounded version promise: numpy>=1.26,<3
I. Declares the supported interpreter range
J. Pre-built installable artifact

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
