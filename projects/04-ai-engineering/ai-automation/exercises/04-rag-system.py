"""
Exercise 04: RAG (Retrieval-Augmented Generation) System
==========================================================
Build a complete RAG system from scratch: document chunking, embedding,
vector storage, retrieval, reranking, generation, and evaluation.

Prerequisites:
    pip install openai qdrant-client sentence-transformers numpy python-dotenv

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
"""

import os
import json
import re
import time
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

import numpy as np


# ---------------------------------------------------------------------------
# 1. Document Models
# ---------------------------------------------------------------------------

@dataclass
class Document:
    """A source document."""
    id: str
    content: str
    metadata: dict = field(default_factory=dict)
    source: str = ""


@dataclass
class Chunk:
    """A chunk of text from a document."""
    id: str
    content: str
    document_id: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)
    embedding: list[float] | None = None


@dataclass
class RetrievalResult:
    """A retrieval result with score and source."""
    chunk: Chunk
    score: float
    rerank_score: float | None = None


@dataclass
class RAGResponse:
    """The final RAG response."""
    answer: str
    sources: list[RetrievalResult]
    context_used: str
    latency_ms: float


# ---------------------------------------------------------------------------
# 2. Document Chunking Strategies
# ---------------------------------------------------------------------------

class ChunkingStrategy(Enum):
    FIXED_SIZE = "fixed_size"
    SENTENCE = "sentence"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"


