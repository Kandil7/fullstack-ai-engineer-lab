# Glossary: RAG Systems

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| RAG | Retrieval-Augmented Generation | Combine retrieval with generation |
| Ingestion | Processing documents for storage | Offline, preprocessing step |
| Chunking | Splitting documents into pieces | Balance context and precision |
| Retrieval | Finding relevant documents | Semantic or keyword-based |
| Context | Information provided to LLM | The "augmented" in RAG |
| Grounding | Answer based on retrieved docs | Prevents hallucination |
| Faithfulness | Answer supported by context | Quality metric |
| Relevance | Answer matches the question | Quality metric |
| Hallucination | LLM makes up facts | What RAG helps prevent |
| Vector Store | Database for embeddings | ChromaDB, Pinecone |
| Source Citation | Referencing retrieved docs | Builds trust |
| Chunk Overlap | Shared text between chunks | Maintains context |

---

## Detailed Definitions

### RAG (Retrieval-Augmented Generation)

**Definition:** A technique that combines information retrieval with language model generation. Instead of relying solely on the model's training data, RAG retrieves relevant documents and uses them as context for generating answers.

**Example:**
```python
# Without RAG (limited to training data)
response = llm.generate("What is our company's vacation policy?")
# May hallucinate or say "I don't know"

# With RAG (grounded in actual documents)
relevant_docs = retrieve("vacation policy", company_documents)
response = llm.generate(
    f"Based on: {relevant_docs}\n\nWhat is our vacation policy?"
)
# Answer is grounded in actual policy documents
```

**Related Terms:** Ingestion, Retrieval, Context, Grounding

**Key Benefits:**
- Up-to-date information
- Reduced hallucination
- Source citations
- Private data access

---

### Ingestion

**Definition:** The offline process of loading, processing, and indexing documents for later retrieval. Includes chunking, embedding, and storing.

**Example:**
```python
class IngestionPipeline:
    def ingest(self, documents):
        # Step 1: Load documents
        loaded = self.load_documents(documents)
        
        # Step 2: Chunk documents
        chunks = self.chunk_documents(loaded)
        
        # Step 3: Generate embeddings
        embeddings = self.embed_chunks(chunks)
        
        # Step 4: Store in vector database
        self.store_vectors(chunks, embeddings)
        
        return len(chunks)
```

**Related Terms:** Chunking, Embedding, Vector Store

**Key Steps:**
1. Load documents
2. Clean/preprocess
3. Chunk text
4. Generate embeddings
5. Store in vector database

---

### Chunking

**Definition:** Splitting long documents into smaller, manageable pieces for embedding and retrieval. Balances context preservation with retrieval precision.

**Example:**
```python
def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

# Example
document = "This is a long document..." * 100
chunks = chunk_text(document, chunk_size=500)
print(f"Created {len(chunks)} chunks")
```

**Related Terms:** Overlap, Context Window, Embedding

**Strategies:**
- Fixed-size: Simple, consistent
- Sentence-based: Preserves grammar
- Semantic: Splits at meaning boundaries
- Recursive: Hierarchical splitting

---

### Retrieval

**Definition:** The process of finding and returning the most relevant documents for a given query from the vector database.

**Example:**
```python
def retrieve(query, vector_db, top_k=5):
    """Retrieve relevant documents."""
    # Generate query embedding
    query_embedding = embed(query)
    
    # Search vector database
    results = vector_db.search(
        query_embedding,
        top_k=top_k
    )
    
    return results

# Usage
relevant_docs = retrieve(
    "How do I reset my password?",
    company_kb,
    top_k=3
)
```

**Related Terms:** Similarity Search, Vector Database, Relevance

**Methods:**
- Semantic: Embedding similarity
- Keyword: BM25, TF-IDF
- Hybrid: Combined approaches
- Reranking: Post-retrieval optimization

---

### Context

**Definition:** The information retrieved and formatted for the language model to use when generating a response. The "augmented" part of RAG.

**Example:**
```python
def build_context(query, retrieved_docs, max_tokens=3000):
    """Build context for generation."""
    context_parts = []
    current_tokens = 0
    
    for doc in retrieved_docs:
        doc_tokens = len(doc["content"].split())
        if current_tokens + doc_tokens > max_tokens:
            break
        context_parts.append(doc["content"])
        current_tokens += doc_tokens
    
    return "\n\n".join(context_parts)

# Usage
context = build_context(query, retrieved_docs)
response = llm.generate(f"Context: {context}\n\nQuestion: {query}")
```

**Related Terms:** Prompt, Token Limit, Generation

**Key Considerations:**
- Token budget
- Document ordering
- Relevance ranking
- Source attribution

---

### Grounding

**Definition:** Ensuring the language model's response is based on retrieved information rather than its training data. Reduces hallucination and improves accuracy.

