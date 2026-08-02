# Content Standards — Canonical Templates

> Every file created or retrofitted under this plan conforms to the templates here.
> This document is the single source of truth for structure; the phase documents
> (02–08) supply only the *topic content* to pour into these shapes.

---

## 0. Why Standardize

The audit found three competing lecture templates and three competing glossary
templates in `01-core-python/lectures/` alone (Gap E in the master plan). The
content is good; the inconsistency is what makes the module hard to navigate and
impossible to generate against. One template, enforced.

---

## 1. Naming and Layout

```text
<section>/
├── NN-topic-slug.py                 # exercise, kebab-case, zero-padded
├── lectures/
│   ├── NN-topic-slug-lecture.md
│   ├── NN-topic-slug-glossary.md
│   └── README.md                    # section index
├── challenges/
│   └── NN-topic-slug/
│       ├── README.md                # the 3 challenge briefs
│       ├── starter.py               # stubs the learner fills
│       ├── solution.py              # reference implementation
│       └── test_challenge.py        # hidden tests, pytest
└── README.md                        # section overview
```

**Rules**
- Prefix is zero-padded two digits, unique within its directory. *(The pandas
  double-series violation is Tier 0 work.)*
- Slug in the `.py`, the lecture, the glossary, and the challenge dir must match
  exactly. A mismatch is what left 21 pandas files orphaned from lectures.
- One topic per prefix. Never two files sharing a number.

---

## 2. Exercise File Template (`NN-topic.py`)

The existing voice is preserved — `# Example N:` headers, `# =====` rules, inline
expected output. The **only** additions are the type-hinted signatures, the
complexity annotations, and the mandatory `_verify()` block.

```python
"""
<Section> — NN: <Topic Title>
==============================================
Topics: <comma-separated subtopics>

Why this matters for AI/backend engineering:
    <2-3 lines: the concrete production or ML scenario where this decides
     correctness, cost, or latency.>

Run:      python NN-topic.py
Verify:   python NN-topic.py --verify
Reference: <official docs URL — docs.python.org preferred over w3schools>
"""

from __future__ import annotations

import sys

# ============================================================
# 1. <First Concept>
# ============================================================
# <2-4 comment lines of explanation before any code.>
# Complexity: O(1) amortized / O(n) space   <- when a data structure is involved

# Example 1: <what this demonstrates>
fruits = ["apple", "banana", "cherry"]
print(f"Fruits: {fruits}")

# Output:
# Fruits: ['apple', 'banana', 'cherry']


# ============================================================
# 2. <Second Concept>
# ============================================================
# ...


# ============================================================
# N. Production Pattern
# ============================================================
# The idiomatic form a senior engineer would actually ship, with the
# reasoning made explicit.

def parse_config(raw: str) -> dict[str, str]:
    """Parse KEY=VALUE lines, ignoring blanks and comments.

    Chosen over a regex because the grammar is fixed and str.partition
    is ~4x faster here and far easier to read.
    """
    config: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if sep:
            config[key.strip()] = value.strip()
    return config


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: <the wrong version>
#   bad = [x for x in items if items.count(x) > 1]   # O(n^2)
# CORRECT:
#   from collections import Counter
#   counts = Counter(items)                          # O(n)
#   good = [x for x, n in counts.items() if n > 1]


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Each assert carries a message naming the concept under test.
    assert parse_config("A=1\n# note\n\nB=2") == {"A": "1", "B": "2"}, \
        "parse_config must skip blanks and comments"

    from collections import Counter
    assert [x for x, n in Counter([1, 1, 2]).items() if n > 1] == [1], \
        "Counter-based dedup must find repeated elements"

    print("[OK] NN-topic: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. <takeaway>")
        print("2. <takeaway>")
        _verify()          # always runs, so plain execution is also a test
```

### Hard requirements

| # | Rule | Rationale |
|---|---|---|
| E1 | Ends with `_verify()` containing ≥5 `assert`s, each with a message | Gap A: 0 of 277 files self-verify today |
| E2 | `_verify()` runs on plain `python file.py` too | Makes every run a test |
| E3 | Any data structure or algorithm carries a complexity annotation | Gap B |
| E4 | Module docstring has "Why this matters for AI/backend engineering" | Gap D / P3 |
| E5 | Reference URL prefers `docs.python.org` over `w3schools.com` | Raise the ceiling past tutorial level |
| E6 | Type hints on every `def` | Module targets 3.10+; hints are baseline |
| E7 | No `input()` at import scope | Made 146 practice calls un-gradeable |
| E8 | Deterministic: seed RNG, `MPLBACKEND=Agg`, no network, no wall-clock asserts | CI must be reproducible |
| E9 | Writes only under `output/` or `tempfile`, and cleans up | `19-logging.py` leaked a temp file and crashed on Windows |
| E10 | ASCII-only in `print()`; Unicode in comments/markdown only | 4 measured `UnicodeEncodeError` failures on Windows cp1252 |

