# Case Study: RAG Service — Glossary 23

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Citation | Output | A source reference attached to a claim |
| Confidence | Output | A score expressing answer certainty |
| Eval Gate | Quality | The threshold the suite score must pass |
| Idempotent | Ingestion | Re-running ingestion does not duplicate |
| Ingestion | Pipeline | Loading and indexing source documents |
| Public Contract | Design | The service's external interface |
| Source | Output | The document backing a claim |
| Two-Stage | Retrieval | Wide retrieval followed by reranking |

## Detailed Definitions
### Citation
**Definition**: A reference linking a claim to its source chunk.
**Related**: Source

### Confidence
**Definition**: A numeric signal of answer reliability for downstream use.
**Related**: Citation

### Eval Gate
**Definition**: The suite-score threshold blocking weak changes.
**Related**: Two-Stage

### Idempotent
**Definition**: A property where repeated ingestion yields the same index.
**Related**: Ingestion

### Ingestion
**Definition**: The load → clean → chunk → embed → store stage.
**Related**: Idempotent

### Public Contract
**Definition**: The minimal external interface (ask → answer + sources).
**Related**: Citation

### Source
**Definition**: The specific document chunk a claim is based on.
**Related**: Citation

### Two-Stage
**Definition**: Retrieving wide, then reranking to a sharp top-k.
**Related**: Eval Gate

## Key Concepts Summary
### The Design
- Tiny public contract, swappable internals

### The Rules
- Cite every claim
- Gate every change

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Citation — ___
2. Ingestion — ___
3. Eval gate — ___
4. Idempotent — ___
5. Two-stage — ___

**Answers:** 1-d, 2-e, 3-b, 4-c, 5-a where a=retrieve then rerank, b=quality
threshold, c=no duplicate ingestion, d=claim-source link, e=load and index.
