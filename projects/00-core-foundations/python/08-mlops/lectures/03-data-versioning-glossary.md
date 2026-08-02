# Data Versioning — Glossary 03

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| CAS (Content-Addressed Storage) | Data | Storage keyed by content hash |
| Digest | Cryptography | The output of a hash function |
| Lineage | MLOps | The chain of sources/transforms producing a dataset |
| Manifest | MLOps | Structured metadata describing a dataset version |
| Raw Source | Data | The unprocessed origin of data |
| Streaming Hash | Data | Hashing in chunks to bound memory |
| Transform | Data | A processing step between raw and final |

## Detailed Definitions
### CAS (Content-Addressed Storage)
**Definition**: A storage scheme where the address is derived from the content
hash, so identical content maps to one address.
**Example**:
```python
path = f"{root}/{name}/{sha256(content)}"
```
**Complexity**: O(n) hash, O(1) dedupe.
**Related**: Digest, Streaming Hash

### Digest
**Definition**: The fixed-length output of a hash function.
```python
import hashlib
print(hashlib.sha256(b"data").hexdigest()[:8])
```
**Related**: CAS

### Lineage
**Definition**: The record of how a dataset was produced: raw sources,
transforms, and parameters.
**Related**: Manifest, Raw Source

### Manifest
**Definition**: A JSON-style document describing a dataset version: name, rows,
columns, source hash, transforms, params.
**Related**: Lineage

### Raw Source
**Definition**: Original, unprocessed data before any transform.
**Related**: Lineage

### Streaming Hash
**Definition**: Updating a hash over chunks so large files never load fully
into memory.
```python
h = hashlib.sha256()
for chunk in f:  # 64KB at a time
    h.update(chunk)
```
**Related**: Digest

### Transform
**Definition**: A processing step (dropna, one-hot, clip) applied to data.
**Related**: Lineage

## Key Concepts Summary
### Identity Is Content
- Same bytes -> same address -> same version
- Changing bytes -> new address -> new version

### The Lineage Chain
- raw sources -> transforms -> features table -> model (recorded at each step)

## Practice Terms
Match each term to its definition (answers at the bottom).
1. CAS — ___
2. Manifest — ___
3. Lineage — ___
4. Streaming hash — ___
5. Transform — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=processing step, b=content-keyed
storage, c=dataset metadata, d=provenance chain, e=chunked hashing.