class DocumentChunker:
    """Split documents into chunks using various strategies."""

    @staticmethod
    def fixed_size(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        """Split text into fixed-size chunks with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap if end < len(text) else end
        return chunks

    @staticmethod
    def sentence_based(text: str, max_chunk_size: int = 1000) -> list[str]:
        """Split text by sentences, grouping them into chunks."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            if current_size + len(sentence) > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
            current_chunk.append(sentence)
            current_size += len(sentence)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    @staticmethod
    def recursive(text: str, chunk_size: int = 500, overlap: int = 50,
                  separators: list[str] | None = None) -> list[str]:
        """Recursively split by separators (paragraphs -> sentences -> chars)."""
        if separators is None:
            separators = ["\n\n", "\n", ". ", " "]

        if len(text) <= chunk_size:
            return [text]

        for sep in separators:
            if sep in text:
                parts = text.split(sep)
                chunks = []
                current = ""

                for part in parts:
                    if len(current) + len(part) + len(sep) <= chunk_size:
                        current += part + sep
                    else:
                        if current:
                            chunks.append(current.strip())
                        current = part + sep

                if current:
                    chunks.append(current.strip())

                if all(len(c) <= chunk_size * 1.2 for c in chunks):
                    return chunks

        # Fallback to fixed size
        return DocumentChunker.fixed_size(text, chunk_size, overlap)

    @staticmethod
    def markdown_aware(text: str, max_chunk_size: int = 1000) -> list[str]:
        """Split markdown by headers, preserving structure."""
        sections = re.split(r'\n(?=#{1,4}\s)', text)
        chunks = []
        current_chunk = ""

        for section in sections:
            if len(current_chunk) + len(section) <= max_chunk_size:
                current_chunk += section
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = section

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    @classmethod
    def chunk(cls, text: str, strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE,
              **kwargs) -> list[str]:
        """Chunk text using the specified strategy."""
        strategies = {
            ChunkingStrategy.FIXED_SIZE: cls.fixed_size,
            ChunkingStrategy.SENTENCE: cls.sentence_based,
            ChunkingStrategy.RECURSIVE: cls.recursive,
            ChunkingStrategy.MARKDOWN: cls.markdown_aware,
        }
        return strategies[strategy](text, **kwargs)


# ---------------------------------------------------------------------------
# 3. Embedding Engine
# ---------------------------------------------------------------------------

class EmbeddingEngine:
    """Generate embeddings for text chunks."""

    def __init__(self, use_local: bool = True, model: str | None = None):
        self.use_local = use_local
        if use_local:
            from sentence_transformers import SentenceTransformer
            self.model_name = model or "all-MiniLM-L6-v2"
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
        else:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model_name = model or "text-embedding-3-small"
            self.dimension = 1536

    def embed(self, text: str) -> list[float]:
        if self.use_local:
            return self.model.encode(text).tolist()
        else:
            resp = self.client.embeddings.create(model=self.model_name, input=text)
            return resp.data[0].embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if self.use_local:
            return self.model.encode(texts).tolist()
        else:
            # Batch in groups of 100
            all_embs = []
            for i in range(0, len(texts), 100):
                batch = texts[i:i+100]
                resp = self.client.embeddings.create(model=self.model_name, input=batch)
                all_embs.extend([d.embedding for d in resp.data])
            return all_embs


# ---------------------------------------------------------------------------
# 4. Vector Store
# ---------------------------------------------------------------------------

class VectorStore:
    """Simple vector store using Qdrant (in-memory or server)."""

    def __init__(self, collection: str = "rag_docs", dimension: int = 384):
        from qdrant_client import QdrantClient
        from qdrant_client.models import VectorParams, Distance

        self.client = QdrantClient(":memory:")
        self.collection = collection

        self.client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
        )

    def add(self, chunks: list[Chunk]):
        """Add chunks with embeddings to the store."""
        from qdrant_client.models import PointStruct

        points = []
        for chunk in chunks:
            if chunk.embedding is None:
                continue
            points.append(PointStruct(
                id=hash(chunk.id) % (2**63),
                vector=chunk.embedding,
                payload={
                    "chunk_id": chunk.id,
                    "content": chunk.content,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    **chunk.metadata,
                },
            ))

        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search for similar chunks."""
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=top_k,
        )
        return [
            {
                "score": hit.score,
                "chunk_id": hit.payload.get("chunk_id"),
                "content": hit.payload.get("content"),
                "document_id": hit.payload.get("document_id"),
                "metadata": {k: v for k, v in hit.payload.items()
                             if k not in ("chunk_id", "content", "document_id")},
            }
            for hit in results
        ]


# ---------------------------------------------------------------------------
# 5. Retrieval Engine
# ---------------------------------------------------------------------------

class RetrievalEngine:
    """Retrieve relevant chunks for a query."""

    def __init__(self, embedding_engine: EmbeddingEngine, vector_store: VectorStore):
        self.embedder = embedding_engine
        self.store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        """Retrieve top-k relevant chunks."""
        query_emb = self.embedder.embed(query)
        results = self.store.search(query_emb, top_k=top_k)

        return [
            RetrievalResult(
                chunk=Chunk(
                    id=r["chunk_id"],
                    content=r["content"],
                    document_id=r["document_id"],
                    chunk_index=0,
                    metadata=r["metadata"],
                ),
                score=r["score"],
            )
            for r in results
        ]


# ---------------------------------------------------------------------------
# 6. Reranker
# ---------------------------------------------------------------------------

class CrossEncoderReranker:
    """Rerank retrieval results using cross-encoder scoring."""

    def __init__(self):
        # Using a simple heuristic reranker for demo
        # In production, use cross-encoder models like ms-marco-MiniLM-L-6-v2
        pass

    def rerank(self, query: str, results: list[RetrievalResult],
               top_k: int = 3) -> list[RetrievalResult]:
        """Rerank results based on query-document relevance."""
        for result in results:
            # Heuristic scoring based on:
            # 1. Query term overlap
            # 2. Chunk length (prefer medium-length chunks)
            # 3. Original retrieval score

            query_terms = set(query.lower().split())
            doc_terms = set(result.chunk.content.lower().split())
            term_overlap = len(query_terms & doc_terms) / max(len(query_terms), 1)

            # Length score (prefer 200-800 chars)
            content_len = len(result.chunk.content)
            if 200 <= content_len <= 800:
                length_score = 1.0
            elif content_len < 200:
                length_score = content_len / 200
            else:
                length_score = 800 / content_len

            # Combined rerank score
            result.rerank_score = (
                0.4 * result.score +      # Original retrieval score
                0.4 * term_overlap +       # Query-term overlap
                0.2 * length_score         # Length preference
            )

        results.sort(key=lambda x: x.rerank_score or 0, reverse=True)
        return results[:top_k]


# ---------------------------------------------------------------------------
# 7. Generation Engine
# ---------------------------------------------------------------------------

class GenerationEngine:
    """Generate answers using retrieved context."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def generate(self, query: str, context_chunks: list[RetrievalResult]) -> RAGResponse:
        """Generate an answer given a query and context."""
        start = time.time()

        # Build context
        context_parts = []
        for i, result in enumerate(context_chunks, 1):
            source = result.chunk.metadata.get("source", result.chunk.document_id)
            context_parts.append(
                f"[Source {i}: {source}]\n{result.chunk.content}"
            )
        context = "\n\n".join(context_parts)

        # Build prompt
        prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on 
