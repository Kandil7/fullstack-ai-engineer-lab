# MLOps — 03: Data Versioning

## Topic Overview

Data versioning is the practice of giving every dataset a stable, content-derived
identity and recording its provenance — where it came from, how it was built, and
what it is compatible with. Code has Git; data needs an equivalent because raw
data, processed datasets, splits, and features change over time, and a model
trained on yesterday's data is not the same model as one trained on today's.

The core insight is **content addressing**: a dataset's identity is the hash of
its bytes (see Lecture 01). Versioning then answers three questions:
1. **Which version is this?** — a short content hash (`v2 = sha256:c9a3...`)
2. **What changed?** — a diff between two versions' hashes, plus a changelog
3. **What produced it?** — provenance: the raw sources, the transform code, the
   seed, and the config that created this version

The standard open tool is **DVC** (Data Version Control): it stores data in an
object store (S3, GCS, Azure, local), keeps a tiny `.dvc` pointer file in Git
containing the hash, and lets you `dvc checkout` any historical version.
Hugging Face **Datasets** and **LakeFS** (git-like semantics for data lakes)
are alternatives for different scales. Everything below is tool-agnostic — the
*principles* are what an AI engineer must internalize.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Compute and use content-derived dataset versions (`sha256` of bytes)
2. Build a provenance record linking raw sources → transform → output version
3. Diff two dataset versions and explain what changed
4. Store large datasets in an object store while keeping pointers in Git (DVC model)
5. Version splits and preprocessing artifacts, not just raw data
6. Design a versioning scheme that makes retraining and rollback safe
7. Detect "silent drift" — a dataset that changed without anyone noticing

## Prerequisites

| Need | Where |
|---|---|
| Content hashing | `08-mlops/lectures/01-reproducibility-lecture.md` |
| pandas basics | `03-libraries/pandas/` |
| Git | `00-core-foundations/git-linux/` |
| JSON | `01-core-python/` |

## 1. Why Filenames Are Not Versions

`dataset_v2_final.csv` is not a version — it is a lie wearing a filename. The
same filename can hold different bytes after an overwrite; two files with
different names can hold identical bytes. Content addressing fixes both:

```python
import hashlib, json

def dataset_version(data_bytes: bytes) -> str:
    """A version is the content hash, not a filename."""
    return f"sha256:{hashlib.sha256(data_bytes).hexdigest()[:16]}"

print(dataset_version(b"row1,row2"))
print(dataset_version(b"row1,row2"))          # identical bytes → identical version
print(dataset_version(b"row1,row2CHANGED"))   # any change → new version
```

Output (conceptually):
```
sha256:6f1a3c...
sha256:6f1a3c...
sha256:b7d9e2...
```

## 2. The DVC Model: Blobs in the Store, Pointers in Git

Large datasets do not belong in Git. DVC's pattern: the **blob** (actual data)
lives in an object store; a small `.dvc` file (the *pointer*) lives in Git and
records the hash. Git versions the pointers; the object store versions the
blobs. This gives you `git` history for free and deduplicates storage — the
same blob is stored once regardless of how many pointers reference it.

```yaml
# data/train.csv.dvc  (pointer file, lives in Git)
outs:
- md5: c9a3d1e4f5b6a7c8...
  path: train.csv
  size: 10485760
```

The workflow is: `dvc add data/train.csv` → commit the `.dvc` pointer →
`dvc push` the blob to the remote → anyone can `dvc pull` and `dvc checkout`
any historical version by checking out the matching Git commit.

## 3. Provenance: The Recipe That Built a Version

A hash tells you *what* the bytes are, not *how they were made*. Provenance
records the recipe: raw sources (with their own hashes), transform code (git
SHA), config, and seed. Two datasets with identical hashes built from different
recipes are the same data; two datasets with the same recipe but different raw
sources must hash differently.

```python
from dataclasses import dataclass, asdict
import json

@dataclass
class Provenance:
    version: str                 # sha256 of the output bytes
    raw_sources: list[str]       # hashes of the raw inputs
    transform_git_sha: str       # code that produced this version
    config: dict[str, str]       # params of the transform
    seed: int
    created_by: str
    notes: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)
```

Output (conceptually):
```
{"version": "sha256:c9a3...", "raw_sources": ["sha256:1f2b...", ...],
 "transform_git_sha": "9f2c1b7a", "config": {"imputer": "median", "norm": "z"},
 "seed": 42, "created_by": "data-pipeline v3.2"}
```