> **E10 is not cosmetic.** Four files fail today purely from emoji/π in `print()`
> on a Windows console. Use `[OK]`, `->`, `pi` in program output.

---

## 3. Lecture Template (`NN-topic-lecture.md`)

Twelve sections, in this order, with these exact headings. Sections 10 and 11 are
**new** to this plan and are what convert a tutorial into senior training.

```markdown
# <Section> — NN: <Topic Title>

## Topic Overview
<2-4 paragraphs. What it is, why it exists, where it fits.>

## Learning Objectives
By the end of this lecture, you will be able to:
1. <verb-first, testable>
...  (6-10 items)

## Prerequisites
| Need | Where |
|---|---|
| <concept> | `NN-other-lecture.md` (relative link to the prerequisite) |

## 1..N. <Key Concepts>
<Numbered `##` sections. Each: prose, then a runnable block, then expected
output as a comment. Never a code block without its output.>

## Common Mistakes to Avoid
### Mistake 1: <name>
```
# WRONG — <why>
# CORRECT — <why>
```python
<3-6 mistakes, each with the failure mode named.>

## Best Practices
1..10 <numbered, imperative>

## Complexity and Cost                      <!-- NEW -->
| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `list.insert(0, x)` | O(n) | O(1) | `deque.appendleft` — O(1) |
<Mandatory whenever a data structure, algorithm, or I/O pattern appears.>

## AI Engineering Relevance                 <!-- NEW -->
**Where this shows up:** <concrete system: a RAG pipeline, a training loop,
an inference endpoint.>

| Concept here | Used for |
|---|---|
| `bisect.insort` | maintaining a top-k reranked candidate list |

**Scale note:** <what changes at 1M rows / 200 concurrent requests / 10GB.>

## Practice Exercises
### Exercise 1: <name>  (Difficulty: Easy)
<Statement, signature, expected I/O. No solution — solutions live in
challenges/.>
<4-6 exercises, Easy → Hard.>

## Summary
| Concept | Description |
|---|---|
<table, then 3-5 sentence close.>

## Quick Reference
| Task | Idiom |
|---|---|

## Next Steps
Next: **[NN+1 topic](NN+1-topic-lecture.md)**.
Continues in: **[Phase N — topic](../../<path>-lecture.md)**   <!-- cross-phase -->
Official docs: <links>
```

### Hard requirements

| # | Rule |
|---|---|
| L1 | All 12 headings present, exact spelling, exact order |
| L2 | `## Complexity and Cost` mandatory for any structure/algorithm/I-O topic |
| L3 | `## AI Engineering Relevance` mandatory — no exceptions |
| L4 | `## Next Steps` must cross-link forward, including across phases (Gap E: 0/41 do this today) |
| L5 | Every code block shows expected output |
| L6 | 350–700 lines. Under 350 is thin; over 700 should split |
| L7 | Exercises state difficulty; solutions live only in `challenges/` |

---

## 4. Glossary Template (`NN-topic-glossary.md`)

One scheme, replacing the three now in use.

```markdown
# <Topic> — Glossary NN

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Closure | Function | A function retaining its enclosing scope |
<15-30 rows, alphabetical.>

## Detailed Definitions
### <Term>            <!-- alphabetical, ### level, no A/B/C letter grouping -->
**Definition**: <1-3 sentences.>
**Example**:
```
<runnable snippet with output>

```text
**Complexity**: <when applicable>
**Related**: <Term>, <Term>

## Key Concepts Summary
### <Grouping>
- <bullet>

## Practice Terms
Match each term to its definition (answers at the bottom).
1. <term> — ___
**Answers:** 1-<letter>, ...
```

### Hard requirements

| # | Rule |
|---|---|
| G1 | Exactly these four `##` sections, these names |
| G2 | `### Term` — flat and alphabetical. No `### A` / `#### Term` nesting |
| G3 | ≥15 terms; every term has a runnable example |
| G4 | 250–500 lines (5 existing glossaries are under 210 and need expansion) |
| G5 | `**Related**` on every term, forming a navigable web |

