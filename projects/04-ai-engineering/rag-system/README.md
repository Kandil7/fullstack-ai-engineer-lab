# RAG System — Retrieval-Augmented Generation

Full RAG pipeline for the ThanaweyaGPT educational AI platform. From document ingestion
through retrieval to answer generation, with quality evaluation and optimization.

---

## Pipeline Overview

```
┌─────────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐     ┌────────────┐
│  Ingestion  │ ──→ │ Chunking │ ──→ │ Embedding │ ──→ │ Storage  │ ──→ │ Retrieval  │
└─────────────┘     └──────────┘     └───────────┘     └──────────┘     └─────┬──────┘
                                                                              │
┌─────────────┐     ┌──────────┐                                              │
│  Evaluation │ ←── │Generation│ ←────────────────────────────────────────────┘
└─────────────┘     └──────────┘
```

### Stage Details

| Stage        | Technology          | Input              | Output             |
| ------------ | ------------------- | ------------------ | ------------------ |
| Ingestion    | Custom pipeline     | PDF, MD, HTML      | Raw text           |
| Chunking     | Recursive splitter  | Raw text           | Text chunks        |
| Embedding    | OpenAI / local model| Text chunks        | Vectors + metadata |
| Storage      | Qdrant              | Vectors + metadata | Indexed collection |
| Retrieval    | Hybrid search       | User query         | Top-k documents    |
| Generation   | LLM (GPT-4/Claude)  | Query + context    | Answer             |

---

## Ingestion Pipeline

### Document Processing

```python
# Pseudocode for document ingestion
def ingest_document(file_path: str, course_id: str):
    # 1. Extract text
    text = extract_text(file_path)  # PDF, Markdown, HTML
    
    # 2. Chunk
    chunks = chunk_text(text, chunk_size=512, overlap=50)
    
    # 3. Embed
    vectors = embed_batch(chunks)
    
    # 4. Store with metadata
    for chunk, vector in zip(chunks, vectors):
        qdrant.upsert(
            collection="educational_content",
            point=PointStruct(
                id=uuid4(),
                vector=vector,
                payload={
                    "content": chunk.text,
                    "course_id": course_id,
                    "source_file": file_path,
                    "chunk_index": chunk.index,
                }
            )
        )
```

### Chunking Strategies

| Content Type     | Chunk Size | Overlap | Method              |
| ---------------- | ---------- | ------- | ------------------- |
| Lesson text      | 512 tokens | 50      | Recursive splitter  |
| Textbook chapter | 1024 tokens| 100     | Paragraph-aware     |
| Code snippets    | Whole chunk| 0       | No splitting        |
| Math formulas    | Whole chunk| 0       | No splitting        |

---

## Retrieval

### Query Processing

1. **Query understanding** — classify intent (factual, explanation, problem-solving)
2. **Query expansion** — add synonyms and related terms
3. **Query embedding** — convert to vector
4. **Hybrid search** — combine vector + keyword search
5. **Reranking** — cross-encoder for precision

### Retrieval Configuration

```yaml
retrieval:
  top_k: 10                    # Initial retrieval count
  final_k: 5                   # After reranking
  score_threshold: 0.65        # Minimum relevance score
  reranker: cross-encoder      # Reranking model
  hybrid_alpha: 0.7            # Vector vs keyword weight (0=pure keyword, 1=pure vector)
```

### Context Window Management

```python
def build_context(query: str, max_tokens: int = 3000) -> str:
    results = retrieve(query, top_k=10)
    
    context = []
    total_tokens = 0
    
    for doc in results:
        doc_tokens = count_tokens(doc.content)
        if total_tokens + doc_tokens > max_tokens:
            break
        context.append(doc.content)
        total_tokens += doc_tokens
    
    return "\n\n---\n\n".join(context)
```

---

## Generation

### RAG Prompt Template

```markdown
## Context
The following educational content was retrieved for this question:

{context}

## Question
{user_question}

## Instructions
1. Answer based ONLY on the provided context
2. If the context doesn't contain the answer, say "I don't have enough information"
3. Cite the source when possible
4. Use the student's language (Arabic or English)
5. Provide step-by-step explanations for problem-solving questions
```

### Generation Settings

| Parameter       | Value | Rationale                    |
| --------------- | ----- | ---------------------------- |
| temperature     | 0.3   | Lower for factual accuracy   |
| max_tokens      | 1000  | Concise responses            |
| top_p           | 0.9   | Slight diversity             |

---

## Evaluation Framework

### Metrics

| Metric               | Description                         | Target  |
| -------------------- | ----------------------------------- | ------- |
| Faithfulness         | Answer grounded in context          | > 0.85  |
| Answer relevance     | Answer addresses the question       | > 0.80  |
| Context precision    | Retrieved docs are relevant         | > 0.75  |
| Context recall       | All needed docs were retrieved      | > 0.70  |
| Hallucination rate   | Information not in context          | < 5%    |

### Evaluation Process

1. Create golden test set (100+ Q&A pairs)
2. Run RAG pipeline on each question
3. Score against criteria
4. Identify failure modes
5. Iterate on chunking/retrieval/generation
6. Track improvements over time

---

## Failure Modes and Mitigations

| Failure Mode          | Symptom                    | Mitigation                    |
| --------------------- | -------------------------- | ----------------------------- |
| Poor chunking         | Wrong context retrieved    | Tune chunk size/overlap       |
| Embedding mismatch    | Irrelevant results         | Try different embedding model |
| Context overflow      | Key info cut off           | Increase max_tokens, rerank   |
| Hallucination         | Made-up information        | Lower temperature, ground more|
| Language mismatch      | Wrong language response    | Add language filter to retrieval|
| Stale content         | Outdated information       | Re-ingest updated documents   |

---

## Performance Targets

| Metric              | Target    |
| ------------------- | --------- |
| End-to-end latency  | < 3 sec   |
| Retrieval latency   | < 200ms   |
| Generation latency  | < 2 sec   |
| Cost per query      | < $0.01   |
| Accuracy (F1)       | > 0.80    |

---

## Getting Started

```bash
# Install dependencies
pip install openai qdrant-client langchain

# Ingest sample documents
python scripts/ingest.py --input docs/sample/ --course math-101

# Query the RAG system
python scripts/query.py "What is the derivative of sin(x)?"

# Run evaluation
python scripts/evaluate.py --dataset eval/golden_set.json
```
