# MLOps — 04: Model Registry

## Topic Overview

A model registry is the system of record for models: it stores model versions
with their metadata, manages their **lifecycle stages** (staging, production,
archived), and makes deployment a deliberate, auditable, *reversible* act. If
experiment tracking is a team's *memory* of runs, the registry is the *front
door* of production: it answers "which model is live, what did it replace, and
why?"

The registry sits between training and serving. Training produces a candidate
artifact; the registry accepts it with a version number and metadata (metrics,
data hash, git SHA — see Lectures 01–03); a promotion mechanism moves it from
`staging` to `production`; and serving infrastructure pulls the *registered*
artifact, never an ad-hoc file. Tools: **MLflow Model Registry** (open,
self-hostable), **W&B Registry**, **SageMaker Model Registry**, **Vertex AI
Model Registry**. All implement the same core: versioned model objects with
lifecycle stages and lineage.

Why this matters for an AI engineer: the registry is the enforcement point of
model governance. Without it, "deploy model X" means "copy some file to a
server and hope" — untraceable, unrollbackable, and un-auditable. With it,
every deployment is a recorded transition between stages, and rolling back is
as simple as promoting the previous version again.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the registry data model: model name → versions → lifecycle stages
2. Register a trained model with full metadata (metrics, lineage, signature)
3. Move models through stages (staging → production → archived) with gating
4. Implement promotion rules (metric thresholds, manual approval, shadow test)
5. Roll back a bad production deployment safely and fast
6. Design a registry layout that scales to hundreds of models
7. Wire serving to the registry so deploys are pointer flips, not file copies

## Prerequisites

| Need | Where |
|---|---|
| Experiment tracking | `08-mlops/lectures/02-experiment-tracking-lecture.md` |
| Data versioning | `08-mlops/lectures/03-data-versioning-lecture.md` |
| Reproducibility | `08-mlops/lectures/01-reproducibility-lecture.md` |
| Model packaging | upcoming `08-mlops/lectures/05-model-packaging-lecture.md` |

## 1. The Registry Data Model

A registry organizes models in three levels:

```
Model name (e.g. "churn-predictor")
 └── Version 1  (stage: production)  ← live
 └── Version 2  (stage: staging)     ← being validated
 └── Version 3  (stage: None/registered) ← just trained
```

Each version carries **metadata**: metrics, params, data hash, git SHA, model
signature (input/output schema), and the artifact location. The **stage** is a
controlled transition, not a free-for-all: production transitions should
require evidence (metrics, approval, shadow-test results).

```python
from dataclasses import dataclass, field

@dataclass
class ModelVersion:
    name: str
    version: int
    stage: str = "none"            # none | staging | production | archived
    metrics: dict[str, float] = field(default_factory=dict)
    data_hash: str = ""
    git_sha: str = ""
    artifact_path: str = ""
    notes: str = ""
```

Output (conceptually):
```
ModelVersion(name='churn-predictor', version=1, stage='none', ...)
```

## 2. Registering a Model: The Contract Between Training and Production

Registration is where a training artifact becomes a *governed* object. The
minimal contract: the artifact is immutable, has a version, and carries the
lineage from Lectures 01–03. In MLflow:

```python
import mlflow

with mlflow.start_run():
    # ... train ...
    mlflow.sklearn.log_model(model, "model")
    # register: version the artifact under a model name
    result = mlflow.register_model(
        model_uri="runs:/<RUN_ID>/model",
        name="churn-predictor",
    )
    print("Registered version", result.version)
```

Output (conceptually):
```
Registered version 1
```

**Immutability is the rule**: never overwrite a registered version. Every
change — even a one-line fix — is a new version. That is what makes rollback
possible and audits honest.

## 3. Lifecycle Stages and Transitions

Stages encode intent. The canonical flow:

```
none → staging → production → archived
        (validate)   (deploy)     (retire)
```

Promotion to production should be **gated**: the promotion function checks the
candidate's metrics against the incumbent's, checks it passed validation, and
records the operator's decision. A simple gate:

```python
def promote_to_production(
    candidate: ModelVersion, incumbent: ModelVersion | None
) -> bool:
    """Promotion gate: candidate must beat incumbent on the target metric."""
    if incumbent is None:
        return True
    key = "val_acc"
    return candidate.metrics.get(key, 0.0) >= incumbent.metrics.get(key, 0.0)
```

Output (conceptually):
```
True   (candidate 0.918 >= incumbent 0.902)
```

Real gates add: shadow-test pass, drift threshold, manual approval field, and
a recorded `promoted_by` / `promoted_at` / `reason` — because "why did this
ship?" is a question you will answer in an audit.

## 4. Serving From the Registry: Deploy = Pointer Flip

The registry is not a warehouse; it is the deployment source of truth. Serving
pulls the artifact for the model version in `production` stage — so deploying
v3 means "promote v3 to production", and the serving layer picks it up on its
next poll. Rollback is the same operation in reverse: promote v2 back.

```python
def deployed_artifact(registry: dict, model_name: str) -> str:
    """Return the artifact path of the production version."""
    for v in registry[model_name]:
        if v.stage == "production":
            return v.artifact_path
    raise RuntimeError(f"no production version for {model_name}")
```

Output (conceptually):
```
"s3://ml-artifacts/churn-predictor/1/model.pt"
```

This pattern is what makes **instant rollback** possible: a bad deploy is a
2-second stage transition, not a redeploy-from-source adventure.

## 5. Auditing and Governance

The registry is the audit trail of every model decision. A good audit query:

```python
def audit_model(registry: dict, name: str) -> list[dict]:
    """Full history: every version, its stage, lineage, and promotion notes."""
    return [
        {
            "version": v.version,
            "stage": v.stage,
            "metrics": v.metrics,
            "data_hash": v.data_hash,
            "git_sha": v.git_sha,
            "notes": v.notes,
        }
        for v in sorted(registry[name], key=lambda x: x.version)
    ]
```

Output (conceptually):
```
[{'version': 1, 'stage': 'archived', 'metrics': {'val_acc': 0.902}, ...},
 {'version': 2, 'stage': 'production', 'metrics': {'val_acc': 0.918}, ...}]
```

Regulators and ML-risk teams ask exactly these questions: *which models are in
production, what version, on what data, with what validation evidence, and who
approved the promotion?* The registry answers all of them in one query.

## Every Use Case

- **Production deployment control**: deploys are promoted versions, never
  ad-hoc file copies.
- **Rollback**: a bad release is a stage transition back to the previous
  production version — seconds, not a redeploy.
- **Model governance / compliance**: full version history with lineage and
  approval notes (SR 11-7, GDPR model audits).
- **Multi-environment management**: dev/staging/production stages per version
  keep environments aligned.
- **Shadow and canary testing**: the registry stores shadow-test results next
  to the version, informing the promotion decision.
- **Model retirement**: archiving old versions preserves history without
  serving them.
- **Team handoff**: a new engineer onboards by reading the registry, not by
  hunting through notebooks.
- **Multi-model systems**: RAG pipelines, ensembles, and agent systems register
  each component model/dataset/embedder with its own version and lineage.

## Real-World Use Cases for AI Engineers

- **Banking model lifecycle**: a credit-risk model's every version is
  registered with the validation committee's approval note. When the
  committee retires the model, it is *archived*, not deleted — the regulator
  can still inspect the exact model that was live on a given date.
- **E-commerce ranking**: a promotion candidate must beat the incumbent's
  offline AUC and pass a 24-hour shadow test (serving live traffic without
  affecting users). The registry stores both pieces of evidence; the deploy
  is a pointer flip that a 3-person team performs in under a minute.
- **RAG system upgrades**: the embedding model and the LLM are registered
  separately. Upgrading the embedder is a new version; the retrieval eval
  scores from Lecture 10 (Phase 9) are attached to that version, gating the
  promotion. Rollback to the previous embedder is one stage transition.
- **Healthcare triage**: every production version records its validation
  dataset hash and approval sign-off. The registry's audit query is what the
  hospital's quality board runs quarterly.
- **Startup with 1 ML engineer**: even alone, the registry is the memory that
  lets you answer "which model is live and why did I ship it?" after 6 months
  — and safely roll back without re-reading your own old notebooks.