the provided context. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {query}

Answer (be specific, cite sources when possible):"""

        # Generate response
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        answer = response.choices[0].message.content or ""
        latency = (time.time() - start) * 1000

        return RAGResponse(
            answer=answer,
            sources=context_chunks,
            context_used=context,
            latency_ms=latency,
        )


# ---------------------------------------------------------------------------
# 8. Complete RAG Pipeline
# ---------------------------------------------------------------------------

class RAGPipeline:
    """End-to-end RAG system combining all components."""

    def __init__(self, use_local_embeddings: bool = True,
                 generation_model: str = "gpt-4o-mini"):
        self.chunker = DocumentChunker()
        self.embedder = EmbeddingEngine(use_local=use_local_embeddings)
        self.store = VectorStore(
            collection="rag_pipeline",
            dimension=self.embedder.dimension,
        )
        self.retriever = RetrievalEngine(self.embedder, self.store)
        self.reranker = CrossEncoderReranker()
        self.generator = GenerationEngine(model=generation_model)

        self._documents: dict[str, Document] = {}
        self._chunks: list[Chunk] = []
        self._next_chunk_id = 0

    def ingest(self, documents: list[Document],
               chunking_strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE,
               chunk_size: int = 500) -> int:
        """Ingest documents into the RAG system."""
        all_chunks = []

        for doc in documents:
            self._documents[doc.id] = doc
            texts = self.chunker.chunk(
                doc.content,
                strategy=chunking_strategy,
                chunk_size=chunk_size,
            )

            for i, text in enumerate(texts):
                chunk = Chunk(
                    id=f"{doc.id}_chunk_{i}",
                    content=text,
                    document_id=doc.id,
                    chunk_index=i,
                    metadata={"source": doc.source, **doc.metadata},
                )
                self._chunks.append(chunk)
                all_chunks.append(chunk)

        # Generate embeddings in batch
        print(f"Generating embeddings for {len(all_chunks)} chunks...")
        embeddings = self.embedder.embed_batch([c.content for c in all_chunks])

        for chunk, emb in zip(all_chunks, embeddings):
            chunk.embedding = emb

        # Store in vector database
        self.store.add(all_chunks)
        print(f"Stored {len(all_chunks)} chunks in vector store")

        return len(all_chunks)

    def query(self, query: str, *, top_k: int = 5, rerank: bool = True,
              context_limit: int = 3) -> RAGResponse:
        """Query the RAG system."""
        # Retrieve
        results = self.retriever.retrieve(query, top_k=top_k)

        # Rerank
        if rerank and results:
            results = self.reranker.rerank(query, results, top_k=context_limit)

        # Generate
        response = self.generator.generate(query, results[:context_limit])
        return response

    def stats(self) -> dict:
        """Get pipeline statistics."""
        return {
            "documents": len(self._documents),
            "chunks": len(self._chunks),
            "embedding_dimension": self.embedder.dimension,
            "collection": self.store.collection,
        }


# ---------------------------------------------------------------------------
# 9. RAG Evaluation
# ---------------------------------------------------------------------------

class RAGEvaluator:
    """Evaluate RAG system quality."""

    def __init__(self):
        pass

    def evaluate_retrieval(self, query: str, retrieved_chunks: list[RetrievalResult],
                           relevant_ids: list[str]) -> dict:
        """Evaluate retrieval quality."""
        retrieved_ids = [r.chunk.id for r in retrieved_chunks]

        # Precision@k
        relevant_retrieved = sum(1 for cid in retrieved_ids if cid in relevant_ids)
        precision = relevant_retrieved / len(retrieved_ids) if retrieved_ids else 0

        # Recall@k
        recall = relevant_retrieved / len(relevant_ids) if relevant_ids else 0

        # MRR (Mean Reciprocal Rank)
        mrr = 0
        for i, cid in enumerate(retrieved_ids):
            if cid in relevant_ids:
                mrr = 1 / (i + 1)
                break

        return {
            "precision": precision,
            "recall": recall,
            "mrr": mrr,
            "retrieved_count": len(retrieved_ids),
            "relevant_count": len(relevant_ids),
        }

    def evaluate_answer(self, answer: str, context: str, query: str) -> dict:
        """Evaluate answer quality using heuristics."""
        # Faithfulness: answer should relate to context
        answer_terms = set(answer.lower().split())
        context_terms = set(context.lower().split())
        faithfulness = len(answer_terms & context_terms) / max(len(answer_terms), 1)

        # Relevance: answer should address the query
        query_terms = set(query.lower().split())
        answer_terms_query = set(answer.lower().split())
        relevance = len(query_terms & answer_terms_query) / max(len(query_terms), 1)

        # Completeness: answer should be substantial
        completeness = min(len(answer) / 200, 1.0)

        return {
            "faithfulness": faithfulness,
            "relevance": relevance,
            "completeness": completeness,
            "answer_length": len(answer),
        }


# ---------------------------------------------------------------------------
# 10. Demo Functions
# ---------------------------------------------------------------------------

def demo_chunking():
    """Demo: Different chunking strategies."""
    print("=" * 60)
    print("DEMO 1: Document Chunking")
    print("=" * 60)

    sample_text = """# Introduction to RAG

