# Pandas teaching-file remediation (backlog R2/R3/R4 + latent bugs)

### Context

Repo: fullstack-ai-engineer-lab, module projects/00-core-foundations/python. Task: repair 14 broken pandas teaching files (13 under 03-libraries/pandas/advanced/ + 24-case-study-ml-prep.py) audited on 2026-07-29 against admin/mastery-plan/10-remediation-backlog.md (R2 API drift, R3 encoding, R4 optional deps). Env: Python 3.13, pandas 2.2.3, numpy 2.4.1, matplotlib 3.10.7, scipy 1.16.3; openpyxl/seaborn installed, xlsxwriter/category_encoders missing. Verified by running each file from the module root (must exit 0).

### Explanation

Each file was run to capture the ACTUAL traceback, then fixed minimally. R2 API drift: (1) .loc[len/df.index]=[...] list must match full column count — added the missing 'id' value; (2) column assignment length mismatch — pd.array([...] + [None]*16) and np.tile(parsed_dates, 5) to hit 20 rows; (3) str.replace dict-as-pat no longer valid — chain one replace per dict item with regex=False; (4) pivot() on non-unique pairs — pivot_table(aggfunc='sum'); (5) .join([list]) rejects suffixes — chain pairwise joins + rename before join; (6) .str has no eq/ne/lt/le/gt/ge accessors — plain Series operators; (7) pd.to_datetime mixed formats needs format='mixed' in pandas 2.x; (8) crosstab has no fill_value kwarg — fillna(0) after; (9) qcut duplicate bin edges — duplicates='drop' AND drop the fixed label list (bin count shrinks); (10) .xs([...]) list keys — tuple key per xs + pd.concat; (11) loc[idx[:, :], idx[:, [cols]]] unhashable — plain column list; (12) Styler.highlight_null(null_color=) — renamed to color=. R3 encoding: emoji fruit map → ASCII labels (cp1252 cannot encode U+1F34E), sparkline '█' → '#', apply() kwargs= → direct kwds (latent bug). R4 deps: try/except import guards for openpyxl/seaborn per backlog template, plus xlsxwriter and category_encoders (both missing here); skipped sections wrapped in if/else with "[skip] ..." messages. Structural/latent: 14-io-csv-json partitioned parquet cannot target BytesIO (pyarrow needs a real directory → output/parquet_partitioned/); 15-io-excel-sql read 'sales' from the wrong in-memory DB (engine vs sqlite3 conn); 21-case-study-eda merge omitted 'cost' (KeyError at profit calc); 24-case-study-ml-prep broadcast (10050,) vs (10000,) from noise loop using stale n after dup concat → len(df); SimpleImputer fill_value='missing' on already-one-hot int64 cols → 0; Series has no to_parquet → .to_frame().

### Alternatives

(a) Fix qcut by keeping labels and forcing unique edges via smaller q — rejected: q=5 on ~6 unique values cannot produce 5 unique edges; auto-labels + duplicates='drop' is the only correct form. (b) For multi-xs, loc[[tuple, tuple]] — rejected: AssertionError on 3-level MultiIndex (verified in REPL). (c) For 15-io-excel-sql, writing 'sales' to both DBs — rejected in favor of reading back through the engine (single source of truth, smaller diff). (d) Setting MPLBACKEND via env var at run time instead of in-file — rejected; in-file setdefault before pyplot import matches E8/CI contract.

### Rationale (Why this?)

The audit only captured the FIRST failure per file; running each file revealed 10 additional latent bugs downstream (str.eq accessor, apply kwargs=, crosstab fill_value, to_datetime format='mixed', parquet partition target, wrong in-memory DB, missing 'cost' merge column, broadcast stale n, imputer fill_value dtype, Series.to_parquet, sample(200) on 100 rows, IndexSlice column tuple). Fixes follow the documented backlog exactly where it applies (pivot_table aggfunc, tuple xs, duplicates='drop', color=, pairwise joins, ASCII labels, [skip] guards). Conditions to revisit: if openpyxl/seaborn are ever installed, guards still run the full sections; xlsxwriter/category_encoders remain optional by design (backlog R4 recommends adding them to requirements.txt).

### Exercises

1. Re-run the 14 files with `python <file>` from projects/00-core-foundations/python and confirm exit 0 (done here — all PASS). 2. Uninstall openpyxl in a venv and re-run 14/15 to confirm the "[skip] openpyxl not installed" path degrades cleanly. 3. Write a smoke-runner loop (R10) that executes each file with a 30s timeout and asserts exit 0 — the missing CI gate that let all 34 backlog failures through. 4. Fix the remaining pandas backlog entries: 20-performance.py syntax error (R1.2). 5. Try replicating the qcut NaN edge case: build a Series of 6 identical values and confirm duplicates='drop' still returns all-valid bins.

### Next Steps

R10 CI gate (run_smoke_tests.py with --all/--verify, 30s timeouts, MPLBACKEND=Agg, skip-list) to prevent regression; then R1.2 (20-performance.py syntax), remaining R2 numpy entries (10/12/28), R5 SQL, R6 MongoDB, R8 pandas renumbering + missing lecture pairs.

---
