# MLOps — 13: Feature Stores

## Topic Overview

A feature store is the shared infrastructure that computes, stores, versions,
and serves **features** — the transformed inputs models consume — in two modes:
**offline** (bulk, historical features for training) and **online** (low-latency
features for serving). Before feature stores, every team re-computed the same
features for every model: ten models, ten copies of "days since last purchase",
ten subtly different implementations, ten drift stories. The feature store is
the fix: one canonical definition, one computation, served both to training and
to serving — eliminating **training-serving skew** at the source.

The canonical open tool is **Feast** (Python-native, offline from the
data warehouse + online from Redis); cloud options are **Databricks Feature
Store**, **SageMaker Feature Store**, **Vertex AI Feature Store**. The core
concepts: **feature views** (grouped feature definitions), **entities**
(join keys — user_id, transaction_id), **point-in-time correctness** (each
training row gets the features *as of its event time*), and the **online vs
offline split**.

Why this matters for an AI engineer: the feature store is where ML engineering
meets data engineering. It is the answer to the two most expensive ML problems:
**skew** (train on features you cannot serve) and **duplication** (every team
re-inventing the same features). Mastering the pattern — one definition, two
serving modes, point-in-time joins — is a core senior skill.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain entities, feature views, and the offline/online split
2. Implement point-in-time correct feature joins (no leakage)
3. Serve features online (low-latency) and offline (bulk training) from one definition
4. Compute features once and reuse them across models
5. Detect and prevent training-serving skew with the store
6. Version features and handle backfills / corrections
7. Compare Feast vs cloud feature stores for a given stack

## Prerequisites

| Need | Where |
|---|---|
| pandas/DataFrames | `03-libraries/pandas/` |
| Data versioning | `08-mlops/lectures/03-data-versioning-lecture.md` |
| Serving | `08-mlops/lectures/07-model-serving-lecture.md` |
| Monitoring/skew | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |
| Time-series basics | `07-machine-learning/` |

## 1. The Problem: Ten Models, Ten Feature Implementations

Without a feature store, each model team hand-rolls features:

```python
# Team A's "days_since_last_purchase"
days = (today - purchases.groupby("user_id")["ts"].max()).dt.days

# Team B's "days_since_last_purchase" — subtly different (weekly agg)
days = (today - purchases.groupby("user_id")["ts"].resample("W").max()).dt.days
```

Output (conceptually):
```
Two teams, two definitions, two models that disagree on the same user.
```

The result: inconsistent models, duplicated computation, and skew between what
training computed and what serving can produce. The feature store replaces
"ten copies" with **one definition, registered once**:

```python
# One canonical definition, in the feature store
@feature_view(entities=["user_id"], ttl="30d", online=True)
def days_since_last_purchase(purchases, now):
    return (now - purchases.groupby("user_id")["ts"].max()).dt.days
```

## 2. The Core Data Model

| Concept | What it is | Example |
|---|---|---|
| **Entity** | the join key of the feature | `user_id`, `transaction_id` |
| **Feature view** | a group of features computed together | `user_activity` view |
| **Offline store** | bulk historical features for training | warehouse / parquet |
| **Online store** | low-latency current features for serving | Redis / DynamoDB |
| **Point-in-time join** | features *as of* each training row's event time | no leakage |

The genius of the split: **one definition, two servings**. Training reads
history from the offline store; serving reads current values from the online
store — both produced by the same feature-view code, so skew is impossible by
construction.

## 3. Point-in-Time Correctness (No Leakage)

The #1 subtle correctness issue in feature engineering: **leakage**. A
training row dated March 1 must use features *as of March 1*, not features
computed with data from March 10. A naive left-join to a feature table that
was computed later silently leaks future information — and the model looks
amazing on validation and collapses in production.

```python
import pandas as pd

def point_in_time_join(events: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    """Join each event to features AS OF the event time — no future leakage."""
    events = events.sort_values("event_ts")
    features = features.sort_values("feature_ts")
    # for each event row, take the latest feature row with feature_ts <= event_ts
    joined = pd.merge_asof(
        events, features,
        left_on="event_ts", right_on="feature_ts",
        by="user_id", direction="backward",
    )
    return joined

# event at 10:00 gets features from ≤10:00, never from 11:00
```

