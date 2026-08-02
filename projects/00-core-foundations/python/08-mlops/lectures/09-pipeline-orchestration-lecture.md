# MLOps — 09: Pipeline Orchestration

## Topic Overview

Pipeline orchestration is the discipline of running ML workflows — data
ingestion → preprocessing → training → evaluation → registration → deployment —
as **reliable, scheduled, observable systems** rather than scripts run by hand.
An ML pipeline is a DAG of steps with dependencies, retries, caching, and
scheduling; orchestration is the software that runs that DAG, exactly once,
in the right order, with failure recovery.

The two dominant open tools are **Prefect** and **Airflow**. Prefect is
Python-native and delightful for ML (dynamic DAGs, `@task`/`@flow`
decorators); Airflow is the industry-standard batch orchestrator (static
DAGs defined in Python, scheduler + workers + UI). **Kubeflow Pipelines**
and **Dagster** are the ML-native alternatives. All share the core concepts:
**tasks** (units of work), **flows/DAGs** (dependency graphs), **runs**
(executions with state), **retries** (auto-retry on failure), **caching**
(skip unchanged steps), and **scheduling** (cron/event triggers).

Why this matters for an AI engineer: orchestration is what turns "retraining"
from a manual ritual into a governed, repeatable system — with audit history,
failure alerts, and incremental execution. It is also the integration point
with the reproducibility contract: every pipeline run should produce a
`RunRecord` (Lecture 01).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Model an ML workflow as a DAG of tasks with dependencies
2. Define a Prefect flow with retries, caching, and scheduling
3. Distinguish Airflow (static DAG, scheduler) vs Prefect (dynamic, Python-native)
4. Make tasks idempotent and safely retryable
5. Cache intermediate steps so unchanged work is skipped
6. Handle failures: retries, backoff, alerting, dead-letter paths
7. Track pipeline runs and their artifacts for audit
8. Wire pipeline outputs into the model registry

## Prerequisites

| Need | Where |
|---|---|
| Reproducibility | `08-mlops/lectures/01-reproducibility-lecture.md` |
| Experiment tracking | `08-mlops/lectures/02-experiment-tracking-lecture.md` |
| Model registry | `08-mlops/lectures/04-model-registry-lecture.md` |
| Python functions/decorators | `01-core-python/`, `02-advanced-python/` |

## 1. The ML Pipeline as a DAG

An ML workflow decomposes into steps with clear dependencies:

```
ingest → validate → preprocess → split → train → evaluate → register → deploy
                 ↘            ↘
                (data hash)  (train on val split)
```

Each step is a **task**: a pure-ish function of its inputs with a defined
output. The DAG is the dependency graph; orchestration executes it respecting
order, in parallel where independent, and with state tracked per task.

```python
# conceptual task graph (Prefect-style)
@task
def ingest() -> str:
    return "data/raw/2026-08-02.csv"

@task
def preprocess(raw_path: str) -> str:
    return f"{raw_path}.clean.parquet"

@task
def train(clean_path: str) -> str:
    return "model/artifacts/churn-v3.pkl"

# flow wires the dependencies
flow = ingest() >> preprocess >> train  # conceptual
```

Output (conceptually):
```
Flow run 'ingest → preprocess → train' completed in 4m 12s
```

## 2. Prefect: Python-Native Orchestration

Prefect decorates Python functions with `@task` and `@flow`; the orchestrator
tracks state, retries, and caching. Retries are declared per task; caching
declares that a task whose inputs are unchanged should be skipped.

```python
from prefect import flow, task

@task(retries=2, retry_delay_seconds=10, cache_policy=None)
def ingest(url: str) -> str:
    # idempotent: downloading the same source twice yields the same file
    return "data/raw/dataset.csv"

@flow(log_prints=True)
def train_pipeline(source_url: str) -> str:
    raw = ingest(source_url)
    clean = preprocess(raw)          # also a @task
    model_path = train(clean)
    return model_path

if __name__ == "__main__":
    train_pipeline("s3://bucket/source.csv")
```

Output (conceptually):
```
14:01:02.012 INFO  Flow run 'train_pipeline' started
14:01:12.445 INFO  Task 'ingest' completed in 10.4s
14:01:42.119 INFO  Task 'preprocess' completed in 29.6s
14:02:11.903 INFO  Task 'train' completed in 29.7s
14:02:12.001 INFO  Flow run 'train_pipeline' finished in state Completed()
```

**Idempotency is the foundation**: a task is retryable only if running it twice
produces the same result. Downloads overwrite to a stable path; writes go to
content-addressed paths; side effects (DB inserts) are upserts, not raw
appends.

## 3. Airflow: The Industry Batch Standard

