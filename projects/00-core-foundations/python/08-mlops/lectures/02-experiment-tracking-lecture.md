# MLOps — 02: Experiment Tracking

## Topic Overview

Experiment tracking is the discipline of recording *every* run's parameters,
metrics, artifacts, and metadata so that you can answer three questions at any
time in the future: **what did we try, how did it do, and what exactly produced
that result?** Without tracking, an ML team's knowledge lives in notebooks,
chat threads, and `final_v2_USE_THIS.py` files — a collectively unreadable
archive where the best model is indistinguishable from the abandoned one.

A tracking system turns training runs into *first-class records*: each run gets
an ID, a set of hyperparameters (the inputs), a set of metrics (the outputs),
and pointers to artifacts (weights, plots, data hashes). The two canonical open
tools are **MLflow** (Python-native, self-hostable, MLflow Tracking Server +
UI) and **Weights & Biases** (hosted, team-oriented dashboards). Both are thin
clients over the same data model: `experiment → run → params/metrics/artifacts`.

Why this matters for an AI engineer: experiment tracking is the *memory* of an
ML system. Hyperparameter search, model selection, promotion decisions, and
postmortems all read from it. It is also the substrate for **model registry**
(next lecture) — you cannot register, stage, or archive a model you have not
tracked. And it is a compliance artifact: "show me every model we considered
and why we chose this one" is a standard audit request.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the `experiment → run → params/metrics/artifacts` data model
2. Log parameters, metrics, and artifacts with MLflow (or W&B) correctly
3. Structure experiments so comparisons are apples-to-apples
4. Tag runs (e.g. `baseline`, `candidate`, `champion`) and filter the UI
5. Recover the exact config and metrics of any past run from its ID
6. Design a naming/tagging convention that scales to 10k+ runs
7. Avoid the classic pitfalls: logging after exceptions, mutating logged params, unlogged seeds

## Prerequisites

| Need | Where |
|---|---|
| Reproducibility & seeds | `08-mlops/lectures/01-reproducibility-lecture.md` |
| Dictionaries & JSON | `01-core-python/` data structures |
| sklearn basics | `07-machine-learning/10-train-test.py` |
| Logging / print discipline | `02-advanced-python/` logging |

## 1. The Experiment Data Model

Everything a tracking system records fits three buckets:

| Bucket | Example | When |
|---|---|---|
| **Parameters** (inputs) | `lr=1e-3`, `n_layers=4`, `seed=42` | logged *before* training |
| **Metrics** (outputs) | `val_loss=0.31`, `val_acc=0.918` | logged *during/after* training |
| **Artifacts** (files) | `model.pt`, `confusion.png`, `data_hash.txt` | logged after checkpointing |

Parameters are logged *before* the run starts; metrics are logged as they are
computed; artifacts are *file paths or objects* that get copied into the
tracking store. The run's **ID** is the join key: given a run ID, you can
reconstruct its full story.

```python
import mlflow

with mlflow.start_run(run_name="lr-grid-1e-3"):
    mlflow.log_param("lr", 1e-3)
    mlflow.log_param("n_layers", 4)
    mlflow.log_param("seed", 42)

    val_loss = 0.312  # in reality: model.fit(...)
    mlflow.log_metric("val_loss", val_loss)
    mlflow.log_metric("val_acc", 0.918)

    mlflow.log_artifact("model.pt")   # copied into the artifact store
```

Output (conceptually):
```
🏃 View run lr-grid-1e-3 at: http://127.0.0.1:5000/#/experiments/1/runs/<id>
```

## 2. Parameters vs Metrics: The Golden Rule

**Log parameters before training, metrics after.** If you log a parameter after
training, the tracking UI cannot filter runs by it during an experiment sweep —
the filter runs at query time, but the parameter never made it into the record.
The subtle rule: a value that is *known before* training (lr, seed, model class)
is a parameter; a value that is *computed during* training (loss, accuracy,
latency) is a metric. A common bug is logging `n_estimators` as a metric
because it was read from the fitted model — log it as a param from the config.

```python
config = {"lr": 1e-3, "seed": 42}
with mlflow.start_run():
    # BEFORE training: params
    mlflow.log_params(config)
    # DURING/AFTER: metrics
    mlflow.log_metric("val_acc", 0.918)
```

Output (conceptually):
```
(params are queryable before/after; metrics plotted over training steps)
```

## 3. Structured Experiments: One Comparison, One Experiment

The UI is only as good as the grouping. Best practice: **one experiment per
question** (e.g. `churn-lr-vs-xgb`), and runs within it differ in exactly the
variable being tested. Tagging adds human meaning:

```python
with mlflow.start_run(experiment_id=1, run_name="xgb-depth-6"):
    mlflow.set_tags({
        "team": "churn",
        "purpose": "depth comparison",
        "dataset_hash": "sha256:c9a3...",
    })
```

Output (conceptually):
```
Tags: {'team': 'churn', 'purpose': 'depth comparison', ...}
```

At 10k runs you survive on **filters over tags/params**, not memory. Every
candidate that could become a champion should carry a `status` tag
(`baseline` / `candidate` / `champion` / `abandoned`).

## 4. Comparing Runs: `mlflow.search_runs`

The real power of tracking is *querying* the past. `search_runs` returns a
pandas DataFrame of runs matching a filter — the raw material for leaderboards
and promotion reports.

```python
df = mlflow.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.val_acc > 0.9",
    order_by=["metrics.val_acc DESC"],
)
print(df[["run_id", "params.lr", "metrics.val_acc"]].head())
```

Output (conceptually):
```
                                  run_id params.lr  metrics.val_acc
0  b3f2a1c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9   0.001            0.918
```

The ability to turn "which of our 300 runs beat the baseline?" into a
one-line query is what separates a tracked team from a notebook team.

## 5. Logging From Inside Training Loops

For deep learning, metrics are logged per step/epoch so the UI can plot
learning curves. MLflow's `log_metric(..., step=n)` appends to a series.

```python
for epoch in range(5):
    train_loss = 1.2 / (epoch + 1)          # mock
    mlflow.log_metric("train_loss", train_loss, step=epoch)
```

Output (conceptually):
```
train_loss: [1.2, 0.6, 0.4, 0.3, 0.24]  (plotted vs step)
```

For sklearn-style training, log a single final metric plus the params, and
always log the **test** metrics separately from **validation** metrics — mixing
them is the #1 cause of "the leaderboard lied" incidents.

## 6. Artifacts and Environment Linkage

Artifacts close the loop back to reproducibility: log the model file, the
confusion matrix, *and* a `run_record.json` produced by the previous lecture's
`RunRecord`, so the tracking entry *points at* its environment and data hash.
This is how you later answer "what trained this champion?" — click the run,
read the artifacts.

```python
mlflow.log_artifact("run_record.json")   # seed + data_hash + env fingerprint
mlflow.log_artifact("confusion_matrix.png")
mlflow.log_artifact("model.pt")
```

Output (conceptually):
```
Artifacts: run_record.json, confusion_matrix.png, model.pt
```

## Every Use Case

- **Hyperparameter sweeps**: grid/random/Bayesian search over 100+ configs, all
  comparable in one dashboard.
- **Model selection**: the leaderboard query (`search_runs` ordered by metric)
  replaces tribal knowledge.
- **Regression detection**: a drop in val_acc between two commits is caught by
  comparing runs' git SHAs (log the git SHA as a param!).
- **Collaboration across a team**: everyone's runs land in one shared server,
  no more "which of these 5 files did you actually run?"
- **Audit and governance**: a complete, queryable history of what was tried and
  why a specific model was chosen.
- **Budget tracking**: total compute per experiment (log `wall_time_s`,
  `gpu_hrs` as metrics) informs where the team's money goes.
- **Notebook hygiene**: `mlflow.autolog()` on sklearn/keras/xgboost captures
  runs automatically during interactive exploration.
- **Debugging**: reproduce a failing run by pulling its exact params and
  artifact set from the tracking server.

## Real-World Use Cases for AI Engineers

- **Credit-scoring team at a bank**: every candidate model is a tracked run
  with the seed, data hash, and validation report as artifacts. When the model
  risk committee asks "why XGBoost over the logistic baseline?", the ML
  engineer pulls the two runs, orders by expected-loss metric, and shows the
  comparison table — a 2-minute query instead of a week of archaeology.
- **E-commerce search ranking**: the team runs nightly candidate generation.
  A Monday regression is traced to Tuesday's training data by filtering
  `params.dataset_hash` and comparing metric series; the guilty run's data
  hash points at the ingestion bug.
- **Autonomous-vehicle simulation team**: each training run logs the exact
  scenario dataset hash and simulator version. Regressions across 5k runs are
  queryable: "all runs on dataset D2 with seed < 1000 dropped 3% accuracy."
- **LLM prompt engineering teams**: tracking isn't just for training — teams
  log prompt templates, model versions, temperature, and eval metrics for each
  evaluation batch, turning prompt iteration into a queryable experiment
  history (a pattern formalized in Phase 9 GenAI).