Output (conceptually):
```
event_ts=10:00 → feature_ts=09:59 (the latest available), never 11:00
```

`pd.merge_asof` is the workhorse; the direction is *always* `backward` for
point-in-time. This is the same principle as Lecture 09's idempotency and
Lecture 10's validation: the discipline is *what the row knew at that moment*.

## 4. Offline vs Online: The Two Serving Modes

```python
# OFFLINE — training: bulk historical features
train_df = store.get_historical_features(
    entity_df=training_entities,       # user_id + event_ts per row
    features=["user_activity:days_since_last_purchase", ...],
)

# ONLINE — serving: current values, sub-millisecond
feature_vector = store.get_online_features(
    entity_rows=[{"user_id": 42}],
    features=["user_activity:days_since_last_purchase", ...],
).to_dict()
```

Output (conceptually):
```
offline → DataFrame with 1M rows of historical features
online  → {'days_since_last_purchase': 13} in < 5ms
```

The online path serves from the online store (Redis) — no recomputation, no
table scans at request time. This is why the serving endpoint (Lecture 07)
stays fast even with rich features.

## 5. Preventing Training-Serving Skew by Construction

Skew (Lecture 10/11) is normally a *monitoring* problem. The feature store
makes it a *construction* problem: training and serving consume features from
the *same definitions*. If the definition changes, both paths change together
— no drift window where training used the old code and serving the new.

The residual skew risks become: (a) feature *value* staleness in the online
store (ttl/refresh), and (b) batch vs stream freshness (a feature computed
nightly but the online value is 20h stale). Both are *operational* — monitored
with the same drift tooling as Lecture 11 — rather than definitional.

## 6. Versioning, Backfills, and Corrections

Features change; corrections happen. The store versions definitions and
supports **backfill**: recomputing historical features for a corrected
definition. A corrected feature must be a *new version*, and downstream models
must explicitly opt in — never silently overwrite history that trained models.

```python
# correcting a buggy feature = new version, not overwrite
store.register_feature_view(v2_definition)   # old models keep v1 features
# backfill: recompute history for v2 only
store.backfill(feature_views=["user_activity:v2"], start="2026-01-01")
```

Output (conceptually):
```
v2 backfilled; v1 retained for models already trained on it
```

## Every Use Case

- **Shared features across models**: churn, LTV, and recommendation models
  all consume `user_activity` from one definition.
- **Online/offline parity**: ranking features served online must match what
  training saw — the store guarantees it.
- **Fresh feature computation**: stream/batch pipelines write features once;
  every model reads the same values.
- **Historical backfills**: retraining on corrected features without touching
  the live store.
- **Cross-team reuse**: the platform team owns the store; product teams
  consume features as a service.
- **Regulatory lineage**: a feature's provenance (which code, which source)
  is recorded — audit evidence.
- **Feature experimentation**: A/B a new feature definition without retraining
  existing models.

## Real-World Use Cases for AI Engineers

- **Fintech credit scoring**: the credit team and the fraud team both use
  `user_activity` and `payment_history` feature views. When the payment-data
  source changed, the feature store recomputed *once* and both models
  retrained consistently — the alternative (two teams, two recomputations,
  two drift stories) is the incident the store prevents.
- **E-commerce recommendation**: the ranking model's features (clicks, cart,
  session) are served online from Redis in <5ms. The feature store's
  point-in-time join guarantees the offline training rows used the same
  feature values *as of* the event — no more "models that score 0.99 offline
  and collapse online".
- **Ride-hailing pricing**: surge features are computed per-city, stored
  online, and served in the pricing call path. The feature store's online
  latency budget is the pricing SLA — the team tunes the store, not the model.
- **Streaming fraud (Phase 9 synergy)**: real-time features (transaction
  velocity) written from a stream and served online; batch equivalents for
  training — the store unifies both.
- **Platform team**: 15 product teams consume the same feature store; the
  platform team's leverage is one well-governed store, not 15 feature pipelines.

## Common Mistakes to Avoid

