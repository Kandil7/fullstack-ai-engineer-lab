# 🗄️ Phase 4: Database Integration

76+ files across 7 database technologies, each organized into self-contained topic directories.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
04-databases/
├── sql-fundamentals/            # 14 topics: Core SQL concepts
│   ├── 01-relational-model/
│   │   ├── 01-relational-model.py
│   │   └── 01-relational-model-lecture.md
│   └── ... (14 topics)
│
├── sql-sqlite/                  # 12 topics: SQLite exercises
├── postgresql/                  # 6 topics: PostgreSQL exercises
├── mongodb/                     # 12 topics: MongoDB exercises
├── redis/                       # 8 topics: Caching, pub/sub, sessions
├── sqlalchemy/                  # 10 topics: ORM patterns
└── vector-stores/               # 8 topics: Embeddings, similarity search
```

## 📚 Technologies

| Technology | Topics | Focus |
|------------|--------|-------|
| **SQL Fundamentals** | 14 | Portable SQL (DDL, DML, joins, subqueries) |
| **SQLite** | 12 | Portable exercises (built-in sqlite3) |
| **PostgreSQL** | 6 | Advanced features (JSONB, indexes, pooling) |
| **MongoDB** | 12 | Document database (dict stand-in) |
| **Redis** | 8 | Caching, pub/sub, distributed locks |
| **SQLAlchemy** | 10 | ORM patterns (Core + ORM) |
| **Vector Stores** | 8 | Embeddings, similarity search |

## 🚀 Quick Start

```bash
# SQL Fundamentals (no setup needed)
python sql-fundamentals/01-relational-model/01-relational-model.py

# SQLite (no setup needed)
python sql-sqlite/01-getting-started/01-getting-started.py

# PostgreSQL (requires Docker)
docker-compose up -d postgres
python postgresql/01-setup-and-psycopg/01-setup-and-psycopg.py

# MongoDB (uses dict stand-in)
python mongodb/01-getting-started/01-getting-started.py

# Redis (requires Docker)
docker-compose up -d redis
python redis/01-introduction/01-introduction.py

# SQLAlchemy (any database)
python sqlalchemy/01-core-vs-orm/01-core-vs-orm.py

# Vector Stores (embeddings)
python vector-stores/01-vector-search-fundamentals/01-vector-search-fundamentals.py
```

## 📝 Notes

- **sql-fundamentals/** teaches portable SQL (works anywhere)
- **sql-sqlite/** uses SQLite as a portable stand-in (no installation)
- **postgresql/** requires real PostgreSQL (Docker recommended)
- **mongodb/** uses Python dicts as stand-ins (no MongoDB needed)
- **redis/** requires Redis server (Docker recommended)
- **sqlalchemy/** covers ORM patterns for any database
- **vector-stores/** covers modern vector database patterns

---

*Last updated: August 2026*