**Example:**
```python
# Without grounding
prompt = "What is our return policy?"
response = llm.generate(prompt)
# May hallucinate or use training data

# With grounding
docs = retrieve("return policy", company_docs)
prompt = f"""Based on these documents:
{docs}

What is our return policy?
Answer only based on the provided documents."""

response = llm.generate(prompt)
# Response is grounded in actual policy
```

**Related Terms:** Faithfulness, Hallucination, RAG

**Why Important:**
- Prevents making up facts
- Enables citations
- Builds trust
- Ensures accuracy

---

### Faithfulness

**Definition:** A quality metric measuring whether the generated answer is supported by the retrieved context. Low faithfulness indicates hallucination.

**Example:**
```python
def evaluate_faithfulness(answer, context):
    """Evaluate if answer is grounded in context."""
    prompt = f"""Evaluate if this answer is faithful to the context.

Context: {context}
Answer: {answer}

Rate 0-1:
- 0: Contains hallucinations
- 0.5: Partially supported
- 1: Fully supported

Score:"""
    
    response = llm.generate(prompt, temperature=0.0)
    return float(response)

# Usage
score = evaluate_faithfulness(answer, context)
if score < 0.7:
    print("Warning: Low faithfulness - possible hallucination")
```

**Related Terms:** Grounding, Hallucination, Quality Metric

**Importance:**
- Critical quality metric
- Detects hallucination
- Enables monitoring
- Guides improvements

---

### Relevance

**Definition:** A quality metric measuring whether the retrieved documents are actually relevant to the query. Low relevance means poor retrieval.

**Example:**
```python
def evaluate_relevance(query, retrieved_docs):
    """Evaluate if retrieved docs are relevant."""
    prompt = f"""Rate the relevance of these documents to the query.

Query: {query}
Documents: {[doc['content'][:200] for doc in retrieved_docs]}

Rate 0-1:
- 0: Completely irrelevant
- 0.5: Partially relevant
- 1: Highly relevant

Score:"""
    
    response = llm.generate(prompt, temperature=0.0)
    return float(response)

# Usage
score = evaluate_relevance(query, retrieved_docs)
if score < 0.5:
    print("Warning: Low relevance - retrieval may need improvement")
```

**Related Terms:** Retrieval Quality, Precision, Recall

**Importance:**
- Measures retrieval quality
- Guides chunking/retrieval improvements
- Critical for RAG success

---

### Hallucination

**Definition:** When a language model generates information that is factually incorrect, nonsensical, or not supported by the context. RAG helps reduce this by grounding responses in retrieved documents.

**Example:**
```python
# Hallucination example
prompt = "What is the capital of Mars?"
response = llm.generate(prompt)
# LLM might hallucinate an answer like "The capital of Mars is Olympus City"

# RAG prevents this by providing context
context = "Mars does not have any cities or population."
prompt = f"Context: {context}\n\nWhat is the capital of Mars?"
response = llm.generate(prompt)
# Response: "Mars does not have a capital as it has no cities or population."
```

**Related Terms:** Grounding, Faithfulness, Accuracy

**Causes:**
- Lack of relevant context
- Model uncertainty
- Training data gaps
- Conflicting information

---

### Vector Store

**Definition:** A specialized database optimized for storing, indexing, and querying high-dimensional vectors (embeddings). Enables fast similarity search.

**Example:**
```python
import chromadb

# Create vector store
client = chromadb.Client()
collection = client.create_collection("documents")

# Add documents
collection.add(
    documents=["Doc 1", "Doc 2"],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(
    query_texts=["similar document"],
    n_results=2
)
```

**Related Terms:** Embedding, Similarity Search, HNSW

**Popular Options:**
- ChromaDB: Local, simple
- Pinecone: Managed, scalable
- Weaviate: Self-hosted, hybrid
- Milvus: High performance

---

### Source Citation

**Definition:** Referencing the specific documents or passages used to generate an answer. Builds trust and enables verification.

**Example:**
```python
# With source citations
prompt = f"""Answer the question based on the context.
Cite sources using [1], [2], etc.

Context:
[Source 1] Our return policy allows returns within 30 days...
[Source 2] Items must be in original packaging...

Question: What is the return policy?

Answer:"""

# Response includes citations
# "Our return policy allows returns within 30 days [1]. 
#  Items must be in original packaging [2]."
```

**Related Terms:** Trust, Verification, Grounding

**Benefits:**
- Enables fact-checking
- Builds user trust
- Supports auditing
- Identifies sources

---

### Chunk Overlap

**Definition:** The number of shared tokens between consecutive chunks. Maintains context across chunk boundaries, preventing information loss.

