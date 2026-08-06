# Delivery Report — Polars 01–06 & Matplotlib 21–24 (Phase 3: Libraries)

**Date:** 2026-08-06
**Scope:** `projects/00-core-foundations/python` module — Polars topics 01–06 and
Matplotlib topics 21–24, per `admin/mastery-plan/04-phase-3-libraries.md`.
**Status:** COMPLETE — all deliverables authored, all verification green.

---

## 1. Deliverables per topic

| Topic | Exercise | Lecture | Glossary | Challenge | Quiz |
|---|---|---|---|---|---|
| polars-01-introduction | `03-libraries/polars/01-introduction.py` | `lectures/01-introduction-lecture.md` | `lectures/01-introduction-glossary.md` | `challenges/01-introduction/` (README, starter, solution, test) | `supplementary/quizzes/polars-01-introduction-quiz.md` |
| polars-02-expressions | `02-expressions.py` | `02-expressions-lecture.md` | `02-expressions-glossary.md` | `challenges/02-expressions/` | `polars-02-expressions-quiz.md` |
| polars-03-lazy-evaluation | `03-lazy-evaluation.py` | `03-lazy-evaluation-lecture.md` | `03-lazy-evaluation-glossary.md` | `challenges/03-lazy-evaluation/` | `polars-03-lazy-evaluation-quiz.md` |
| polars-04-pandas-comparison | `04-pandas-comparison.py` | `04-pandas-comparison-lecture.md` | `04-pandas-comparison-glossary.md` | `challenges/04-pandas-comparison/` | `polars-04-pandas-comparison-quiz.md` |
| polars-05-pyarrow-parquet | `05-pyarrow-parquet.py` | `05-pyarrow-parquet-lecture.md` | `05-pyarrow-parquet-glossary.md` | `challenges/05-pyarrow-parquet/` | `polars-05-pyarrow-parquet-quiz.md` |
| polars-06-larger-than-memory | `06-larger-than-memory.py` | `06-larger-than-memory-lecture.md` | `06-larger-than-memory-glossary.md` | `challenges/06-larger-than-memory/` | `polars-06-larger-than-memory-quiz.md` |
| matplotlib-21-object-oriented-api | `03-libraries/matplotlib/21-object-oriented-api.py` | `lectures/21-…-lecture.md` | `lectures/21-…-glossary.md` | `challenges/21-object-oriented-api/` | `matplotlib-21-object-oriented-api-quiz.md` |
| matplotlib-22-styling-and-themes | `22-styling-and-themes.py` | `22-…-lecture.md` | `22-…-glossary.md` | `challenges/22-styling-and-themes/` | `matplotlib-22-styling-and-themes-quiz.md` |
| matplotlib-23-ml-visualization | `23-ml-visualization.py` | `23-…-lecture.md` | `23-…-glossary.md` | `challenges/23-ml-visualization/` | `matplotlib-23-ml-visualization-quiz.md` |
| matplotlib-24-saving-and-export | `24-saving-and-export.py` | `24-…-lecture.md` | `24-…-glossary.md` | `challenges/24-saving-and-export/` | `matplotlib-24-saving-and-export-quiz.md` |

Supporting docs: `03-libraries/polars/README.md`, `03-libraries/polars/lectures/README.md`,
`03-libraries/matplotlib/README.md` (updated), `03-libraries/matplotlib/lectures/README.md`,
regenerated `INDEX.md` for both libraries (`scripts/update_readmes.py --dir <lib> --index --write`).

## 2. Challenge test counts

| Suite | Tests | Result |
|---|---|---|
| polars 01–06 (challenges) | 76 | 76 passed |
| matplotlib 21–24 (challenges) | 43 | 43 passed |
| **Combined** | **119** | **119 passed** (4.26s) |

Command: `python -m pytest 03-libraries\polars\challenges 03-libraries\matplotlib\challenges -q --import-mode=importlib`

Per-challenge: polars 01=14, 02=15, 03=11, 04=13, 05=11, 06=12; matplotlib 21=10, 22=9, 23=12, 24=12.

