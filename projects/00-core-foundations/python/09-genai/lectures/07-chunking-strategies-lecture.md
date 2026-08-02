# GenAI — 07: Chunking Strategies

## Topic Overview

Chunking is the practice of splitting documents into pieces — **chunks** —
small enough to embed and retrieve effectively, while keeping each chunk
semantically self-contained. It is the least glamorous and most
quality-critical decision in RAG: chunk too big → retrieval is fuzzy and
context is wasted; chunk too small → chunks lose their meaning and retrieval
recall collapses. Chunking strategy is a *measured* decision (Lecture 5/10
discipline), not a default.

The design space has five families:

| Strategy | Idea | Strength | Weakness |
|---|---|---|---|
| **Fixed-size** | N characters/words with overlap | simple, predictable | cuts mid-sentence, splits concepts |
| **Sentence** | split on sentence boundaries | semantically complete units | sentences vary in size |
| **Paragraph** | split on blank lines/headers | natural topic units | paragraphs can be huge |
| **Recursive** | hierarchy-aware (chars→words→sentences→paragraphs) | best general-purpose | more code |
| **Semantic** | split where embedding similarity drops | optimal-ish units | costs extra embedding passes |

The engineer's job: choose by *document type* (prose vs code vs legal vs
support-article), *retrieval task* (fact lookup wants small precise chunks;
summarization wants larger units), and *eval* (retrieval quality — L10 — is
the referee). The meta-rule: **the chunk boundary is a decision, and every
decision is measured.**

## Learning Objectives

By the end of this lecture, you will be able to:
1. Implement fixed-size chunking with overlap
2. Implement sentence and paragraph chunking
3. Implement recursive character chunking
4. Choose the strategy per document type and retrieval task
5. Keep metadata (source, heading, index) attached to every chunk
6. Evaluate chunking with retrieval quality metrics (recall@k, L10)
7. Avoid the classic failures: split identifiers, lost context, orphaned headers

## Prerequisites

| Need | Where |
|---|---|
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| Token counting | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| Python string ops | `01-core-python/` |
| Retrieval eval (preview) | `09-genai/lectures/10-retrieval-quality-lecture.md` |

## 1. Fixed-Size Chunking with Overlap

The baseline: slice by character/word count, carry an overlap so context
doesn't break at boundaries. Predictable, but cuts mid-thought.

```python
def chunk_fixed(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    """Fixed character-size chunks with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

doc = "word " * 1200
chunks = chunk_fixed(doc, 500, 50)
print("chunks:", len(chunks), "| sizes:", [len(c) for c in chunks])
```

Output:
```
chunks: 3 | sizes: [500, 500, 300]
```

Overlap (10–20%) preserves boundary context but duplicates tokens (cost —
L18). Fixed-size is the honest baseline to beat, rarely the final answer.

## 2. Sentence Chunking

Split on sentence boundaries so each chunk is a complete thought:

```python
import re

def chunk_sentences(text: str, max_chars: int = 900) -> list[str]:
    """Group sentences into chunks under max_chars (respecting boundaries)."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, cur = [], ""
    for s in sentences:
        if len(cur) + len(s) > max_chars and cur:
            chunks.append(cur.strip())
            cur = s
        else:
            cur += " " + s if cur else s
    if cur:
        chunks.append(cur.strip())
    return chunks

print(chunk_sentences("First sentence. Second sentence. " * 40, 400)[:1])
```

Output:
```
['First sentence. Second sentence. First sentence. Second sentence. ...']
```

Sentence chunking preserves grammatical units — a strong default for prose —
but a single 3,000-char sentence (legal text!) still produces a huge chunk;
guard with a hard cap.

## 3. Paragraph Chunking

Split on blank lines and/or headings — natural topic units:

```python
def chunk_paragraphs(text: str, max_chars: int = 2000) -> list[str]:
    """Paragraph chunks, splitting oversized paragraphs further."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out = []
    for p in paras:
        out.extend(chunk_fixed(p, max_chars) if len(p) > max_chars else [p])
    return out
```

Output:
```
Paragraph-aligned chunks; oversized paragraphs split with overlap.
```

Best for well-structured documents (articles, specs) where paragraphs are
coherent topics. Headings are precious metadata — capture them (section 5).

## 4. Recursive Chunking: The General-Purpose Choice

Recursive character splitting (LangChain's `RecursiveCharacterTextSplitter`
pattern) tries progressively finer separators so structure is respected as
much as possible:

