# 🌐 Phase 5: Web Frameworks

72+ files across 2 major Python web frameworks, each organized into self-contained topic directories.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
05-web-frameworks/
├── fastapi/                     # 52 topics: Routing, auth, websockets
│   ├── 01-introduction/
│   │   ├── 01-introduction.py
│   │   ├── 01-introduction-lecture.md
│   │   └── 01-introduction-glossary.md
│   └── ... (52 topics)
│
└── django/                      # 20 topics: Reference guides
    ├── 01-introduction/
    │   ├── 01-introduction.py
    │   ├── 01-introduction-lecture.md
    │   └── 01-introduction-glossary.md
    └── ... (20 topics)
```

## 📚 Frameworks

| Framework | Topics | Style |
|-----------|--------|-------|
| **FastAPI** | 52 | Runnable scripts with `uvicorn` |
| **Django** | 20 | Reference guides with code snippets |

### FastAPI Topics (01-52)
Covers routing, parameters, request/response models, dependencies, middleware, security, websockets, databases, testing, and more.

### Django Topics (01-20)
Covers apps, URLs, views, templates, static files, admin, models, migrations, forms, auth, relationships, querysets, pagination, and REST framework.

## 🚀 Quick Start

### FastAPI
```bash
# Install dependencies
pip install fastapi uvicorn

# Run any FastAPI topic
cd fastapi/01-introduction
uvicorn 01-introduction:app --reload

# Open docs
# http://127.0.0.1:8000/docs
```

### Django
```bash
# Install Django
pip install django

# Reference guides are in django/NN-topic/
# See django/01-introduction/01-introduction.py for setup instructions
```

## 📝 Notes

- **FastAPI/** topics are fully runnable with `uvicorn`
- **Django/** topics are reference-only (Django not installed by default)
- All FastAPI topics include automatic OpenAPI documentation
- FastAPI topics demonstrate modern async Python patterns

---

*Last updated: August 2026*
