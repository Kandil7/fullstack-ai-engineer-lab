# Model Packaging — Glossary 05

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Artifact | Packaging | The packaged model plus its metadata |
| Environment Pin | Packaging | Exact dependency versions recorded with the model |
| JSON Contract | Packaging | A safe, language-neutral serialization |
| Manifest | Packaging | The model's schema + environment document |
| ONNX | Packaging | A portable computation-graph format |
| Pickle | Python | Python's object serializer; executes code on load |
| Serialization | Packaging | Converting an object to bytes for storage |
| Supply Chain | Security | The chain of artifact producers/consumers |

## Detailed Definitions
### Artifact
**Definition**: The packaged deliverable: model bytes + schema + environment
manifest.
**Related**: Manifest, Serialization

### Environment Pin
**Definition**: Recording exact library versions so behavior cannot silently
drift.
```python
"env": {"numpy": "2.1.3", "python": "3.13"}
```
**Related**: Manifest

### JSON Contract
**Definition**: Serializing weights/config as JSON - portable, safe (no code
execution).
**Related**: Serialization

### Manifest
**Definition**: A document bundling schema, format, library, and version.
**Related**: Artifact

### ONNX
**Definition**: An open format for representing trained models as a portable
graph, executable by ONNX Runtime.
**Related**: Serialization

### Pickle
**Definition**: Python's serializer that can execute arbitrary code via
`__reduce__` during unpickling - never load untrusted pickles.
**Related**: Supply Chain

### Serialization
**Definition**: The act of converting an in-memory object into storable bytes
and back.
**Related**: Artifact

### Supply Chain
**Definition**: The chain from model author to production loader; any untrusted
link is an attack surface.
**Related**: Pickle

## Key Concepts Summary
### Safe vs Unsafe
- Safe: JSON, protobuf, ONNX
- Risky: pickle from untrusted sources

### The Bundle
- Model bytes + schema + environment manifest = one artifact

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Pickle — ___
2. Manifest — ___
3. ONNX — ___
4. Serialization — ___
5. Supply chain — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=artifact provenance chain, b=code-
executing serializer, c=schema+env document, d=portable graph format,
e=object to bytes.
