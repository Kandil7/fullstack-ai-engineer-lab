# 🗺️ Python Learning Path

> **Fullstack AI Engineer Lab** — Complete learning map through all 9 phases.

---

## 📊 Overview

```
Foundations ──> Libraries ──> Backend ──> Databases ──> DSA ──> ML ──> MLOps ──> GenAI ──> Projects
   Phase 1       Phase 3      Phase 5     Phase 4      Phase 6   Phase 7   Phase 8   Phase 9    🏆
   Phase 2
```

---

## 🚀 Phase 1: Core Python Fundamentals
**Directory:** `01-core-python/`  
**Files:** `01-introduction.py` → `41-inner-classes.py`  
**Lectures:** `01-core-python/lectures/`

| Week | Topics | Files | Milestone |
|------|--------|-------|-----------|
| 1 | Introduction, Setup, Syntax, Output, Comments | 01–05 | Run first Python script |
| 2 | Variables, Data Types, Numbers, Casting, Strings | 06–10 | Understand all basic types |
| 3 | Booleans, Operators, Lists, Tuples, Sets, Dicts | 11–16 | Master collections |
| 4 | If/Else, Match, While Loops, For Loops | 17–20 | Control program flow |
| 5 | Functions, Range, Arrays, Iterators | 21–24 | Write reusable code |
| 6 | Modules, Dates, Math, JSON, RegEx | 25–29 | Use standard library |
| 7 | Try/Except, String Formatting, None, User Input | 30–33 | Handle errors |
| 8 | Classes, Inheritance, Polymorphism, Encapsulation | 34–37 | Master OOP |
| 9 | File Handling, PIP, VirtualEnv, Inner Classes | 38–41 | Real-world Python |
| 10 | **Practice Problems** | `practice_all.py` | Solve 99 problems! |

---

## ⚡ Phase 2: Advanced Python
**Directory:** `02-advanced-python/`  
**Files:** `01-decorators.py` → `20-patterns.py`  
**Prerequisites:** Phase 1 complete

| Order | Topic | Key Concepts |
|-------|-------|-------------|
| 1 | Decorators | `@wraps`, caching, retry, class decorators |
| 2 | Generators | `yield`, pipelines, `send()`, memory efficiency |
| 3 | Context Managers | `with` statement, `contextlib`, resource mgmt |
| 4 | Async/Await | `asyncio`, tasks, semaphores, producer-consumer |
| 5 | Type Hints | Annotations, `Generic`, `Protocol`, `TypeVar` |
| 6 | Dataclasses | `@dataclass`, frozen, serialization |
| 7 | Enums | Auto values, flags, string enums |
| 8 | ABCs | Abstract classes, interfaces, plugins |
| 9 | Functools | `reduce`, `partial`, `lru_cache` |
| 10 | Itertools | Combinatorics, `groupby`, chaining |
| 11 | Collections | `Counter`, `defaultdict`, `namedtuple`, `deque` |
| 12 | Properties | Getter/setter, caching, validation |
| 13 | Slots | Memory optimization |
| 14 | Metaclasses | Class creation control, registries |
| 15 | Descriptors | `__get__`, `__set__`, validation |
| 16 | Threading | Concurrent I/O-bound tasks |
| 17 | Multiprocessing | Parallel CPU-bound tasks |
| 18 | Unit Testing | `unittest`, mocking, TDD |
| 19 | Logging | Levels, handlers, formatters |
| 20 | Design Patterns | Singleton, Factory, Observer, Strategy |

---

## 📊 Phase 3: Data Science Libraries
**Directory:** `03-libraries/`  
**Prerequisites:** Phase 1 complete  

### Suggested Order:
```
NumPy ──> Pandas ──> Matplotlib ──> SciPy
(01-28)   (01-24)      (01-20)       (01-12)
```

| Library | Files | Covers |
|---------|-------|--------|
| **NumPy** | 28 files | Arrays, indexing, reshaping, ufuncs, random, set ops |
| **Pandas** | 24 files | Series, DataFrames, I/O, cleaning, groupby, merge, plotting |
| **Matplotlib** | 20 files | Line, scatter, bar, histogram, pie, 3D, contour |
| **SciPy** | 12 files | Constants, optimization, integration, stats, I/O |

---

## 🗄️ Phase 4: Databases
**Directory:** `04-databases/`  
**Prerequisites:** Phase 1 complete

| Module | Files | Approach |
|--------|-------|----------|
| **MySQL** | 12 files | Uses `sqlite3` as stand-in (identical SQL syntax) |
| **MongoDB** | 11 files | Uses Python dicts as stand-in documents |

---

## 🌐 Phase 5: Web Frameworks
**Directory:** `05-web-frameworks/`  
**Prerequisites:** Phase 1 (and optionally Phase 2 for advanced patterns)

| Framework | Files | Type |
|-----------|-------|------|
| **FastAPI** | 25 files | Runnable scripts (use `uvicorn`) |
| **Django** | 20 files | Reference guides with code snippets |

