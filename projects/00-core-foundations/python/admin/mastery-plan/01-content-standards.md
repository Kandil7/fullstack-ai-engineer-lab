# Content Standards — Unified Per-Topic Organization

> **Single source of truth** for content structure, naming, and organization.
> Every file created or retrofitted under this plan conforms to these standards.

---

## 1. Why Standardize

The audit found:
- Lectures scattered in section-level `lectures/` directories
- Challenges in separate `challenges/` directories
- Quizzes isolated in `supplementary/quizzes/`
- No consistent per-topic organization

**Solution:** Each topic gets its own directory containing ALL related artifacts.

---

## 2. Per-Topic Directory Structure

```
section/
├── NN-topic-slug/                    # Topic directory
│   ├── NN-topic-slug.py              # Exercise (runnable code)
│   ├── NN-topic-slug-lecture.md      # Lecture (detailed explanation)
│   ├── NN-topic-slug-glossary.md     # Glossary (key terms)
│   ├── NN-topic-slug-quiz.md         # Quiz (20 questions)
│   └── challenges/
│       └── NN-topic-slug/
│           ├── README.md             # Challenge brief (3 tiers)
│           ├── starter.py            # Learner starter code
│           ├── solution.py           # Reference implementation
│           └── test_challenge.py     # Hidden tests (pytest)
├── README.md                         # Section overview
└── INDEX.md                          # Auto-generated index
```

---

## 3. Naming Conventions

### File Naming
- **Pattern:** `NN-topic-slug.{py,md}`
- **Prefix:** Zero-padded 2 digits (01-99)
- **Slug:** kebab-case, matching across ALL artifacts
- **Example:** `01-introduction.py`, `01-introduction-lecture.md`

### Directory Naming
- **Pattern:** `NN-topic-slug/`
- **Must match** the exercise filename exactly
- **Example:** `01-introduction/`

### Rules
1. One topic per prefix (no duplicates)
2. Slug must match across all artifacts
3. Prefix is unique within its section
4. Never two files sharing a number

---

## 4. Content Templates

### Exercise Template (`NN-topic.py`)

```python
"""
<Section> — NN: <Topic Title>
==============================================
Topics: <comma-separated subtopics>

Why this matters for AI/backend engineering:
    <2-3 lines: the concrete production or ML scenario>

Run:      python NN-topic.py
Verify:   python NN-topic.py --verify
Reference: <official docs URL>
"""

from __future__ import annotations
import sys

# ============================================================
# 1. <First Concept>
# ============================================================
# <Explanation before code>

# Example 1: <what this demonstrates>
code_example()

# Output:
# expected output


# ============================================================
# N. Production Pattern
# ============================================================
# The idiomatic form a senior engineer would ship

def production_function():
    """Docstring with purpose and reasoning."""
    pass


# ============================================================
# Verification Block
# ============================================================
def _verify() -> None:
    """Run all assertions — called by smoke tests."""
    print(f"[OK] {__file__}: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        # Demo mode
        pass
```

### Lecture Template (`NN-topic-lecture.md`)

```markdown
# NN: <Topic Title>

> **Duration:** <X> minutes | **Prerequisites:** <prerequisites>

## 🎯 Learning Objectives
By the end of this lecture, you will be able to:
1. <Objective 1>
2. <Objective 2>
3. <Objective 3>

## 📚 Key Concepts

### Concept 1: <Name>
<Explanation with examples>

### Concept 2: <Name>
<Explanation with examples>

## 💻 Code Examples

### Example 1: <Basic Usage>
```python
# code here
```

### Example 2: <Advanced Usage>
```python
# code here
```

## ⚠️ Common Pitfalls
1. <Pitfall 1>
2. <Pitfall 2>

## 🏭 Production Patterns
<How this is used in real systems>

## 📝 Summary
- <Key point 1>
- <Key point 2>
- <Key point 3>

## 🔗 Next Steps
- <Related topic>
- <Practice exercise>
```

### Glossary Template (`NN-topic-glossary.md`)

```markdown
# NN: <Topic Title> — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|------------|---------|
| <term1> | <definition> | `<example>` |
| <term2> | <definition> | `<example>` |

## Detailed Definitions

### <Term 1>
**Definition:** <clear definition>

**Example:**
```python
# example code
```

**Related:** <related terms>

### <Term 2>
**Definition:** <clear definition>

**Example:**
```python
# example code
```

**Related:** <related terms>

## Alphabetical Index
1. <term1> → <brief definition>
2. <term2> → <brief definition>
```

