# Phase 3 — Data Libraries (`03-libraries/`)

> **Current:** 105 exercises (NumPy 28, pandas **45**, Matplotlib 20, SciPy 12),
> 84 lectures. **87/105 pass — 18 fail.**
> **Target:** ~130 exercises, every one with a lecture, plus Polars/PyArrow.
>
> This section has the module's worst structural defect (**R8**, pandas double
> series) and its worst API-drift debt (11 files written against older versions).

---

## 1. Current State

| Library | Exercises | Lectures | Glossaries | Smoke result |
|---|---|---|---|---|
| NumPy | 28 | 28 | 28 | 24/28 — **4 fail** |
| pandas | **45** | **24** | **24** | 31/45 — **14 fail** |
| Matplotlib | 20 | 20 | 20 | **20/20 ✅** |
| SciPy | 12 | 12 | 12 | **12/12 ✅** |

Matplotlib and SciPy are clean and need only the standard Tier 1 retrofit.

---

## 2. R8 — Resolving the pandas Double Series (do this first)

45 exercises but 24 lectures: two independently-authored series were merged into
one directory. **21 files have no lecture and no glossary.**

### 2.1 The collision

| Prefix | W3Schools series (has lecture) | EXPANSION_PLAN series (**orphaned**) |
|---|---|---|
| 02 | `02-getting-started.py` | `02-inspecting-data.py` |
| 03 | `03-series.py` | `03-indexing-selection.py` |
| 04 | `04-dataframes.py` | `04-filtering.py` |
| 05 | `05-load-data.py` | `05-missing-data.py` |
| 06 | `06-reading-json.py` | `06-data-types.py` |
| 07 | `07-data-viewing.py` | `07-string-methods.py` |
| 08 | `08-data-selecting.py` | `08-datetime.py` |
| 09 | `09-data-loc.py` | `09-groupby-aggregation.py` |
| 10 | `10-data-drop.py` | `10-pivot-tables.py` |
| 11 | `11-rename-columns.py` | `11-merging-joining.py` |
| 12 | `12-iterating.py` | `12-window-functions.py` |
| 13 | `13-clearing-data.py` | `13-apply-map.py` |

Plus orphans with unique prefixes: `14-categorical-data`, `15-io-csv-json`,
`16-io-excel-sql`, `17-data-cleaning`, `18-visualization`, `19-multiindex`,
`20-performance`, `21-styling`, `22-case-study-eda`.

### 2.2 Decision: keep both, renumber into one 34-topic progression

The EXPANSION_PLAN series is **more advanced and more valuable** for AI work
(`20-performance`, `19-multiindex`, `12-window-functions`, `09-groupby-aggregation`).
Deleting it would remove the best pandas content in the module. The W3Schools
series is the gentler on-ramp. Sequence basics → professional.

**Target numbering** (`old → new`):