**Example:**
```python
def chunk_with_overlap(text, chunk_size=500, overlap=50):
    """Create overlapping chunks."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

# Without overlap
# Chunk 1: [...words 1-500]
# Chunk 2: [...words 501-1000]
# Problem: Context lost at boundary

# With overlap
# Chunk 1: [...words 1-500]
# Chunk 2: [...words 451-950]
# Overlap: Words 451-500 appear in both
```

**Related Terms:** Chunking, Context, Continuity

**Typical Values:**
- 10-20% of chunk size
- 50-100 words overlap
- More overlap = more context, more storage

---

### Precision

**Definition:** The proportion of retrieved documents that are actually relevant. Higher precision means fewer irrelevant results.

**Example:**
```python
def calculate_precision(retrieved, relevant):
    """Calculate precision@k."""
    retrieved_set = set(retrieved)
    relevant_set = set(relevant)
    
    if not retrieved_set:
        return 0.0
    
    found = len(retrieved_set.intersection(relevant_set))
    return found / len(retrieved_set)

# Example
relevant_docs = {"doc1", "doc2", "doc3"}
retrieved_docs = {"doc1", "doc2", "doc4"}

precision = calculate_precision(retrieved_docs, relevant_docs)
print(f"Precision: {precision:.2f}")  # 0.67 (2 of 3 are relevant)
```

**Related Terms:** Recall, F1 Score, Retrieval Quality

**Trade-off:**
- Higher precision = fewer results, less noise
- Lower precision = more results, potentially more relevant

---

### Recall

**Definition:** The proportion of relevant documents that were successfully retrieved. Higher recall means fewer missed relevant results.

**Example:**
```python
def calculate_recall(retrieved, relevant):
    """Calculate recall@k."""
    retrieved_set = set(retrieved)
    relevant_set = set(relevant)
    
    if not relevant_set:
        return 0.0
    
    found = len(retrieved_set.intersection(relevant_set))
    return found / len(relevant_set)

# Example
relevant_docs = {"doc1", "doc2", "doc3", "doc4", "doc5"}
retrieved_docs = {"doc1", "doc2", "doc3"}

recall = calculate_recall(retrieved_docs, relevant_docs)
print(f"Recall: {recall:.2f}")  # 0.60 (found 3 of 5)
```

**Related Terms:** Precision, F1 Score, Retrieval Quality

**Trade-off:**
- Higher recall = more results, potentially more noise
- Lower recall = fewer results, potentially missing relevant docs

---

### Query Expansion

**Definition:** Modifying the search query to improve retrieval quality. Can include adding synonyms, reformulating, or generating multiple queries.

**Example:**
```python
def expand_query(query, llm):
    """Expand query with related terms."""
    prompt = f"""Generate 3 alternative phrasings of this query:
    
Query: {query}

Return them as a list."""
    
    response = llm.generate(prompt)
    # Parse response into list
    expanded_queries = [query] + parse_list(response)
    
    return expanded_queries

# Usage
queries = expand_query("How do I reset my password?", llm)
# ["How do I reset my password?",
#  "Password reset instructions",
#  "Change my password",
#  "Forgot password help"]
```

**Related Terms:** Retrieval, Query, Synonym

**Benefits:**
- Improves recall
- Handles synonyms
- Better coverage
- More robust retrieval

---

### Reranking

**Definition:** Reordering retrieved documents after initial retrieval to improve relevance. Often uses more sophisticated models than the initial retrieval.

**Example:**
```python
def rerank(query, retrieved_docs, top_k=5):
    """Rerank retrieved documents."""
    # Using cross-encoder for reranking
    from sentence_transformers import CrossEncoder
    
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # Create query-document pairs
    pairs = [(query, doc["content"]) for doc in retrieved_docs]
    
    # Get relevance scores
    scores = model.predict(pairs)
    
    # Sort by score
    ranked = sorted(
        zip(retrieved_docs, scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [doc for doc, score in ranked[:top_k]]
```

**Related Terms:** Retrieval, Cross-Encoder, Quality

**Why Important:**
- Improves precision
- Better than initial retrieval
- Uses more compute for quality
- Common in production RAG

---

### Document Store

**Definition:** A database storing the original documents and their metadata, separate from the vector store. Used for retrieving full document content.

**Example:**
```python
# Separate document store from vector store
class DocumentStore:
    def __init__(self):
        self.documents = {}
    
    def add(self, doc_id, content, metadata):
        self.documents[doc_id] = {
            "content": content,
            "metadata": metadata
        }
    
    def get(self, doc_id):
        return self.documents.get(doc_id)

# Vector store for retrieval
vector_store.add(doc_id, embedding, metadata)

# Document store for full content
doc_store.add(doc_id, full_content, metadata)
```

**Related Terms:** Vector Store, Metadata, Content

**Why Separate:**
- Vector store optimized for search
- Document store optimized for retrieval
- Different storage requirements
- Flexible management

---

### Token Budget

