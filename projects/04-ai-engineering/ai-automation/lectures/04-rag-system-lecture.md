# Lecture 04: RAG Systems (Retrieval-Augmented Generation)

## Topic Overview

Retrieval-Augmented Generation (RAG) combines the power of large language models with external knowledge retrieval. Instead of relying solely on the model's training data, RAG systems fetch relevant documents and use them as context for generating accurate, up-to-date responses. This lecture covers the complete RAG pipeline—from document ingestion to answer generation—and teaches you to build production-ready RAG systems.

**Duration:** 4-5 hours  
**Difficulty:** Intermediate to Advanced  
**Prerequisites:** Lecture 03 (Vector Embeddings), Lecture 01 (LLM API Integration)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the RAG architecture and why it matters
2. **Implement** a complete RAG pipeline from scratch
3. **Design** effective document chunking strategies
4. **Build** retrieval systems with vector databases
5. **Create** context-aware prompts for generation
6. **Evaluate** RAG system quality (relevance, faithfulness, accuracy)
7. **Optimize** RAG performance (latency, cost, quality)
8. **Handle** common RAG challenges (hallucination, context limits)

---

## Key Concepts

### 1. Why RAG?

LLMs have limitations that RAG addresses:

```
LLM alone:
┌─────────────────────────────────────────────────────┐
│  User Query → LLM → Response                        │
│                                                     │
│  Problems:                                          │
│  • Knowledge cutoff (can't know recent events)      │
│  • Hallucination (makes up facts)                   │
│  • No access to private data                        │
│  • Can't cite sources                               │
└─────────────────────────────────────────────────────┘

RAG:
┌─────────────────────────────────────────────────────┐
│  User Query → Retrieve Relevant Docs → LLM → Response│
│                                                     │
│  Benefits:                                          │
│  • Up-to-date information                          │
│  • Grounded in actual documents                     │
│  • Can access private knowledge bases               │
│  • Provides source citations                        │
└─────────────────────────────────────────────────────┘
```

### 2. The RAG Pipeline

Complete RAG system architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INGESTION PHASE (Offline):                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │ Documents│ → │ Chunking│ → │Embedding│ → │ Vector  │     │
│  │          │   │         │   │         │   │   DB    │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                                                                 │
│  QUERY PHASE (Online):                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │  Query   │ → │Embedding│ → │ Retrieve│ → │ Generate│     │
│  │          │   │         │   │   Docs  │   │ Response│     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Document Ingestion

How to process different document types:

```python
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import hashlib


@dataclass
class Document:
    """A document with metadata."""
    content: str
    metadata: dict
    doc_id: str = None
    
    def __post_init__(self):
        if self.doc_id is None:
            self.doc_id = hashlib.md5(self.content.encode()).hexdigest()


class DocumentLoader:
    """Load documents from various sources."""
    
    def load_text(self, file_path: str) -> Document:
        """Load plain text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Document(
            content=content,
            metadata={
                "source": file_path,
                "type": "text",
                "size": len(content)
            }
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load PDF file."""
        import PyPDF2
        
        documents = []
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            
            for page_num, page in enumerate(pdf_reader.pages):
                content = page.extract_text()
                if content:
                    documents.append(Document(
                        content=content,
                        metadata={
                            "source": file_path,
                            "type": "pdf",
                            "page": page_num + 1
                        }
                    ))
        
        return documents
    
    def load_markdown(self, file_path: str) -> List[Document]:
        """Load markdown file, split by sections."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by headers
        sections = content.split('\n## ')
        documents = []
        
        for i, section in enumerate(sections):
            if i == 0:
                # First section might not have header
                header = "Introduction"
                body = section
            else:
                lines = section.split('\n', 1)
                header = lines[0].strip()
                body = lines[1] if len(lines) > 1 else ""
            
            documents.append(Document(
                content=f"## {header}\n{body}" if i > 0 else body,
                metadata={
                    "source": file_path,
                    "type": "markdown",
                    "section": header
                }
            ))
        
        return documents
    
    def load_directory(self, dir_path: str, glob_pattern: str = "*.md") -> List[Document]:
        """Load all matching files from a directory."""
        documents = []
        path = Path(dir_path)
        
        for file_path in path.glob(glob_pattern):
            if file_path.is_file():
                if file_path.suffix == '.md':
                    documents.extend(self.load_markdown(str(file_path)))
                elif file_path.suffix == '.txt':
                    documents.append(self.load_text(str(file_path)))
        
        return documents
```