## Common Mistakes to Avoid

### Mistake 1: Logging parameters after training
```
# WRONG — too late to filter by
model = fit(X, y)
mlflow.log_param("n_estimators", model.n_estimators)
# CORRECT — log from config BEFORE training
mlflow.log_params(config)
```

### Mistake 2: Not logging the seed / data hash
Without them the run is not reproducible — tracking without reproducibility is
an incomplete memory.

### Mistake 3: Logging inside an exception handler
The run stays `RUNNING` forever. Use `mlflow.start_run()` as a context manager
or end the run in a `finally` block.

### Mistake 4: Mixing val and test metrics
The leaderboard will silently rank models by whichever metric was overwritten
last. Keep separate, clearly named metric keys.

### Mistake 5: Mutating the config dict after logging
`mlflow.log_params(config)` followed by `config["lr"] = 1e-4` desyncs the
record from reality. Freeze configs or log a deep copy.

### Mistake 6: One giant experiment with no tagging
At 10k runs, an untagged experiment is unqueryable. Tag every run's purpose.

## Best Practices

1. Log all params *before* training, from the config object
2. Log the git SHA and dataset hash as params on every run
3. Use one experiment per comparison question
4. Tag runs (`baseline`/`candidate`/`champion`) as part of the run lifecycle
5. Log val and test metrics under separate keys
6. Log artifacts (`model.pt`, `run_record.json`, plots) on every run
7. Use `mlflow.autolog()` in notebooks, explicit logging in shipped pipelines
8. Add a `status` tag and a promotion comment when a run becomes champion
9. Freeze config objects before logging
10. Make the tracking server a shared, backed-up infrastructure piece

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Log a param/metric | O(1) | O(1) | batch via `log_params`/`log_metrics` |
| Search 10k runs | O(n) filter | O(1) | pre-filter by experiment + tags |
| Store 10GB of artifacts | O(1) per file | O(10GB) | dedupe by content hash |
| autolog per sklearn fit | O(1) | O(1) | explicit logging in pipelines |

## AI Engineering Relevance

**Where this shows up:** every training run, hyperparameter search, model
selection decision, and promotion review in an ML platform.

| Concept here | Used for |
|---|---|
| Run ID + params | exact reproduction of any past experiment |
| Metric series | learning curves, regression detection |
| Tags | 10k-run-scale filtering and governance |
| Artifacts | model files + reproducibility records linked to the run |

**Scale note:** a team of 10 running 50 experiments/day accumulates ~100k runs
a year. Everything — budgets, governance, promotion — is a query over that
history. Design the schema (params/metrics/tags) for queryability from day one.

## Practice Exercises

### Exercise 1: Log and Query (Easy)
Using a mock tracking dict (no MLflow needed), implement `track(config, metrics)`
that records params-before, metrics-after, and supports `search_runs(filter)`
returning runs whose val_acc exceeds a threshold.

### Exercise 2: Leaderboard Query (Medium)
Given 30 mock runs with `lr`, `seed`, `val_acc`, write `leaderboard(limit=5)`
that returns the top 5 runs by val_acc with their full config — and prove the
ordering is stable under re-insertion.

### Exercise 3: Champion Promotion Audit (Hard)
Simulate the lifecycle: 50 candidate runs → auto-tag top-3 as `candidate` →
promote the best to `champion` with a comment. Write `audit(champion_run_id)`
that returns the full lineage: params, metrics, data hash, and git SHA.

## Summary

| Concept | Description |
|---|---|
| Run | one training execution, identified by an ID |
| Params | inputs logged before training |
| Metrics | outputs logged during/after training |
| Artifacts | files attached to a run (weights, records, plots) |
| Tags | human metadata for filtering at scale |

Experiment tracking turns a team's collective trial-and-error into a queryable,
auditable, shareable history. The teams that win on model quality are not
necessarily the ones that train the most — they are the ones that *remember*
every run precisely and can compare them rigorously.

## Quick Reference

| Task | Idiom |
|---|---|
| Start a run | `with mlflow.start_run(run_name=...):` |
| Log config | `mlflow.log_params(config)` |
| Log a metric | `mlflow.log_metric("val_acc", 0.918)` |
| Attach files | `mlflow.log_artifact("model.pt")` |
| Query history | `mlflow.search_runs(filter_string=...)` |

## Next Steps

Next: **[03 Data Versioning](03-data-versioning-lecture.md)** — versioning the
datasets your experiments consume.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://mlflow.org/docs/latest/tracking.html,
https://docs.wandb.ai/guides/track
