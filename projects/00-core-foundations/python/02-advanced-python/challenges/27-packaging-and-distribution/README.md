# Challenge 27: Packaging and Distribution

Parse versions like PEP 440, evaluate requirement specifiers, and
resolve the newest compatible version — the resolver, miniaturized.

## 🥉 Bronze — PEP 440 Parse (~15 min)

**Task:** Implement `parse_version(v)` returning a comparable tuple
`(major, minor, patch, rc)` — the first three from the dotted core
(zero-padded), the last the pre-release number (`"rc1"` → `1`; no
pre-release → a huge sentinel like `2**63` so finals sort after
pre-releases).

**Signature:**
```python
def parse_version(v: str) -> tuple[int, int, int, int]:
```

| Input | Comparable result |
|---|---|
| `"1.2.0"` | `(1, 2, 0, BIG)` |
| `"1.2.0rc1"` | `(1, 2, 0, 1)` |
| `"1.26"` | `(1, 26, 0, BIG)` — zero-padded |
| `"2.0.0"` | `(2, 0, 0, BIG)` |

**Constraints:** `"1.2.0rc1".split(".")` produces `"0rc1"` — `int()`
raises `ValueError`. Partition the suffix **before** splitting
(`v.partition("rc")`). This tier is pure parsing; comparisons come
next.

---

## 🥈 Silver — Compare + Specifiers (~35 min)

**Task:** implement two functions:

1. `compare_versions(a, b) -> int` — `-1` / `0` / `1` using
   `parse_version`.
2. `matches_requirement(req, version) -> bool` — evaluates simple
   specifiers of the form `"op1ver1,op2ver2"` where each op is one of
   `>=`, `>`, `<=`, `<`, `==`. All clauses must hold.

**Signatures:**
```python
def compare_versions(a: str, b: str) -> int
def matches_requirement(req: str, version: str) -> bool
```

| Input | Expected |
|---|---|
| `compare_versions("1.2.0rc1", "1.2.0")` | `-1` |
| `compare_versions("1.10.0", "1.9.9")` | `1` (string compare says the opposite!) |
| `compare_versions("1.26", "1.26.0")` | `0` (PEP 440 zero-padding) |
| `matches_requirement(">=1.26,<3", "1.26.0")` | `True` |
| `matches_requirement(">=1.26,<3", "3.0.0")` | `False` |
| `matches_requirement("==2.0", "2.0.0")` | `True` |

**Constraints:** never compare version *strings* — `"1.10.0" < "1.9.9"`
lexicographically. Parse both sides, then compare tuples. Follow
pip's default: a pre-release version (`1.2.0rc1`) does **not** satisfy
a spec that never mentions a pre-release token (`rc`/`a`/`b`/`dev`/
`post`).

---

## 🥇 Gold — Resolver + Manifest Reader (~75 min)

**Task:** implement two functions.

1. `latest_compatible(available, spec)` — return the **newest version
   in `available` that satisfies `spec`** (via `compare_versions` and
   `matches_requirement`); `None` if none matches.
2. `pyproject_info(toml_text)` — parse TOML with `tomllib` and return
   `{name, version, requires_python, dependencies, extras, scripts}`
   (lists/dicts as declared; `requires_python` as the raw string).

**Signatures:**
```python
def latest_compatible(available: list[str], spec: str) -> str | None
def pyproject_info(toml_text: str) -> dict
```

| Input | Expected |
|---|---|
| `latest_compatible(["1.9.9", "1.10.0", "2.0.0rc1"], ">=1.9,<2")` | `"1.10.0"` |
| `latest_compatible(["1.0.0", "1.2.0rc1", "1.2.0"], ">=1.1")` | `"1.2.0"` (final beats its rc) |
| `latest_compatible(["1.0.0"], ">=2.0")` | `None` |
| `pyproject_info('<manifest with name/version/requires-python/dependencies/extras/scripts>')` | extracted dict |

**Constraints:** `max(available)` is a *string* max — it returns
`"1.9.9"` where the resolver must return `"1.10.0"`. The `rc` must
never win over its own final (`1.2.0rc1` < `1.2.0`).

---

## Running

```bash
pytest challenges/27-packaging-and-distribution/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/27-packaging-and-distribution/test_challenge.py -v
```

## Test File Structure

```
challenges/27-packaging-and-distribution/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