Airflow defines **static DAGs** in Python; a scheduler parses them and
distributes tasks to workers. It is heavier but battle-tested for enterprise
batch schedules.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    dag_id="churn_retrain",
    schedule="0 2 * * *",              # daily at 02:00
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    t_ingest = PythonOperator(task_id="ingest", python_callable=ingest)
    t_preprocess = PythonOperator(task_id="preprocess", python_callable=preprocess)
    t_train = PythonOperator(task_id="train", python_callable=train)

    t_ingest >> t_preprocess >> t_train
```

Output (conceptually):
```
DAG churn_retrain scheduled daily at 02:00 — each task a UI-visible state.
```

**Choice guide:** Airflow when the org already runs it and schedules are
stable/cron-like; Prefect when you want Python-native dynamic pipelines and
tight ML integration; Dagster when asset-awareness (data/feature lineage) is
the priority.

## 4. Caching and Incremental Execution

The killer feature of orchestration: **skip work that didn't change**. If the
raw data hash is unchanged, the preprocess task should not re-run — it should
return its cached result. This turns a 4-hour retraining into a 10-minute job
on unchanged days.

```python
@task
def preprocess(raw_path: str) -> str:
    # cached by input identity: if raw_path's content hash is unchanged,
    # the orchestrator returns the previous result without re-running
    return "data/clean/2026-08-02.parquet"
```

Output (conceptually):
```
Task 'preprocess' Cached — using previous result (inputs unchanged)
```

Cache keys must be derived from *content*, not timestamps — the
content-addressing from Lecture 03 is exactly the right key.

## 5. Failure Handling: Retries, Backoff, Alerting

Production pipelines fail — network blips, quota exhaustion, data surprises.
The design goal is *automatic recovery where safe, human alerting where not*.

```python
@task(retries=3, retry_delay_seconds=30)
def ingest(url: str) -> str:
    # transient network errors auto-retry with backoff
    ...

@task
def validate(df_path: str) -> bool:
    if not schema_ok(df_path):
        raise ValueError("schema violation")   # NOT retryable — data problem
```

Output (conceptually):
```
retry 1 after 30s... retry 2 after 60s... succeeded
```

**Rule:** retry *transient* failures (network, 429, timeout); do NOT retry
*permanent* failures (schema violation, bad config) — they fail forever and
burn budget. Alerts route to the owning team with the run ID.

## 6. Pipeline Runs as Audit Records

Every orchestrated run produces state — the orchestrator's run history is
itself the operational audit trail. The AI-engineer discipline: each run
also emits a `RunRecord` (seed, data hash, metrics, artifact paths) into the
tracking system, linking the run to the model registry entry.

```python
@task
def record_run(data_hash: str, metrics: dict) -> None:
    # write RunRecord JSON into MLflow/W&B (Lecture 02)
    import json
    json.dump({"data_hash": data_hash, "metrics": metrics},
              open("outputs/run_record.json", "w"))
