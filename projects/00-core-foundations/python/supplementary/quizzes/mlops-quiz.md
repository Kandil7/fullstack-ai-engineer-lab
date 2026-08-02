# MLOps: Production Machine Learning - Quiz

## Topic Overview
MLOps is the discipline of shipping and operating ML models in production:
reproducibility, experiment tracking, data versioning, model registries,
packaging, Docker, serving, optimization, orchestration, validation,
monitoring, CI/CD, feature stores, A/B testing, and cost management. This
quiz covers the core concepts of the full production lifecycle.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What does reproducibility in ML require pinning?
- **A)** Only the random seed
- **B)** Code, data, and environment (libraries, seeds, platform)
- **C)** Only the dataset path
- **D)** The model architecture

**Correct Answer: B** — Three pillars must be pinned: code (git SHA + diff), data (content hash), and environment (Python/deps versions, seeds). Seeding alone covers none of the other two.

---

### Q2. Why is seeding only Python's `random` a bug?
- **A)** `random` is not deterministic
- **B)** NumPy (and PyTorch/TF) have separate RNG streams that also need seeding
- **C)** Seeding `random` slows training
- **D)** Seeds are not needed in production

**Correct Answer: B** — Python's `random` and NumPy's RNG are independent streams; PyTorch and TensorFlow add more. Seeding only one stream leaves the others nondeterministic, so runs diverge silently.

---

### Q3. What is the correct way to version a dataset?
- **A)** By filename (e.g., `dataset_v2_final.csv`)
- **B)** By a content hash of its bytes
- **C)** By `last_modified` timestamp
- **D)** By who created it

**Correct Answer: B** — A hash of the bytes is unambiguous: two files with the same name but different bytes are different versions. Filenames and timestamps lie; content hashes don't.

---

### Q4. In the DVC model, what lives in Git?
- **A)** The full dataset blobs
- **B)** Small `.dvc` pointer files containing the hash
- **C)** Only the code
- **D)** The object store URL

**Correct Answer: B** — Blobs live in an object store; tiny pointer files (with the hash) live in Git. Git versions the pointers, which lets you `dvc checkout` any historical version.

---

### Q5. What is a model registry's primary purpose?
- **A)** Storing raw datasets
- **B)** The system of record for model versions with lifecycle stages and lineage
- **C)** Running training jobs
- **D)** Serving web traffic

**Correct Answer: B** — The registry tracks versions, stages (staging/production/archived), and lineage, making deployment a deliberate, auditable, reversible act.

---

### Q6. What makes rollback fast in a registry-based deployment?
- **A)** Re-training the old model
- **B)** Promoting the previous version back to production (a pointer flip)
- **C)** Deleting the bad version
- **D)** Restarting the server

**Correct Answer: B** — Serving pulls from the registry's production stage; rollback is a stage transition to the previous version — seconds, not a redeploy.

---

### Q7. What is the #1 packaging mistake?
- **A)** Using the wrong file extension
- **B)** Saving the bare classifier without the preprocessor/scaler
- **C)** Saving too many files
- **D)** Not using cloud storage

**Correct Answer: B** — The preprocessor is part of the model. Saving only the classifier means served inputs arrive unnormalized and predictions silently degrade.

---

### Q8. Why use multi-stage Docker builds for ML?
- **A)** To train faster
- **B)** To keep the serving image small (no compilers/training deps)
- **C)** To use more GPUs
- **D)** To bypass the registry

**Correct Answer: B** — Training images carry compilers + dev deps (2GB+); a multi-stage build copies only the model + runtime into a slim serving image (~400MB), cutting rollout time and risk.

---

### Q9. What is the correct layer order in a Dockerfile for cache efficiency?
- **A)** Code first, dependencies last
- **B)** Dependencies (rarely change) first, then model, then code (most change)
- **C)** Everything in one `RUN`
- **D)** Model first, code last

**Correct Answer: B** — Docker caches layers; putting rarely-changing layers (deps) first means code changes only rebuild the last layer, keeping builds fast.

---

### Q10. What is the most important discipline in model serving?
- **A)** Using the newest framework
- **B)** Loading the model once at startup (never per request)
- **C)** Returning raw exceptions to clients
- **D)** Making endpoints synchronous