### 4. Chunking Strategies

Different strategies for splitting documents:

```python
from typing import List
import re


class TextChunker:
    """Various chunking strategies."""
    
    @staticmethod
    def fixed_size(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 100
    ) -> List[str]:
        """Split into fixed-size chunks with overlap."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    @staticmethod
    def sentence_based(
        text: str,
        max_sentences: int = 5
    ) -> List[str]:
        """Split by sentences, grouping into chunks."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        
        for sentence in sentences:
            current_chunk.append(sentence)
            if len(current_chunk) >= max_sentences:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    @staticmethod
    def recursive(
        text: str,
        chunk_size: int = 1000,
        separators: List[str] = None
    ) -> List[str]:
        """Recursively split by separators."""
        if separators is None:
            separators = ["\n\n", "\n", ". ", " "]
        
        if len(text) <= chunk_size:
            return [text]
        
        # Try each separator
        for separator in separators:
            if separator in text:
                parts = text.split(separator)
                chunks = []
                current = ""
                
                for part in parts:
                    if len(current) + len(part) < chunk_size:
                        current += part + separator
                    else:
                        if current:
                            chunks.append(current.strip())
                        current = part + separator
                
                if current:
                    chunks.append(current.strip())
                
                # Recursively chunk if needed
                final_chunks = []
                for chunk in chunks:
                    if len(chunk) > chunk_size:
                        final_chunks.extend(
                            TextChunker.recursive(chunk, chunk_size, separators[1:])
                        )
                    else:
                        final_chunks.append(chunk)
                
                return final_chunks
        
        # Fallback: split by words
        words = text.split()
        chunks = []
        current = []
        
        for word in words:
            current.append(word)
            if len(" ".join(current)) >= chunk_size:
                chunks.append(" ".join(current))
                current = []
        
        if current:
            chunks.append(" ".join(current))
        
        return chunks
    
    @staticmethod
    def semantic(
        text: str,
        similarity_threshold: float = 0.5
    ) -> List[str]:
        """Split where semantic similarity drops."""
        from sentence_transformers import SentenceTransformer
        import numpy as np
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        embeddings = model.encode(sentences)
        
        chunks = []
        current_chunk = [sentences[0]]
        
        for i in range(1, len(sentences)):
            # Calculate similarity with previous sentence
            similarity = np.dot(embeddings[i-1], embeddings[i]) / (
                np.linalg.norm(embeddings[i-1]) * np.linalg.norm(embeddings[i])
            )
            
            if similarity < similarity_threshold:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]
            else:
                current_chunk.append(sentences[i])
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
```

### 5. Retrieval Strategies

How to find relevant documents:

```python
from typing import List, Optional
from dataclasses import dataclass
import numpy as np
from openai import OpenAI
import chromadb


@dataclass
class RetrievalResult:
    """A retrieval result with score and metadata."""
    content: str
    score: float
    metadata: dict
    doc_id: str


class Retriever:
    """Document retrieval with multiple strategies."""
    
    def __init__(self, collection_name: str = "documents"):
        self.client = OpenAI()
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def add_documents(self, documents: List[dict]):
        """Add documents to the index."""
        texts = [doc["content"] for doc in documents]
        embeddings = [self._get_embedding(text) for text in texts]
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=[doc.get("metadata", {}) for doc in documents],
            ids=[doc.get("id", f"doc_{i}") for i, doc in enumerate(documents)]
        )
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
        score_threshold: float = 0.0
    ) -> List[RetrievalResult]:
        """Basic semantic retrieval."""
        
        query_embedding = self._get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters
        )
        
        retrieval_results = []
        for i in range(len(results["ids"][0])):
            score = 1 - results["distances"][0][i]  # Convert to similarity
            
            if score >= score_threshold:
                retrieval_results.append(RetrievalResult(
                    content=results["documents"][0][i],
                    score=score,
                    metadata=results["metadatas"][0][i],
                    doc_id=results["ids"][0][i]
                ))
        
        return retrieval_results
    
    def retrieve_with_reranking(
        self,
        query: str,
        initial_k: int = 20,
        final_k: int = 5
    ) -> List[RetrievalResult]:
        """Retrieve more results, then rerank."""
        
        # Get initial results
        initial_results = self.retrieve(query, top_k=initial_k)
        
        # Rerank using cross-encoder (simplified)
        # In production, use a cross-encoder model
        reranked = sorted(
            initial_results,
            key=lambda x: x.score,
            reverse=True
        )[:final_k]
        
        return reranked
    
    def retrieve_hybrid(
        self,
        query: str,
        top_k: int = 5,
        semantic_weight: float = 0.7
    ) -> List[RetrievalResult]:
        """Combine semantic and keyword search."""
        
        # Semantic search
        semantic_results = self.retrieve(query, top_k=top_k * 2)
        
        # Keyword search (simplified - using metadata)
        # In production, use BM25 or similar
        keyword_results = []
        for result in semantic_results:
            # Simple keyword matching
            query_words = query.lower().split()
            content_words = result.content.lower().split()
            keyword_score = sum(1 for w in query_words if w in content_words) / len(query_words)
            keyword_results.append((result, keyword_score))
        
        # Combine scores
        combined = []
        for result, kw_score in keyword_results:
            combined_score = semantic_weight * result.score + (1 - semantic_weight) * kw_score
            combined.append((result, combined_score))
        
        # Sort by combined score
        combined.sort(key=lambda x: x[1], reverse=True)
        
        return [result for result, score in combined[:top_k]]
```

