# MLOps Engineer — Interview Questions

A senior-level interview bank covering the Phase 8 MLOps curriculum. Each
question includes the ideal answer's key points and a follow-up.

## Foundational

### 1. "Walk me through how you'd make a training run reproducible."
**Key points:**
- Seed every RNG stream once (Python `random`, NumPy, PyTorch/TF) at process start
- Pin code (git SHA + dirty flag), data (content hash), environment (lockfile + Python version)
- Build a `RunRecord` linking seed, data hash, env fingerprint, metrics
- Verify: two runs with the same seed produce identical results (a CI gate)
- Use committed split-index files so splits survive data growth

**Follow-up:** How do you make *distributed* training reproducible? (Seed inside each worker's init — parent seeds don't reach workers.)

### 2. "What's the difference between a parameter and a metric in experiment tracking?"
**Key points:**
- Parameters: inputs known *before* training (lr, seed, config) — logged before the run
- Metrics: outputs computed *during* training (loss, accuracy) — logged during/after
- Filtering/leaderboards only work if params were logged before
- Always log git SHA + data hash as params for reproducibility

**Follow-up:** How would you structure experiments so 10k runs stay queryable? (One experiment per comparison question; tags: baseline/candidate/champion.)

### 3. "How is data versioning different from code versioning?"
**Key points:**
- Filenames/timestamps lie; content hashes are identity (sha256 of bytes)
- DVC model: blobs in object store, pointers in Git
- Provenance = the recipe: raw sources + transform git SHA + config + seed
- Version splits and fitted preprocessors (silent-drift protection)
- Diff between versions + human changelog

**Follow-up:** Why not just store data in Git? (History bloat, slow checkouts; pointers keep Git small.)

## Serving & Production

### 4. "How would you serve a model at 5k QPS with p99 < 50ms?"
**Key points:**
- Load model once at startup; validate inputs with Pydantic
- Profile: is the bottleneck model compute, preprocessing, or I/O?
- ONNX export + FP16/INT8 quantization (golden-test validated)
- Dynamic batching on GPU; response caching for repeated inputs
- Right-size instances; health checks; gateway for auth + canary

**Follow-up:** When would you switch from a FastAPI DIY server to Triton/KServe? (GPU utilization, multi-model, or platform-native needs.)

### 5. "What's the difference between a model registry and experiment tracking?"
**Key points:**
- Tracking: records every run (params/metrics/artifacts) — the memory
- Registry: the system of record for *governed* model versions with lifecycle stages (none/staging/production/archived) and lineage
- Deploy = promote a registry version; rollback = promote the previous version
- Registration carries the lineage from tracking (metrics, data hash, git SHA)

**Follow-up:** What gates a promotion to production? (Metric beats incumbent on frozen eval + validation evidence + recorded operator reason.)

### 6. "A model works in the notebook but collapses in production. Diagnose."
**Key points:**
- Check packaging: was the preprocessor/scaler packaged with the model?
- Check feature order/schema at serving vs training (signature validation)
- Check env drift: different library versions in serving container
- Check training-serving skew: live feature distributions vs training stats
- Check the frozen eval gate: was the candidate ever measured on the right set?

**Follow-up:** How do you detect skew *before* users complain? (Serving-input validation + monitoring PSI/drift + delayed-label feedback.)

## Monitoring & Operations

### 7. "How do you monitor a model when ground truth is delayed?"
**Key points:**
- Instrument every prediction (trace_id, features/hash, proba, latency)
- Proxy signals: input drift (PSI/KL), prediction drift (output distribution)
- Delayed labels: join real outcomes to earlier predictions → realized precision/recall
- Alert on sustained windows (3-of-5) with severity escalation
- Triage: is it drift, a business change, or a model regression?

**Follow-up:** When would you retrain vs roll back? (Roll back if the regression is the new version; retrain if the world changed — drift is a data problem.)

### 8. "What does the eval gate in ML CI/CD actually check?"
**Key points:**
- Candidate model must beat the champion on a *frozen* eval set (never its own training split)
- CI runs: lint/type/unit (code) + data validation (schema/stats) + golden-output tests
- DVC pulls the pinned data version so numbers are comparable
- Nightly heavy eval; fast subset in PRs
- Promotion: staging → shadow → canary → production, all recorded

**Follow-up:** Why gate on a frozen eval set rather than the candidate's val split? (The candidate would referee its own game — its own split is untrusted.)

### 9. "What is a point-in-time join and why does it matter?"
**Key points:**
- Each training row gets features *as of its event time* — no future data
- `pd.merge_asof(..., direction="backward")` on (entity, event_ts)
- Prevents leakage: a model that "scores 0.99 offline" but collapses in production is usually leaking
- Feature stores (Feast) enforce this by construction; versions protect history

**Follow-up:** What's the difference between online and offline features in a feature store? (Offline = bulk history for training; online = sub-ms current values for serving; one definition, two servings = skew-free.)

### 10. "How do you A/B test a new model without fooling yourself?"
**Key points:**
- Pre-register: primary metric, allocation, sample size (from baseline + min effect), stopping rule
- Sample-size math first (power 0.8, alpha 0.05) — underpowered tests prove nothing
- Chi-squared for rates, t-test for means; test once at the planned size
- Guardrail metrics (latency, error rate, secondary outcomes)
- Stratify to catch Simpson's paradox; record the verdict in the registry

**Follow-up:** What's the peeking problem? (Stopping at the first p<0.05 you see inflates the false-positive rate far above 5%.)

## Cost & Architecture

### 11. "Where does ML cost actually go, and what do you do about it?"
**Key points:**
- Three pillars: training (GPU hours × runs), storage (version history), inference (per-request, forever)
- Measure unit costs first; apply the biggest lever
- Training: spot instances, caching unchanged steps, early stopping, experiment caps
- Storage: content-hash dedup, cold-store archives
- Inference: quantization, batching, caching — the *permanent* bill
- Budget + alert per model; log cost as a metric per run

**Follow-up:** When is local/hosted not a "better/worse" question? (It's a measured trade: quality (eval), unit cost (math), latency, privacy, ops burden — recomputed as volume changes.)

### 12. "Design an end-to-end ML platform for 20 teams."
**Key points:**
- Shared stations: tracking, registry, feature store, serving, monitoring, CI templates
- Reproducibility first: run records, data versioning, pinned envs
- Eval gates as the quality bar; promotion = pipeline decision, recorded
- Docker images as the deploy unit; registry as the deploy catalog
- Cost: per-team attribution, budgets, alerts
- The assembly line is the product — teams get the discipline by using the platform

**Follow-up:** What's the weakest link in most platforms? (Monitoring/delayed-label feedback and eval-set freshness are usually the last stations wired and the first to rot.)
