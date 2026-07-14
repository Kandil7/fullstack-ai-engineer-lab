"""
Exercise 03: Vector Embeddings
================================
Master embedding generation, vector databases, hybrid search, caching,
and similarity search for AI-powered applications.

Prerequisites:
    pip install openai qdrant-client sentence-transformers numpy python-dotenv

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
    QDRANT_URL=http://localhost:6333  (optional, defaults to local)
"""

import os
import json
import time
import hashlib
import numpy as np
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# 1. OpenAI Embedding Generation
# ---------------------------------------------------------------------------

class OpenAIEmbedder:
    """Generate embeddings using OpenAI's embedding models."""

    def __init__(self, model: str = "text-embedding-3-small", dimensions: int = 1536):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )
        return response.data[0].embedding

    def embed_batch(self, texts: list[str], batch_size: int = 100) -> list[list[float]]:
        """Generate embeddings for multiple texts with batching."""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch,
                dimensions=self.dimensions,
            )
            all_embeddings.extend([d.embedding for d in response.data])

        return all_embeddings


# ---------------------------------------------------------------------------
# 2. Local Embedding (Sentence Transformers)
# ---------------------------------------------------------------------------

class LocalEmbedder:
    """Generate embeddings locally using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()


# ---------------------------------------------------------------------------
# 3. Embedding Cache
# ---------------------------------------------------------------------------

class EmbeddingCache:
    """Cache embeddings to avoid redundant API calls."""

    def __init__(self, cache_dir: str = ".embedding_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self._cache: dict[str, list[float]] = {}

    def _key(self, text: str, model: str) -> str:
        """Generate a cache key from text and model."""
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, model: str = "default") -> list[float] | None:
        """Get a cached embedding."""
        key = self._key(text, model)

        # Check in-memory cache first
        if key in self._cache:
            return self._cache[key]

        # Check disk cache
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                data = json.load(f)
                self._cache[key] = data
                return data

        return None

    def set(self, text: str, embedding: list[float], model: str = "default"):
        """Store an embedding in cache."""
        key = self._key(text, model)
        self._cache[key] = embedding

        # Persist to disk
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_path, "w") as f:
            json.dump(embedding, f)

    def cached_embed(self, text: str, embed_fn, model: str = "default") -> list[float]:
        """Get or compute an embedding."""
        cached = self.get(text, model)
        if cached is not None:
            return cached

        embedding = embed_fn(text)
        self.set(text, embedding, model)
        return embedding

    def clear(self):
        """Clear all cached embeddings."""
        self._cache.clear()
        for f in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, f))


# ---------------------------------------------------------------------------
# 4. Qdrant Vector Database Operations
# ---------------------------------------------------------------------------

class VectorStore:
    """Interface for Qdrant vector database operations."""

    def __init__(self, collection_name: str = "documents", dimension: int = 1536,
                 url: str | None = None):
        from qdrant_client import QdrantClient
        from qdrant_client.models import VectorParams, Distance

        self.collection_name = collection_name
        self.dimension = dimension
        self.client = QdrantClient(url=url or os.getenv("QDRANT_URL", ":memory:"))

        # Create collection if it doesn't exist
        collections = [c.name for c in self.client.get_collections().collections]
        if collection_name not in collections:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
            )

    def upsert(self, ids: list[int], vectors: list[list[float]],
               payloads: list[dict] | None = None):
        """Insert or update vectors in the store."""
        from qdrant_client.models import PointStruct

        points = []
        for i, (vec_id, vector) in enumerate(zip(ids, vectors)):
            payload = payloads[i] if payloads else {}
            points.append(PointStruct(id=vec_id, vector=vector, payload=payload))

        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector: list[float], top_k: int = 5,
               filter_dict: dict | None = None) -> list[dict]:
        """Search for similar vectors."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        query_filter = None
        if filter_dict:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filter_dict.items()
            ]
            query_filter = Filter(must=conditions)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=query_filter,
        )

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
            }
            for hit in results
        ]

    def delete(self, ids: list[int]):
        """Delete vectors by ID."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=ids,
        )

    def get_collection_info(self) -> dict:
        """Get collection statistics."""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "vectors_count": info.vectors_count,
            "status": info.status,
        }


# ---------------------------------------------------------------------------
# 5. Similarity Search Utilities
# ---------------------------------------------------------------------------

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    a_arr = np.array(a)
    b_arr = np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


def dot_product(a: list[float], b: list[float]) -> float:
    """Compute dot product similarity."""
    return float(np.dot(np.array(a), np.array(b)))


def euclidean_distance(a: list[float], b: list[float]) -> float:
    """Compute Euclidean distance (lower = more similar)."""
    return float(np.linalg.norm(np.array(a) - np.array(b)))


def rank_by_similarity(query_vec: list[float], doc_vectors: list[dict],
                       top_k: int = 5) -> list[dict]:
    """Rank documents by similarity to query."""
    scored = []
    for doc in doc_vectors:
        score = cosine_similarity(query_vec, doc["vector"])
        scored.append({**doc, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# ---------------------------------------------------------------------------
# 6. Hybrid Search (Semantic + Keyword)
# ---------------------------------------------------------------------------

class HybridSearch:
    """Combine semantic (vector) search with keyword matching."""

    def __init__(self, embedder: LocalEmbedder, store: VectorStore):
        self.embedder = embedder
        self.store = store

    def search(self, query: str, *, top_k: int = 5,
               semantic_weight: float = 0.7,
               keyword_weight: float = 0.3) -> list[dict]:
        """
        Hybrid search combining semantic similarity and keyword matching.
        
        Args:
            query: Search query
            top_k: Number of results
            semantic_weight: Weight for semantic similarity (0-1)
            keyword_weight: Weight for keyword matching (0-1)
        """
        # Semantic search
        query_embedding = self.embedder.embed(query)
        semantic_results = self.store.search(query_vector=query_embedding, top_k=top_k * 2)

        # Keyword scoring
        query_words = set(query.lower().split())

        for result in semantic_results:
            payload = result.get("payload", {})
            text = payload.get("text", "").lower()
            doc_words = set(text.split())

            # Jaccard-like keyword overlap
            overlap = len(query_words & doc_words)
            total = len(query_words | doc_words) if query_words | doc_words else 1
            keyword_score = overlap / total

            # Combined score
            result["combined_score"] = (
                semantic_weight * result["score"] +
                keyword_weight * keyword_score
            )

        # Sort by combined score
        semantic_results.sort(key=lambda x: x["combined_score"], reverse=True)
        return semantic_results[:top_k]


# ---------------------------------------------------------------------------
# 7. Complete Embedding Pipeline
# ---------------------------------------------------------------------------

class EmbeddingPipeline:
    """End-to-end embedding pipeline with caching and vector storage."""

    def __init__(self, use_local: bool = True, collection: str = "documents"):
        if use_local:
            self.embedder = LocalEmbedder()
            dimension = self.embedder.dimension
        else:
            self.embedder = OpenAIEmbedder()
            dimension = 1536

        self.cache = EmbeddingCache()
        self.store = VectorStore(collection_name=collection, dimension=dimension)
        self.use_local = use_local

    def index_texts(self, texts: list[str], ids: list[int] | None = None,
                    metadata: list[dict] | None = None) -> int:
        """Index a batch of texts into the vector store."""
        if ids is None:
            ids = list(range(len(texts)))
        if metadata is None:
            metadata = [{}] * len(texts)

        # Generate embeddings (with caching)
        embeddings = []
        for text in texts:
            emb = self.cache.cached_embed(
                text,
                self.embedder.embed,
                model="local" if self.use_local else "openai"
            )
            embeddings.append(emb)

        # Store in vector database
        payloads = [{"text": text, **meta} for text, meta in zip(texts, metadata)]
        self.store.upsert(ids=ids, vectors=embeddings, payloads=payloads)

        return len(texts)

    def search(self, query: str, top_k: int = 5, filter_dict: dict | None = None) -> list[dict]:
        """Search for similar texts."""
        query_emb = self.embedder.embed(query)
        return self.store.search(query_vector=query_emb, top_k=top_k, filter_dict=filter_dict)

    def info(self) -> dict:
        """Get pipeline statistics."""
        return self.store.get_collection_info()


# ---------------------------------------------------------------------------
# 8. Demo Functions
# ---------------------------------------------------------------------------

def demo_similarity():
    """Demo: Computing similarity between vectors."""
    print("=" * 60)
    print("DEMO 1: Similarity Computation")
    print("=" * 60)

    # Create a local embedder for demo
    embedder = LocalEmbedder()
    print(f"Model dimension: {embedder.dimension}\n")

    # Embed some texts
    texts = [
        "The cat sat on the mat",
        "A feline rested on the rug",
        "Python is a programming language",
        "Machine learning algorithms process data",
    ]

    embeddings = embedder.embed_batch(texts)

    # Compute pairwise similarities
    print("Pairwise similarities:")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"  '{texts[i][:30]}...' <-> '{texts[j][:30]}...': {sim:.4f}")

    # Find most similar to a query
    query = "A cat lying on a carpet"
    query_emb = embedder.embed(query)
    print(f"\nQuery: '{query}'")
    print("\nRankings:")
    for text, emb in sorted(zip(texts, embeddings), key=lambda x: cosine_similarity(query_emb, x[1]), reverse=True):
        sim = cosine_similarity(query_emb, emb)
        print(f"  {sim:.4f} | {text}")


def demo_vector_store():
    """Demo: Vector database operations."""
    print("\n" + "=" * 60)
    print("DEMO 2: Vector Store Operations")
    print("=" * 60)

    embedder = LocalEmbedder()
    store = VectorStore(collection_name="demo", dimension=embedder.dimension)

    # Index some documents
    documents = [
        {"text": "Python is great for data science", "category": "programming"},
        {"text": "Rust is known for memory safety", "category": "programming"},
        {"text": "Cats are independent pets", "category": "animals"},
        {"text": "Dogs are loyal companions", "category": "animals"},
        {"text": "Machine learning requires large datasets", "category": "ai"},
        {"text": "Deep learning uses neural networks", "category": "ai"},
    ]

    ids = list(range(len(documents)))
    vectors = embedder.embed_batch([d["text"] for d in documents])
    store.upsert(ids=ids, vectors=vectors, payloads=documents)

    print(f"Indexed {len(documents)} documents")
    print(f"Collection info: {store.get_collection_info()}\n")

    # Semantic search
    query = "What language should I learn for AI?"
    query_vec = embedder.embed(query)
    results = store.search(query_vector=query_vec, top_k=3)

    print(f"Query: '{query}'")
    print("Results:")
    for r in results:
        print(f"  Score: {r['score']:.4f} | {r['payload']['text']}")

    # Filtered search
    print("\nFiltered search (category=programming):")
    results = store.search(query_vector=query_vec, top_k=3, filter_dict={"category": "programming"})
    for r in results:
        print(f"  Score: {r['score']:.4f} | {r['payload']['text']}")


def demo_embedding_cache():
    """Demo: Embedding caching."""
    print("\n" + "=" * 60)
    print("DEMO 3: Embedding Caching")
    print("=" * 60)

    embedder = LocalEmbedder()
    cache = EmbeddingCache(cache_dir=".demo_cache")

    # First call - no cache
    start = time.time()
    emb1 = cache.cached_embed("Test text for caching", embedder.embed, model="local")
    first_time = time.time() - start
    print(f"First call (no cache): {first_time:.4f}s")

    # Second call - from cache
    start = time.time()
    emb2 = cache.cached_embed("Test text for caching", embedder.embed, model="local")
    second_time = time.time() - start
    print(f"Second call (cached): {second_time:.4f}s")
    print(f"Speedup: {first_time / max(second_time, 0.0001):.1f}x")

    # Verify same embedding
    print(f"Embeddings match: {emb1 == emb2}")

    # Clean up
    cache.clear()
    print("Cache cleared.")


def demo_hybrid_search():
    """Demo: Hybrid search combining semantic + keyword."""
    print("\n" + "=" * 60)
    print("DEMO 4: Hybrid Search")
    print("=" * 60)

    embedder = LocalEmbedder()
    store = VectorStore(collection_name="hybrid_demo", dimension=embedder.dimension)

    # Index documents
    documents = [
        {"text": "Python web frameworks: Django, Flask, FastAPI", "topic": "web"},
        {"text": "JavaScript frontend: React, Vue, Angular", "topic": "frontend"},
        {"text": "Python data analysis with pandas and numpy", "topic": "data"},
        {"text": "Machine learning with scikit-learn and TensorFlow", "topic": "ml"},
        {"text": "REST API design patterns and best practices", "topic": "api"},
        {"text": "Python testing with pytest and unittest", "topic": "testing"},
    ]

    ids = list(range(len(documents)))
    vectors = embedder.embed_batch([d["text"] for d in documents])
    store.upsert(ids=ids, vectors=vectors, payloads=documents)

    # Create hybrid searcher
    hybrid = HybridSearch(embedder, store)

    # Search
    query = "Python web development"
    results = hybrid.search(query, top_k=3, semantic_weight=0.7, keyword_weight=0.3)

    print(f"Query: '{query}'\n")
    print("Results (semantic_weight=0.7, keyword_weight=0.3):")
    for r in results:
        print(f"  Combined: {r['combined_score']:.4f} | {r['payload']['text']}")


def demo_full_pipeline():
    """Demo: End-to-end embedding pipeline."""
    print("\n" + "=" * 60)
    print("DEMO 5: Full Pipeline")
    print("=" * 60)

    # Initialize pipeline
    pipeline = EmbeddingPipeline(use_local=True, collection="pipeline_demo")

    # Index documents
    documents = [
        "Retrieval-Augmented Generation combines search with language models",
        "Vector embeddings capture semantic meaning of text",
        "Chunking strategies affect retrieval quality in RAG systems",
        "Hybrid search combines dense and sparse retrieval methods",
        "Reranking improves relevance of retrieved documents",
        "Prompt engineering optimizes LLM output quality",
    ]

    metadata = [
        {"topic": "rag", "difficulty": "intermediate"},
        {"topic": "embeddings", "difficulty": "beginner"},
        {"topic": "rag", "difficulty": "advanced"},
        {"topic": "search", "difficulty": "intermediate"},
        {"topic": "rag", "difficulty": "advanced"},
        {"topic": "prompting", "difficulty": "beginner"},
    ]

    count = pipeline.index_texts(documents, metadata=metadata)
    print(f"Indexed {count} documents")
    print(f"Pipeline info: {pipeline.info()}\n")

    # Search
    query = "How does RAG work?"
    results = pipeline.search(query, top_k=3)
    print(f"Query: '{query}'")
    print("Results:")
    for r in results:
        print(f"  Score: {r['score']:.4f} | {r['payload']['text'][:60]}...")

    # Filtered search
    print("\nFiltered (topic=rag):")
    results = pipeline.search(query, top_k=3, filter_dict={"topic": "rag"})
    for r in results:
        print(f"  Score: {r['score']:.4f} | {r['payload']['text'][:60]}...")


# ---------------------------------------------------------------------------
# 9. Main Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Vector Embeddings Exercises")
    print("=" * 60)
    print()

    # Run demos (all use local embeddings, no API key needed)
    demo_similarity()
    demo_vector_store()
    demo_embedding_cache()
    demo_hybrid_search()
    demo_full_pipeline()

    print("\nAll demos complete!")