### 6. Context Construction

How to build the context for the LLM:

```python
from typing import List
from dataclasses import dataclass


@dataclass
class Context:
    """Constructed context for RAG generation."""
    prompt: str
    sources: List[str]
    total_tokens: int


class ContextBuilder:
    """Build context from retrieved documents."""
    
    def __init__(self, max_context_tokens: int = 3000):
        self.max_context_tokens = max_context_tokens
    
    def build_context(
        self,
        query: str,
        documents: List[dict],
        template: str = None
    ) -> Context:
        """Build context from query and documents."""
        
        if template is None:
            template = """Answer the question based on the provided context.

Context:
{context}

Question: {question}

Answer:"""
        
        # Format documents as context
        context_parts = []
        sources = []
        current_tokens = 0
        
        for i, doc in enumerate(documents):
            doc_text = f"[{i+1}] {doc['content']}"
            doc_tokens = len(doc_text.split())  # Approximate
            
            if current_tokens + doc_tokens > self.max_context_tokens:
                break
            
            context_parts.append(doc_text)
            sources.append(doc.get("metadata", {}).get("source", f"Document {i+1}"))
            current_tokens += doc_tokens
        
        context = "\n\n".join(context_parts)
        
        # Build final prompt
        prompt = template.format(
            context=context,
            question=query
        )
        
        return Context(
            prompt=prompt,
            sources=sources,
            total_tokens=current_tokens
        )
    
    def build_context_with_citations(
        self,
        query: str,
        documents: List[dict]
    ) -> str:
        """Build context with inline citations."""
        
        prompt = """Answer the question based on the provided context.
Include citations in your response using [1], [2], etc.

Context:
"""
        
        for i, doc in enumerate(documents):
            prompt += f"[{i+1}] {doc['content']}\n\n"
        
        prompt += f"Question: {query}\nAnswer:"
        
        return prompt
```

### 7. Answer Generation

How to generate answers with RAG:

```python
from typing import List, Optional
from dataclasses import dataclass
from openai import OpenAI


@dataclass
class RAGResponse:
    """A RAG-generated response with metadata."""
    answer: str
    sources: List[str]
    confidence: float
    model: str
    tokens_used: int


class RAGGenerator:
    """Generate answers using RAG."""
    
    def __init__(self, model: str = "gpt-4"):
        self.client = OpenAI()
        self.model = model
    
    def generate(
        self,
        query: str,
        context: str,
        sources: List[str],
        temperature: float = 0.3
    ) -> RAGResponse:
        """Generate an answer from query and context."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant that answers questions 
based on provided context. Always cite your sources using [1], [2], etc.
If the context doesn't contain enough information, say so clearly."""
            },
            {
                "role": "user",
                "content": f"""Context:
{context}

Question: {query}

Answer based on the context above. Cite sources where applicable."""
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        
        answer = response.choices[0].message.content
        
        # Simple confidence estimation
        confidence = self._estimate_confidence(answer, context)
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            model=self.model,
            tokens_used=response.usage.total_tokens
        )
    
    def generate_with_sources(
        self,
        query: str,
        retrieved_docs: List[dict]
    ) -> RAGResponse:
        """Generate answer with explicit source tracking."""
        
        # Build context with source references
        context_parts = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs):
            context_parts.append(f"[Source {i+1}]: {doc['content']}")
            sources.append(doc.get("metadata", {}).get("source", f"Doc {i+1}"))
        
        context = "\n\n".join(context_parts)
        
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant. Answer questions using 
the provided sources. Always reference sources as [Source 1], [Source 2], etc.
Be precise and only use information from the sources."""
            },
            {
                "role": "user",
                "content": f"""Sources:
{context}

Question: {query}

Provide a comprehensive answer citing the relevant sources."""
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        )
        
        return RAGResponse(
            answer=response.choices[0].message.content,
            sources=sources,
            confidence=self._estimate_confidence(
                response.choices[0].message.content,
                context
            ),
            model=self.model,
            tokens_used=response.usage.total_tokens
        )
    
    def _estimate_confidence(self, answer: str, context: str) -> float:
        """Simple confidence estimation."""
        # Check if answer mentions "I don't know" or similar
        uncertain_phrases = [
            "i don't know",
            "i'm not sure",
            "the context doesn't",
            "no information",
            "cannot determine"
        ]
        
        answer_lower = answer.lower()
        uncertainty_count = sum(1 for phrase in uncertain_phrases if phrase in answer_lower)
        
        if uncertainty_count > 0:
            return 0.3
        
        # Check citation count
        citation_count = answer.count("[") 
        if citation_count >= 2:
            return 0.8
        elif citation_count == 1:
            return 0.6
        else:
            return 0.5
```

