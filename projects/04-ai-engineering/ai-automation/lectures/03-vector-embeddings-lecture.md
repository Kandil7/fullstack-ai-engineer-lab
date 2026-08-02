# Lecture 03: Vector Embeddings

## Topic Overview

Vector embeddings are the bridge between human language and machine understanding. They transform text, images, and other data into numerical representations (vectors) that capture semantic meaning. This lecture covers how embeddings work, how to generate them, how to store them in vector databases, and how to use them for semantic search—the foundation of RAG systems.

**Duration:** 3-4 hours  
**Difficulty:** Intermediate  
**Prerequisites:** Lecture 01 (LLM API Integration), Basic linear algebra concepts

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** what vector embeddings are and why they matter
2. **Generate** embeddings using OpenAI, Cohere, and open-source models
3. **Compare** embedding models and choose the right one
4. **Calculate** similarity between embeddings (cosine, dot product, Euclidean)
5. **Store** and query embeddings using vector databases (Pinecone, Weaviate, ChromaDB)
6. **Implement** semantic search systems
7. **Optimize** embedding generation for cost and performance
8. **Handle** common embedding challenges (dimensionality, normalization)

---

## Key Concepts

### 1. What Are Vector Embeddings?

Vector embeddings are dense numerical representations of data (text, images, audio) in a high-dimensional space. Similar items are positioned close together in this space.

```
Text: "The cat sat on the mat"
          ↓ [Embedding Model]
Vector: [0.023, -0.156, 0.089, ..., 0.234]  (1536 dimensions)
```

**Why embeddings matter:**
- **Semantic understanding:** "happy" and "joyful" are close in vector space
- **Search:** Find similar documents without exact keyword matching
- **Recommendation:** Suggest items based on meaning, not just tags
- **Clustering:** Group similar content automatically

### 2. How Embeddings Capture Meaning

Embeddings are trained on large text corpora to learn relationships between words and concepts.

```
Similar concepts are CLOSE in vector space:
    "king" ──────────── "queen"
      │                    │
      │                    │
    "man" ──────────── "woman"
    
Distance(king, queen) ≈ Distance(man, woman)
```

**Example:**
```python
from openai import OpenAI

client = OpenAI()

# Generate embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=[
        "The cat sat on the mat",
        "A feline rested on the rug",
        "Python is a programming language"
    ]
)

# Compare similarities
import numpy as np

embeddings = [item.embedding for item in response.data]

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# "cat" and "feline" should be similar
sim_1_2 = cosine_similarity(embeddings[0], embeddings[1])
print(f"Cat-Feline similarity: {sim_1_2:.3f}")  # ~0.85

# "cat" and "Python" should be less similar
sim_1_3 = cosine_similarity(embeddings[0], embeddings[2])
print(f"Cat-Python similarity: {sim_1_3:.3f}")  # ~0.45
```

### 3. Embedding Models

Different models produce different embedding dimensions and quality:

| Model | Provider | Dimensions | Max Tokens | Cost/1M Tokens |
|-------|----------|------------|------------|-----------------|
| text-embedding-3-small | OpenAI | 1536 | 8191 | $0.02 |
| text-embedding-3-large | OpenAI | 3072 | 8191 | $0.13 |
| embed-english-v3.0 | Cohere | 1024 | 512 | $0.10 |
| all-MiniLM-L6-v2 | HuggingFace | 384 | 256 | Free |
| BGE-large-en-v1.5 | HuggingFace | 1024 | 512 | Free |

**Example: Using different models:**
```python
# OpenAI
from openai import OpenAI

client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world"
)
embedding_openai = response.data[0].embedding  # 1536 dimensions

# HuggingFace (open source)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_hf = model.encode("Hello world")  # 384 dimensions

# Cohere
import cohere

co = cohere.Client(api_key="your-key")
response = co.embed(
    texts=["Hello world"],
    model="embed-english-v3.0"
)
embedding_cohere = response.embeddings[0]  # 1024 dimensions
```

### 4. Similarity Metrics

How to measure distance between vectors:

**Cosine Similarity (most common):**
```python
import numpy as np

def cosine_similarity(a, b):
    """Measure angle between vectors (-1 to 1)."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Perfect match
print(cosine_similarity([1, 0, 0], [1, 0, 0]))  # 1.0

# Orthogonal (unrelated)
print(cosine_similarity([1, 0, 0], [0, 1, 0]))  # 0.0

# Opposite
print(cosine_similarity([1, 0, 0], [-1, 0, 0]))  # -1.0
```

**Dot Product:**
```python
def dot_product(a, b):
    """Simple vector multiplication (unnormalized)."""
    return np.dot(a, b)
```

**Euclidean Distance:**
```python
def euclidean_distance(a, b):
    """Straight-line distance between points."""
    return np.linalg.norm(np.array(a) - np.array(b))
```

**When to use which:**
- **Cosine:** Most common, normalized, works with different magnitudes
- **Dot Product:** When vectors are normalized, faster to compute
- **Euclidean:** When absolute distance matters

### 5. Vector Databases

Vector databases store embeddings and enable fast similarity search.

**Popular vector databases:**

| Database | Type | Best For |
|----------|------|----------|
| Pinecone | Managed | Production, scalability |
| Weaviate | Self-hosted | Flexibility, hybrid search |
| ChromaDB | Embedded | Development, simplicity |
| Milvus | Self-hosted | Scale, performance |
| Qdrant | Self-hosted | Performance, filtering |

**Example: ChromaDB (local development)**
```python
import chromadb

# Create client and collection
client = chromadb.Client()
collection = client.create_collection("documents")

# Add documents
collection.add(
    documents=[
        "Python is a programming language",
        "JavaScript is used for web development",
        "Machine learning requires data",
        "Deep learning uses neural networks"
    ],
    metadatas=[
        {"category": "programming", "language": "python"},
        {"category": "programming", "language": "javascript"},
        {"category": "ai", "topic": "ml"},
        {"category": "ai", "topic": "dl"}
    ],
    ids=["doc1", "doc2", "doc3", "doc4"]
)

# Query
results = collection.query(
    query_texts=["What is Python used for?"],
    n_results=2
)

print(results["documents"][0])
# ['Python is a programming language', 'JavaScript is used for web development']
```

**Example: Pinecone (production)**
```python
import pinecone
from openai import OpenAI

# Initialize
pinecone.init(api_key="your-key", environment="us-east1-gcp")
index = pinecone.Index("documents")

# Generate embedding
client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Python programming"
)
embedding = response.data[0].embedding

# Upsert
index.upsert([
    ("doc1", embedding, {"text": "Python is a programming language"})
])

# Query
results = index.query(
    vector=embedding,
    top_k=5,
    include_metadata=True
)

for match in results["matches"]:
    print(f"Score: {match['score']:.3f} - {match['metadata']['text']}")
```

### 6. Semantic Search

Using embeddings to find relevant documents based on meaning, not keywords.

**Traditional keyword search:**
```python
# ❌ Keyword search fails on synonyms
documents = [
    "The canine retrieved the ball",
    "The dog played fetch",
    "Python is a snake"
]

query = "puppy playing"
# Keyword search returns: nothing (no exact match)
```

**Semantic search:**
```python
# ✅ Semantic search understands meaning
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Index documents
doc_embeddings = model.encode(documents)

# Query
query_embedding = model.encode("puppy playing")

# Find similar
similarities = np.dot(doc_embeddings, query_embedding)
best_match_idx = np.argmax(similarities)

print(documents[best_match_idx])
# "The dog played fetch" (semantically similar!)
```

### 7. Chunking Strategies

For long documents, you need to split them into chunks before embedding:

**Fixed-size chunking:**
```python
def chunk_fixed_size(text, chunk_size=500, overlap=50):
    """Split text into fixed-size chunks with overlap."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks
```

**Sentence-based chunking:**
```python
import nltk

def chunk_sentences(text, max_sentences=5):
    """Split text by sentences."""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences])
        chunks.append(chunk)
    
    return chunks
```

**Semantic chunking:**
```python
def chunk_semantic(text, threshold=0.5):
    """Split where semantic similarity drops."""
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences)
    
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])
        
        if similarity < threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
```

---

## Code Examples

### Example 1: Complete Semantic Search System