---

## 5. Code Challenge Template (`challenges/NN-topic/`)

The missing rung between reading a lecture and building a project.

**`README.md`**
```markdown
# Challenge NN: <Topic>

## 🥉 Bronze — <name>   (~15 min)
**Task:** <one paragraph.>
**Signature:** `def solve(data: list[int]) -> int:`
| Input | Expected |
|---|---|
| `[1,2,3]` | `6` |
**Constraints:** n ≤ 10^3. Any correct approach passes.

## 🥈 Silver — <name>   (~35 min)
<As above, plus:>
**Constraints:** n ≤ 10^6 — an O(n²) solution will time out.

## 🥇 Gold — <name>   (~75 min)
<As above, plus:>
**Constraints:** stream of 10^7, memory ≤ 50 MB. Must be single-pass.
**Follow-up:** what breaks first at 10^9?

## Running
```
pytest challenges/NN-topic/test_challenge.py -v

```text
```

**`starter.py`** — signatures + docstrings, bodies `raise NotImplementedError`.
**`solution.py`** — reference implementation, with a comment on *why* this approach.
**`test_challenge.py`** — pytest, importing `starter`; includes correctness,
edge cases (empty, single, duplicates, negatives), and a performance guard for
Silver/Gold.

### Hard requirements

| # | Rule |
|---|---|
| C1 | Three tiers, always: bronze/silver/gold |
| C2 | Silver and Gold constrained so the naive solution *fails*, forcing the right structure |
| C3 | Tests cover empty / single / duplicate / boundary |
| C4 | Gold has a performance or memory assertion |
| C5 | `starter.py` never contains a working body |

---

## 6. Quiz Template

Matches the existing good format in `supplementary/quizzes/` (which already has
difficulty tags and explained answer keys — keep it).

```markdown
# <Topic> Quiz

## Topic Overview
## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

## Questions
### Question 1
**<stem>**

A) ...
B) ...
C) ...
D) ...

**Difficulty:** Easy | Medium | Hard

## Score Tracking
Count your correct answers: _____ / 20
**Scoring Guide:** ...

## Answer Key
1. **B) <answer>** — <explanation of why right AND why the distractors are wrong.>
```

**Rules:** 20 questions; mix ≈6 Easy / 9 Medium / 5 Hard; ≥8 questions must be
"what does this code output?" using a real snippet; every answer explains the
distractors, not just the key.

---

## 7. Determinism and CI Contract

Every exercise must satisfy this, or CI cannot gate the module.

```python
import os, random
import numpy as np

random.seed(42)
np.random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window
```

| Constraint | Why |
|---|---|
| No network calls | Offline CI; mock or embed fixtures |
| No `input()` at import scope | Blocks the runner (E7) |
| Timing printed but never asserted | Wall-clock is not reproducible |
| Files only under `output/` or `tempfile`, closed before delete | Windows `PermissionError`, measured in `19-logging.py` |
| Multiprocessing workers at module top level | `AttributeError: Can't get local object`, measured in `17-multiprocessing.py` |
| ASCII-only in stdout | 4 measured `UnicodeEncodeError` on cp1252 |

**Gate command:**
```bash
python run_smoke_tests.py --all --verify
pytest tests/ -q
```
Both must be green before any PR merges.

---

## 8. Style

Aligned to the existing `pyproject.toml` (`line-length = 100`, `target-version = py310`).

- `black` and `ruff` clean; `mypy` clean on new files
- `snake_case` functions, `PascalCase` classes, `UPPER_SNAKE` constants
- Type hints everywhere; prefer `list[int]` over `List[int]` (3.10+)
- Docstrings on every public function: one-line summary, then Args/Returns/Raises
- `print()` is allowed and expected in teaching files (`T201` already ignored)

---

## 9. Definition of Done

A topic ships only when **all seven** hold:

- [ ] `NN-topic.py` runs clean, `_verify()` passes, ≥5 asserts
- [ ] `NN-topic-lecture.md` — 12 sections, complexity + AI-relevance present
- [ ] `NN-topic-glossary.md` — 4 sections, ≥15 terms
- [ ] `challenges/NN-topic/` — 3 tiers, tests pass against `solution.py`, fail against `starter.py`
- [ ] Quiz has ≥3 questions on this topic
- [ ] Section `README.md` and `lectures/README.md` index the new files
- [ ] `black`, `ruff`, `mypy` clean; smoke tests green

---

*Standards for the plan in [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Phase documents 02–08 supply topic content for these templates.*