## Common Mistakes to Avoid

### Mistake 1: Overwriting registered versions
```
# WRONG — destroys history and rollback ability
registry.overwrite("churn-predictor", v1, new_weights)
# CORRECT — new version
registry.register("churn-predictor", new_weights)
```

### Mistake 2: Ungated production promotions
Anyone can push any version to production → untraceable regressions. Gate and
record the decision.

### Mistake 3: Deploying from files instead of the registry
`cp model.pt server:/models/` breaks the audit trail and the rollback story.

### Mistake 4: No lineage in the registry entry
A version without data hash and git SHA is a model without an origin story.

### Mistake 5: Deleting archived versions
Archives are history; deleting them erases the audit trail. Archive, never delete.

### Mistake 6: Versioning by "final" in the name
The registry's version numbers are the source of truth; naming chaos undermines it.

## Best Practices

1. Immutable versions: every change is a new version
2. Gate promotions: metric threshold + validation evidence + recorded reason
3. Serve from the registry, never from ad-hoc files
4. Attach full lineage (metrics, data hash, git SHA) at registration
5. Archive, never delete; preserve the complete history
6. Record who/when/why for every stage transition
7. Attach shadow/canary results to the candidate version
8. Version each component of multi-model systems separately
9. Make the registry part of CI: failing candidates never register as production-ready
10. Test the rollback path in staging before you ever need it in production

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Register a version | O(1) + artifact copy | O(model) | store artifact by content hash |
| Stage transition | O(1) | O(1) | — |
| Audit query | O(versions) | O(1) | index by model name |
| Serve from registry | O(1) pointer read | O(1) | cache the artifact locally |

## AI Engineering Relevance

**Where this shows up:** every deployment, rollback, audit, and model-retirement
decision. The registry is where ML engineering meets production discipline.

| Concept here | Used for |
|---|---|
| Version + stage | controlled, reversible deployments |
| Lineage metadata | audits: what data/code produced this model |
| Promotion gates | prevent unvalidated models from reaching users |
| Deploy = pointer flip | instant rollback and canary rollouts |

**Scale note:** at hundreds of models, manual spreadsheets break. The registry
is the single source of truth that keeps 5 teams from deploying conflicting
versions of the same model name.

## Practice Exercises

### Exercise 1: Register and Promote (Easy)
Implement `register(registry, ModelVersion)` and `promote(registry, name,
version, stage="production")`, then walk a model through none→staging→production.

### Exercise 2: Gated Promotion (Medium)
Extend promotion so a candidate can only reach production if its `val_acc`
beats the incumbent *and* `shadow_pass` is true; return `False` with a reason
otherwise.

### Exercise 3: Rollback Playbook (Hard)
Simulate: v1 in production, v2 promoted (with an incident: `incident=True`),
then rollback to v1. Write `rollback(registry, name, to_version)` that moves
v2 back to `staging` and v1 back to `production`, and assert the serving
function now returns v1's artifact.

### Exercise 4: Audit Report (Medium)
Write `audit_model` that returns the full history sorted by version with stage,
metrics, data hash, and promotion notes — and assert a retried query returns
identical results (determinism).

## Summary

| Concept | Description |
|---|---|
| Model version | immutable, numbered artifact with lineage |
| Stage | none → staging → production → archived |
| Promotion gate | evidence-based transition control |
| Deploy = pointer flip | serve from the registry, roll back in seconds |
| Audit trail | who, when, why, on what data |

The model registry is the enforcement point of ML governance: it makes
deployments deliberate, rollbacks mechanical, and audits a single query. Every
production ML system worth running has one.

## Quick Reference

| Task | Idiom |
|---|---|
| Register model | `mlflow.register_model(runs:/..., name)` |
| Promote | `client.transition_model_version_stage(name, v, "production")` |
| Serve prod | read artifact of the `production` stage version |
| Roll back | promote the previous version back to production |
| Audit | query versions + stage + lineage |

## Next Steps

Next: **[05 Model Packaging](05-model-packaging-lecture.md)** — turning a
registered artifact into a self-contained, deployable unit.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://mlflow.org/docs/latest/model-registry.html,
https://docs.wandb.ai/guides/registry
