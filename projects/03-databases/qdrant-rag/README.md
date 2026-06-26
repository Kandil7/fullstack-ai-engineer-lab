# Qdrant Vector Database — RAG Storage

Qdrant implementation for vector storage, similarity search, and retrieval-augmented
generation (RAG) in the ThanaweyaGPT educational platform.

---

## Collection Design

### Primary Collection: `educational_content`

Stores embeddings for all educational material (lessons, textbook chapters, exercises).

| Field           | Type       | Purpose                              |
| --------------- | ---------- | ------------------------------------ |
| `id`            | UUID       | Point identifier                     |
| `vector`        | float[1536]| Embedding vector (OpenAI ada-002)    |
| `content`       | string     | Original text chunk                  |
| `source_type`   | keyword    | lesson, textbook, exercise, website  |
| `course_id`     | keyword    | Associated course                    |
| `module_id`     | keyword    | Associated module                    |
| `language`      | keyword    | ar (Arabic), en (English), tr (Turkish)|
| `difficulty`    | integer    | 1-5 difficulty level                 |
| `created_at`    | datetime   | Ingestion timestamp                  |

### Collection: `chat_history`

Stores embeddings of past chat messages for context retrieval.

| Field           | Type       | Purpose                              |
| --------------- | ---------- | ------------------------------------ |
| `vector`        | float[1536]| Message embedding                    |
| `message`       | string     | Original message text                |
| `user_id`       | keyword    | Message author                       |
| `session_id`    | keyword    | Chat session                         |
| `role`          | keyword    | user, assistant                      |
| `created_at`    | datetime   | Message timestamp                    |

---

## Embedding Strategies

### Model Selection

| Model              | Dimensions | Cost       | Quality  | Use Case           |
| ------------------ | ---------- | ---------- | -------- | ------------------ |
| text-embedding-3-small | 1536   | $0.02/1M   | Good     | General content    |
| text-embedding-3-large | 3072   | $0.13/1M   | Best     | High-precision RAG |
| nomic-embed-text   | 768        | Self-hosted| Good     | Cost-sensitive     |

### Chunking Strategy

Content is chunked before embedding:

- **Lesson content:** 512 tokens with 50-token overlap
- **Textbook chapters:** 1024 tokens with 100-token overlap
- **Chat messages:** Individual messages (no chunking)
- **Code snippets:** Entire snippet as single vector

---

## Hybrid Search

Combine semantic (vector) search with keyword (exact) matching:

```python
# Qdrant hybrid search example
results = client.search(
    collection_name="educational_content",
    query_vector=[0.1, 0.2, ...],  # Query embedding
    query_filter=Filter(
        must=[
            FieldCondition(key="language", match=MatchValue(value="ar")),
            FieldCondition(key="course_id", match=MatchValue(value="math-101")),
        ]
    ),
    limit=10,
    score_threshold=0.7,
)
```

### Search Pipeline

1. **Query embedding** — embed user question
2. **Vector search** — find top-20 semantically similar chunks
3. **Metadata filter** — apply curriculum/language/difficulty filters
4. **Keyword boost** — boost exact matches on key terms
5. **Rerank** — cross-encoder reranking of top-10
6. **Return top-5** — provide to LLM as context

---

## Metadata Filtering for Curriculum Alignment

Filter retrieval results by educational metadata:

```json
{
  "must": [
    {"key": "language", "match": {"value": "ar"}},
    {"key": "course_id", "match": {"value": "physics-201"}},
    {"key": "difficulty", "range": {"gte": 2, "lte": 4}}
  ]
}
```

This ensures the AI tutor retrieves content appropriate for the student's:
- **Language** (Arabic primary, Turkish secondary)
- **Course** (aligned to enrolled curriculum)
- **Level** (not too easy, not too hard)

---

## Performance Targets

| Metric              | Target    | Current |
| ------------------- | --------- | ------- |
| Search latency (p95)| < 100ms   | —       |
| Ingestion rate      | > 100 docs/sec | —  |
| Recall@10           | > 0.85    | —       |
| Precision@5         | > 0.70    | —       |

---

## Getting Started

```bash
# Start Qdrant
docker compose -f infra/docker/docker-compose.yml up -d qdrant

# Access REST API
curl http://localhost:6333/collections

# Access Web Dashboard
# Open http://localhost:6333/dashboard in browser
```