---

## ⚙️ Phase 6: Data Structures & Algorithms
**Directory:** `06-data-structures-algorithms/`  
**Files:** 20 exercise files + lectures  
**Prerequisites:** Phase 1 complete

| Category | Topics |
|----------|--------|
| Data Structures | Arrays, Stacks, Queues, Linked Lists, Hash Tables, Trees |
| Algorithms | Linear/Binary Search, Bubble/Selection/Insertion/Quick/Merge Sort |

---

## 🤖 Phase 7: Machine Learning
**Directory:** `07-machine-learning/`  
**Files:** 23 exercise files + lectures  
**Prerequisites:** Phases 1, 3 (NumPy, Pandas)

| Order | Algorithm | Type |
|-------|-----------|------|
| 1 | Linear Regression | Supervised |
| 2 | Polynomial Regression | Supervised |
| 3 | Multiple Regression | Supervised |
| 4 | Decision Trees | Supervised |
| 5 | Logistic Regression | Supervised |
| 6 | K-Means | Unsupervised |
| 7 | PCA | Unsupervised |
| 8 | Random Forest | Supervised |
| 9 | SVM | Supervised |
| 10 | KNN | Supervised |

---

## 🚀 Phase 8: MLOps (Production Machine Learning)
**Directory:** `08-mlops/`  
**Files:** 16 exercise files (self-verifying) + full-detail lectures + glossaries  
**Prerequisites:** Phase 7 (ML)

| # | Topic | Production concern |
|---|-------|--------------------|
| 1 | Reproducibility | seeds, env capture, content hashing, run records |
| 2 | Experiment Tracking | params/metrics/artifacts, leaderboards |
| 3 | Data Versioning | content addressing, provenance, diffs |
| 4 | Model Registry | versions, lifecycle stages, promotion, rollback |
| 5 | Model Packaging | joblib/ONNX/pyfunc, signatures |
| 6 | Docker for ML | images, multi-stage, GPU, 12-factor |
| 7 | Model Serving | FastAPI endpoints, validation, latency |
| 8 | Inference Optimization | quantization, ONNX, batching |
| 9 | Pipeline Orchestration | DAGs, retries, caching (Prefect/Airflow) |
| 10 | Data Validation | pandera schemas, skew detection |
| 11 | Monitoring & Drift | PSI, prediction drift, delayed labels |
| 12 | CI/CD for ML | eval gates, staged promotion |
| 13 | Feature Stores | entities, point-in-time joins |
| 14 | A/B Testing Models | sample size, chi-squared, t-test |
| 15 | Cost Optimization | unit costs, spot, dedup, budgets |
| 16 | Case Study: E2E | the full lifecycle as one system |

---

## 🧠 Phase 9: GenAI (LLMs, RAG, Agents, Production)
**Directory:** `09-genai/`  
**Files:** 25 exercise files (self-verifying, no network needed) + full-detail lectures + glossaries  
**Prerequisites:** Phase 8 (MLOps)

| # | Topic | Area |
|---|-------|------|
| 1–5 | LLM fundamentals, API clients, structured output, prompt engineering, prompt eval | Foundations |
| 6–12 | Embeddings, chunking, document processing, RAG baseline, retrieval quality, advanced retrieval, reranking | RAG |
| 13–16 | Tool calling, agent patterns, multi-agent, memory & context | Agents |
| 17–22 | Observability, caching/cost, guardrails, evaluation frameworks, fine-tuning, local models | Production |
| 23–25 | Case studies: RAG service, agent, extraction pipeline | Capstones |

---

## 🏆 Capstone Projects
**Directory:** `capstones/`

After completing all phases, reinforce your skills with these projects:

| Project | Phase Prereqs | Skills Practiced |
|---------|---------------|------------------|
| `01-calculator/` | Phase 1 | Functions, control flow, user input |
| `02-file-manager/` | Phase 1–2 | File I/O, classes, CLI arguments |
| `03-api-server/` | Phase 1–5 | FastAPI, databases, authentication |
| `04-data-analyzer/` | Phase 1–3 | Pandas, Matplotlib, NumPy |
| `05-ml-pipeline/` | Phase 1–7 | Scikit-learn, model evaluation, deployment |

---

## 📚 Supplementary Materials

| Resource | Location | Purpose |
|----------|----------|---------|
| **Quizzes** | `supplementary/quizzes/` (31 files) | Self-assessment for all topics (incl. MLOps + GenAI) |
| **Interviews** | `supplementary/interviews/` (18 files) | Interview prep with Q&A + coding challenges (incl. MLOps + GenAI) |

---

## 💡 Quick Start

```bash
# 1. Install Python 3.8+
python --version

# 2. (Optional) Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start with Phase 1
cd 01-core-python/
python 01-introduction.py

# 5. Run smoke tests
cd ..
python run_smoke_tests.py
```
