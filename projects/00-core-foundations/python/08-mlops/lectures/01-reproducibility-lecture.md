# MLOps — 01: Reproducibility

## Topic Overview

Reproducibility is the property that a training run — given the same code, the
same data, and the same environment — produces byte-identical results. It is
the load-bearing foundation of every other MLOps practice: you cannot debug,
audit, compare, or ship a model you cannot reproduce. "It worked on my machine"
is not a result; it is an incident waiting to happen, because a model that
trains to different numbers each run is effectively a *different model* each
run, and a production system cannot reason about a moving target.

Three things must be pinned for a run to be reproducible: **code** (the exact
commit and working-tree state), **data** (the exact bytes that fed training),
and **environment** (library versions, Python version, OS, CPU/GPU
architecture, and every random seed). In a single-person prototype you can get
away with pinning none of them; in a team of fifty engineers shipping to
millions of users, every one of these becomes a production question. Model
governance, compliance audits (GDPR Article 22, model risk management under
SR 11-7 in banking), incident postmortems, and A/B rollout decisions all begin
with the question: *what exactly trained this model?*

Modern ML practice treats reproducibility as **content addressing**: every
artifact (dataset, feature vector, model weights, evaluation report) gets an
identity derived from its bytes. Identities are cheap to compute, impossible to
fake, and make collaboration and audit trail automatic. The tools that
institutionalize this — DVC, MLflow, W&B, Git LFS, Hugging Face Hub — are all
thin wrappers over the same idea: *hash the bytes, record the links.*

## Learning Objectives

By the end of this lecture, you will be able to:
1. Seed every RNG (Python `random`, NumPy, PyTorch, TensorFlow) once at process start
2. Capture a full environment fingerprint (Python version, platform, dependencies)
3. Hash dataset content for content-addressed versioning
4. Build a `RunRecord` linking seed, data hash, environment, and metrics
5. Diagnose a "works on my machine" failure from its root causes
6. Design a deterministic split / augmentation strategy that survives team collaboration
7. Write a CI gate that fails when a run is not reproducible
8. Explain the regulatory and business reasons reproducibility is mandatory in production

## Prerequisites

| Need | Where |
|---|---|
| Python `random` module | `01-core-python/09-strings.py`, `01-core-python/10-strings.py` |
| NumPy basics and RNG | `03-libraries/numpy/01-introduction.py`, `03-libraries/numpy/03-array-operations.py` |
| Git fundamentals | `00-core-foundations/git-linux/` |
| Hashing basics | `01-core-python/` dictionary and bytes sections |

## 1. The Three Pillars: Code, Data, Environment

A reproducible run pins three independent axes. Each axis failing alone is
enough to break reproducibility, and they fail in different ways.

| Pillar | What must be pinned | Typical failure |
|---|---|---|
| **Code** | commit SHA, working-tree diff, entrypoint | "works on my machine" — stale checkout |
| **Data** | exact bytes: source files, preprocessing transforms, split indices | silently regenerated / resampled dataset |
| **Environment** | Python version, all pip deps with pins, OS, seed | numpy 2.x lands, results shift |

In practice this means a `RunRecord` carries: `git_sha`, `git_dirty: bool`,
`data_hash`, `split_seed`, `python_version`, `platform`, and a pinned
`requirements.txt` fingerprint (hash of the lockfile itself).

## 2. Seed Discipline

Every stochastic operation — shuffling, sampling, weight initialization,
dropout, augmentation, distributed data sharding — draws from a pseudo-random
stream. If the stream is not seeded, it starts from fresh entropy each process,
so two runs diverge at the *first* stochastic op. Python's `random`, NumPy's
RNG, PyTorch's CUDA RNG, and TensorFlow's global seed are **separate streams**:
seeding only one is a subtle bug that silently reproduces across *some* runs
and not others.

```python
import random
import numpy as np

random.seed(42)      # python stream
np.random.seed(42)   # numpy stream — a DIFFERENT stream

# PyTorch (if installed):
# torch.manual_seed(42)          # CPU + CUDA
# torch.cuda.manual_seed_all(42) # multi-GPU

# TensorFlow (if installed):
# tf.random.set_seed(42)
```

Output (conceptually):
```
# Both streams are now pinned; every downstream draw is deterministic.
```

**The one-call rule:** seed once at the top of the pipeline, before any data
loading, so that every downstream draw — including ones you did not write
yourself (sklearn's internal RNGs are driven by NumPy's global stream) — is
covered. Re-seeding *inside* a loop is the classic bug: it collapses every fold
of cross-validation onto the same split.

```python
def seed_all(seed: int = 42) -> None:
    """Pin every RNG stream exactly once, at process start."""
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass
```

## 3. Environment Capture

A run record must answer: *what code, what data, what libraries, what seed?*
The environment fingerprint captures the runtime so a broken run can be
reconstructed. In practice this is a **lockfile** (exact pins) plus a captured
environment dict. Ranges like `numpy>=1.24` are a reproducibility lie — `>=`
admits any future release.

