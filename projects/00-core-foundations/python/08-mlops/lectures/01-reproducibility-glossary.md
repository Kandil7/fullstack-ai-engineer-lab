# Reproducibility — Glossary 01

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Content-Addressed Storage | Data | Storage keyed by a hash of the content, so identical data dedupes |
| Deterministic | Property | Producing identical results across runs when seeded identically |
| Environment Fingerprint | MLOps | Snapshot of Python version, platform, and library versions |
| Jitter | Retry | Random perturbation of a delay to desynchronize retries |
| Lockfile | MLOps | Exact, pinned dependency versions for reproducible installs |
| Pseudo-Random Generator | Python | A deterministic stream of numbers seeded by an initial value |
| Run Record | MLOps | Seed + data hash + env + metrics captured per training run |
| Seed | Python | The initial value that pins a random stream |
| SHA-256 | Cryptography | A cryptographic hash producing a fixed 64-hex-char digest |
| Streaming Hash | Data | Hashing a large file in chunks to bound memory |

## Detailed Definitions
### Content-Addressed Storage
**Definition**: Storage where the address of a blob is derived from its content
(usually a SHA-256 prefix). The same content always maps to the same address.
**Example**:
```python
import hashlib
addr = hashlib.sha256(b"x,y\n1,2\n").hexdigest()[:16]
print(addr)  # deterministic for these exact bytes
```
**Complexity**: O(n) to compute, O(1) lookup by name.
**Related**: SHA-256, Run Record

### Deterministic
**Definition**: A pipeline that, given the same inputs, seeds, and environment,
produces identical outputs every run.
**Example**: two `random.seed(42)` calls followed by `random.random()` yield the
same first draw.
**Complexity**: n/a.
**Related**: Seed, Environment Fingerprint

### Environment Fingerprint
**Definition**: A structured record of the runtime: Python version, OS,
executable path, and library versions.
**Example**:
```python
import platform
print(platform.python_version())  # e.g. 3.13.1
```
**Complexity**: O(deps).
**Related**: Lockfile, Run Record

### Lockfile
**Definition**: A file pinning exact dependency versions (e.g. `numpy==2.1.3`),
so installs are reproducible.
**Related**: Environment Fingerprint

### Pseudo-Random Generator
**Definition**: An algorithm that produces a deterministic sequence of numbers
from a seed. Python's `random` and NumPy's `default_rng` are separate PRNGs.
**Example**:
```python
import random
random.seed(7)
print([random.random() for _ in range(3)])
```
**Related**: Seed

### Run Record
**Definition**: The audit object capturing everything needed to re-run a
training job: seed, data hash, environment, and resulting metrics.
**Related**: Environment Fingerprint, Content-Addressed Storage

### Seed
**Definition**: The integer (or bytes) that initializes a PRNG; identical seeds
produce identical streams.
**Related**: Pseudo-Random Generator, Deterministic

### SHA-256
**Definition**: A 256-bit cryptographic hash. Small changes in input produce
completely different digests.
**Example**:
```python
import hashlib
print(hashlib.sha256(b"a").hexdigest()[:8])
print(hashlib.sha256(b"b").hexdigest()[:8])  # totally different
```
**Related**: Content-Addressed Storage

### Streaming Hash
**Definition**: Updating a hash incrementally over chunks, bounding memory for
large files.
```python
h = hashlib.sha256()
for chunk in file_iterable:  # 64KB chunks
    h.update(chunk)
```
**Related**: SHA-256

## Key Concepts Summary
### The Three Pins
- Code: git commit hash
- Data: content hash
- Environment: lockfile + platform

### Why Reproducibility Matters
- Debugging requires a rerun
- Audits require an answer to "what trained this?"
- Comparison requires identical conditions

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Seed — ___
2. Lockfile — ___
3. SHA-256 — ___
4. Streaming hash — ___
5. Deterministic — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=runs identically, b=initial value
of a PRNG, c=pinned dependency versions, d=64-hex digest, e=chunked hashing.
