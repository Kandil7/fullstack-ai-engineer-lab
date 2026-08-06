# Packaging and Distribution Quiz

## Topic Overview
This quiz covers `pyproject.toml`, semantic versioning and PEP 440
normalization, pre-releases, requirement specifiers, extras, entry
points, and the manifest-vs-lockfile distinction.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**Which file is the single source of truth for a Python package?**

A) `setup.py`
B) `pyproject.toml`
C) `requirements.txt`
D) `Pipfile`

**Difficulty:** Easy

---

### Question 2
**A bug fix that changes no public behavior bumps which number?**

A) Major
B) Minor
C) Patch
D) Build

**Difficulty:** Easy

---

### Question 3
**What does `requires-python = ">=3.10"` promise?**

A) The package installs only with Python 3.10
B) The package supports Python 3.10 and later
C) The package requires Python 10.3
D) The package works on any Python

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
from packaging.specifiers import SpecifierSet

s = SpecifierSet(">=1.26,<3")
print(s.contains("1.26.0", prereleases=True), s.contains("3.0.0", prereleases=True))
```

A) `True False`
B) `True True`
C) `False False`
D) `False True`

**Difficulty:** Easy

---

### Question 5
**Where do optional dependency sets like `rag_utils[qdrant]` live in the manifest?**

A) `[project.dependencies]`
B) `[project.optional-dependencies]`
C) `[build-system]`
D) `[tool.pytest]`

**Difficulty:** Easy

---

### Question 6
**What does `rag-index = "rag_utils.indexer:main"` under `[project.scripts]` create?**

A) A Python function named `rag-index`
B) A console command that calls `main()` after install
C) A system service
D) A pytest fixture

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
def parse(v):
    core, _, rc = v.partition("rc")
    parts = [int(p) for p in core.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts + ([int(rc)] if rc else [2**63]))

print(parse("1.2.0rc1") < parse("1.2.0"))
```

A) `True` — pre-releases sort before their final
B) `False` — rc sorts after the final
C) `True` — 1 is smaller than 2
D) `ValueError`

**Difficulty:** Medium

---

### Question 8
**Why is `"1.10.0" > "1.9.9"` wrong as a string comparison?**

A) Strings cannot be compared
B) Lexicographic order makes `"1.10.0" < "1.9.9"` — compare int tuples
C) Python raises TypeError for version strings
D) It is correct — versions compare fine as strings

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
def normalize(v):
    parts = [int(p) for p in v.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)

print(normalize("1.26") == normalize("1.26.0"))
```

A) `True` — PEP 440 zero-padding
B) `False` — 26 != 26.0
C) `True` — 1.26 is 1.260
D) `ValueError`

**Difficulty:** Medium

---

### Question 10
**What happens when `int()` is called on the parts of `"1.2.0rc1".split(".")`?**

A) `(1, 2, 0, 1)` — works fine
B) `ValueError` — `"0rc1"` is not an int
C) `(1, 2)` — rc is dropped
D) `(1, 2, 0)` — rc is ignored silently

**Difficulty:** Medium

---

### Question 11
**A lockfile pins `numpy==1.26.4` while the manifest says `numpy>=1.26,<3`. Which is true?**

A) They contradict; the manifest wins
B) The lockfile records the resolved present; the manifest allows the range
C) The lockfile replaces the manifest
D) The manifest pins; the lockfile allows

**Difficulty:** Medium

---

### Question 12
**What is the output of this code?**
```python
import tomllib, io

text = """
[project]
name = "rag_utils"
version = "1.2.0"
"""
data = tomllib.load(io.StringIO(text))
print(data["project"]["version"])
```

A) `1.2.0`
B) `rag_utils`
C) `project`
D) `TypeError: StringIO not supported`

**Difficulty:** Medium

---

### Question 13
**Which specifier correctly bounds a dependency against a future major?**

A) `"numpy>=1.26"`
B) `"numpy>=1.26,<3"`
C) `"numpy==*"`
D) `"numpy>=1.26,<=3"`

**Difficulty:** Medium

---

### Question 14
**What is the output of this code?**
```python
def compare(a, b):
    pa = [int(p) for p in a.split(".")]
    pb = [int(p) for p in b.split(".")]
    while len(pa) < 3:
        pa.append(0)
    while len(pb) < 3:
        pb.append(0)
    return -1 if pa < pb else (1 if pa > pb else 0)