Retrieval-Augmented Generation (RAG) is a technique that combines 
retrieval and generation. It was introduced by Facebook AI Research in 2020.

## How RAG Works

RAG operates in three main steps:
1. **Document Processing**: Documents are split into chunks
2. **Retrieval**: Relevant chunks are found using vector similarity
3. **Generation**: An LLM generates an answer using retrieved context

## Benefits of RAG

RAG offers several advantages over fine-tuning:
- No need to retrain the model
- Easy to update knowledge base
- Transparent and auditable
- Cost-effective for domain-specific applications

## Conclusion

RAG is becoming the standard approach for knowledge-intensive NLP tasks."""

    strategies = [
        (ChunkingStrategy.FIXED_SIZE, {"chunk_size": 200, "overlap": 20}),
        (ChunkingStrategy.SENTENCE, {"max_chunk_size": 300}),
        (ChunkingStrategy.RECURSIVE, {"chunk_size": 300}),
        (ChunkingStrategy.MARKDOWN, {"max_chunk_size": 300}),
    ]

    for strategy, kwargs in strategies:
        chunks = DocumentChunker.chunk(sample_text, strategy, **kwargs)
        print(f"\n{strategy.value} ({len(chunks)} chunks):")
        for i, chunk in enumerate(chunks[:3]):  # Show first 3
            preview = chunk[:80].replace("\n", " ")
            print(f"  [{i}] {preview}...")
        if len(chunks) > 3:
            print(f"  ... and {len(chunks) - 3} more chunks")


def demo_retrieval():
    """Demo: Document ingestion and retrieval."""
    print("\n" + "=" * 60)
    print("DEMO 2: Ingestion & Retrieval")
    print("=" * 60)

    pipeline = RAGPipeline(use_local_embeddings=True)

    # Sample documents
    documents = [
        Document(
            id="doc1",
            content="Python is a high-level programming language known for its simplicity. "
                    "It supports multiple paradigms including object-oriented, functional, and "
                    "procedural programming. Python is widely used in data science, web development, "
                    "and automation.",
            metadata={"topic": "programming", "language": "python"},
            source="Python Guide",
        ),
        Document(
            id="doc2",
            content="Machine learning is a subset of artificial intelligence that enables systems "
                    "to learn from data. Key concepts include supervised learning, unsupervised "
                    "learning, and reinforcement learning. Popular algorithms include neural networks, "
                    "decision trees, and support vector machines.",
            metadata={"topic": "ai", "level": "beginner"},
            source="ML Handbook",
        ),
        Document(
            id="doc3",
            content="RAG (Retrieval-Augmented Generation) combines search with language models. "
                    "It retrieves relevant documents and uses them as context for generation. "
                    "This approach reduces hallucination and keeps responses factual.",
            metadata={"topic": "rag", "level": "intermediate"},
            source="RAG Tutorial",
        ),
        Document(
            id="doc4",
            content="Vector databases store embeddings for efficient similarity search. "
                    "Popular options include Pinecone, Weaviate, Qdrant, and ChromaDB. "
                    "They support metadata filtering and hybrid search.",
            metadata={"topic": "databases", "level": "intermediate"},
            source="Vector DB Guide",
        ),
    ]

    # Ingest
    count = pipeline.ingest(documents)
    print(f"\nPipeline stats: {pipeline.stats()}")

    # Query
    queries = [
        "What is RAG and how does it work?",
        "Which programming language is good for data science?",
        "What are vector databases used for?",
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = pipeline.retriever.retrieve(query, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. Score: {r.score:.4f} | {r.chunk.content[:60]}...")


def demo_reranking():
    """Demo: Reranking retrieval results."""
    print("\n" + "=" * 60)
    print("DEMO 3: Reranking")
    print("=" * 60)

    pipeline = RAGPipeline(use_local_embeddings=True)

    # Reuse documents
    documents = [
        Document("d1", "RAG combines retrieval and generation for accurate answers.",
                 metadata={"topic": "rag"}, source="RAG Guide"),
        Document("d2", "Vector embeddings capture semantic meaning of text for search.",
                 metadata={"topic": "embeddings"}, source="Embeddings Book"),
        Document("d3", "Fine-tuning trains a model on specific domain data.",
                 metadata={"topic": "training"}, source="Training Guide"),
    ]

    pipeline.ingest(documents)

    query = "How does RAG work?"
    print(f"Query: '{query}'\n")

    # Without reranking
    results = pipeline.retriever.retrieve(query, top_k=3)
    print("Without reranking:")
    for r in results:
        print(f"  Score: {r.score:.4f} | {r.chunk.content[:50]}...")

    # With reranking
    reranked = pipeline.reranker.rerank(query, results, top_k=3)
    print("\nWith reranking:")
    for r in reranked:
        print(f"  Original: {r.score:.4f} -> Reranked: {r.rerank_score:.4f} | {r.chunk.content[:50]}...")


def demo_full_pipeline():
    """Demo: Complete RAG pipeline with generation."""
    print("\n" + "=" * 60)
    print("DEMO 4: Full RAG Pipeline")
    print("=" * 60)

    pipeline = RAGPipeline(use_local_embeddings=True, generation_model="gpt-4o-mini")

    # Ingest knowledge base
    documents = [
        Document("kb1", """Retrieval-Augmented Generation (RAG) is a technique that enhances 
