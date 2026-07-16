# Deep Dive: RAG System

**Last updated:** 2026-06-26

**Project reference:** `projects/04-ai-engineering/rag-system`

A comprehensive look at the Retrieval-Augmented Generation pipeline — from document
ingestion through retrieval to cited answer generation.

---

## 1. End-to-End Pipeline

### High-Level Architecture
```
Documents (PDF, MD, HTML)
    ↓
Document Loader (parse, extract text)
    ↓
Chunking Engine (split into retrieval units)
    ↓
Embedding Service (text → vectors)
    ↓
Qdrant Indexer (upsert vectors + metadata)
    ↓
┌──────────────────────────────────┐
│         Query Time               │
│                                  │
│  User Query                     │
│    ↓                             │
│  Query Embedding                │
│    ↓                             │
│  Qdrant Retrieval (top-20)      │
│    ↓                             │
│  Reranker (top-5)               │
│    ↓                             │
│  Prompt Construction            │
│    ↓                             │
│  LLM Generation (with cites)   │
│    ↓                             │
│  Cited Answer                   │
└──────────────────────────────────┘
```

### Request Flow Detail
1. User sends query: "What is the company's refund policy?"
2. Query is embedded using the same model as indexing
3. Qdrant performs hybrid search: semantic + keyword, with metadata filter
4. Top 20 candidates returned with scores and payloads
5. Reranker re-scores using cross-encoder (more accurate but slower)
6. Top 5 chunks selected as context
7. Prompt assembled with system instruction + context chunks + question
8. LLM generates answer, citing sources `[1]` through `[5]`
9. Response returned with answer + source attribution

---

## 2. Advanced Chunking

### Why Chunking Is Critical
The #1 factor in RAG quality is not the model — it's the chunking strategy. Bad chunks
mean bad retrieval, which means bad answers regardless of LLM quality.

### Strategies Compared

| Strategy | Best For | Drawback |
|---|---|---|
| Fixed-size (512 tokens) | Quick baseline | Splits mid-sentence |
| Recursive splitter | General documents | May miss semantic boundaries |
| Semantic splitter | Topic-rich documents | Requires embedding calls during indexing |
| Document-aware | Structured docs (MD, HTML) | Only works with parseable formats |
| Agentic splitter | Complex heterogeneous docs | Slow, expensive |

### Optimal Chunk Configuration
```
Chunk size:     512–1024 tokens (sweet spot for most use cases)
Overlap:        50–100 tokens (prevents losing context at boundaries)
Separators:     ["\n\n", "\n", ". ", " ", ""]
Keep separator: True (preserves readability)
```

### Metadata Enrichment
Every chunk should carry:
- `source`: filename or URL
- `section`: heading under which it appears
- `position`: chunk index within the document
- `doc_id`: unique document identifier
- `language`: detected language
- `content_type`: "text", "code", "table", "list"

---

## 3. Hybrid Search

### Why Hybrid Beats Pure Semantic
- Semantic search misses exact matches: "QDR-2024" as a product code
- Keyword search misses synonyms: "refund" vs "money back"
- Hybrid combines both: high recall without sacrificing precision

### Implementation with Qdrant
```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Semantic search
semantic_results = client.search(
    collection_name="documents",
    query_vector=embedding,
    limit=20,
    query_filter=Filter(must=[FieldCondition(key="language", match=MatchValue(value="en"))])
)

# Keyword search via payload filtering + sparse vectors (Qdrant 1.7+)
# or via external BM25 index

# Reciprocal Rank Fusion
def rrf_fusion(semantic_hits, keyword_hits, k=60):
    scores = {}
    for rank, hit in enumerate(semantic_hits):
        scores[hit.id] = scores.get(hit.id, 0) + 1 / (k + rank + 1)
    for rank, hit in enumerate(keyword_hits):
        scores[hit.id] = scores.get(hit.id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### Filter Strategies
- **Pre-filter:** apply metadata filter before vector search (reduces search space)
- **Post-filter:** retrieve top-k, then filter (may return fewer than k results)
- **Hybrid filter:** apply must-have filters pre-search, nice-to-have post-search

---

## 4. Reranking

### Cross-Encoder vs Bi-Encoder
- **Bi-encoder** (used for retrieval): encodes query and document independently, fast
- **Cross-encoder** (used for reranking): encodes query+document together, accurate
- Cross-encoder sees the interaction between query and document — much better relevance

### Reranking Pipeline
```
Retrieve top 20 (bi-encoder, ~50ms)
    ↓