**Correct Answer: B** — Model loading is the slowest operation; loading per request destroys latency. Load once at module level/startup and validate inputs with Pydantic.

---

### Q11. What does p99 latency tell you that average doesn't?
- **A)** Nothing
- **B)** The worst-case experience for real users (long-tail requests)
- **C)** The total throughput
- **D)** The model accuracy

**Correct Answer: B** — Averages hide stragglers. p99 (and p95) reveal the long tail that actual users experience; if p99 is 5x p50, something is wrong.

---

### Q12. What is the biggest throughput lever for GPU serving?
- **A)** Buying more CPUs
- **B)** Dynamic batching (multiple requests per GPU batch)
- **C)** Using bigger models
- **D)** Disabling health checks

**Correct Answer: B** — GPUs amortize launch overhead across a batch; a batch of 32 often costs barely more than a batch of 1, multiplying throughput.

---

### Q13. What is the main benefit of orchestration (Prefect/Airflow)?
- **A)** Faster model training
- **B)** Reliable, scheduled, retried, cached, observable pipelines
- **C)** Automatic model tuning
- **D)** Cloud storage

**Correct Answer: B** — Orchestration turns scripts into governed DAGs: retries, caching, scheduling, and audit history are inherited by every pipeline.

---

### Q14. What is data validation's #1 production value?
- **A)** Faster training
- **B)** Catching corrupt/drifted data at pipeline boundaries before it poisons models
- **C)** Reducing storage
- **D)** Improving model accuracy directly

**Correct Answer: B** — Bad data is the #1 cause of silent model degradation. Validation gates at ingest/train/serve boundaries catch corruption before it reaches the model.

---

### Q15. What does PSI (Population Stability Index) measure?
- **A)** Model accuracy over time
- **B)** Shift in a feature's distribution between reference (training) and live data
- **C)** Server CPU usage
- **D)** Cache hit rate

**Correct Answer: B** — PSI measures distribution shift in binned histograms (stable <0.1, watch 0.1-0.25, drift >0.25) — the standard tripwire for input drift.

---

### Q16. What is the "eval gate" in ML CI/CD?
- **A)** A lint check on the code
- **B)** A gate where the candidate model must beat the champion on a frozen eval set
- **C)** A security scan
- **D)** A database check

**Correct Answer: B** — Code CI tests code; ML CI adds the eval gate: the candidate must not regress the frozen champion eval. Without it, "CI green" means nothing for model quality.

---

### Q17. What does a point-in-time join prevent?
- **A)** Slow queries
- **B)** Data leakage (using future feature values in training rows)
- **C)** Duplicate rows
- **D)** Memory errors

**Correct Answer: B** — A training row dated March 1 must use features *as of* March 1. `pd.merge_asof(..., direction="backward")` prevents future information leaking into training.

---

### Q18. What is the primary metric discipline for A/B testing models?
- **A)** Watch the dashboard daily and stop at the first p<0.05
- **B)** Pre-register the metric, sample size, and stopping rule; test once
- **C)** Run until you like the result
- **D)** Test 10 metrics and pick the best one

**Correct Answer: B** — Peeking and multiple comparisons invalidate experiments. Pre-compute the sample size, pre-register one primary metric, and test once at the planned size.

---

### Q19. What is the biggest recurring cost in a mature ML system (usually)?
- **A)** Training compute (one-time per run)
- **B)** Inference (paid on every request, forever)
- **C)** Storage
- **D)** Developer salaries

**Correct Answer: B** — Inference is the permanent bill — every prediction costs money forever. Quantization, batching, and caching (Lecture 8/18) are the recurring-cost levers.

---

### Q20. What does the `RunRecord` tie together?
- **A)** Server logs
- **B)** Seed, data hash, environment fingerprint, and metrics
- **C)** Usernames and passwords
- **D)** Docker images

**Correct Answer: B** — The RunRecord (seed, data hash, env fingerprint, metrics) is the audit trail: given a run ID you can reconstruct exactly what trained a model — the foundation of debugging, audits, and compliance.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | B | 13 | B |
| 4 | B | 14 | B |
| 5 | B | 15 | B |
| 6 | B | 16 | B |
| 7 | B | 17 | B |
| 8 | B | 18 | B |
| 9 | B | 19 | B |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong MLOps knowledge