language models by retrieving relevant information from external knowledge bases before 
generating responses. RAG was introduced by Facebook AI Research (FAIR) in 2020 and has 
since become a standard approach for building knowledge-intensive AI applications.

The RAG pipeline consists of three main stages:
1. Document Processing: Splitting documents into manageable chunks
2. Retrieval: Finding relevant chunks using vector similarity search
3. Generation: Creating responses using the retrieved context as grounding

RAG offers several advantages over fine-tuning:
- No model retraining required
- Easy knowledge base updates
- Transparent and auditable responses
- Cost-effective for domain-specific applications""",
            source="RAG Documentation"
        ),
        Document("kb2", """Vector embeddings are numerical representations of text that capture 
semantic meaning. When text is converted to embeddings, similar concepts end up close together 
in vector space. This enables semantic search, where you can find relevant documents based 
on meaning rather than exact keyword matches.

Common embedding models include:
- OpenAI text-embedding-3-small/large
- Sentence Transformers (all-MiniLM-L6-v2)
- Cohere embed-v3

Vector databases like Qdrant, Pinecone, and Weaviat store these embeddings and enable 
efficient similarity search at scale.""",
            source="Embeddings Guide"
        ),
        Document("kb3", """Document chunking is critical for RAG performance. Poor chunking 