---

## Code Examples

### Example 1: Complete RAG System

```python
"""
Production-ready RAG system with all components.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
import hashlib
from openai import OpenAI
import chromadb


@dataclass
class RAGConfig:
    """Configuration for RAG system."""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    max_context_tokens: int = 3000
    temperature: float = 0.3


@dataclass
class Document:
    """Document with content and metadata."""
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    doc_id: str = ""
    
    def __post_init__(self):
        if not self.doc_id:
            self.doc_id = hashlib.md5(self.content.encode()).hexdigest()[:12]


class RAGSystem:
    """Complete RAG system with ingestion, retrieval, and generation."""
    
    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        self.openai_client = OpenAI()
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name="rag_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    # ========== INGESTION ==========
    
    def ingest_text(self, text: str, metadata: Dict = None) -> str:
        """Ingest raw text."""
        chunks = self._chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                content=chunk,
                metadata=metadata or {},
                doc_id=f"text_{hashlib.md5(chunk.encode()).hexdigest()[:8]}"
            )
            self._add_document(doc)
        
        return f"Ingested {len(chunks)} chunks"
    
    def ingest_file(self, file_path: str) -> str:
        """Ingest a file."""
        path = Path(file_path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = {
            "source": str(path),
            "filename": path.name,
            "extension": path.suffix
        }
        
        return self.ingest_text(content, metadata)
    
    def ingest_documents(self, documents: List[Document]) -> str:
        """Ingest multiple documents."""
        total_chunks = 0
        
        for doc in documents:
            chunks = self._chunk_text(doc.content)
            for chunk in chunks:
                chunk_doc = Document(
                    content=chunk,
                    metadata={**doc.metadata, "chunk_of": doc.doc_id},
                    doc_id=f"{doc.doc_id}_{hashlib.md5(chunk.encode()).hexdigest()[:6]}"
                )
                self._add_document(chunk_doc)
                total_chunks += 1
        
        return f"Ingested {total_chunks} chunks from {len(documents)} documents"
    
    def _chunk_text(self, text: str) -> List[str]:
        """Chunk text using configured strategy."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.config.chunk_size - self.config.chunk_overlap):
            chunk = " ".join(words[i:i + self.config.chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def _add_document(self, doc: Document):
        """Add a document to the vector store."""
        embedding = self._get_embedding(doc.content)
        
        self.collection.add(
            documents=[doc.content],
            embeddings=[embedding],
            metadatas=[doc.metadata],
            ids=[doc.doc_id]
        )
    
    # ========== RETRIEVAL ==========
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        filters: Dict = None
    ) -> List[Dict]:
        """Retrieve relevant documents."""
        top_k = top_k or self.config.top_k
        
        query_embedding = self._get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters
        )
        
        retrieved = []
        for i in range(len(results["ids"][0])):
            retrieved.append({
                "content": results["documents"][0][i],
                "score": 1 - results["distances"][0][i],
                "metadata": results["metadatas"][0][i],
                "doc_id": results["ids"][0][i]
            })
        
        return retrieved
    
    # ========== GENERATION ==========
    
    def generate(
        self,
        query: str,
        context_docs: List[Dict] = None,
        temperature: float = None
    ) -> Dict:
        """Generate answer with RAG."""
        temperature = temperature or self.config.temperature
        
        # Retrieve if not provided
        if context_docs is None:
            context_docs = self.retrieve(query)
        
        # Build context
        context = self._build_context(query, context_docs)
        
        # Generate
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant that answers questions 
based on provided context. Always cite sources using [1], [2], etc.
If the context doesn't contain enough information, say so."""
            },
            {
                "role": "user",
                "content": context
            }
        ]
        
        response = self.openai_client.chat.completions.create(
            model=self.config.llm_model,
            messages=messages,
            temperature=temperature
        )
        
        answer = response.choices[0].message.content
        
        # Extract sources
        sources = list(set(
            doc.get("metadata", {}).get("source", "Unknown")
            for doc in context_docs
        ))
        
        return {
            "answer": answer,
            "sources": sources,
            "context_docs": context_docs,
            "tokens_used": response.usage.total_tokens
        }
    
    def _build_context(self, query: str, documents: List[Dict]) -> str:
        """Build context string for generation."""
        context_parts = []
        
        for i, doc in enumerate(documents):
            context_parts.append(f"[{i+1}] {doc['content']}")
        
        context = "\n\n".join(context_parts)
        
        return f"""Context:
{context}

Question: {query}

Answer based on the context above. Cite sources using [1], [2], etc."""
    
    # ========== HELPERS ==========
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.openai_client.embeddings.create(
            model=self.config.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def get_stats(self) -> Dict:
        """Get system statistics."""
        return {
            "total_documents": self.collection.count(),
            "embedding_model": self.config.embedding_model,
            "llm_model": self.config.llm_model,
            "chunk_size": self.config.chunk_size
        }


# Usage
rag = RAGSystem()

# Ingest documents
rag.ingest_file("data/company_policies.md")
rag.ingest_file("data/product_docs.md")

# Query
result = rag.generate("What is our vacation policy?")

print("Answer:", result["answer"])
print("Sources:", result["sources"])
```

