# Advanced Python - 27: Packaging and Distribution

## Topic Overview

The whole curriculum so far has been one file at a time. This lecture is the moment the code becomes a **product**: a `pyproject.toml` that declares metadata, dependencies, and entry points; **semantic versioning** (1.2.0 → 1.3.0 → 2.0.0 — what each bump means to every consumer); **requirement specifiers** (`numpy>=1.26,<3` is a promise with boundaries); **extras** for optional feature sets (`rag_utils[dev]` vs `rag_utils[qdrant]`); and **entry points** that turn a package into a CLI (`rag-index`). The phase doc's canonical case is packaging a shared `rag_utils` library — the one thing every other component imports.

Two pieces of machinery matter more than the rest: **PEP 440 normalization** (why `1.26` and `1.26.0` are the same version, and how `parse_version` must normalize before comparing) and **lockfiles** (why `numpy>=1.26` in a manifest and `numpy==1.26.4` in a lockfile are two different promises). The exercise implements a semver comparator against PEP 440 rules — including the `rc` (pre-release) parsing trap — and parses real `requires-python` specifiers with `packaging`.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read and write a `pyproject.toml` for a library with dependencies
2. Explain semver: when to bump major, minor, patch — and pre-releases
3. Parse requirement specifiers and evaluate whether a version satisfies them
4. Design extras and entry points for a package
5. Normalize versions per PEP 440 before comparing
6. Explain the difference between a manifest and a lockfile

---

## Prerequisites

| Need | Where |
|---|---|
| Modules and imports | Phase 1 modules |
| Functions, CLI `if __name__ == "__main__"` | Phase 1 |
| `tomllib` (std lib, 3.11+) | Python docs |
| Dependency concepts | Phase 1 project work, pip usage |

---

## 1. pyproject.toml: The Package Manifest

`pyproject.toml` is the single source of truth: metadata, build system, dependencies, extras, entry points, and tool config all live here.

```toml
[project]
name = "rag_utils"
version = "1.2.0"
description = "Shared utilities for the RAG pipeline"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.26,<3",
    "pydantic>=2.5",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.8"]
qdrant = ["qdrant-client>=1.9"]

[project.scripts]
rag-index = "rag_utils.indexer:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

```
name=rag_utils version=1.2.0 requires-python=>=3.10 deps=2 extras=['dev', 'qdrant'] scripts=['rag-index']
```

The exercise parses exactly this file with `tomllib` and asserts every field: the version string, the dependency count, the extras, and the entry point. `requires-python = ">=3.10"` is a *contract* — the package promises to work on 3.10+ and the installer enforces it.

---

## 2. Semver: What a Bump Means

Semantic versioning is a promise in three numbers: `major.minor.patch`. Bump **patch** (1.2.0 → 1.2.1) for bug fixes only; **minor** (1.2.0 → 1.3.0) for backward-compatible features; **major** (1.2.0 → 2.0.0) for breaking changes. Pre-releases are `rc`/`a`/`b` suffixes: `1.3.0rc1` is *older* than `1.3.0`.

```python
def parse_version(v: str) -> tuple[int, int, int, int]:
    # "1.2.0rc1" -> split the rc suffix, then the dotted core
    core, _, rc = v.partition("rc")
    parts = [int(p) for p in core.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return (parts[0], parts[1], parts[2], int(rc) if rc else 2**63)
```

```
1.2.0rc1 < 1.2.0 -> True   (rc releases sort before their final)
2.0.0 > 1.9.9    -> True   (major bump dominates)
1.10.0 > 1.9.9   -> True   (numeric, not string, comparison)
```

The `rc` trap: `"1.2.0rc1".split(".")` gives `["1", "2", "0rc1"]` — `int("0rc1")` raises `ValueError`. The fix is partitioning on `"rc"` first (or splitting the suffix), exactly as the exercise does. And string comparison must never be used: `"1.10.0" < "1.9.9"` is `True` lexicographically but wrong numerically — versions are compared as tuples of ints.

---

## 3. Requirement Specifiers: Promises With Boundaries

`numpy>=1.26,<3` is a range: any version from 1.26 (inclusive) up to, but not including, 3.0. The `packaging` library evaluates these predicates correctly — including PEP 440 normalization like `1.26 == 1.26.0`.

```python
from packaging.specifiers import SpecifierSet
from packaging.version import Version

def matches_requirement(req: str, version: str) -> bool:
    return Version(version) in SpecifierSet(req)
```

```
numpy>=1.26,<3  vs 1.26.0    -> True   (PEP 440 normalizes 1.26 == 1.26.0)
numpy>=1.26,<3  vs 3.0.0     -> False  (exclusive upper bound)
python>=3.10    vs 3.11.9    -> True
```

The exercise implements its own `_normalize` (zero-padding) so its hand-rolled comparator agrees with `packaging` on the `1.26 == 1.26.0` case — then uses `packaging` itself for the specifier checks. Two layers: understand the rules (implement them), then trust the standard library for production (use `packaging`).

---

## 4. Extras and Entry Points

**Extras** make optional feature sets opt-in: `pip install rag_utils[qdrant]` brings the Qdrant client; `rag_utils[dev]` brings test tooling. Nobody installs everything. **Entry points** (`[project.scripts]`) turn a module function into a console command: installing the package creates `rag-index` on the PATH that calls `rag_utils.indexer:main`.

```python
def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else [])
    if "--version" in args:
        print("rag_utils 1.2.0")
        return 0
    print("indexing", len(args), "sources")
    return 0