```

Output (conceptually):
```
RunRecord written: seed=42 data_hash=sha256:c9a3... metrics={...}
```

This is how "which run produced this production model?" becomes a
one-query answer: orchestrator run history + registry lineage + tracking
records all point at each other.

## Every Use Case

- **Scheduled retraining**: nightly/weekly retrain on fresh data with
  automatic promotion gates.
- **Feature pipelines**: scheduled feature computation feeding a feature store.
- **Data ingestion**: cron-driven pulls from APIs/DBs with validation gates.
- **Model validation & gating**: every candidate run through eval + fairness +
  drift checks before registry promotion.
- **Batch scoring**: nightly scoring of large cohorts (Lecture 07 batch path).
- **Experimentation pipelines**: same DAG, parameterized runs for sweeps.
- **Data science self-service**: analysts trigger flows with params via UI/API.
- **Disaster recovery**: replay any historical run from its inputs.

## Real-World Use Cases for AI Engineers

- **Fintech nightly retrain**: a Prefect flow ingests transactions, validates
  schema (dead-lettering bad rows), trains, evaluates, and — only if the
  candidate beats the incumbent on the golden eval — registers a new model
  version. The promotion gate lives *in the pipeline*, not in a human's
  head. Failures page the on-call engineer with the run ID.
- **E-commerce feature freshness**: a feature pipeline recomputes daily
  user-session features; caching means unchanged sources skip recomputation,
  cutting a 6-hour job to 40 minutes on quiet days — and the feature store
  always serves fresh-enough data.
- **RAG ingestion pipeline (Phase 9)**: document ingestion → chunking →
  embedding → index update runs on a schedule; incremental runs only re-embed
  *changed documents* (content hashes from Lecture 03), keeping index-update
  cost proportional to change, not corpus size.
- **ML platform team**: hundreds of models, one shared orchestration layer —
  retries, caching, and audit history are inherited, not re-implemented per
  model.
- **Startup ML ops**: one engineer runs the whole lifecycle as scheduled
  flows; the UI's run history is the de-facto "what happened in production"
  log that board reviews read.

## Common Mistakes to Avoid

### Mistake 1: Non-idempotent tasks
```
# WRONG — append duplicates on retry
open("events.csv", "a").write(rows)
# CORRECT — upsert or write to a content-addressed path
```

### Mistake 2: Retrying permanent failures
Schema violations fail forever; retries burn budget and mask the alert. Classify
failures: transient → retry, permanent → alert immediately.

### Mistake 3: Cache keys based on timestamps
`cache_key=now()` defeats caching. Key on content hashes.

### Mistake 4: Giant monolithic tasks
One task doing ingest+clean+train+deploy is un-retryable and un-cacheable.
Split into a DAG.

### Mistake 5: No alerts on permanent failure
A pipeline that fails silently at 2am is a model serving stale data. Alert with
run IDs.

### Mistake 6: Side effects hidden in tasks
A task that both trains and pushes to the registry is a side-effect trap —
push only on explicit promotion steps.

## Best Practices

1. Model workflows as DAGs of small, focused tasks
2. Make every task idempotent (safe to run twice)
3. Cache by content hash, skip unchanged work
4. Retry transient failures with backoff; alert immediately on permanent ones
5. Emit a `RunRecord` per pipeline run linking to tracking + registry
6. Put promotion gates inside the pipeline, not in human rituals
7. Log run IDs everywhere for cross-referencing
8. Parameterize flows (config via inputs) for sweeps and reuse
9. Keep deploy as an explicit, gated step — never a hidden side effect
10. Choose Prefect/Airflow/Dagster by team context, not hype

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Run a 4h pipeline | 4h | O(artifacts) | caching unchanged steps |
| Re-run unchanged day | minutes | O(1) | cache + skip |
| Retry a task | retry_delay | O(1) | classify failures first |
| Parallel independent tasks | max(task times) | O(n tasks) | parallelize the DAG |

## AI Engineering Relevance

**Where this shows up:** every scheduled retrain, feature computation, eval
gate, and batch job. Orchestration is the operating system of ML systems.

| Concept here | Used for |
|---|---|
| DAG + tasks | governed, repeatable workflows |
| Retries/idempotency | reliable unattended execution |
| Caching | incremental execution at scale |
| Promotion gates | validation before registry promotion |

**Scale note:** at hundreds of pipelines, the orchestration layer's audit
history, caching, and retries are what let 5 engineers operate what would
otherwise be 50 hand-run scripts. Everything runs exactly once, with a
record of every run.

## Practice Exercises

### Exercise 1: Model a DAG (Easy)
Given ingest/preprocess/train/evaluate/register/deploy tasks, draw the
dependency DAG and state which steps can run in parallel.

### Exercise 2: Idempotency Audit (Medium)
Write `is_idempotent(fn, input)` that runs a function twice and returns True
if the second run's observable effects (file contents, DB rows) match the
first — test it against an append and an upsert version.

### Exercise 3: Retry Classifier (Medium)
Implement `run_with_policy(fn, transient_types)` that retries only
`transient_types` exceptions with backoff and raises immediately on permanent
ones; test with a network-error and a schema-error fake.

### Exercise 4: Pipeline-to-Registry Wiring (Hard)
Build a mock 4-task pipeline (ingest → preprocess → train → register) where
the register task only promotes if the eval metric beats the incumbent; assert
that a failing candidate never reaches the registry's production stage.

## Summary

| Concept | Description |
|---|---|
| DAG | the workflow's dependency graph |
| Task | a unit of work, idempotent, retryable |
| Run | one execution with tracked state |
| Caching | skip unchanged work |
| Promotion gate | validation inside the pipeline |

Orchestration turns ML from manual ritual into governed system: retries,
caching, scheduling, and audit history are inherited by every pipeline. The
AI engineer who masters orchestration stops babysitting training runs and
starts operating an ML platform.

## Quick Reference

| Task | Idiom |
|---|---|
| Define a task | `@task(retries=2)` |
| Define a flow | `@flow` wiring `task()` calls |
| Schedule | `schedule="0 2 * * *"` (cron) |
| Cache | key on content hashes, not timestamps |
| Retry policy | transient → retry, permanent → alert |

## Next Steps

Next: **[10 Data Validation](10-data-validation-lecture.md)** — validating data
at the pipeline boundaries where silent corruption happens.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://docs.prefect.io/, https://airflow.apache.org/docs/
