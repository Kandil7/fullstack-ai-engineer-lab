# Learning Path: RAG Systems with Qdrant

**Last updated:** 2026-08-06

**Goal:** build a production-quality Retrieval-Augmented Generation system using Qdrant
as the vector database, covering the full pipeline from embedding to cited answers.

**Primary project:** `projects/04-ai-engineering/rag-system`

---

## Milestones

### 1. Embeddings Fundamentals (Week 1)
- What embeddings are: dense vector representations of meaning
- Embedding models: OpenAI `text-embedding-3-small`, Cohere `embed-v3`, open-source `bge-base`
- Dimensions: 384 vs 768 vs 1536 — tradeoff between cost and quality
- Cosine similarity vs dot product vs Euclidean distance
- When to normalize vectors and why
- Embedding API: input → tokenization → model → vector array

### 2. Chunking Strategies (Week 1–2)
- Why chunking matters: context windows, retrieval precision, noise reduction
- **Fixed-size chunking:** 512 tokens with 50-token overlap — simple baseline
- **Recursive text splitting:** split by paragraphs → sentences → tokens
- **Semantic chunking:** split at topic boundaries using embedding similarity
- **Document-structure-aware:** split by markdown headers, HTML sections, code blocks
- Chunk size tradeoffs:
  - Too small → loses context, retrieval returns fragments
  - Too large → noisy retrieval, wastes context window
- Metadata enrichment: add source filename, section title, page number to each chunk

### 3. Qdrant Setup & Collection Management (Week 2)
- Qdrant concepts: collections, points, vectors, payloads
- Docker setup: `docker run -p 6333:6333 qdrant/qdrant`
- Creating a collection with distance metric and vector dimensions
- Payload schema design: what metadata to store, indexable fields
- Filtering: payload-based filters (`must`, `should`, `must_not`)
- Index types: HNSW (graph), flat (exact), on-disk for large datasets

```python
# Collection creation example
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient("localhost", port=6333)
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
```

### 4. Indexing Pipeline (Week 2–3)
- End-to-end pipeline: document → chunks → embed → upsert to Qdrant
- Batch processing: embed in batches of 100+ to reduce API calls
- Idempotency: deterministic point IDs from content hash or source+position
- Incremental indexing: detect new/changed documents, avoid re-embedding
- Error handling: retry failed embeddings, partial upsert recovery
- Progress tracking: log indexed count, failed chunks, timing

### 5. Retrieval Patterns (Week 3–4)
- **Semantic search:** embed query → cosine similarity → top-k
- **Hybrid search:** combine semantic + keyword (BM25) scores
  - Qdrant `hybrid` search or external fusion (RRF, weighted sum)
- **Filtered retrieval:** narrow by metadata before similarity search
  - Example: search only within "legal" documents, or published after 2023
- **Multi-query retrieval:** expand user query into sub-queries, merge results
- **Parent-child retrieval:** retrieve small chunks, return surrounding context
- **MMR (Maximal Marginal Relevance):** diversity in results — avoid near-duplicates
- Recall@k vs Precision@k vs MRR — when each matters

### 6. Reranking (Week 4)
- Why rerank: first-stage retrieval is approximate, reranker is precise
- Cross-encoder rerankers: `cohere-rerank`, `bge-reranker-v2`, `jina-reranker`
- Pipeline: retrieve top 20 → rerank → return top 5
- Cost vs quality: reranking 20 docs adds ~100ms, dramatically improves relevance
- When to skip reranking: low-latency requirements, small collections

### 7. LLM Generation with Context (Week 4–5)
- Prompt structure: system message + retrieved context + user question
- Citation format: ask LLM to cite `[1]`, `[2]` matching source chunks
- Context window management: fit top-k chunks within token budget
- Faithfulness: LLM should only answer from provided context
- Hallucination detection: flag answers not grounded in retrieved chunks
- Streaming: stream LLM response for better UX

### 8. Evaluation Framework (Week 5–6)
- **RAGAs metrics:**
  - `context_precision`: are retrieved chunks relevant?
  - `context_recall`: does retrieval cover the ground truth?
  - `faithfulness`: is the answer grounded in context?
  - `answer_relevancy`: does the answer address the question?
