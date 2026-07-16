# 🐍 Python Learning Module — Fullstack AI Engineer Lab

> **405+ files across 7 learning phases** — from `print("Hello")` to production ML pipelines.

---

## 📋 Quick Navigation

| Phase | Directory | Files | Focus |
|-------|-----------|-------|-------|
| **1** | `01-core-python/` | 43 | Python fundamentals: syntax → OOP → file I/O |
| **2** | `02-advanced-python/` | 20 | Decorators → async → metaclasses → design patterns |
| **3** | `03-libraries/` | 84 | NumPy, Pandas, Matplotlib, SciPy |
| **4** | `04-databases/` | 23 | MySQL (sqlite3 stand-in), MongoDB (dict stand-in) |
| **5** | `05-web-frameworks/` | 45 | FastAPI (runnable), Django (reference) |
| **6** | `06-data-structures-algorithms/` | 20 | Arrays → trees → sorts → searches |
| **7** | `07-machine-learning/` | 23 | Regression → classification → clustering → PCA |
| 📚 | `supplementary/` | 127+ | Lectures, quizzes (29), interviews (16) |
| 🏆 | `projects/` | 5 | Capstone mini-projects combining all phases |

---

## 🚀 Getting Started

```bash
# 1. Requirements
pip install -r requirements.txt

# 2. Start with Phase 1
cd 01-core-python
python 01-introduction.py

# 3. Follow the learning path
# See: learning_path.md for the recommended order

# 4. Verify everything works
python run_smoke_tests.py
```

---

## 🏗️ Directory Structure

```
python/
├── 01-core-python/                  # 📘 Phase 1: Python Fundamentals
│   ├── 01-introduction.py → 41-inner-classes.py
│   ├── practice_all.py
│   └── practice_no_solutions.py
│
├── 02-advanced-python/              # 🔬 Phase 2: Advanced Python
│   ├── 01-decorators.py → 20-patterns.py
│   └── lectures/                    # Topic-specific lectures
│
├── 03-libraries/                    # 📊 Phase 3: Data Science Libraries
│   ├── numpy/        (28 files)
│   ├── pandas/       (24 files)
│   ├── matplotlib/   (20 files)
│   └── scipy/        (12 files)
│
├── 04-databases/                    # 🗄️ Phase 4: Database Integration
│   ├── mysql/        (12 files)
│   └── mongodb/      (11 files)
│
├── 05-web-frameworks/               # 🌐 Phase 5: Backend Development
│   ├── fastapi/      (25 files + exercises + lectures)
│   └── django/       (20 files)
│
├── 06-data-structures-algorithms/   # ⚙️ Phase 6: DSA
│   ├── 01-introduction.py → 20-merge-sort.py
│   └── lectures/
│
├── 07-machine-learning/             # 🤖 Phase 7: Machine Learning
│   ├── 01-getting-started.py → 23-k-nearest-neighbors.py
│   └── lectures/
│
├── supplementary/                   # 📚 Supplementary Materials
│   ├── lectures/01-core-python/     # 82 lecture + glossary files
│   ├── quizzes/                     # 29 self-assessment quizzes
│   └── interviews/                  # 16 interview prep guides
│
├── projects/                        # 🏆 Capstone Mini-Projects
│   ├── 01-calculator/
│   ├── 02-file-manager/
│   ├── 03-api-server/
│   ├── 04-data-analyzer/
│   └── 05-ml-pipeline/
│
├── _dev/                            # 🛠️ Dev Utilities
│   ├── validate_structure.py
│   ├── check_typos.py
│   └── update_readmes.py
│
├── requirements.txt                 # 📦 All dependencies
├── learning_path.md                 # 🗺️ Full learning map
├── run_smoke_tests.py               # ✅ Smoke test runner
└── README.md                        # 📖 This file
```

---

## 📖 Learning Path

See **[learning_path.md](learning_path.md)** for a complete, week-by-week learning schedule covering all 7 phases.

**Recommended order:** Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 4 → Phase 6 → Phase 7 → Projects

---

## ✅ Quick Start by Goal

| If you want to... | Start here |
|-------------------|------------|
| Learn Python from scratch | `01-core-python/01-introduction.py` |
| Master advanced Python | `02-advanced-python/01-decorators.py` |
| Do data science | `03-libraries/numpy/01-introduction.py` |
| Build web APIs | `05-web-frameworks/fastapi/01-introduction.py` |
| Learn SQL/NoSQL | `04-databases/mysql/01-getting-started.py` |
| Practice algorithms | `06-data-structures-algorithms/01-introduction.py` |
| Build ML models | `07-machine-learning/01-getting-started.py` |
| Prep for interviews | `supplementary/interviews/` |
| Test yourself | `supplementary/quizzes/` |
| Build a project | `projects/01-calculator/` |

---

## 📝 Notes

- Each `.py` file is **self-contained** and runnable with `python filename.py`
- All FastAPI files can be served with `uvicorn filename:app --reload`
- Matplotlib plots save to `./output/` (no display required)
- MySQL exercises use built-in `sqlite3` — no driver needed
- MongoDB exercises use Python dicts as document stand-ins
- Quiz files are `.md` — edit them or use as flashcards
- Interview files contain both questions AND solutions

---

## 📦 Dependencies

See [requirements.txt](requirements.txt) for the full list.  
Most Phase 1–2 exercises need **no external packages**.

---

## 🔗 Related Resources

- [Fullstack AI Engineer Lab (root)](../../README.md)
- [Project Plans](../../docs/plan/)
- [Architecture Docs](../../docs/architecture/)
- [Infrastructure](../../infra/)

---

*Last updated: July 2026*