Rerank top 20 (cross-encoder, ~100ms)
    ↓
Return top 5 (high precision)
```

### Popular Rerankers
| Model | Latency | Quality | Cost |
|---|---|---|---|
| Cohere Rerank v3 | ~80ms | High | $1/1000 queries |
| bge-reranker-v2-m3 | ~150ms | High | Free (self-hosted) |
| jina-reranker-v1 | ~100ms | Medium-High | Free tier available |

---

## 5. Evaluation Framework

### RAGAs Metrics

**Context Precision**
```
= (number of relevant chunks in top-k) / k
Measures: are the retrieved chunks actually relevant?
High precision = less noise in context
```

**Context Recall**
```
= (relevant chunks retrieved) / (total relevant chunks in corpus)
Measures: did we find all the relevant information?
High recall = complete answers
```

**Faithfulness**
```
= (claims in answer supported by context) / (total claims in answer)
Measures: is the LLM making things up?
High faithfulness = trustworthy answers
```

**Answer Relevancy**
```
= similarity between answer and query
Measures: does the answer actually address the question?
High relevancy = on-topic responses
```

### Evaluation Dataset Structure
```json
{
  "question": "What is the refund policy?",
  "answer": "Refunds are available within 30 days...",
  "contexts": ["Refund Policy: Items may be returned within 30 days..."],
  "ground_truth": "Full refund within 30 days of purchase with receipt."
}
```

### Automated Eval Pipeline
```
1. Load evaluation dataset (20-50 Q&A pairs)
2. For each question:
   a. Run RAG pipeline
   b. Capture: retrieved chunks, generated answer, latency, tokens
3. Compute RAGAs metrics against ground truth
4. Generate report: aggregate scores + per-question breakdown
5. Compare against baseline (previous prompt/model/chunking change)
6. Gate: fail deployment if metrics degrade beyond threshold
```

---

## 6. Common Failure Modes

| Failure | Root Cause | Fix |
|---|---|---|
| Answer not in retrieved context | Poor retrieval, wrong chunking | Improve chunking, add hybrid search |
| LLM ignores context | Prompt too vague, context too long | Explicit instructions, truncate context |
| Retrieved chunks irrelevant | Embedding model mismatch, no reranking | Match embedding model, add reranker |
| Hallucination | Context insufficient, model too creative | Stronger faithfulness prompt, lower temperature |
| Slow response | Too many chunks, slow reranker | Reduce top-k, batch embedding calls |
| Wrong language retrieved | No language filter in retrieval | Add language metadata filter |

### Debugging Checklist
1. **Retrieve only:** run retrieval without LLM — are the chunks relevant?
2. **Context check:** put retrieved chunks in prompt — does the answer improve?
3. **Embedding inspection:** compare query embedding similarity with correct chunk
4. **Chunk inspection:** read the actual chunk text — is it coherent and complete?
5. **Prompt audit:** is the system message clear about using only provided context?

---

## 7. Production Deployment

### Performance Budgets
```
Query embedding:     < 50ms
Qdrant retrieval:    < 100ms
Reranking:           < 150ms
LLM generation:      < 2000ms (streaming)
Total end-to-end:    < 3000ms
```

### Cost Optimization
- Cache embeddings for repeated queries (semantic deduplication)
- Use smaller embedding model for non-critical paths
- Batch embedding calls during indexing (not query time)
- Cache retrieval results for identical queries (24h TTL)
- Use cheaper LLM for simple questions, expensive for complex

### Monitoring
- Retrieval latency (p50, p95, p99)
- RAGAs scores over time (drift detection)
- Hallucination rate (manual sampling + automated detection)
- Cost per query (embedding + retrieval + generation)
- Error rate and failure modes

---

## Self-Check

Can you explain:
- Why chunking strategy matters more than LLM choice?
- How hybrid search combines semantic and keyword strengths?
- The tradeoff between retrieval speed and reranking accuracy?
- How RAGAs `faithfulness` detects hallucinations?
- The debugging flow when RAG produces a bad answer?

---

## ملخص عربي (Arabic Summary)

نظرة معمقة في نظام RAG: خط الأنابيب الكامل من تحميل المستندات إلى توليد الإجابات
المدعومة بالمراجع. يشمل التقسيم المتقدم، البحث الهجين، إعادة الترتيب، إطار تقييم
RAGAs، أوضاع الفشل الشائعة، والنشر الإنتاجي مع ميزانيات الأداء والتكلفة.