| New | File | Source | Lecture status |
|---|---|---|---|
| 01 | `01-introduction` | W3 | exists |
| 02 | `02-series` | W3 (`03-series`) | exists, renumber |
| 03 | `03-dataframes` | W3 (`04-dataframes`) | exists, renumber |
| 04 | `04-inspecting-data` | EXP (`02-inspecting-data`) | **author** |
| 05 | `05-load-data-csv` | W3 (`05-load-data`) | exists, renumber |
| 06 | `06-load-json` | W3 (`06-reading-json`) | exists, renumber |
| 07 | `07-data-viewing` | W3 (`07-data-viewing`) | exists, renumber |
| 08 | `08-selecting-basics` | W3 (`08-data-selecting`) | exists, renumber |
| 09 | `09-loc-iloc` | W3 (`09-data-loc`) | exists, renumber |
| 10 | `10-indexing-selection` | EXP (`03-indexing-selection`) | **author** |
| 11 | `11-filtering` | EXP (`04-filtering`) | **author** |
| 12 | `12-dropping-data` | W3 (`10-data-drop`) | exists, renumber |
| 13 | `13-rename-columns` | W3 (`11-rename-columns`) | exists, renumber |
| 14 | `14-new-columns` | W3 (`14-data-new-column`) | exists, renumber |
| 15 | `15-missing-data` | EXP (`05-missing-data`) | **author** |
| 16 | `16-data-types` | EXP (`06-data-types`) | **author** |
| 17 | `17-categorical-data` | EXP (`14-categorical-data`) | **author** |
| 18 | `18-string-methods` | EXP (`07-string-methods`) | **author** |
| 19 | `19-datetime` | EXP (`08-datetime`) | **author** |
| 20 | `20-cleaning-data` | W3 (`13-clearing-data`) | exists, renumber |
| 21 | `21-data-cleaning-advanced` | EXP (`17-data-cleaning`) | **author** |
| 22 | `22-iterating` | W3 (`12-iterating`) | exists, renumber |
| 23 | `23-apply-map` | EXP (`13-apply-map`) | **author** |
| 24 | `24-statistics` | W3 (`15-statistics`) | exists, renumber |
| 25 | `25-groupby-basics` | W3 (`22-groupby`) | exists, renumber |
| 26 | `26-groupby-aggregation` | EXP (`09-groupby-aggregation`) | **author** |
| 27 | `27-pivot-tables` | EXP (`10-pivot-tables`) | **author** |
| 28 | `28-merge` | W3 (`20-merge`) | exists, renumber |
| 29 | `29-concat` | W3 (`21-concat`) | exists, renumber |
| 30 | `30-merging-joining` | EXP (`11-merging-joining`) | **author** |
| 31 | `31-window-functions` | EXP (`12-window-functions`) | **author** |
| 32 | `32-multiindex` | EXP (`19-multiindex`) | **author** |
| 33 | `33-correlation` | W3 (`23-corr`) | exists, renumber |
| 34 | `34-plotting` | W3 (`24-plotting` + `16`–`19` charts) | consolidate |
| 35 | `35-io-formats` | EXP (`15-io-csv-json` + `16-io-excel-sql`) | **author** |
| 36 | `36-performance` | EXP (`20-performance`) | **author** |
| 37 | `37-styling` | EXP (`21-styling`) | **author** |
| 38 | `38-case-study-eda` | EXP (`22-case-study-eda`) | **author** |

**Work:** 38 renames (git mv, preserving history), 17 new lecture+glossary pairs,
lecture renumbering, README rebuild. The chart files `16-scatter-plot`,
`17-histogram`, `18-pie-chart`, `19-bar-chart` fold into `34-plotting` — they
duplicate Matplotlib coverage and pandas plotting deserves one consolidated topic.

**Sequence the renames before any fixes** so R2 patches are applied once, to
final filenames.

---

## 3. NumPy (28 → 34)

### 3.1 Fix 4 failures (R2/R3)
| File | Error | Fix |
|---|---|---|
| `10-array-iterating` | `'ndarray' has no attribute 'index'` | `np.where(arr == v)[0][0]` |
| `12-array-split` | `array split does not result in an equal division` | `np.array_split` |
| `27-ufunc-trigonometric` | `UnicodeEncodeError 'π'` | print `pi` not `π` |
| `28-ufunc-set-operations` | ambiguous truth value | `.any()` / `.all()` |

### 3.2 The real gap
28 files cover the W3Schools NumPy surface (creation, indexing, ufuncs) but miss
what makes NumPy fast — the thing an AI engineer must understand:

| New | Topic | Concepts |
|---|---|---|
| 29 | `29-broadcasting-deep.py` | Broadcasting rules formally; shape alignment; `newaxis`; when it silently allocates; common shape bugs; `(n,)` vs `(n,1)` |
| 30 | `30-vectorization.py` | Loop → vectorized rewrites, measured; `np.where` vs branches; masking; `einsum`; when a loop is unavoidable; `np.vectorize` is *not* fast |
| 31 | `31-memory-and-strides.py` | `strides`; C vs Fortran order; **view vs copy** (extends `07-copy-vs-view`); `ascontiguousarray`; cache locality; `nbytes`; alignment |
| 32 | `32-dtypes-and-precision.py` | float32 vs float64 (memory and speed); overflow and wraparound; `nan`/`inf` propagation; `isclose`; structured dtypes; casting rules; **float16 for inference** |
| 33 | `33-linear-algebra.py` | `matmul`/`@`; `solve` over `inv`; decompositions (LU/QR/SVD/Cholesky); eigen; norms; conditioning; batched matmul; BLAS threading |
| 34 | `34-advanced-indexing.py` | Fancy indexing; boolean masks; `ix_`; `take`/`put`; `argsort`/`argpartition` (**top-k**); `searchsorted`; `unique(return_counts)`; fancy indexing copies |