## 3. Quiz composition (all 10 quizzes)

- Format: 20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output, with Answer Key and Scoring line.
- Code-output audit (final): polars 01=11, 02=12, 03=8, 04=8, 05=8, 06=8; matplotlib 21=8, 22=8, 23=8, 24=8. All ≥8 ✓
- Every code-output snippet was executed to confirm the stated answer (see §5 for the three traps caught and fixed).

## 4. Deviations from plan

1. **Challenge 04 gold verdict (pandas comparison):** the initial test failed on float
   last-bit inequality (`0.5400...01 vs 0.5400...00`). Test changed to tolerance-based
   comparison — documented in the challenge README.
2. **Challenge 06 lazy end-to-end (larger-than-memory):** the source-scan verification
   (`globals().values()` scan) also saw the bronze function's eager `collect()`. The
   verification was scoped to the `sink_join` function body only.
3. **Challenge 24 silver (saving/export):** matplotlib ≥3.10 always writes PNG color type
   6 (RGBA) even for opaque saves, so byte-25 transparency detection is impossible, and
   IDAT rows are filter-encoded (row[0] != 0) which blocks alpha scanning without a full
   PNG decoder. Silver was redesigned to `export_report(path)` — PNG vs SVG format
   detection with `has_alpha` = channel presence — and the version note documented in the
   challenge README.
4. **Polars topic titles (assumption):** the `04-phase-3-libraries.md` Polars table was
   truncated on read; the six slugs (01-introduction … 06-larger-than-memory) were chosen
   by intent and match the plan's ordering, but the plan's exact wording was never
   re-verified. Flagged for a follow-up re-read of the plan doc.

## 5. Verification results

- Exercises: all 10 run with `--verify`, exit code 0 (polars 01–06, matplotlib 21–24).
- Challenges: combined suite 119 passed (see §2).
- Quiz snippets: 11 code-output snippets executed. Three traps caught and fixed during
  the audit:
  1. `write_parquet(compression="none")` is **invalid** in polars 1.43 — the codec name is
     `"uncompressed"`; the quiz now uses the valid name.
  2. zstd vs uncompressed on a tiny/run-compressible frame: RLE/bit-packing already
     shrinks runs, so zstd can be *larger* (475 vs 457 B on 2 rows; 513 vs 494 B on 100k
     zeros). The quiz now uses cycling data `[i % 1000 for i in range(100_000)]` where
     zstd = 3,466 B vs uncompressed = 133,530 B → `True`, and the key explains the trap.
  3. `plt.rcParams["figure.dpi"]` reads back as float — prints `120.0`, not `120`.

## 6. Environment & version notes (polars 1.43.2)

- Python 3.13.11 · polars 1.43.2 · pyarrow 25.0.0 · sklearn 1.7.2 · matplotlib 3.10.7.
- `print(df)` / `explain()` Unicode crashes cp1252 → inspect via `to_dict(as_series=False)`/`rows()`.
- `.alias()` binds tighter than arithmetic → parenthesize.
- `rank()` defaults ascending → `rank(descending=True)`.
- CSV filter pushdown shows as `SELECTION` inside the scan, not a `FILTER` node.
- `scan_parquet(dir)` requires parquet-only directories.
- `to_numpy(allow_copy=False)` raises `RuntimeError` for String columns.
- `sort()` puts nulls FIRST → use `sort(..., nulls_last=True)`.
- `write_parquet` compression: valid codecs are snappy/gzip/brotli/lz4/zstd/uncompressed
  (`"none"` is NOT accepted); "uncompressed" still RLE/bit-packs runs.
- Matplotlib ≥3.10 PNGs are RGBA (color type 6) even when opaque.

## 7. Remaining / optional follow-ups

- Re-read `04-phase-3-libraries.md` to confirm the six Polars topic slugs verbatim (deviation 4).
- Optionally: add the 10 quizzes to a quiz-runner or the assessment system
  (`admin/mastery-plan/09-assessment-system.md`).