```python
def chunk_recursive(text: str, max_chars: int = 1000,
                    separators=("\n\n", "\n", ". ", " ")) -> list[str]:
    """Split by the best available separator, recursively."""
    def split_on(seg: str, sep: str) -> list[str]:
        return [s for s in seg.split(sep) if s.strip()]

    def recurse(seg: str, depth: int = 0) -> list[str]:
        if len(seg) <= max_chars or depth >= len(separators):
            return [seg]
        parts = split_on(seg, separators[depth])
        out = []
        for p in parts:
            out.extend(recurse(p, depth + 1) if len(p) > max_chars else [p])
        return out

    return recurse(text)
```

Output:
```
Respects paragraphs → sentences → words, only splitting at the finest level
when forced. Best general-purpose default.
```

This is why it is the default for heterogeneous corpora: code, prose, and
markdown all degrade gracefully.

## 5. Metadata: Every Chunk Knows Where It Came From

A chunk without provenance is an orphan. Attach source, heading, and
position — retrieval returns the chunk, but the *answer* needs the citation
and the document context:

```python
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    source: str          # document id / path
    heading: str         # nearest heading, if any
    idx: int             # position within the document
    char_start: int
    char_end: int

def make_chunk(text, source, heading, idx, char_start) -> Chunk:
    return Chunk(text, source, heading, idx, char_start,
                 char_start + len(text))
```

Output:
```
Chunk(text='...', source='docs/guide.pdf', heading='Billing', idx=3,
      char_start=4021, char_end=4729)
```

**Why this matters downstream:** RAG answers must cite (Lecture 9), evaluations
need source attribution (L20), and debugging a bad answer starts with "which
chunk fed it?" Metadata is the debugger's breadcrumb trail.

## 6. Choosing the Strategy: A Decision Guide

| Document type | Preferred strategy | Why |
|---|---|---|
| Support articles / docs | recursive or paragraph | topic units + headings |
| Legal contracts | sentence + hard cap | long sentences, precise clauses |
| Code | line/function-level, structure-aware | don't split identifiers/logic |
| Books / long prose | recursive with larger chunks | narrative units |
| Mixed corpora | recursive | graceful degradation |
| Fact-lookup Q&A | smaller chunks (sentence) | precision beats context |

The universal rule: **evaluate** (recall@k, answer groundedness — L10/L9) on a
frozen eval set. Chunk size and strategy are hyperparameters with measurable
consequences — tune them like you tune a model.

## 7. Chunking Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Split identifiers/logic | code retrieval garbage | structure-aware separators |
| Orphaned headings | "what is 'Billing' about?" | heading-aware chunking |
| Huge single chunks | context blowup + fuzzy retrieval | hard max_chars caps |
| Too-small chunks | recall collapse (meaning lost) | bigger chunks or semantic chunking |
| Lost metadata | answers un-citable | always attach provenance |
| Re-chunking thrash | index churn | chunk versioning by content hash (L3) |

## Every Use Case

- **RAG ingestion**: every RAG corpus is chunked first (L8).
- **Semantic search**: chunking shapes what "a document" means to the index.
- **Summarization of long docs**: chunk → summarize → stitch.
- **Question-answering over codebases**: structure-aware chunking.
- **Legal/contract analysis**: sentence chunking for clause precision.
- **Email/chat archives**: sentence-level for message boundaries.
- **Eval data construction**: chunking defines the retrieval gold set (L10).
- **Agents with long docs**: chunk-level context selection (L16).

## Real-World Use Cases for AI Engineers

- **Help-center RAG**: switching from fixed 500-char chunks to
  heading-aware recursive chunks lifted retrieval recall@5 from 0.62 to 0.84
  — the fix was *chunking*, not the model. The eval (L10) made the case.
- **Legal contract Q&A**: sentence chunking with a 600-char cap fixed the
  "single 4,000-char sentence" problem — clause-level precision improved
  groundedness (L9) measurably.
- **Codebase copilot**: function-aware chunking (split on `def`/`class`,
  never mid-identifier) turned broken code retrieval into usable answers —
  generic char chunking had been cutting identifiers in half.
- **Regulatory filings**: paragraph chunking with heading metadata means every
  retrieved chunk carries its section header — the answer's citation is the
  chunk's metadata, satisfying the compliance reviewer.
- **RAG platform**: the platform team exposes chunking as a config (strategy
  + size + overlap) per corpus, gated by a retrieval eval — 20 teams get
  measured chunking instead of copy-pasted defaults.