- **Custom metrics:**
  - End-to-end latency (retrieval + generation)
  - Token usage per query (cost tracking)
  - Citation accuracy (does `[1]` actually correspond to the source?)
- Evaluation dataset: curated Q&A pairs with ground truth answers
- Automated eval pipeline: run metrics on every prompt/model change

### 9. Production Considerations (Week 6–7)
- Caching: cache embeddings, cache retrieval results for repeated queries
- Rate limiting: embedding API and LLM API rate limits
- Monitoring: query latency, retrieval quality drift, error rates
- A/B testing: compare chunking strategies, models, prompt templates
- Data versioning: track which document versions are indexed

---

## The 20% That Unlocks 80%

| Concept | Why It Matters |
|---|---|
| Chunking strategy | Directly controls retrieval quality — more than model choice |
| Hybrid search | Catches what semantic alone misses (exact names, codes) |
| Reranking | Cheap quality boost: 100ms for significantly better answers |
| RAGAs evaluation | Quantifiable quality instead of vibes-based assessment |
| Metadata filtering | Narrows search space, dramatically improves precision |

---

## Pipeline Architecture

```
User Query
    ↓
Query Embedding (text-embedding-3-small)
    ↓
Qdrant Retrieval (hybrid: semantic + BM25)
    ↓  top 20 results
Reranker (cohere-rerank / bge-reranker)
    ↓  top 5 results
Prompt Construction (context + question)
    ↓
LLM Generation (with citations)
    ↓
Cited Answer + Sources
```

---

## Daily Pattern

1h theory/research paper reading → 3h build (one pipeline stage) → 1h eval/measure → 1h recall/Anki.

---

## Key Resources

