# 🐍 Python Learning Module — Fullstack AI Engineer Lab

> **350+ exercise files across 9 learning phases** — from `print("Hello")` to production ML pipelines and GenAI systems.
> Each topic ships with a lecture + glossary pair, and most phases include quizzes and interview prep.

---

## 📋 Quick Navigation

| Phase | Directory | Focus |
|-------|-----------|-------|
| **1** | `01-core-python/` | Python fundamentals: syntax → OOP → file I/O |
| **2** | `02-advanced-python/` | Decorators → async → metaclasses → design patterns |
| **3** | `03-libraries/` | NumPy, Pandas, Matplotlib, SciPy |
| **4** | `04-databases/` | MySQL (sqlite3 stand-in), MongoDB (dict stand-in) |
| **5** | `05-web-frameworks/` | FastAPI (runnable), Django (reference-only) |
| **6** | `06-data-structures-algorithms/` | Arrays → trees → sorts → searches |
| **7** | `07-machine-learning/` | Regression → classification → clustering → PCA |
| **8** | `08-mlops/` | Reproducibility → registry → serving → monitoring → A/B |
| **9** | `09-genai/` | LLMs → RAG → agents → eval → fine-tuning → production |
| 📚 | `supplementary/` | Quizzes + interview prep |
| 🏆 | `projects/` | Capstone mini-projects combining all phases |

> **Lectures & glossaries live inside each phase** (`01-core-python/lectures/`, `02-advanced-python/lectures/`, …), one lecture + one glossary per exercise.

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
│   ├── practice_all.py / practice_no_solutions.py
│   └── lectures/                    # lecture + glossary per topic
│
├── 02-advanced-python/              # 🔬 Phase 2: Advanced Python
│   ├── 01-decorators.py → 20-patterns.py
│   └── lectures/
│
├── 03-libraries/                    # 📊 Phase 3: Data Science Libraries
│   ├── numpy/        (28 files + lectures)
│   ├── pandas/       (basics + case studies + lectures)
│   ├── matplotlib/   (basics + advanced + lectures)
│   └── scipy/        (12 files + lectures)
│
├── 04-databases/                    # 🗄️ Phase 4: Database Integration
│   ├── mysql/        (12 files, sqlite3 stand-in)
│   └── mongodb/      (11 files, dict stand-in)
│
├── 05-web-frameworks/               # 🌐 Phase 5: Backend Development
│   ├── fastapi/      (25 files + exercises + lectures)
│   └── django/       (reference snippets — Django not required)
│
├── 06-data-structures-algorithms/   # ⚙️ Phase 6: DSA
│   ├── 01-introduction.py → 20-merge-sort.py
│   └── lectures/
│
├── 07-machine-learning/             # 🤖 Phase 7: Machine Learning
│   ├── 01-getting-started.py → 23-k-nearest-neighbors.py
│   └── lectures/
│
├── 08-mlops/                        # 🚀 Phase 8: MLOps (Production ML)
│   ├── 01-reproducibility.py → 16-case-study-e2e.py
│   └── lectures/                    # full-detail lectures + glossaries
│
├── 09-genai/                        # 🧠 Phase 9: GenAI (LLMs, RAG, Agents)
│   ├── 01-llm-fundamentals.py → 25-case-study-extraction.py
│   └── lectures/                    # full-detail lectures + glossaries
│
├── supplementary/                   # 📚 Quizzes + interview prep
│   ├── quizzes/                     # self-assessment per topic
│   └── interviews/                  # Q&A + coding challenges
│
├── projects/                        # 🏆 Capstone Mini-Projects
│   ├── 01-calculator/
│   ├── 02-file-manager/
│   ├── 03-api-server/
│   ├── 04-data-analyzer/
│   └── 05-ml-pipeline/
│
├── tests/                           # ✅ Unit tests (pytest)
├── _dev/                            # 🛠️ Dev utilities
│   ├── validate_structure.py
│   ├── check_typos.py
│   └── update_readmes.py
│
├── docs/mastery-plan/               # 📈 Baseline audit + 40-week roadmap
├── requirements.txt                 # 📦 All dependencies
├── learning_path.md                 # 🗺️ Full learning map
├── run_smoke_tests.py               # ✅ Smoke test runner
└── README.md                        # 📖 This file
```

---

## 📖 Learning Path

See **[learning_path.md](learning_path.md)** for the complete, week-by-week learning schedule covering all 9 phases.

**Recommended order:** Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 4 → Phase 6 → Phase 7 → Phase 8 → Phase 9 → Projects

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
| Ship ML to production | `08-mlops/01-reproducibility.py` |
| Build LLM/RAG/agents | `09-genai/01-llm-fundamentals.py` |
| Prep for interviews | `supplementary/interviews/` |
| Test yourself | `supplementary/quizzes/` |
| Build a project | `projects/01-calculator/` |

---

## 📝 Notes

- Each `.py` file is **self-contained** and runnable with `python filename.py`
- All FastAPI files can be served with `uvicorn filename:app --reload`
- Matplotlib plots save to `./output/` (no display required; headless with `MPLBACKEND=Agg`)
- MySQL exercises use built-in `sqlite3` — no driver needed
- MongoDB exercises use Python dicts as document stand-ins
- Django is **reference-only**: not installed by default and excluded from smoke tests
- Quiz files are `.md` — edit them or use as flashcards
- Interview files contain both questions AND solutions
- Run the suite: `python -m pytest tests -q`

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

*Last updated: August 2026*