### Example 2: RAG Evaluation System

```python
"""
Evaluate RAG system quality.
"""
from dataclasses import dataclass
from typing import List
from openai import OpenAI


@dataclass
class EvalCase:
    """A test case for RAG evaluation."""
    question: str
    expected_answer: str
    relevant_doc_ids: List[str]


@dataclass
class EvalResult:
    """Evaluation result for a single case."""
    question: str
    generated_answer: str
    expected_answer: str
    relevance_score: float  # Is the answer relevant?
    faithfulness_score: float  # Is it grounded in context?
    answer_correctness: float  # Does it match expected?


class RAGEvaluator:
    """Evaluate RAG system quality."""
    
    def __init__(self, rag_system):
        self.rag = rag_system
        self.client = OpenAI()
    
    def evaluate(
        self,
        eval_cases: List[EvalCase]
    ) -> List[EvalResult]:
        """Evaluate RAG on test cases."""
        
        results = []
        
        for case in eval_cases:
            # Get RAG response
            rag_result = self.rag.generate(case.question)
            
            # Evaluate using LLM-as-judge
            relevance = self._evaluate_relevance(
                case.question,
                rag_result["answer"],
                [doc["content"] for doc in rag_result["context_docs"]]
            )
            
            faithfulness = self._evaluate_faithfulness(
                rag_result["answer"],
                [doc["content"] for doc in rag_result["context_docs"]]
            )
            
            correctness = self._evaluate_correctness(
                rag_result["answer"],
                case.expected_answer
            )
            
            results.append(EvalResult(
                question=case.question,
                generated_answer=rag_result["answer"],
                expected_answer=case.expected_answer,
                relevance_score=relevance,
                faithfulness_score=faithfulness,
                answer_correctness=correctness
            ))
        
        return results
    
    def _evaluate_relevance(
        self,
        question: str,
        answer: str,
        contexts: List[str]
    ) -> float:
        """Evaluate if answer is relevant to question."""
        
        prompt = f"""Rate the relevance of this answer to the question.

Question: {question}
Answer: {answer}

Rate on a scale of 0-1:
- 0: Completely irrelevant
- 0.5: Partially relevant
- 1: Fully relevant

Provide only the numerical score."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def _evaluate_faithfulness(
        self,
        answer: str,
        contexts: List[str]
    ) -> float:
        """Evaluate if answer is grounded in context."""
        
        prompt = f"""Evaluate if this answer is faithful to the provided context.

Context:
{chr(10).join(contexts)}

Answer: {answer}

Rate on a scale of 0-1:
- 0: Answer contains hallucinations
- 0.5: Answer is partially supported
- 1: Answer is fully supported by context

Provide only the numerical score."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def _evaluate_correctness(
        self,
        generated: str,
        expected: str
    ) -> float:
        """Evaluate correctness against expected answer."""
        
        prompt = f"""Compare these two answers and rate their similarity.

Generated: {generated}
Expected: {expected}

Rate on a scale of 0-1:
- 0: Completely different
- 0.5: Partially similar
- 1: Essentially identical

Provide only the numerical score."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def summarize_results(self, results: List[EvalResult]) -> dict:
        """Summarize evaluation results."""
        
        if not results:
            return {"error": "No results"}
        
        return {
            "total_cases": len(results),
            "avg_relevance": sum(r.relevance_score for r in results) / len(results),
            "avg_faithfulness": sum(r.faithfulness_score for r in results) / len(results),
            "avg_correctness": sum(r.answer_correctness for r in results) / len(results),
            "min_relevance": min(r.relevance_score for r in results),
            "min_faithfulness": min(r.faithfulness_score for r in results),
            "worst_cases": [
                {
                    "question": r.question,
                    "relevance": r.relevance_score,
                    "faithfulness": r.faithfulness_score
                }
                for r in sorted(results, key=lambda x: x.relevance_score)[:3]
            ]
        }
```