```python
import platform
import sys
import hashlib

def environment_fingerprint(lockfile_path: str) -> dict[str, str]:
    """Capture a minimal but sufficient environment fingerprint."""
    with open(lockfile_path, "rb") as fh:
        lockfile_hash = hashlib.sha256(fh.read()).hexdigest()[:16]
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "lockfile_sha256": lockfile_hash,
    }
```

Output (conceptually):
```
{'python_version': '3.11.4', 'platform': 'Windows-11-10.0.22631',
 'machine': 'AMD64', 'lockfile_sha256': '9f2c1b7a...'}
```

## 4. Content-Addressed Data Versioning

Version datasets by a hash of their bytes, never by filename or
`last_modified`. Two files with the same name but different bytes are different
versions; the hash makes that unambiguous and deduplication automatic. For
large files, hash in **chunks** so you never load the whole file into memory.

```python
import hashlib

def sha256_stream(path: str, chunk_size: int = 64 * 1024) -> str:
    """Content hash without loading the file into memory. O(1) memory."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()
```

Output (conceptually):
```
'c9a3d1e4f5b6a7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2'
```

A dataset is then identified by `sha256:9f2c1b7a...` and *provenance* (how it
was built from raw sources) is a first-class record. DVC stores exactly this
hash-to-path map in `.dvc` files and pushes the blobs to an object store.

## 5. The Run Record

A `RunRecord` (seed, data hash, environment, metrics) is the audit trail.
Regulatory environments and incident reviews both start from this record. A
practical schema:

```python
from dataclasses import dataclass, asdict
import json

@dataclass
class RunRecord:
    run_id: str            # e.g. run_2026-08-02T18:30:00_abc123
    git_sha: str
    git_dirty: bool
    seed: int
    data_hash: str
    env_fingerprint: dict[str, str]
    metrics: dict[str, float]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)
```

Output (conceptually):
```
{"run_id": "run_..._abc123", "git_sha": "9f2c...", "git_dirty": false,
 "seed": 42, "data_hash": "sha256:c9a3...", "env_fingerprint": {...},
 "metrics": {"val_acc": 0.918}}
```

## 6. Deterministic Splits and Augmentation

Even with seeds pinned, a **split index file** (the exact row indices used for
train/val/test) is stronger than re-deriving the split from a seed: it survives
new rows being appended to the dataset, and it lets teammates share the exact
same split without sharing a random state. This is the difference between "the
same split" and "a split that happened to be the same".

```python
def make_split_indices(
    n_rows: int, val_frac: float = 0.2, seed: int = 42
) -> dict[str, list[int]]:
    """Deterministic, seed-independent split indices saved as JSON."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n_rows)
    val_n = int(n_rows * val_frac)
    return {
        "train": sorted(idx[val_n:].tolist()),
        "val": sorted(idx[:val_n].tolist()),
    }
```

Output (conceptually):
```
{'train': [20, 21, 22, ...], 'val': [0, 1, 2, ...]}
```

The indices are committed to the repo; the split never changes even when the
dataset grows. For augmentation, pin the augmentation seed **per sample** (the
index is the seed), so an image augmented at index 7 is identical in every run.

## Every Use Case

- **Experiment comparison**: comparing two hyperparameter configs is only
  meaningful if both trained on identical data splits and seeds.
- **Bug isolation**: a metric regression after a code change is only
  diagnosable if the baseline run is reproducible.
- **Compliance and audit**: banking, healthcare, and insurance models must
  demonstrate *what* trained the model and *when*; regulators subpoena run
  records.
- **CI/CD for ML**: a pipeline that cannot reproduce locally cannot be safely
  promoted from staging to production.
- **Multi-team collaboration**: three engineers training on "the same dataset"
  with different preprocessing orders produce three different models.
- **Disaster recovery**: losing a model artifact is fine if the run record lets
  you rebuild it byte-for-byte.
- **A/B and shadow deployment**: deciding whether the new model won requires
  the old model to be rerun under identical conditions.
- **Research and publication**: reviewers reject results that cannot be
  reproduced by the authors' own scripts.

## Real-World Use Cases for AI Engineers

- **Banking model risk management (SR 11-7 / OCC 2011-12)**: every credit-risk
  model must ship with a model development document and be independently
  validated. The validation team *re-runs* your training. If the re-run
  diverges, the model is not approved. AI engineers build the run-record
  pipeline that makes this re-run a one-command operation.
- **Healthcare trial reproducibility**: an ML triage model used in a clinical
  pilot must produce identical predictions for identical inputs across sites.
  A site with a different sklearn version would silently change triage
  decisions — reproducibility here is a patient-safety issue.
- **E-commerce recommendation retraining**: nightly retraining with an
  unseeded shuffle produces recommendation lists that differ run-to-run;
  A/B tests on ranking changes become statistically uninterpretable. The ML
  platform team seeds everything and version-addresses the training data so
  the nightly job is a *pure function* of (code, data, env).
- **Ad-tech auction modeling**: bidding models trained non-reproducibly cause
  "phantom" metric swings that the growth team attributes to the wrong
  cause — a week of misattributed revenue.
