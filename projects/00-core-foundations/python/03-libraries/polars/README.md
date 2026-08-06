# Polars Tutorial Exercises

Complete, runnable Python scripts covering Polars for data engineering
and ML pipelines: the expression API, lazy evaluation, pandas parity,
PyArrow/Parquet interop, and larger-than-memory processing.

Each script is self-contained with inline teaching comments, a plain
run (demo + self-verification), and a `--verify` flag:

```bash
# Run any single exercise (demo + checks)
python 01-introduction.py

# Verify only
python 01-introduction.py --verify
```

## Exercises

| # | File | Topic |
|---|------|-------|
| 01 | `01-introduction.py` | DataFrame/Series basics, Arrow memory model, eager vs lazy |
| 02 | `02-expressions.py` | The expression API: select / with_columns / filter / group_by |
| 03 | `03-lazy-evaluation.py` | scan_csv/scan_parquet, query plans, predicate + projection pushdown |
| 04 | `04-pandas-comparison.py` | Side-by-side idioms: filter, groupby-agg, join, new columns |
| 05 | `05-pyarrow-parquet.py` | Parquet layout, compression (none/snappy/zstd), zero-copy reads |
| 06 | `06-larger-than-memory.py` | Streaming engine, sinks, out-of-core joins, null handling |

## Requirements

- Python 3.10+
- `polars` (>= 1.0; verified on 1.43.x)
- `pyarrow` (bundled with polars; used directly in exercise 05)
- `pandas` (exercise 04 parity demo)

```bash
pip install polars pyarrow pandas
```

## Companion Material

| Artifact | Location |
|----------|----------|
| Lectures + glossaries | `lectures/` (`NN-topic-lecture.md`, `NN-topic-glossary.md`) |
| Challenges (Bronze/Silver/Gold + pytest) | `challenges/NN-topic/` |
| Quizzes (20 Q, answer keys) | `supplementary/quizzes/polars-NN-topic-quiz.md` |

Run all challenge tests from the module root:

```bash
python -m pytest 03-libraries/polars/challenges --import-mode=importlib
```

## Design Decisions

- Deterministic: `np.random.default_rng(42)` everywhere; no
  wall-clock assertions (benchmarks are printed, never asserted)
- ASCII-only stdout: Polars' Unicode table renderer and plan text
  crash cp1252 consoles, so inspection uses `to_dict(as_series=False)`
  / `rows()` and plan checks use `"SELECTION" in plan`
- Optional deps degrade: if polars is missing, scripts print
  `[skip] ... install with: pip install polars` and exit 0
- Every script ends with `_verify()` (>= 5 assertions); plain runs
  print `[OK] NN-topic: all checks passed`
