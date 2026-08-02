# RAG Baseline — Glossary 09

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Augmentation | RAG | Building a prompt with retrieved context |
| Context | RAG | The retrieved chunks given to the model |
| Corpus | RAG | The full set of source documents |
| Grounded Answer | RAG | An answer derived from retrieved context |
| Index | RAG | The chunk→embedding store |
| Retrieval | RAG | Finding relevant chunks for a query |
| Top-k | RAG | The number of chunks returned per query |
| Vector Store | Infrastructure | Persistent storage for embeddings |

## Detailed Definitions
### Augmentation
**Definition**: The prompt stage where retrieved chunks are inserted as
context.
**Related**: Context

### Context
**Definition**: The retrieved chunks the model must answer from.
**Related**: Augmentation

### Corpus
**Definition**: All source documents that get chunked and embedded.
**Related**: Index

### Grounded Answer
**Definition**: Output supported by the provided context, with citations.
**Related**: Augmentation

### Index
**Definition**: The structure mapping chunks to their embeddings.
**Related**: Vector Store

### Retrieval
**Definition**: Embedding the query and ranking chunks by similarity.
**Related**: Top-k

### Top-k
**Definition**: How many chunks are passed to generation.
**Related**: Retrieval

### Vector Store
**Definition**: A database optimized for embedding storage and search.
**Related**: Index

## Key Concepts Summary
### The Pipeline
- Index → Retrieve → Augment → Generate

### The Rules
- Answer only from context, or say "I don't know"
- Cite every claim

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Index — ___
2. Top-k — ___
3. Augment — ___
4. Corpus — ___
5. Grounded — ___

**Answers:** 1-b, 2-e, 3-a, 4-c, 5-d where a=context prompt stage, b=chunk→
embedding store, c=source documents, d=context-derived answer, e=chunks per
query.