leads to irrelevant context and degraded answers. Best practices include:

1. Chunk Size: 200-1000 characters typically works well
2. Overlap: 10-20% overlap preserves context across chunks
3. Semantic Boundaries: Split at paragraph or section boundaries
4. Metadata: Preserve source information for citation

Recursive splitting is often the best default strategy, as it tries to maintain 
semantic coherence while respecting size limits.""",
            source="Chunking Best Practices"
        ),
    ]

    pipeline.ingest(documents)
    print(f"Pipeline: {pipeline.stats()}\n")

    # Query with full generation
    query = "What are the benefits of RAG compared to fine-tuning?"
    print(f"Query: {query}")
    response = pipeline.query(query, top_k=3, rerank=True)

    print(f"\nAnswer: {response.answer}")
    print(f"\nSources used: {len(response.sources)}")
    for i, source in enumerate(response.sources, 1):
        print(f"  [{i}] {source.chunk.metadata.get('source', 'unknown')} (score: {source.score:.4f})")
    print(f"\nLatency: {response.latency_ms:.0f}ms")


def demo_evaluation():
    """Demo: RAG evaluation metrics."""
    print("\n" + "=" * 60)
    print("DEMO 5: RAG Evaluation")
    print("=" * 60)

    evaluator = RAGEvaluator()

    # Simulate retrieval results
    query = "What is RAG?"
    retrieved = [
        RetrievalResult(
            chunk=Chunk("c1", "RAG combines retrieval and generation", "d1", 0),
            score=0.92,
        ),
        RetrievalResult(
            chunk=Chunk("c2", "Vector search finds relevant documents", "d2", 0),
            score=0.85,
        ),
    ]
    relevant_ids = ["c1"]

    # Evaluate retrieval
    retrieval_metrics = evaluator.evaluate_retrieval(query, retrieved, relevant_ids)
    print("Retrieval Metrics:")
    print(f"  Precision: {retrieval_metrics['precision']:.2f}")
    print(f"  Recall: {retrieval_metrics['recall']:.2f}")
    print(f"  MRR: {retrieval_metrics['mrr']:.2f}")

    # Evaluate answer
    answer = "RAG is Retrieval-Augmented Generation, a technique that combines search with LLMs."
    context = "RAG combines retrieval and generation for accurate answers."
    answer_metrics = evaluator.evaluate_answer(answer, context, query)
    print(f"\nAnswer Metrics:")
    print(f"  Faithfulness: {answer_metrics['faithfulness']:.2f}")
    print(f"  Relevance: {answer_metrics['relevance']:.2f}")
    print(f"  Completeness: {answer_metrics['completeness']:.2f}")


# ---------------------------------------------------------------------------
# 11. Main Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("RAG System Exercises")
    print("=" * 60)
    print()

    # Run demos
    demo_chunking()
    demo_retrieval()
    demo_reranking()
    # demo_full_pipeline()  # Uncomment if OPENAI_API_KEY is set
    demo_evaluation()

    print("\nAll demos complete!")
    print("Uncomment demo_full_pipeline() to run with OpenAI API.")