This is the **dataset lineage** that audits demand: "show me exactly how the
data that trained the champion model was produced."

## 4. Diffs Between Versions

Versioning without diffing is just renaming. A practical diff for tabular data:

```python
def dataset_diff(old: list[tuple], new: list[tuple]) -> dict:
    """Row-level summary diff between two versions."""
    old_set, new_set = set(old), set(new)
    return {
        "added_rows": len(new_set - old_set),
        "removed_rows": len(old_set - new_set),
        "changed_rows": sum(1 for r in old_set & new_set if False),  # placeholder
        "total_old": len(old),
        "total_new": len(new),
    }

print(dataset_diff([(1, "a"), (2, "b")], [(1, "a"), (3, "c")]))
```

Output (conceptually):
```
{'added_rows': 1, 'removed_rows': 1, 'total_old': 2, 'total_new': 2}
```

A changelog entry ("v3 adds 5k rows of 2026Q2 transactions, fixes null
customer_id") should accompany every new version so that *humans* can navigate
what the hashes encode.

## 5. Versioning Splits and Preprocessing

The most dangerous silent change in ML is a split or preprocessing drift: the
raw data is unchanged but the split indices or the normalization constants
changed, so the model quietly trains on different data. Solution: version the
*splits* and *preprocessing artifacts* (imputer means, scaler params) as
first-class objects with their own hashes, and record them in the run record.

```python
def version_preprocessor(scaler_params: dict) -> str:
    """A scaler's identity is the params it fitted with."""
    raw = json.dumps(scaler_params, sort_keys=True).encode()
    return f"sha256:{hashlib.sha256(raw).hexdigest()[:16]}"

print(version_preprocessor({"mean": [0.5, 1.2], "scale": [0.1, 0.3]}))
```

Output (conceptually):
```
sha256:4b1e9c...
```

## 6. Rollback and Retraining Safety

With content-addressed versions, "roll back to the data that trained v2" is a
mechanical operation: checkout the Git commit, `dvc checkout`, retrain. The
safety property is that **a model and its data version never get separated** —
the model artifact records its data version (see Lecture 01's `RunRecord`),
so you can always reconstruct the exact training conditions.

| Safety property | Mechanism |
|---|---|
| A model knows its data | `RunRecord.data_hash` |
| Data is recoverable | `dvc pull` the stored blob |
| Nothing silently changes | hash-of-bytes identity |
| Diff is reviewable | changelog + row-level diff tool |

## Every Use Case

- **Retraining on schedule**: nightly/quarterly refreshes with clear version
  boundaries so metric changes are attributable to *data changes*.
- **Data science experimentation**: trying a preprocessing change is a new
  version; comparing models trained on v2 vs v3 is a controlled experiment.
- **Compliance and audit**: prove what data trained a production model
  (GDPR, banking, healthcare).
- **Disaster recovery**: restore any historical dataset version from the store.
- **Multimodal/ML teams sharing**: image sets, text corpora, and tabular data
  shared across teams with stable references.
- **Debugging model regressions**: a drop in metrics is often a data version
  change, not a code change — the diff tells you.
- **Experiments on streaming data**: windowed datasets versioned per window
  enable offline replay of production conditions.

## Real-World Use Cases for AI Engineers

- **Fraud detection at a payments company**: the model retrains weekly on
  transaction data. A spike in false positives is traced to `data v14` which
  changed the negative sampling ratio. The team diffs v13 vs v14, sees the
  ratio change, and reverts the sampling config — the fraud model returns to
  baseline in one retraining cycle, *because every model records its data
  version*.
- **Recommendation systems**: candidate generation uses a user-event corpus
  that grows daily. Without versioning, A/B tests comparing "new model" vs
  "old model" are confounded by "new data". Versioning keeps the comparison
  fair: both models train on the same pinned dataset version.
- **Healthcare imaging**: a model trained on site A's scans and site B's scans
  must be auditable. Each dataset version records the acquisition protocol and
  site; the clinical validation report references exact versions.
- **LLM fine-tuning data**: instruction datasets evolve rapidly. Versioning the
  fine-tuning corpus (and its deduplication) is what lets teams answer "which
  data mix produced this model's behavior change?"
- **Data lake / feature teams**: a central team publishes feature data as
  versioned artifacts; downstream training pipelines pin a version, so a bad
  feature release cannot silently poison every downstream model.

## Common Mistakes to Avoid

### Mistake 1: Versioning by filename or timestamp
```
# WRONG — filename can hold different bytes
"dataset_v2_final.csv"
# CORRECT — content hash
"sha256:c9a3d1e4..."
```

### Mistake 2: Committing large blobs to Git
Git history balloons and checkouts slow to a crawl. Blobs → object store,
pointers → Git.

### Mistake 3: No provenance
A hash with no recipe is a number with no story. Record raw sources, code SHA,
config, seed.

### Mistake 4: Not versioning splits/preprocessing
The raw data is unchanged but the split changed — the silent killer of
reproducibility. Version the split indices and fitted preprocessors.

### Mistake 5: Overwriting in place
Never mutate the file at the current path — write a new version, update the
pointer. Mutation destroys history.

### Mistake 6: Ignoring the changelog
Hashes are for machines; a one-line human note ("added 2026Q2 rows") is what
makes the history navigable.

## Best Practices

1. Identity = hash of bytes; never trust filenames
2. Store blobs in an object store; keep pointers in Git
3. Record provenance on every version (raw sources, code SHA, config, seed)
4. Write a human changelog per version
5. Version splits and fitted preprocessors as first-class objects
6. Pin the data version in every training run's `RunRecord`
7. Provide a `diff` command for any two versions
8. Add a CI check that fails when a dataset changes without a new version
9. Automate version creation in the ingestion pipeline (no manual steps)
10. Backup the object store; the pointers are worthless without the blobs

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Hash a 10GB dataset | O(n) reads | O(1) | streamed 64KB chunks |
| Store blob in object store | O(n) upload | O(n) | dedupe by hash (content addressing) |
| Diff two versions | O(n) | O(n) | hash buckets + row-level diff |
| Pointer file in Git | O(1) | O(1) | — |
| dvc checkout a version | O(n) pull | O(n) | — |

## AI Engineering Relevance

**Where this shows up:** every data ingestion pipeline, retraining job, and
model audit. Data versioning is what makes retraining safe: without it, "train
the same model again" is a roll of the dice.

| Concept here | Used for |
|---|---|
| Content hash | stable dataset identity |
| Provenance | auditable lineage raw → processed → model |
| Versioned splits | fair model comparisons |
| Pin data version | rollback-safe retraining |

**Scale note:** at petabyte scale, hashing must be streamed and blobs must be
chunked (a single 10GB file is fine; a million small files is not — batch them
or use a chunked format like Parquet). Versioning cost grows with data size,
but the cost of *not* versioning grows with team size.

## Practice Exercises

### Exercise 1: Content Versions (Easy)
Write `version(data: list[tuple]) -> str` returning a short sha256 prefix, and
prove equal data → equal version, changed data → changed version.

### Exercise 2: Provenance Record (Medium)
Build a `Provenance` dataclass from a raw source, transform git SHA, config,
and seed; serialize it; and write `provenance_of(version, store)` that returns
the record for a given version from a mock store.

### Exercise 3: Safe Retrain Simulator (Hard)
Simulate the lifecycle: dataset v1 → train → model A; dataset v2 (with a
changelog) → train → model B. Write `rollback(model_a_id, version_store)` that
checks out v1's data, re-runs training, and asserts the re-trained model's
metrics match model A's recorded metrics within tolerance.

### Exercise 4: Split Versioning (Medium)
Generate train/val indices for a 1000-row dataset; version the split JSON;
append 100 rows and show the *saved* split version is unchanged while a
re-derived split would change — demonstrating why indices are committed.

## Summary

| Concept | Description |
|---|---|
| Content address | hash of bytes = identity |
| DVC model | blobs in store, pointers in Git |
| Provenance | recipe that built the version |
| Diff | what changed between versions |
| Split/preprocess versioning | the silent-drift protection |

Data is the most changeable part of an ML system and the least guarded. Content
addressing plus provenance gives data the same rigor that Git gives code — and
makes retraining, rollback, and audit mechanical rather than heroic.

## Quick Reference

| Task | Idiom |
|---|---|
| Version data | `sha256(data_bytes)` — content hash |
| Add to DVC | `dvc add data/train.csv && git commit` |
| Store blobs | `dvc push -r s3-remote` |
| Restore version | `git checkout <sha> && dvc checkout` |
| Diff versions | row-level `set(old) - set(new)` summary |

## Next Steps

Next: **[04 Model Registry](04-model-registry-lecture.md)** — the model side of
the lineage: versioning, staging, and promoting models.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://dvc.org/doc/start/data-management,
https://huggingface.co/docs/datasets,
https://docs.lakefs.io/