```python
"""
Production-ready semantic search with embeddings.
"""
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
from openai import OpenAI
import chromadb


@dataclass
class SearchResult:
    """A search result with metadata."""
    content: str
    score: float
    metadata: dict
    id: str


class SemanticSearchEngine:
    """Full-featured semantic search engine."""
    
    def __init__(
        self,
        collection_name: str = "documents",
        embedding_model: str = "text-embedding-3-small"
    ):
        self.client = OpenAI()
        self.embedding_model = embedding_model
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def _get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def add_document(
        self,
        content: str,
        metadata: Optional[dict] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """Add a document to the search index."""
        
        # Generate ID if not provided
        if doc_id is None:
            doc_id = f"doc_{self.collection.count()}"
        
        # Generate embedding
        embedding = self._get_embedding(content)
        
        # Store in ChromaDB
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        
        return doc_id
    
    def add_documents_batch(
        self,
        documents: List[dict]
    ) -> List[str]:
        """Add multiple documents efficiently."""
        
        texts = [doc["content"] for doc in documents]
        embeddings = self._get_embeddings_batch(texts)
        
        ids = [doc.get("id", f"doc_{i}") for i, doc in enumerate(documents)]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None
    ) -> List[SearchResult]:
        """Search for similar documents."""
        
        # Generate query embedding
        query_embedding = self._get_embedding(query)
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters
        )
        
        # Format results
        search_results = []
        for i in range(len(results["ids"][0])):
            search_results.append(SearchResult(
                content=results["documents"][0][i],
                score=1 - results["distances"][0][i],  # Convert distance to similarity
                metadata=results["metadatas"][0][i],
                id=results["ids"][0][i]
            ))
        
        return search_results
    
    def delete_document(self, doc_id: str) -> bool:
        """Remove a document from the index."""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception:
            return False
    
    def get_stats(self) -> dict:
        """Get collection statistics."""
        return {
            "total_documents": self.collection.count(),
            "embedding_model": self.embedding_model
        }


# Usage
engine = SemanticSearchEngine()

# Add documents
engine.add_documents_batch([
    {
        "content": "Python is great for data science and machine learning",
        "metadata": {"category": "programming", "topic": "python"}
    },
    {
        "content": "JavaScript is the language of the web",
        "metadata": {"category": "programming", "topic": "javascript"}
    },
    {
        "content": "Deep learning requires large datasets and GPU compute",
        "metadata": {"category": "ai", "topic": "deep_learning"}
    },
    {
        "content": "React is a popular frontend framework",
        "metadata": {"category": "framework", "topic": "react"}
    }
])

# Search
results = engine.search("machine learning frameworks", top_k=3)

for result in results:
    print(f"Score: {result.score:.3f} | {result.content}")
```

### Example 2: Embedding Visualization

```python
"""
Visualize embeddings in 2D/3D space.
"""
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from openai import OpenAI
from typing import List, Tuple


class EmbeddingVisualizer:
    """Visualize embeddings using dimensionality reduction."""
    
    def __init__(self):
        self.client = OpenAI()
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings for texts."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return np.array([item.embedding for item in response.data])
    
    def reduce_dimensions(
        self,
        embeddings: np.ndarray,
        n_components: int = 2,
        perplexity: int = 30
    ) -> np.ndarray:
        """Reduce dimensions using t-SNE."""
        tsne = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            random_state=42
        )
        return tsne.fit_transform(embeddings)
    
    def plot_2d(
        self,
        texts: List[str],
        labels: List[str] = None,
        title: str = "Embedding Visualization"
    ):
        """Plot embeddings in 2D."""
        
        # Get embeddings
        embeddings = self.get_embeddings(texts)
        
        # Reduce to 2D
        reduced = self.reduce_dimensions(embeddings, n_components=2)
        
        # Plot
        plt.figure(figsize=(12, 8))
        
        if labels is None:
            labels = [t[:30] + "..." for t in texts]
        
        scatter = plt.scatter(
            reduced[:, 0],
            reduced[:, 1],
            c=range(len(texts)),
            cmap='viridis',
            s=100
        )
        
        # Add labels
        for i, label in enumerate(labels):
            plt.annotate(
                label,
                (reduced[i, 0], reduced[i, 1]),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9
            )
        
        plt.title(title)
        plt.colorbar(scatter)
        plt.tight_layout()
        plt.savefig("output/embeddings_2d.png", dpi=150)
        plt.show()
    
    def find_clusters(
        self,
        texts: List[str],
        n_clusters: int = 3
    ) -> List[Tuple[str, int]]:
        """Find clusters in embeddings."""
        from sklearn.cluster import KMeans
        
        embeddings = self.get_embeddings(texts)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings)
        
        return list(zip(texts, clusters))


# Usage
visualizer = EmbeddingVisualizer()

texts = [
    "Python programming",
    "JavaScript web development",
    "Machine learning algorithms",
    "Deep neural networks",
    "Data science analysis",
    "Frontend frameworks",
    "React components",
    "Natural language processing",
    "Computer vision",
    "React hooks"
]

visualizer.plot_2d(texts, title="Tech Topics Embeddings")
```