**AI relevance across all six:** these *are* the mechanics of embeddings.
`33` covers cosine similarity as a matmul; `34` covers `argpartition` for top-k
retrieval in O(n); `32` explains why serving uses float16; `31` explains why a
transposed array is suddenly 10× slower.

---

## 4. pandas (38 after R8 → 44)

Six additions after the restructure:

| New | Topic | Concepts |
|---|---|---|
| 39 | `39-method-chaining.py` | `.pipe`, `.assign`, `.query`; chained vs stepwise; **`SettingWithCopyWarning` explained properly**; `copy=` semantics |
| 40 | `40-memory-optimization.py` | `dtype` downcasting; `category` for low-cardinality strings; `memory_usage(deep=True)`; chunked `read_csv`; sparse; measured before/after on a wide frame |
| 41 | `41-timeseries-advanced.py` | `DatetimeIndex`; `resample` vs `groupby(Grouper)`; `asfreq`; tz-aware series; `shift`/`diff`/`pct_change`; **rolling windows without leakage**; business calendars |
| 42 | `42-groupby-internals.py` | split-apply-combine mechanics; `agg` vs `transform` vs `filter` vs `apply`; named aggregation; multiple functions; performance ordering; why `apply` is the slow path |
| 43 | `43-pandas-for-ml.py` | Feature engineering; train/test split **without leakage**; `get_dummies` vs sklearn encoders; target encoding; time-based splits; pandas → NumPy handoff; `ColumnTransformer` interop |
| 44 | `44-pandas-pitfalls.py` | Chained assignment; index alignment surprises; `inplace=True` is not faster; float equality; `NaN != NaN`; silent dtype upcasting; `iterrows` is O(n) slow; merge cardinality explosions; `copy-on-write` (pandas 3.0) |

`44` is the most valuable pandas file in the plan — every entry is a bug that has
shipped to production somewhere.

---

## 5. Matplotlib (20 → 24) and SciPy (12 → 16)

Both are clean; extend only.

### Matplotlib
| New | Topic |
|---|---|
| 21 | `21-object-oriented-api.py` — `fig, ax` discipline; why `plt.*` state machine breaks in scripts; `GridSpec`; `subplot_mosaic`; shared axes |
| 22 | `22-styling-and-themes.py` — `rcParams`; stylesheets; colormaps (**perceptually uniform, colorblind-safe**); avoid jet; annotation; publication defaults |
| 23 | `23-ml-visualization.py` — learning curves; confusion matrix; ROC/PR curves; residuals; feature importance; embedding scatter (t-SNE/UMAP); attention heatmaps |
| 24 | `24-saving-and-export.py` — `savefig` DPI; vector vs raster; `bbox_inches="tight"`; transparent; **`Agg` backend for headless CI**; figure size and reproducibility |

### SciPy
| New | Topic |
|---|---|
| 13 | `13-statistical-tests.py` — t-test, chi-square, ANOVA, Mann-Whitney, normality; p-values interpreted honestly; multiple-comparison correction; effect size; **the stats behind A/B testing** |
| 14 | `14-optimization-advanced.py` — `minimize` methods; constraints/bounds; least squares; curve fitting; global optimization; convergence diagnostics; gradient-descent relationship |
| 15 | `15-sparse-matrices.py` — CSR/CSC/COO; when sparse wins; sparse matmul; **TF-IDF matrices are sparse**; memory comparison; scipy.sparse → sklearn |
| 16 | `16-distance-and-similarity.py` — `cdist`/`pdist`; cosine/euclidean/manhattan; **why cosine for embeddings**; normalization; KD-trees and their curse-of-dimensionality limit; brute force vs ANN |

`15` and `16` are direct RAG prerequisites.

---

## 6. New: Polars and PyArrow (`03-libraries/polars/`)

Absent entirely; increasingly the professional default for large data.