### Quiz Template (`NN-topic-quiz.md`)

```markdown
# NN: <Topic Title> — Quiz

> **20 questions** | **Time:** 20 minutes | **Passing:** 70%

## Questions

### Q1: <Question>
- [ ] A) <option>
- [ ] B) <option>
- [ ] C) <option>
- [ ] D) <option>

<details>
<summary>Answer</summary>

**Correct:** <letter>

**Explanation:** <why this is correct>

</details>

### Q2: <Question>
...

## Scoring
- 18-20: **Mastery** ⭐
- 14-17: **Proficient** ✅
- 10-13: **Developing** 📈
- 0-9: **Needs Review** 📚
```

### Challenge Template (`NN-topic-slug/`)

```
NN-topic-slug/
├── README.md           # Challenge brief
├── starter.py          # Learner starter code
├── solution.py         # Reference implementation
└── test_challenge.py   # Hidden tests
```

**README.md:**
```markdown
# Challenge: <Topic Title>

## 🥉 Bronze (Easy)
<Description of easy challenge>

**Goal:** <what learner should achieve>

## 🥈 Silver (Medium)
<Description of medium challenge>

**Goal:** <what learner should achieve>

## 🥇 Gold (Hard)
<Description of hard challenge>

**Goal:** <what learner should achieve>

## 📝 Instructions
1. Open `starter.py`
2. Complete the challenges in order
3. Run `pytest test_challenge.py` to verify
4. Compare with `solution.py` when stuck
```

---

## 5. Section Organization

### Phase 1: Core Python (`01-core-python/`)

```
01-core-python/
├── basics/                           # 01-16: Introduction to Collections
│   ├── 01-introduction/
│   │   ├── 01-introduction.py
│   │   ├── 01-introduction-lecture.md
│   │   ├── 01-introduction-glossary.md
│   │   ├── 01-introduction-quiz.md
│   │   └── challenges/01-introduction/
│   ├── 02-get-started/
│   │   └── ...
│   └── ... through 16-dictionaries/
├── control-flow/                     # 17-20: Conditionals and Loops
├── functions/                        # 21-33, 38: Functions and Modules
├── oop/                              # 34-37, 41: Object-Oriented Programming
├── advanced/                         # 39-40, 42-52: Advanced Topics
├── practice/                         # Practice problems
├── README.md
└── INDEX.md
```

### Phase 2: Advanced Python (`02-advanced-python/`)

```
02-advanced-python/
├── 01-decorators/
│   ├── 01-decorators.py
│   ├── 01-decorators-lecture.md
│   ├── 01-decorators-glossary.md
│   ├── 01-decorators-quiz.md
│   └── challenges/01-decorators/
├── 02-generators/
│   └── ...
└── ... through 34-debugging-techniques/
```

### Phase 3: Libraries (`03-libraries/`)

```
03-libraries/
├── numpy/
│   ├── basics/
│   │   ├── 01-introduction/
│   │   │   ├── 01-introduction.py
│   │   │   ├── 01-introduction-lecture.md
│   │   │   ├── 01-introduction-glossary.md
│   │   │   └── challenges/01-introduction/
│   │   └── ... through 28-ufunc-set-operations/
│   └── advanced/
│       └── ... through 34-advanced-indexing/
├── pandas/
│   ├── basics/
│   ├── advanced/
│   ├── production/
│   └── case-studies/
├── matplotlib/
│   ├── basics/
│   ├── advanced/
│   └── 3d/
├── scipy/
└── polars/
```

---

## 6. Migration Checklist

For each section:
- [ ] Create topic directories
- [ ] Move exercises into topic directories
- [ ] Co-locate lectures & glossaries
- [ ] Add quizzes to topic directories
- [ ] Nest challenges within topics
- [ ] Update README.md
- [ ] Update INDEX.md
- [ ] Update learning_path.md
- [ ] Fix cross-references
- [ ] Run validation tests

---

## 7. Quality Gates

Before marking a topic as complete:
1. ✅ Exercise file exists and runs
2. ✅ Lecture file exists and follows template
3. ✅ Glossary file exists and follows template
4. ✅ Quiz file exists with 20 questions
5. ✅ Challenge directory exists with all artifacts
6. ✅ All cross-references work
7. ✅ Tests pass

---

*Last updated: August 2026*
