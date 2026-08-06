# 📘 Phase 1: Core Python Fundamentals

88 Python files organized into 6 subdirectories covering Python from absolute basics through advanced topics like memory optimization, serialization, and datetime handling.

## 📋 Directory Structure

```
01-core-python/
├── basics/           (16 files) — Introduction to Collections
├── control-flow/     (4 files)  — Conditionals and Loops
├── functions/        (14 files) — Functions, Modules, Error Handling
├── oop/              (5 files)  — Object-Oriented Programming
├── advanced/         (13 files) — Advanced Topics
├── practice/         (2 files)  — Practice Problems
├── challenges/                   — 3-tier challenges per topic
└── lectures/                     — lecture + glossary per topic
```

## 📚 Contents by Subdirectory

### basics/ (01-16): Introduction to Collections
| # | Topic | File |
|---|-------|------|
| 01 | Introduction | `01-introduction.py` |
| 02 | Getting Started | `02-get-started.py` |
| 03 | Syntax | `03-syntax.py` |
| 04 | Output | `04-output.py` |
| 05 | Comments | `05-comments.py` |
| 06 | Variables | `06-variables.py` |
| 07 | Data Types | `07-data-types.py` |
| 08 | Numbers | `08-numbers.py` |
| 09 | Casting | `09-casting.py` |
| 10 | Strings | `10-strings.py` |
| 11 | Booleans | `11-booleans.py` |
| 12 | Operators | `12-operators.py` |
| 13 | Lists | `13-lists.py` |
| 14 | Tuples | `14-tuples.py` |
| 15 | Sets | `15-sets.py` |
| 16 | Dictionaries | `16-dictionaries.py` |

### control-flow/ (17-20): Conditionals and Loops
| # | Topic | File |
|---|-------|------|
| 17 | If/Else | `17-if-else.py` |
| 18 | Match | `18-match.py` |
| 19 | While Loops | `19-while-loops.py` |
| 20 | For Loops | `20-for-loops.py` |

### functions/ (21-33, 38): Functions, Modules, Error Handling
| # | Topic | File |
|---|-------|------|
| 21 | Functions | `21-functions.py` |
| 22 | Range | `22-range.py` |
| 23 | Arrays | `23-arrays.py` |
| 24 | Iterators | `24-iterators.py` |
| 25 | Modules | `25-modules.py` |
| 26 | Dates | `26-dates.py` |
| 27 | Math | `27-math.py` |
| 28 | JSON | `28-json.py` |
| 29 | RegEx | `29-regex.py` |
| 30 | Try/Except | `30-try-except.py` |
| 31 | String Formatting | `31-string-formatting.py` |
| 32 | None | `32-none.py` |
| 33 | User Input | `33-user-input.py` |
| 38 | File Handling | `38-file-handling.py` |

### oop/ (34-37, 41): Object-Oriented Programming
| # | Topic | File |
|---|-------|------|
| 34 | Classes | `34-classes.py` |
| 35 | Inheritance | `35-inheritance.py` |
| 36 | Polymorphism | `36-polymorphism.py` |
| 37 | Encapsulation | `37-encapsulation.py` |
| 41 | Inner Classes | `41-inner-classes.py` |

### advanced/ (39-40, 42-52): Advanced Topics
| # | Topic | File |
|---|-------|------|
| 39 | PIP | `39-pip.py` |
| 40 | VirtualEnv | `40-virtualenv.py` |
| 42 | Pathlib | `42-pathlib.py` |
| 43 | Dataclasses & Namedtuples | `43-dataclasses-and-namedtuples.py` |
| 44 | Logging | `44-logging.py` |
| 45 | Testing with Pytest | `45-testing-with-pytest.py` |
| 46 | CLI & Config | `46-cli-and-config.py` |
| 47 | Exceptions Advanced | `47-exceptions-advanced.py` |
| 48 | Comprehensions & Modern Syntax | `48-comprehensions-and-modern-syntax.py` |
| 49 | Collections Toolkit | `49-collections-toolkit.py` |
| 50 | Datetime & Timezones | `50-datetime-and-timezones.py` |
| 51 | Serialization & Persistence | `51-serialization-and-persistence.py` |
| 52 | Memory & Performance | `52-memory-and-performance.py` |

### practice/: Practice Problems
| File | Description |
|------|-------------|
| `practice_all.py` | 99 problems with solutions |
| `practice_no_solutions.py` | Blank stubs for practice |

## 🚀 Quick Start

```bash
# Run any file from the appropriate subdirectory
python basics/01-introduction.py

# Run all files in a subdirectory
for f in basics/*.py; do python "$f"; done

# Run smoke tests
python ../run_smoke_tests.py --phase 1
```

## 📝 Notes

- Each `.py` file is **self-contained** and runnable
- Lectures and glossaries live in `lectures/` subdirectory
- Challenges live in `challenges/` subdirectory
- Practice files are in `practice/` subdirectory

---

*Last updated: August 2026*