### Example 3: Hybrid Search (Semantic + Keyword)

```python
"""
Combine semantic search with keyword matching.
"""
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
from openai import OpenAI
import chromadb
from rank_bm25 import BM25Okapi


@dataclass
class HybridResult:
    """Combined search result."""
    content: str
    semantic_score: float
    keyword_score: float
    combined_score: float
    metadata: dict


class HybridSearchEngine:
    """Combine semantic and keyword search."""
    
    def __init__(self, alpha: float = 0.7):
        """
        Args:
            alpha: Weight for semantic search (0-1)
                   1.0 = pure semantic, 0.0 = pure keyword
        """
        self.alpha = alpha
        self.client = OpenAI()
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("hybrid_docs")
        
        self.documents = []
        self.tokenized_docs = []
        self.bm25 = None
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return text.lower().split()
    
    def add_documents(self, documents: List[dict]):
        """Add documents with both indexing methods."""
        
        texts = [doc["content"] for doc in documents]
        
        # Generate embeddings for semantic search
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        embeddings = [item.embedding for item in response.data]
        
        # Add to ChromaDB
        ids = [f"doc_{i}" for i in range(len(documents))]
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=[doc.get("metadata", {}) for doc in documents],
            ids=ids
        )
        
        # Build BM25 index for keyword search
        self.documents = texts
        self.tokenized_docs = [self._tokenize(doc) for doc in texts]
        self.bm25 = BM25Okapi(self.tokenized_docs)
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filters: Optional[dict] = None
    ) -> List[HybridResult]:
        """Hybrid search combining semantic and keyword."""
        
        # Semantic search
        query_embedding = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding
        
        semantic_results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2,  # Get more for reranking
            where=filters
        )
        
        # Keyword search
        tokenized_query = self._tokenize(query)
        keyword_scores = self.bm25.get_scores(tokenized_query)
        
        # Normalize scores
        semantic_scores = {
            doc_id: 1 - dist  # Convert distance to similarity
            for doc_id, dist in zip(
                semantic_results["ids"][0],
                semantic_results["distances"][0]
            )
        }
        
        max_keyword = max(keyword_scores) if max(keyword_scores) > 0 else 1
        keyword_scores_norm = {
            i: score / max_keyword 
            for i, score in enumerate(keyword_scores)
        }
        
        # Combine scores
        combined = {}
        for doc_id, sem_score in semantic_scores.items():
            doc_idx = int(doc_id.split("_")[1])
            kw_score = keyword_scores_norm.get(doc_idx, 0)
            
            combined[doc_id] = {
                "content": self.documents[doc_idx],
                "semantic": sem_score,
                "keyword": kw_score,
                "combined": self.alpha * sem_score + (1 - self.alpha) * kw_score,
                "metadata": semantic_results["metadatas"][0][
                    semantic_results["ids"][0].index(doc_id)
                ]
            }
        
        # Sort by combined score
        sorted_results = sorted(
            combined.values(),
            key=lambda x: x["combined"],
            reverse=True
        )[:top_k]
        
        return [
            HybridResult(
                content=r["content"],
                semantic_score=r["semantic"],
                keyword_score=r["keyword"],
                combined_score=r["combined"],
                metadata=r["metadata"]
            )
            for r in sorted_results
        ]


# Usage
engine = HybridSearchEngine(alpha=0.7)  # 70% semantic, 30% keyword

engine.add_documents([
    {"content": "Python is great for machine learning", "metadata": {"topic": "ml"}},
    {"content": "JavaScript powers web applications", "metadata": {"topic": "web"}},
    {"content": "Deep learning uses neural networks", "metadata": {"topic": "dl"}},
    {"content": "TensorFlow is a ML framework", "metadata": {"topic": "framework"}}
])

results = engine.search("AI frameworks", top_k=3)

for r in results:
    print(f"Combined: {r.combined_score:.3f} "
          f"(Sem: {r.semantic_score:.3f}, KW: {r.keyword_score:.3f})")
    print(f"  {r.content}\n")
```

