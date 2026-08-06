# ⚡ Polars — Modern DataFrame Library

6 self-contained topic directories covering the Polars DataFrame library.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
polars/
├── 01-introduction/
│   ├── 01-introduction.py
│   ├── 01-introduction-lecture.md
│   └── 01-introduction-glossary.md
├── 02-expressions/
└── ... (6 topics)
```

## 📚 Topics

| # | Topic | Description |
|---|-------|-------------|
| 01 | Introduction | What is Polars, setup, basic operations |
| 02 | Expressions | Expression API, lazy evaluation |
| 03 | Lazy Evaluation | Query optimization, execution plans |
| 04 | Pandas Comparison | Polars vs Pandas, migration guide |
| 05 | PyArrow & Parquet | Columnar data, Parquet format |
| 06 | Larger than Memory | Out-of-core processing |

## 🚀 Quick Start

```bash
# Run any topic
python 01-introduction/01-introduction.py

# Run all topics
for d in [0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📝 Notes

- Polars is a modern DataFrame library optimized for performance
- Supports lazy evaluation for query optimization
- Compatible with Apache Arrow format
- Faster than Pandas for many operations

---

*Last updated: August 2026*
