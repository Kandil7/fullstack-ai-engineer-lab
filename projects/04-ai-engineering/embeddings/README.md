# Embeddings Pipeline

Embedding generation, caching, and quality evaluation for the RAG system.
Covers model selection, batch processing, and performance optimization.

---

## Model Selection

### Options Comparison

| Model                    | Dimensions | Speed    | Cost          | Quality |
| ------------------------ | ---------- | -------- | ------------- | ------- |
| OpenAI text-embedding-3-small | 1536  | Fast     | $0.02/1M tok  | Good    |
| OpenAI text-embedding-3-large | 3072  | Medium   | $0.13/1M tok  | Best    |
| nomic-embed-text (local) | 768        | Fast     | Free (GPU)    | Good    |
| all-MiniLM-L6-v2         | 384        | Fastest  | Free (CPU)    | Fair    |

### Selection Criteria

- **Development/prototyping:** `all-MiniLM-L6-v2` (free, fast)
- **Production (cost-sensitive):** `nomic-embed-text` (self-hosted)
- **Production (quality-first):** `text-embedding-3-large` (OpenAI)
- **ThanaweyaGPT default:** `text-embedding-3-small` (balance of cost/quality)

---

## Embedding Pipeline

### Ingestion Flow

```
Source Document
    ↓
Text Extraction (PDF, HTML, Markdown)
    ↓
Chunking (512 tokens, 50 overlap)
    ↓
Deduplication (content hash)
    ↓
Embedding (batch API calls)
    ↓
Storage (Qdrant + metadata)
    ↓
Indexing (HNSW parameters)
```

### Batch Processing

```python
# Pseudocode for batch embedding
def embed_batch(texts: list[str], batch_size: int = 100) -> list[list[float]]:
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        embeddings.extend([item.embedding for item in response.data])
    return embeddings
```

**Rate limits:**
- OpenAI: 3000 RPM, 2M tokens/min
- Batch size: 100 texts per request
- Retry with exponential backoff on 429 errors

---

## Caching Strategy

Embeddings are expensive to generate — cache aggressively:

### Cache Key Design

```
embedding:{model}:{content_hash}
```

Where `content_hash` is SHA-256 of the normalized text content.

### Cache Layers

| Layer     | Storage  | TTL    | Hit Rate Target |
| --------- | -------- | ------ | --------------- |
| L1 Memory | Process  | None   | —               |
| L2 Redis  | Redis    | 24 hr  | > 80%           |
| L3 Qdrant | Qdrant   | Forever| 100% (stored)   |

### Cache-Aside Flow

1. Hash the input text
2. Check Redis for `embedding:{hash}`
3. **Hit** → return cached vector
4. **Miss** → call embedding API → store in Redis → return

---

## Quality Evaluation

### Evaluation Criteria

| Metric              | Description                          | Target  |
| ------------------- | ------------------------------------ | ------- |
| Semantic similarity | Cosine similarity of related pairs   | > 0.85  |
| Retrieval accuracy  | Correct docs in top-k results        | > 80%   |
| Consistency         | Same text → same embedding           | 100%    |
| Speed               | Embedding generation latency         | < 100ms |

### Test Dataset

Create golden pairs:
- **Positive pairs:** Same concept, different wording
- **Negative pairs:** Different concepts, similar wording
- **Edge cases:** Arabic text, code snippets, math formulas

```python
# Evaluation example
test_pairs = [
    ("ما هو العدد الأولي؟", "What is a prime number?", 0.9),  # Should be similar
    ("النسبة المئوية", "Percentage", 0.85),                    # Should be similar
    ("النسبة المئوية", "Physics", 0.3),                       # Should be different
]
```

---

## Performance Optimization

### Strategies

1. **Batch requests** — embed multiple texts per API call
2. **Cache aggressively** — never re-embed unchanged content
3. **Async processing** — embed in background during ingestion
4. **Dimension reduction** — use 1536-dim instead of 3072-dim if quality allows
5. **Local models** — for prototyping, avoid API costs

### Monitoring

Track per-embedding metrics:
- Generation time
- Cache hit/miss rate
- API cost per 1000 embeddings
- Quality score (if evaluation running)

---

## Getting Started

```bash
# Install dependencies (Python)
pip install openai qdrant-client redis

# Generate embeddings for a document
python scripts/embed.py --input content.txt --output embeddings.json

# Run evaluation
python scripts/eval_embeddings.py --dataset test_pairs.json
```