- **RAG system ingestion**: an embedding index is reproducible only if the
  chunking + embedding pipeline is seeded and versioned; a re-index that
  shuffles chunk order changes retrieval quality and evaluation numbers.

## Common Mistakes to Avoid

### Mistake 1: Seeding inside a loop
```
# WRONG — every fold re-seeds to the same split
for fold in range(5):
    np.random.seed(42)
# CORRECT — seed once at process start
np.random.seed(42)
for fold in range(5): ...
```

### Mistake 2: Seeding only `random`, not `numpy`
Two separate streams; both must be pinned, plus torch/tf if used.

### Mistake 3: Versioning data by filename
A file can be overwritten while keeping its name — the version silently changes.
Hash the bytes.

### Mistake 4: No environment capture
The model works today and breaks next month when numpy 2.x lands — with no
record of what numpy version trained it.

### Mistake 5: Seeding a *different* process
Distributed training spawns workers; a seed set in the parent does not reach
workers. Seed inside each worker's init.

### Mistake 6: Reusing one seed for split *and* augmentation
The split and the augmentation then share a stream; adding one augmentation op
changes the split. Use separate, dedicated seeds per stage.

## Best Practices

1. Call one `seed_all(seed)` function at the top of every pipeline
2. Record code version (git hash + dirty flag), data hash, and dependency lockfile per run
3. Prefer content hashing for datasets and artifacts — identity from bytes
4. Make the seed a run *parameter*, not a magic number
5. Test that two runs with the same seed produce identical results (a CI gate)
6. Capture the environment before training, not after a failure
7. Commit split-index files instead of re-deriving splits from seeds
8. Use dedicated seeds per stage (split, augmentation, model init)
9. Hash large files in chunks (64 KB) for O(1) memory
10. Treat the lockfile as a first-class artifact; pin exact versions, never `>=`

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Hash a 10GB dataset (streaming) | O(n) reads | O(1) | SHA-256 with 64KB chunks |
| Re-seed mid-pipeline | O(1) | O(1) | seed once, never re-seed |
| Capturing env | O(deps) | O(1) | lockfile via `pip freeze` |
| Commit split indices | O(n) | O(n) | store indices only, not the split arrays |
| Re-run to verify | O(training) | O(1) | gate on seed + env only for smoke tests |

## AI Engineering Relevance

**Where this shows up:** every training job in a CI/CD ML pipeline, model
registry entries, and incident postmortems.

| Concept here | Used for |
|---|---|
| Seed pinning | deterministic CV splits, reproducible hyperparameter runs |
| Environment capture | "what trained this model?" audits |
| Content addressing | linking a model to its exact training data |
| Run record | the audit trail regulators and incident reviews start from |

**Scale note:** at 1M training runs, an unreproducible 1% is 10,000
un-debuggable incidents. Reproducibility is a scale problem, not a nicety —
it is the cheapest insurance an ML platform can buy.

## Practice Exercises

### Exercise 1: Deterministic Draws (Easy)
Write `same_draws(seed: int) -> tuple[list[int], list[int]]` that returns two
identical 5-element random lists by re-seeding between draws. Verify with
`same_draws(42)[0] == same_draws(42)[1]`.

### Exercise 2: Streaming Hash (Medium)
Hash a 100MB temp file in chunks without loading it into memory; verify the
chunked hash equals a single-shot `hashlib.sha256(open(f,'rb').read())` hash.

### Exercise 3: Run Audit Trail (Hard)
Extend `RunRecord` to include a git commit hash and a dependency fingerprint,
and write `rerun(record: RunRecord) -> RunRecord` that "replays" a recorded run
(given a mock `train()` callback) and asserts metrics match within tolerance.

### Exercise 4: Split-Index Stability (Medium)
Given a 1000-row dataset, generate train/val indices twice with the same seed
and once with a different seed; assert the first two are identical and the
third differs. Then append 100 rows and show the *saved* indices are unchanged.

## Summary

| Concept | Description |
|---|---|
| Seed | pins the random stream; one call, process start |
| Environment | code + data + library versions |
| Content hash | unambiguous dataset identity |
| Run record | the audit trail linking it all |
| Split indices | deterministic splits that survive data growth |

Reproducibility is cheap to add and expensive to retrofit. Every run you cannot
reproduce is a run you cannot defend — to your teammates, to your auditors, or
to the customers whose predictions depend on it.

## Quick Reference

| Task | Idiom |
|---|---|
| Seed everything | `random.seed(42); np.random.seed(42); torch.manual_seed(42)` |
| Hash content | `hashlib.sha256(bytes).hexdigest()` |
| Capture env | `platform.python_version()` + `pip freeze` |
| Lock env | `pip freeze > requirements.lock` |
| Verify determinism | run twice, `assert metrics_a == metrics_b` |

## Next Steps

Next: **[02 Experiment Tracking](02-experiment-tracking-lecture.md)** — logging
params, metrics, and artifacts per run.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://docs.python.org/3/library/random.html,
https://numpy.org/doc/stable/reference/random/generator.html,
https://dvc.org/doc/start/data-management