| # | Topic |
|---|---|
| 01 | `01-introduction.py` — why Polars; Arrow memory model; eager vs lazy |
| 02 | `02-expressions.py` — the expression API; `select`/`with_columns`/`filter`; contexts |
| 03 | `03-lazy-evaluation.py` — `scan_csv`/`scan_parquet`; query plans; `explain`; predicate/projection pushdown |
| 04 | `04-pandas-comparison.py` — side-by-side idioms; **measured** benchmarks; migration guide; when pandas is still right |
| 05 | `05-pyarrow-parquet.py` — Arrow tables; Parquet columnar layout; compression; partitioning; zero-copy to NumPy; why Parquet over CSV for datasets |
| 06 | `06-larger-than-memory.py` — streaming; sinks; batch processing; out-of-core joins |

**AI relevance:** Parquet is the standard dataset format; Arrow is the zero-copy
bridge between pandas/Polars/DuckDB/PyTorch. A 50GB training corpus is not a CSV.

---

## 7. Retrofit All Sections (Tier 1)

`_verify()` for all ~130 files. Library-specific patterns:

```python
# NumPy — shapes, dtypes, values
assert result.shape == (3, 4), "broadcasting must produce (3,4)"
assert result.dtype == np.float32, "must stay float32"
assert np.allclose(result, expected), "values must match within tolerance"
assert arr.base is not None, "slicing must return a view, not a copy"

# pandas — shape, dtypes, index, content
assert df.shape == (100, 5)
assert df["cat"].dtype.name == "category"
assert not df.isna().any().any(), "no NaNs after cleaning"
pd.testing.assert_frame_equal(actual, expected)

# Matplotlib — assert artifacts, never pixels
fig.savefig(out / "plot.png", dpi=100)
assert (out / "plot.png").stat().st_size > 1000
assert len(ax.lines) == 3, "three series must be drawn"
```

**Never** assert on wall-clock time (`np.allclose` tolerance, yes; `elapsed < 0.5s`, no).
Set `MPLBACKEND=Agg` and seed `np.random.default_rng(42)`.

Also add to all lectures: `## Complexity and Cost` (memory is the dominant cost
here) and `## AI Engineering Relevance`.

---

## 8. Deliverables

| Item | Count |
|---|---|
| Failure fixes (R2/R3/R4) | 18 |
| pandas renumbering (R8) | 38 renames |
| New pandas lecture+glossary pairs | 17 |
| New NumPy topics | 6 |
| New pandas topics | 6 |
| New Matplotlib topics | 4 |
| New SciPy topics | 4 |
| New Polars/PyArrow section | 6 |
| New lecture+glossary pairs (non-pandas) | 20 |
| `_verify()` retrofits | ~105 |
| Challenges | ~130 dirs |
| Quizzes | ~20 |

---

## 9. Sequencing

| Step | Work | Notes |
|---|---|---|
| 1 | **R8 pandas renumbering** | Must precede pandas fixes so patches land once |
| 2 | R2/R3/R4 fixes (18 files) | Mechanical |
| 3 | 17 orphaned pandas lecture pairs | Largest authoring block |
| 4 | `_verify()` across ~105 files | Parallelizable by library |
| 5 | NumPy `29`–`34` | Prerequisite for ML/GenAI phases |
| 6 | pandas `39`–`44` | `44-pitfalls` first — highest value |
| 7 | SciPy `15`,`16` | Prerequisite for RAG |
| 8 | Matplotlib `21`–`24` | Independent |
| 9 | Polars/PyArrow | Independent; can be deferred |
| 10 | Challenges + quizzes | After exercises |

---

## 10. Exit Criteria

- [ ] Zero failures across all four libraries (from 18)
- [ ] pandas: one series, unique prefixes, **every file has a lecture** (from 24/45)
- [ ] All ~130 files have passing `_verify()`
- [ ] Every lecture has memory/complexity notes and AI relevance
- [ ] NumPy covers broadcasting, strides, dtypes, linalg, top-k indexing
- [ ] pandas covers chaining, memory, time series, leakage, pitfalls
- [ ] SciPy covers sparse matrices and distance metrics (RAG prerequisites)
- [ ] Matplotlib renders headless with `Agg` in CI
- [ ] `requirements.txt` includes `openpyxl`, `seaborn`, `polars`, `pyarrow`

---

*Phase 3 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Fixes: [10-remediation-backlog.md](10-remediation-backlog.md) R2/R3/R4/R8.*