### Mistake 1: Naive joins that leak the future
```
# WRONG — uses features from AFTER the event time
merged = events.merge(feature_table, on="user_id")   # future leakage!
# CORRECT — point-in-time join
pd.merge_asof(events, features, direction="backward", ...)
```

### Mistake 2: One giant feature table per model
Duplication returns; the store exists to share, not to copy.

### Mistake 3: Ignoring online-store freshness (ttl)
A 20h-stale online feature is silent skew. Monitor freshness.

### Mistake 4: Overwriting feature history
Corrections are new versions + backfills; overwriting history silently
retrains nothing but breaks lineage.

### Mistake 5: Not versioning the feature definition
Unversioned definitions drift; the store must version them like code.

### Mistake 6: Computing features inside the serving path
Recompute-per-request destroys latency; the online store is precomputed.

## Best Practices

1. One definition per feature; register once, consume everywhere
2. Always join point-in-time (backward direction) for training
3. Serve online from the online store, not by recomputation
4. Version feature definitions; corrections = new versions + backfill
5. Monitor online-store freshness and value drift
6. Use the store for train/serve parity by construction
7. Record feature provenance for lineage and audits
8. Batch + stream writers feed one store; readers never write
9. Set explicit TTLs per feature
10. Backfill into a new version, never into live history

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Point-in-time join (1M rows) | seconds | O(n) | index by entity + ts |
| Online lookup | <5ms | O(features) | Redis hash by entity key |
| Backfill | O(history) | O(n) | incremental backfill by window |
| Streaming write | per-event | O(events) | micro-batch |

## AI Engineering Relevance

**Where this shows up:** every model with shared or temporal features; every
system where train/serve parity matters — which is most production ML.

| Concept here | Used for |
|---|---|
| One definition, two servings | skew-free parity |
| Point-in-time joins | leakage-free training |
| Online store | low-latency serving with rich features |
| Feature versioning | safe corrections and backfills |

**Scale note:** at 100M entities, the online store must serve sub-ms lookups
(Redis/DynamoDB keyed by entity); the offline store is a data-warehouse-scale
join problem. The store's value compounds with *model count* — ten models
sharing one store is ten times the leverage.

## Practice Exercises

### Exercise 1: Point-in-Time Join (Medium)
Build `point_in_time_join(events, features)` with `merge_asof` and assert: an
event at 10:00 never receives a feature timestamped after 10:00.

### Exercise 2: Offline/Online Parity (Medium)
Write `feature_view(fn)` that registers a function and exposes
`get_offline(entities)` and `get_online(entity)` both calling the same
definition; assert both return identical values for the same entity/time.

### Exercise 3: Backfill as New Version (Hard)
Simulate a feature correction: v1 has a bug, v2 fixes it. Implement
`backfill_as_new_version(store, view, version, window)` that computes v2
history while leaving v1 intact, and assert models trained on v1 still resolve
v1 features.

### Exercise 4: Freshness Monitor (Medium)
Write `check_freshness(online_store, max_age)` that flags features whose
stored value is older than `max_age` — the operational guard against silent
staleness.

## Summary

| Concept | Description |
|---|---|
| Entity | the join key of features |
| Feature view | one canonical definition |
| Offline store | bulk history for training |
| Online store | sub-ms current values for serving |
| Point-in-time | leakage-free, skew-free joins |

The feature store is the infrastructure that makes features *shared, correct,
and skew-free*: one definition serves both training and serving, joins are
point-in-time by construction, and versions protect history. It is the answer
to the two most expensive ML problems — duplication and skew.

## Quick Reference

| Task | Idiom |
|---|---|
| Define feature | `@feature_view(entities=[...], online=True)` |
| Training features | `store.get_historical_features(entity_df, features)` |
| Serving features | `store.get_online_features(rows, features)` |
| Correct a feature | new version + backfill, never overwrite |
| Monitor | freshness + drift on online values |

## Next Steps

Next: **[14 A/B Testing Models](14-ab-testing-models-lecture.md)** — proving a
new model wins in production, not just offline.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://docs.feast.dev/, https://www.featurestore.org/