---

## Common Mistakes to Avoid

### 1. Chunking Too Large
```python
# ❌ BAD: Chunks too large, diluting relevant info
chunks = chunk_text(document, chunk_size=5000)

# ✅ GOOD: Appropriate chunk size
chunks = chunk_text(document, chunk_size=500)
```

### 2. No Context Limit
```python
# ❌ BAD: Passing all retrieved docs to LLM
context = "\n".join([doc.content for doc in all_retrieved])

# ✅ GOOD: Limit context to fit token budget
context = build_context(query, retrieved[:5], max_tokens=3000)
```

### 3. Ignoring Hallucination
```python
# ❌ BAD: Not checking if answer is grounded
response = rag.generate(query)

# ✅ GOOD: Evaluate faithfulness
response = rag.generate(query)
faithfulness = evaluate_faithfulness(response.answer, context)
if faithfulness < 0.7:
    print("Warning: Low faithfulness score")
```

---

## Best Practices

1. **Chunk strategically** - Balance context and precision
2. **Use metadata filtering** - Narrow search space
3. **Limit context tokens** - Prevent context dilution
4. **Cite sources** - Build trust and verifiability
5. **Evaluate regularly** - Measure relevance, faithfulness, accuracy
6. **Handle edge cases** - Graceful fallback when retrieval fails
7. **Cache embeddings** - Reduce API costs
8. **Monitor quality** - Track retrieval and generation metrics
9. **Iterate on prompts** - Optimize context presentation
10. **Use hybrid search** - Combine semantic + keyword

---

## Practice Exercises

### Exercise 1: Q&A System
Build a Q&A system that:
1. Ingests a collection of documents
2. Answers questions with source citations
3. Handles "I don't know" when context is insufficient

### Exercise 2: Document Summarizer
Create a system that:
1. Retrieves relevant sections from long documents
2. Generates summaries with key points
3. Provides confidence scores

### Exercise 3: Multi-Document Analysis
Build a system that:
1. Retrieves from multiple document types
2. Synthesizes information across documents
3. Identifies contradictions or gaps

### Exercise 4: RAG Optimizer
Create tools that:
1. Test different chunk sizes
2. Compare retrieval strategies
3. Optimize for quality vs. latency

### Exercise 5: Production Monitor
Build monitoring that:
1. Logs all RAG queries and responses
2. Tracks retrieval quality over time
3. Alerts on quality degradation

---

## Summary

RAG systems combine retrieval with generation for accurate, grounded responses:

1. **Ingestion** - Process and chunk documents
2. **Retrieval** - Find relevant context
3. **Context Construction** - Build effective prompts
4. **Generation** - Produce answers with citations
5. **Evaluation** - Measure quality systematically

**Key Success Factors:**
- Appropriate chunking strategy
- Effective retrieval
- Proper context construction
- Quality evaluation
- Continuous monitoring

**Next lecture:** AI Agents - Building autonomous systems.