---

## Common Mistakes to Avoid

### 1. Not Normalizing Embeddings
```python
# ❌ BAD: Mixing normalized and unnormalized
embedding_a = model.encode("text a")  # Not normalized
embedding_b = model.encode("text b")  # Not normalized
similarity = cosine_similarity(embedding_a, embedding_b)  # May be wrong

# ✅ GOOD: Always normalize
embedding_a = model.encode("text a", normalize_embeddings=True)
embedding_b = model.encode("text b", normalize_embeddings=True)
similarity = np.dot(embedding_a, embedding_b)  # Correct
```

### 2. Inconsistent Chunking
```python
# ❌ BAD: Different chunk sizes for index vs query
index_chunks = chunk_fixed_size(document, chunk_size=1000)
query_chunks = chunk_fixed_size(query, chunk_size=500)  # Different!

# ✅ GOOD: Consistent chunking
CHUNK_SIZE = 500
index_chunks = chunk_fixed_size(document, chunk_size=CHUNK_SIZE)
query_chunks = chunk_fixed_size(query, chunk_size=CHUNK_SIZE)
```

### 3. Ignoring Metadata Filtering
```python
# ❌ BAD: Searching entire database
results = collection.query(query_embedding, n_results=10)

# ✅ GOOD: Filter by metadata when possible
results = collection.query(
    query_embedding,
    n_results=10,
    where={"category": "python"}  # Narrow search space
)
```

---

## Best Practices

1. **Choose the right model** - Balance cost, speed, and quality
2. **Normalize embeddings** - For consistent similarity scores
3. **Use metadata filtering** - Reduce search space
4. **Chunk strategically** - Balance context and precision
5. **Batch API calls** - Reduce latency and cost
6. **Cache embeddings** - Avoid regenerating for repeated content
7. **Monitor quality** - Test retrieval accuracy regularly
8. **Hybrid search** - Combine semantic + keyword for best results
9. **Update indices** - Re-embed when content changes significantly
10. **Handle failures** - Graceful fallback to keyword search

---

## Practice Exercises

### Exercise 1: Document Q&A
Build a system that:
1. Takes a document as input
2. Chunks it appropriately
3. Creates embeddings
4. Answers questions using retrieved context

### Exercise 2: Recommendation Engine
Create a recommendation system that:
1. Takes user preferences as text
2. Finds similar items in a catalog
3. Returns top 5 recommendations with explanations

### Exercise 3: Deduplication System
Build a system that:
1. Detects near-duplicate documents
2. Groups similar content
3. Suggests merges for overlapping documents

### Exercise 4: Multi-Modal Search
Extend the search engine to handle:
1. Text queries
2. Image descriptions
3. Mixed results

### Exercise 5: Performance Benchmark
Create a benchmark that:
1. Measures search latency
2. Compares different embedding models
3. Tests accuracy on a labeled dataset

---

## Summary

Vector embeddings are the foundation of semantic AI systems:

1. **Embeddings** capture meaning as numerical vectors
2. **Similarity metrics** measure distance between concepts
3. **Vector databases** enable fast similarity search
4. **Chunking** handles long documents effectively
5. **Hybrid search** combines semantic + keyword for best results
6. **Production systems** need caching, monitoring, and fallbacks

**Next lecture:** RAG Systems - Combining retrieval with generation.