| Topic | Resource |
|---|---|
| Qdrant docs | [qdrant.tech/documentation](https://qdrant.tech/documentation/) |
| RAGAs | [docs.ragas.io](https://docs.ragas.io/) |
| LangChain chunking | [python.langchain.com](https://python.langchain.com) |
| OpenAI embeddings | [platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings) |
| Cohere rerank | [docs.cohere.com/docs/reranking](https://docs.cohere.com/docs/reranking) |

---

## Practice Tasks

1. Set up Qdrant via Docker and create a collection with 1536-dim cosine vectors
2. Build an indexing pipeline: load 10 PDFs → chunk → embed → upsert
3. Implement semantic search with metadata filtering
4. Add hybrid search combining Qdrant + BM25
5. Integrate a reranker and measure improvement in precision@5
6. Build a RAG endpoint: query → retrieve → rerank → generate with citations
7. Create an eval dataset of 20 Q&A pairs and run RAGAs metrics
8. Compare chunking strategies (fixed vs recursive vs semantic) with eval metrics

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                   RAG System Architecture              │
│                                                       │
│  ┌──────────────┐         ┌─────────────────────┐    │
│  │  Ingestion   │         │    Query Pipeline    │    │
│  │  Pipeline    │         │                      │    │
│  │              │         │  Query → Embed       │    │
│  │  Documents   │         │    ↓                 │    │
│  │    ↓         │         │  Qdrant Search       │    │
│  │  Chunker     │         │    ↓                 │    │
│  │    ↓         │         │  Reranker            │    │
│  │  Embedder    │         │    ↓                 │    │
│  │    ↓         │         │  Prompt + Context    │    │
│  │  Qdrant ↑    │         │    ↓                 │    │
│  └──────────────┘         │  LLM → Cited Answer  │    │
│                           └─────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

### Chunking Strategy Comparison

```
Fixed-size (512 tokens, 50 overlap)
├── Pros: simple, fast, predictable
├── Cons: splits mid-sentence, loses context
└── Use when: quick prototype, uniform documents

Recursive text splitting
├── Pros: respects paragraph/sentence boundaries
├── Cons: may create uneven chunk sizes
└── Use when: general documents, mixed content

Semantic chunking
├── Pros: topic-aware splits, coherent chunks
├── Cons: requires embedding calls during indexing
└── Use when: quality matters more than speed

Document-structure-aware
├── Pros: leverages inherent document structure
├── Cons: only works with parseable formats
└── Use when: structured docs (markdown, HTML, PDFs)
```

### Retrieval Pattern Decision Tree

```
What type of query?
├─ Exact match (codes, names) → Keyword/BM25
├─ Conceptual (how does X work?) → Semantic search
├─ Mixed → Hybrid search (semantic + BM25)
│
Need high precision?
├─ YES → Add reranking step (top 20 → top 5)
└─ NO → Return top-k directly
│
Have metadata filters?
├─ Language filter → Pre-filter before search
├─ Date filter → Pre-filter before search
└─ Topic filter → Pre-filter or post-filter depending on selectivity
```

### Embedding Model Selection

| Model | Dimensions | Speed | Quality | Cost |
|---|---|---|---|---|
| text-embedding-3-small | 1536 | Fast | Good | $0.02/1M tokens |
| text-embedding-3-large | 3072 | Medium | Better | $0.13/1M tokens |
| Cohere embed-v3 | 1024 | Fast | Good | $0.10/1M tokens |
| bge-base-en | 768 | Fast | Good | Free (self-hosted) |
| multilingual-e5-large | 1024 | Medium | Good multilingual | Free (self-hosted) |

### Evaluation Metrics Deep Dive

**Context Precision@k**
```
Precision@5 = (relevant chunks in top 5) / 5
Example: 3 relevant chunks in top 5 → 0.6
Target: > 0.7
```

**Faithfulness Score**
```
Faithfulness = (claims supported by context) / (total claims)
Example: Answer makes 10 claims, 8 supported → 0.8
Target: > 0.85
```

**Answer Relevancy**
```
Relevancy = cosine similarity(answer_embedding, query_embedding)
Example: answer closely matches query intent → 0.92
Target: > 0.8
```

### Qdrant Collection Configuration

```python
from qdrant_client.models import (
    Distance, VectorParams, OptimizersConfigDiff,
    HnswConfigDiff, QuantizationConfig
)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE,
        on_disk=True,           # store vectors on disk for large collections
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,
    ),
    hnsw_config=HnswConfigDiff(
        m=16,                   # connections per node
        ef_construct=100,       # build-time search width
        full_scan_threshold=10000,
    ),
)

# Create payload indexes for filtered search
client.create_payload_index(
    collection_name="documents",
    field_name="language",
    field_schema="keyword",
)
client.create_payload_index(
    collection_name="documents",
    field_name="source_type",
    field_schema="keyword",
)
```

### Production Checklist

- [ ] Embedding model matches between indexing and query time
- [ ] Chunk size tested with eval dataset (512 vs 1024)
- [ ] Metadata fields indexed in Qdrant for filtered search
- [ ] Reranker integrated and latency measured
- [ ] Eval dataset created with 20+ Q&A pairs
- [ ] RAGAs metrics computed and baseline recorded
- [ ] Caching layer for repeated queries
- [ ] Error handling for embedding API failures
- [ ] Monitoring dashboards for latency and quality

---

## Self-Check

Can you explain:
- Why chunk size and overlap affect retrieval quality?
- The difference between semantic search and hybrid search?
- How reranking improves upon first-stage retrieval?
- What RAGAs `faithfulness` measures and how to improve it?
- When to use filtered retrieval vs post-retrieval filtering?
- How to choose between embedding models for your use case?
- The tradeoffs of HNSW parameters (m, ef_construct)?

---

## ملخص عربي (Arabic Summary)

مسار بناء نظام RAG مع Qdrant: من أساسيات التضمينات واستراتيجيات التقسيم إلى الإعداد
والفهرسة والبحث الدلالي والهجيني، مع إعادة الترتيب وتقييم الجودة بـ RAGAs.
يشمل مخططات المعمارية ومخططات اتخاذ القرار لاستراتيجيات البحث والتقسيم، وإعدادات
Qdrant التفصيلية، ومقارنة نماذج التضمين، وقائمة التحقق للنشر الإنتاجي.