**Definition:** The maximum number of tokens allocated for context in a RAG prompt. Balances completeness with model limits and cost.

**Example:**
```python
def build_context_with_budget(query, docs, token_budget=3000):
    """Build context within token budget."""
    context_parts = []
    current_tokens = 0
    
    for doc in docs:
        doc_tokens = len(doc["content"].split())
        if current_tokens + doc_tokens > token_budget:
            # Truncate or skip
            remaining = token_budget - current_tokens
            if remaining > 100:  # Minimum useful chunk
                truncated = " ".join(doc["content"].split()[:remaining])
                context_parts.append(truncated)
            break
        
        context_parts.append(doc["content"])
        current_tokens += doc_tokens
    
    return "\n\n".join(context_parts)
```

**Related Terms:** Context, Token, Budget

**Considerations:**
- Model context window
- Cost per token
- Completeness vs. precision
- Document importance

---

### Semantic Search

**Definition:** Search based on meaning rather than keywords. Uses embeddings to find documents that are semantically similar to the query.

**Example:**
```python
# Keyword search fails on synonyms
# Query: "puppy" won't match "dog"

# Semantic search succeeds
query_embedding = embed("puppy")
doc_embedding = embed("dog")
similarity = cosine_similarity(query_embedding, doc_embedding)
# High similarity despite different words
```

**Related Terms:** Embedding, Similarity, Meaning

**Advantages:**
- Understands synonyms
- Grasps context
- Handles paraphrases
- Cross-lingual potential

---

### Hybrid Search

**Definition:** Combining semantic search with keyword search for better retrieval. Leverages strengths of both approaches.

**Example:**
```python
def hybrid_search(query, vector_db, keyword_index, alpha=0.7):
    """Combine semantic and keyword search."""
    # Semantic search
    semantic_results = vector_db.search(embed(query), top_k=10)
    
    # Keyword search
    keyword_results = keyword_index.search(query, top_k=10)
    
    # Combine scores
    combined = {}
    for doc in semantic_results:
        combined[doc.id] = alpha * doc.score
    
    for doc in keyword_results:
        if doc.id in combined:
            combined[doc.id] += (1 - alpha) * doc.score
        else:
            combined[doc.id] = (1 - alpha) * doc.score
    
    # Sort by combined score
    ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    
    return ranked[:5]
```

**Related Terms:** Semantic, Keyword, BM25

**Benefits:**
- Better recall
- Handles exact matches
- More robust
- Production standard

---

### Evaluation

**Definition:** Systematically measuring RAG system quality across multiple dimensions (retrieval, generation, faithfulness).

**Example:**
```python
class RAGEvaluator:
    def evaluate(self, test_cases):
        results = []
        
        for case in test_cases:
            # Get RAG response
            response = self.rag.generate(case.question)
            
            # Evaluate components
            retrieval_score = self.evaluate_retrieval(
                case.question,
                response["context_docs"]
            )
            
            generation_score = self.evaluate_generation(
                response["answer"],
                case.expected_answer
            )
            
            faithfulness_score = self.evaluate_faithfulness(
                response["answer"],
                response["context_docs"]
            )
            
            results.append({
                "retrieval": retrieval_score,
                "generation": generation_score,
                "faithfulness": faithfulness_score
            })
        
        return results
```

**Related Terms:** Metrics, Quality, Testing

**Key Metrics:**
- Retrieval: Precision, Recall, MRR
- Generation: Relevance, Fluency
- End-to-end: Faithfulness, Correctness

---

### Prompt Template

**Definition:** A reusable prompt structure with placeholders for context and query, ensuring consistent RAG prompts.

**Example:**
```python
RAG_TEMPLATE = """Answer the question based on the provided context.

Context:
{context}

Question: {question}

Instructions:
1. Answer based only on the context
2. Cite sources using [1], [2], etc.
3. If context doesn't contain the answer, say so
4. Be concise and accurate

Answer:"""

# Usage
prompt = RAG_TEMPLATE.format(
    context="\n\n".join([f"[{i+1}] {doc}" for i, doc in enumerate(docs)]),
    question=query
)
```

**Related Terms:** Prompt, Template, Consistency

**Benefits:**
- Consistent formatting
- Easy to maintain
- Version control
- Team collaboration

---

## Summary

Understanding these terms is essential for building effective RAG systems:

1. **RAG:** Combine retrieval with generation
2. **Ingestion:** Process documents for storage
3. **Chunking:** Split documents appropriately
4. **Retrieval:** Find relevant context
5. **Context:** Information for the LLM
6. **Grounding:** Answer based on documents
7. **Faithfulness:** Quality metric for grounding
8. **Relevance:** Quality metric for retrieval
9. **Hallucination:** What RAG helps prevent
10. **Vector Store:** Database for embeddings

**Next:** See Lecture 05 for AI agents.