print(compare("1.26", "1.26.0"))
```

A) `0` — normalized equal
B) `-1` — 1.26 is smaller
C) `1` — 1.26 is bigger
D) `ValueError`

**Difficulty:** Medium

---

### Question 15
**A breaking API change ships as 2.0.0. Consumers upgrading from 1.x should expect:**

A) Nothing to change
B) Possible breaking changes requiring migration
C) Automatic data migration
D) The package to refuse installation

**Difficulty:** Medium

---

### Question 16
**What is the output of this code?**
```python
versions = ["1.9.9", "1.10.0", "2.0.0rc1"]
print(max(versions), max(int(p) for p in "1.10.0".split(".")))
```

A) `2.0.0rc1 10`
B) `1.9.9 10`
C) `1.10.0 1`
D) `2.0.0rc1 1`

**Difficulty:** Hard

---

### Question 17
**The resolver must pick the newest version satisfying `>=1.9,<2` from `["1.9.9", "1.10.0", "2.0.0rc1"]`. What should it return?**

A) `1.9.9` — string max
B) `1.10.0` — parsed max in range
C) `2.0.0rc1` — the string max
D) `None` — no version matches

**Difficulty:** Hard

---

### Question 18
**By pip's default, does `2.0.0rc1` satisfy the spec `<2`?**

A) Yes — rc1 < 2.0.0 numerically
B) No — pre-releases are excluded unless the spec mentions one
C) Yes — rc versions always match
D) Only if the resolver is run in debug mode

**Difficulty:** Hard

---

### Question 19
**Which is the reproducible-install workflow?**

A) `pip install .` from the manifest every time
B) Resolve once into a lockfile; install from the lockfile everywhere
C) Freeze after every install and commit nothing
D) Manually pin the newest version in the manifest

**Difficulty:** Hard

---

### Question 20
**What is the output of this code?**
```python
def latest(available, spec):
    best = None
    for v in available:
        ok = True
        for clause in spec.split(","):
            op, ver = clause[0], clause[1:].strip()
            a = int(v.split(".")[0])
            b = int(ver.split(".")[0])
            if op == "<" and not (a < b):
                ok = False
        if ok and (best is None or v > best):
            best = v
    return best

print(latest(["1.9.9", "1.10.0"], "<2"))
```

A) `1.10.0`
B) `1.9.9`
C) `2.0.0`
D) `None`

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! The packaging contract is yours.
- 14-17: Good! Review the PEP 440 questions.
- 10-13: Fair. Re-read the specifier and lockfile sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **B) `pyproject.toml`** — the PEP 621 single source of truth. A is
   legacy, C is a dependency list without metadata, D is another
   ecosystem.

2. **C) Patch** — semver: fixes bump patch. A is breaking, B is
   features, D is not part of semver.

3. **B) The package supports Python 3.10 and later** — the lower
   bound. A reads it as exact, C misreads the decimal, D ignores it.

4. **A) `True False`** — 1.26.0 is in the range (normalized),
   3.0.0 is excluded by the exclusive upper bound. B, C, D misjudge
   one or both bounds.

5. **B) `[project.optional-dependencies]`** — extras live there. A
   is the base requirements, C is the build system, D is tool config.

6. **B) A console command that calls `main()` after install** — the
   entry-point mechanism. A is false (names need no dashes in
   Python), C and D are false.

7. **A) `True` — pre-releases sort before their final** — the rc
   rule. B is the reverse, C misreads the tuple, D is false (the
   partition prevents it).

8. **B) Lexicographic order makes `"1.10.0" < "1.9.9"` — compare int
   tuples** — the classic trap. A and C are false, D is the bug.

9. **A) `True` — PEP 440 zero-padding** — 1.26 normalizes to
   (1, 26, 0). B is the unnormalized view, C is wrong math, D is
   false.

10. **B) `ValueError` — `"0rc1"` is not an int** — the split trap;
    partition the suffix first. A would be nice but is false, C and
    D ignore the error.

11. **B) The lockfile records the resolved present; the manifest
    allows the range** — the two promises. A misreads (no
    contradiction), C and D invert the roles.

12. **A) `1.2.0`** — `tomllib` parses the TOML; the version key
    reads cleanly. B is the name, C is the table, D is false
    (`loads`/`StringIO` are supported).

13. **B) `"numpy>=1.26,<3"`** — bounded above by the next major. A
    is open-ended, C is invalid syntax, D would allow 3.0.0.

14. **A) `0` — normalized equal** — zero-padding makes them equal. B
    and C are unnormalized, D is false.

15. **B) Possible breaking changes requiring migration** — the major
    bump contract. A is false, C is false (no auto-migration), D is
    false (2.0 installs).

16. **A) `2.0.0rc1 10`** — string max is wrong (rc wins), but the
    int max of the dotted parts is 10. B shows the string trap
    result, C and D misread the second expression.

17. **B) `1.10.0` — parsed max in range** — the resolver's answer. A
    is the string max, C is out of range, D ignores 1.x matches.

18. **B) No — pre-releases are excluded unless the spec mentions
    one** — pip's default. A is the naive numeric view, C and D are
    false.

19. **B) Resolve once into a lockfile; install from the lockfile
    everywhere** — reproducibility is correctness. A re-resolves
    every time, C loses the record, D defeats ranges.

20. **A) `1.10.0`** — with only major-digit comparison, both satisfy
    `<2`, and the string max picks 1.10.0 — accidentally right here,
    but the comparison is still broken (it would pick `2.0.0rc1`
    wrong in other cases). B is the min, C is not available, D is
    false.