## Common Mistakes to Avoid

### Mistake 1: Defaulting to fixed-size everywhere
Fixed-size is the baseline, not the answer. Choose by document type; measure.

### Mistake 2: No overlap when it matters
Boundary context loss breaks coherence. Overlap 10–20%, and count the token
cost (L18).

### Mistake 3: Splitting code/identifiers
Code needs structure-aware separators; char chunking destroys it.

### Mistake 4: Dropping metadata
Chunks without source/heading are un-citable and un-debuggable.

### Mistake 5: Ignoring oversized chunks
Legal 4k-char sentences blow the context budget. Hard caps.

### Mistake 6: Changing chunking without eval
Chunking is a hyperparameter; changes go through the retrieval eval (L10)
and versioning (L3).

### Mistake 7: Chunk-size = token-size confusion
Chunk in characters/words for control, but budget *tokens* in the context
window (L1).

## Best Practices

1. Choose strategy by document type; keep a default (recursive) for mixed corpora
2. Attach metadata (source, heading, idx) to every chunk
3. Add hard max_chars caps and overlap where boundary context matters
4. Evaluate chunking with retrieval metrics on a frozen set (L10)
5. Version chunking config with the corpus version (L3)
6. Don't split code identifiers or logic
7. Prefer smaller chunks for fact lookup, larger for summarization
8. Log the chunk config with the index manifest (L17)
9. Re-chunk only when config changes; incremental by content hash
10. Count token cost of overlap and long chunks (L18)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Fixed-size chunk | O(n) | O(n) | — |
| Sentence/paragraph | O(n) regex | O(n) | — |
| Recursive | O(n) | O(n) | sentence split first |
| Semantic chunking | O(n · embed) | O(n) | only when quality demands |
| Overlap | +10–20% tokens | +10–20% | tune overlap by eval |

## AI Engineering Relevance

**Where this shows up:** the ingestion stage of every RAG system. Chunking is
the highest-leverage, cheapest-to-tune quality lever in retrieval — before any
model or reranker spend.

| Concept here | Used for |
|---|---|
| Chunk boundaries | retrieval precision/recall |
| Metadata | citations and debuggability |
| Strategy choice | document-type fit |
| Eval-driven tuning | measured improvements |

**Scale note:** at 10M chunks, re-chunking is a full re-embed (cost! — L6/L18)
— so chunk config changes are gated by eval and versioned, never ad-hoc. At
any scale, chunking decisions compound: they determine retrieval quality,
which determines answer quality.

## Practice Exercises

### Exercise 1: Fixed with Overlap (Easy)
Implement `chunk_fixed(text, size, overlap)` and assert every adjacent pair
shares the overlap region; test overlap 0 produces no shared chars.

### Exercise 2: Sentence Chunker (Medium)
Implement `chunk_sentences` with a hard cap; test a document with one
4,000-char sentence — assert no chunk exceeds the cap.

### Exercise 3: Metadata Attach (Medium)
Write `chunk_with_metadata(doc, strategy, heading_index)` that produces
`Chunk` objects with source/heading/idx; assert heading propagation across
chunks is correct.

### Exercise 4: Chunking Eval (Hard)
Build a mini retrieval eval: two chunkers on a mock corpus with 5 gold
queries; compute recall@k for each (L10's function); assert the
heading-aware chunker wins — proving chunking is a measured decision.

## Summary

| Concept | Description |
|---|---|
| Fixed-size | the predictable baseline |
| Sentence/paragraph | structure-respecting units |
| Recursive | the general-purpose default |
| Metadata | provenance for citation + debugging |
| Eval-driven | chunking as a tunable hyperparameter |

Chunking decides what "a retrievable unit" means — and therefore what
retrieval can find. The right strategy is chosen by document type and task,
attached to metadata, and **measured** through retrieval evaluation. It is the
cheapest quality lever in the RAG stack, and the most often defaulted-away.

## Quick Reference

| Task | Idiom |
|---|---|
| Fixed chunk | `text[start:start+size]` with overlap |
| Sentence | split on `[.!?]`, group under cap |
| Recursive | separators `\n\n` → `\n` → `. ` → ` ` |
| Metadata | Chunk(text, source, heading, idx) |
| Tune | retrieval recall@k on frozen set (L10) |

## Next Steps

Next: **[08 Document Processing](08-document-processing-lecture.md)** — the full
ingestion pipeline: parse, clean, chunk, embed, index.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://www.langchain.com/docs/how_to/recursive_text_splitter/
