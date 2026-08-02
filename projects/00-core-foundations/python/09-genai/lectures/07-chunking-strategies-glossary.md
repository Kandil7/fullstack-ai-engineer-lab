# Chunking Strategies — Glossary 07

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Chunk | Pipeline | A unit of document text fed to embeddings/LLM |
| Chunk Boundary | Pipeline | The split point between chunks |
| Fixed-Size Chunking | Strategy | Splitting on token counts |
| Metadata | Pipeline | Source/position tags attached to a chunk |
| Overlap | Strategy | Repeating boundary tokens between chunks |
| Paragraph Chunking | Strategy | Splitting on blank lines |
| Semantic Chunking | Strategy | Splitting where meaning shifts |
| Sentence Chunking | Strategy | Splitting on sentence boundaries |

## Detailed Definitions
### Chunk
**Definition**: A segment of a document sized for embedding and context.
**Related**: Chunk Boundary

### Chunk Boundary
**Definition**: Where one chunk ends and the next begins.
**Related**: Chunk

### Fixed-Size Chunking
**Definition**: Splitting every N tokens regardless of content.
**Related**: Overlap

### Metadata
**Definition**: Source, section, and index info attached to each chunk for
provenance and citation.
**Related**: Chunk

### Overlap
**Definition**: Including tail tokens of the previous chunk in the next, so
boundary sentences survive.
**Related**: Fixed-Size Chunking

### Paragraph Chunking
**Definition**: Splitting on blank lines; context-rich, natural units.
**Related**: Sentence Chunking

### Semantic Chunking
**Definition**: Embedding text and splitting where similarity drops, aligning
with meaning.
**Related**: Chunk Boundary

### Sentence Chunking
**Definition**: Splitting on punctuation; crisp units, short context.
**Related**: Paragraph Chunking

## Key Concepts Summary
### The Rules
- Boundaries must not split answers
- Metadata is non-negotiable
- Strategy follows content shape

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Overlap — ___
2. Semantic — ___
3. Metadata — ___
4. Fixed-size — ___
5. Sentence — ___

**Answers:** 1-c, 2-e, 3-a, 4-b, 5-d where a=source tags, b=token-count splits,
c=repeated boundary tokens, d=punctuation splits, e=meaning-boundary splits.