```

```
$ rag-index --version
rag_utils 1.2.0
$ rag-index docs/ chunker.json
indexing 2 sources
```

The exercise asserts the entry point *declaration* (the `rag-index` script mapping in the manifest) and the function's behavior — you cannot run `pip install .` in the sandbox, but the declaration and the callable are both verifiable. The console-script mechanism is the standard way Python projects ship CLIs: a tiny wrapper function, zero shell scripts.

---

## 5. PEP 440 Normalization

PEP 440 says `1.26` and `1.26.0` are the *same* version: trailing zero segments are padding. The hand-rolled comparator must normalize both sides before comparing.

```python
def _normalize(v: str) -> tuple[int, ...]:
    parts = [int(p) for p in v.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)
```

```
_normalize("1.26")   == (1, 26, 0)
_normalize("1.26.0") == (1, 26, 0)
(1, 26, 0) == (1, 26, 0) -> True
```

This is the exercise's `compare_versions("1.26", "1.26.0") == 0` assertion: without normalization, `"1.26"` and `"1.26.0"` would compare unequal, and every requirement check that depends on equality would be wrong. `packaging.version.Version` does this for real; the hand-rolled version exists so the *rule* is understood, not just imported.

---

## 6. Manifest vs Lockfile

The manifest says what you *allow*; the lockfile says what you *got*. `numpy>=1.26,<3` in `pyproject.toml` is a range; `numpy==1.26.4` in a lockfile pins one exact version. The difference is reproducibility: CI, prod, and every teammate install exactly the same environment from the lockfile, while the manifest keeps the range open for updates you choose to accept.

```
pyproject.toml:  numpy>=1.26,<3   (a promise about the future)
lockfile:        numpy==1.26.4    (a record of the present)
```

The distinction is why `uv lock`/`pip freeze` exist, and why "it works on my machine" stories usually end with "my lockfile was different." For AI services, where a NumPy or tokenizer patch can change outputs, reproducibility is correctness.

---

## Common Mistakes to Avoid

### Mistake 1: String version comparison
```
# WRONG -- lexicographic order: "1.10.0" < "1.9.9" is True
assert "1.10.0" > "1.9.9"
# CORRECT -- parse to int tuples first
assert parse_version("1.10.0") > parse_version("1.9.9")
```

### Mistake 2: Splitting pre-release suffixes naively
```
# WRONG -- int("0rc1") raises ValueError
parts = [int(p) for p in "1.2.0rc1".split(".")]
# CORRECT -- partition off the suffix first
core, _, rc = "1.2.0rc1".partition("rc")
```

### Mistake 3: Forgetting PEP 440 zero-padding
```
# WRONG -- 1.26 and 1.26.0 compare unequal
assert compare("1.26", "1.26.0") == 0   # fails without normalization
# CORRECT -- normalize both sides to (1, 26, 0) before comparing
```

### Mistake 4: Open-ended dependencies
```
# WRONG -- any future 4.0 silently breaks the build
"numpy>=1.26"
# CORRECT -- bound the future you can absorb
"numpy>=1.26,<3"
```

### Mistake 5: No lockfile, or a lockfile nobody uses
```
# WRONG -- manifest-only: every install resolves independently
# CORRECT -- pin resolved versions in a lockfile; CI installs from it
```

---

## Best Practices

1. **Semver by contract**: patch = fixes, minor = features, major = breaking; pre-releases sort before finals.
2. **Compare versions as int tuples**, never as strings.
3. **Normalize per PEP 440** before any equality check.
4. **Bound dependency ranges** (`>=1.26,<3`), don't leave them open-ended.
5. **Put optional features in extras** so installs stay lean.
6. **Ship CLIs via `[project.scripts]`**, not shell wrappers.
7. **Use `packaging` in production**; hand-roll only to learn the rules.
8. **Lock resolved versions** and install from the lockfile everywhere.

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Parse a version | O(len) | O(1) | string compare — wrong results |
| Normalize + compare | O(len) | O(1) | none — it is the correct minimal check |
| Specifier membership | O(specifiers) | O(1) | regex over versions — fragile |
| `tomllib` parse | O(file) | O(file) | yaml — extra dependency |
| Entry-point dispatch | O(1) after import | O(1) | shell script — platform-specific |

Version comparison is microseconds either way — the cost of getting it wrong is silent dependency breakage, not runtime. The cheap-but-wrong alternatives are listed first; use them never.

---

## AI Engineering Relevance

**Where this shows up:** the canonical case is the shared `rag_utils` library: every component (indexer, embedder, retriever, evaluator) imports it, so its versioning *is* the contract between teams. The semver rules decide when a change to the chunking API requires a major bump and a coordinated migration. The extras design decides whether the vector-store client is installed everywhere or only where Qdrant lives. The lockfile decides whether two services running "the same code" actually run the same NumPy — which for embedding math is a reproducibility question, not a taste question.

| Concept here | Used for |
|---|---|
| `pyproject.toml` | the single source of truth for a shared library |
| Semver | the API contract between library and consumers |
| Requirement specifiers | dependency boundaries (`numpy>=1.26,<3`) |
| Extras | optional vendor clients (`rag_utils[qdrant]`) |
| Entry points | `rag-index` CLI from a plain function |
| PEP 440 | `1.26 == 1.26.0` — normalization before comparison |
| Lockfiles | byte-identical environments across CI/prod |

**Scale note:** at one service, a version bug is a one-file fix. At N services importing one library, a bad major bump is a coordinated migration with an owner, a timeline, and a rollback plan. The semver discipline is the cheapest insurance the ecosystem offers: the rules cost nothing and the violations cost everything.

---

## Practice Exercises

### Exercise 1: Parse the Manifest (Difficulty: Easy)
Write a `rag_utils` `pyproject.toml` (as in section 1), parse it with `tomllib`, and assert name, version, `requires-python`, dependency count, extras, and the `rag-index` script.

### Exercise 2: Semver Comparator (Difficulty: Medium)
Implement `compare_versions(a, b) -> int` returning -1/0/1. Assert `1.2.0rc1 < 1.2.0`, `2.0.0 > 1.9.9`, and `1.10.0 > 1.9.9`.

### Exercise 3: PEP 440 Normalization (Difficulty: Medium)
Implement `_normalize` with zero-padding. Assert `compare_versions("1.26", "1.26.0") == 0` and that `parse_version` handles `rc` suffixes without `ValueError`.

### Exercise 4: Specifier Checks (Difficulty: Medium)
With `packaging`, assert `matches_requirement("numpy>=1.26,<3", "1.26.0")`, `matches_requirement("numpy>=1.26,<3", "3.0.0") == False`, and `matches_requirement("python>=3.10", "3.11.9")`.

### Exercise 5: CLI Entry Point (Difficulty: Hard)
Write `main()` for `rag-index` handling `--version` and source args; assert exit codes and output for both invocations. Document how `[project.scripts]` maps the name to the function.

### Exercise 6: Extras Design (Difficulty: Hard)
Add a third extra (e.g. `eval = ["scikit-learn>=1.4"]`) to the manifest and parse it. Write a short argument for why qdrant stays an extra rather than a base dependency, referencing install size and vendor coupling.

---

## Summary

| Concept | Description |
|---|---|
| `pyproject.toml` | manifest: metadata, deps, extras, scripts, build backend |
| Semver | patch/minor/major + pre-releases sort before finals |
| Specifiers | `>=1.26,<3` — bounded promises |
| Extras | optional feature sets (`[dev]`, `[qdrant]`) |
| Entry points | `rag-index` CLI from `rag_utils.indexer:main` |
| PEP 440 | normalization: `1.26 == 1.26.0` |
| Lockfiles | pinned resolved versions; the manifest is the range |

Packaging is the boundary between "code that runs on my machine" and "a product other services can depend on." The manifest declares the contract; semver versions it; specifiers bound it; extras scope it; entry points expose it; the lockfile freezes it. Every rule in this lecture exists because someone's deployment broke without it.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Declare a package | `[project]` in `pyproject.toml` + `[build-system]` |
| Version a change | patch = fix, minor = feature, major = breaking |
| Bound a dependency | `"numpy>=1.26,<3"` |
| Optional features | `[project.optional-dependencies]` extras |
| Ship a CLI | `[project.scripts]` → `pkg.module:main` |
| Compare versions | int tuples + PEP 440 normalization, never strings |
| Check specifiers | `packaging.specifiers.SpecifierSet` |
| Reproduce environments | lockfile (`uv lock` / `pip freeze`), install from it |

---

## Next Steps

Next: **[28-venvs-and-dependency-management-lecture.md](28-venvs-and-dependency-management-lecture.md)** (Phase 2 topic 28) — environments, resolvers, and the practical workflow around the lockfile.
Completes the Phase 2 package: **[29-project-rag-pipeline](../../../02-advanced-python/29-project-rag-pipeline.py)** — build a real, installable RAG service using everything from 21–27.
Official docs: [pyproject.toml](https://packaging.python.org/en/latest/specifications/pyproject-toml/), [PEP 440](https://peps.python.org/pep-0440/), [packaging](https://packaging.pypa.io/en/stable/), [PEP 621](https://peps.python.org/pep-0621/).
