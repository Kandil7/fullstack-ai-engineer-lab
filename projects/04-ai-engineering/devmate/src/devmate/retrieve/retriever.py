"""
Retrieval module with reranking for RAG.
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import httpx

from devmate.config import settings
from devmate.index.vector_store import SearchResult, BaseVectorStore, get_vector_store
from devmate.obs.tracing import tracer


@dataclass
class RerankResult:
    """Result after reranking."""
    id: str
    score: float
    content: str
    metadata: Dict[str, Any]
    original_score: float


class BaseReranker(ABC):
    """Abstract base class for rerankers."""
    
    @abstractmethod
    async def rerank(
        self,
        query: str,
        documents: List[SearchResult],
        top_k: int,
    ) -> List[RerankResult]:
        pass


class CohereReranker(BaseReranker):
    """Cohere reranker API."""
    
    def __init__(self, api_key: str = None, model: str = "rerank-v3.5"):
        self.api_key = api_key
        self.model = model
        self.client = None
        
        if api_key:
            self.client = httpx.AsyncClient(
                base_url="https://api.cohere.ai/v1",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=httpx.Timeout(30.0, connect=10.0),
            )
    
    async def rerank(
        self,
        query: str,
        documents: List[SearchResult],
        top_k: int,
    ) -> List[RerankResult]:
        if not self.client or not documents:
            return [
                RerankResult(
                    id=doc.id,
                    score=doc.score,
                    content=doc.content,
                    metadata=doc.metadata,
                    original_score=doc.score,
                )
                for doc in documents[:top_k]
            ]
        
        async with tracer.trace("rerank.cohere", model=self.model, count=len(documents)):
            docs = [doc.content for doc in documents]
            
            payload = {
                "model": self.model,
                "query": query,
                "documents": docs,
                "top_n": top_k,
                "return_documents": False,
            }
            
            response = await self.client.post("/rerank", json=payload)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data["results"]:
                idx = item["index"]
                original_doc = documents[idx]
                results.append(RerankResult(
                    id=original_doc.id,
                    score=item["relevance_score"],
                    content=original_doc.content,
                    metadata=original_doc.metadata,
                    original_score=original_doc.score,
                ))
            
            return results
    
    async def close(self):
        if self.client:
            await self.client.aclose()


class LocalReranker(BaseReranker):
    """Local reranker using cross-encoder (e.g., bge-reranker)."""
    
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.model_name = model_name
        self._model = None
    
    def _load_model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name, max_length=512)
    
    async def rerank(
        self,
        query: str,
        documents: List[SearchResult],
        top_k: int,
    ) -> List[RerankResult]:
        if not documents:
            return []
        
        self._load_model()
        
        async with tracer.trace("rerank.local", model=self.model_name, count=len(documents)):
            pairs = [(query, doc.content) for doc in documents]
            
            # Run in thread pool
            loop = asyncio.get_event_loop()
            scores = await loop.run_in_executor(
                None,
                lambda: self._model.predict(pairs).tolist()
            )
            
            # Combine with original results
            reranked = []
            for doc, score in zip(documents, scores):
                reranked.append(RerankResult(
                    id=doc.id,
                    score=float(score),
                    content=doc.content,
                    metadata=doc.metadata,
                    original_score=doc.score,
                ))
            
            # Sort by rerank score
            reranked.sort(key=lambda x: x.score, reverse=True)
            
            return reranked[:top_k]


class NoOpReranker(BaseReranker):
    """No-op reranker (passthrough)."""
    
    async def rerank(
        self,
        query: str,
        documents: List[SearchResult],
        top_k: int,
    ) -> List[RerankResult]:
        return [
            RerankResult(
                id=doc.id,
                score=doc.score,
                content=doc.content,
                metadata=doc.metadata,
                original_score=doc.score,
            )
            for doc in documents[:top_k]
        ]


# Reranker factory
RERANKERS = {
    "cohere": CohereReranker,
    "local": LocalReranker,
    "none": NoOpReranker,
}


def get_reranker(name: str = "none", **kwargs) -> BaseReranker:
    """Get reranker by name."""
    if name not in RERANKERS:
        raise ValueError(f"Unknown reranker: {name}. Available: {list(RERANKERS.keys())}")
    return RERANKERS[name](**kwargs)


class Retriever:
    """High-level retriever combining vector search and reranking."""
    
    def __init__(
        self,
        vector_store: BaseVectorStore = None,
        reranker: BaseReranker = None,
        top_k: int = None,
        rerank_top_k: int = None,
    ):
        self.vector_store = vector_store
        self.reranker = reranker or get_reranker("none")
        self.top_k = top_k or settings.rag_top_k
        self.rerank_top_k = rerank_top_k or settings.rag_rerank_top_k
    
    async def retrieve(
        self,
        query: str,
        query_vector: List[float],
        filter: Optional[Dict[str, Any]] = None,
        use_reranker: bool = True,
    ) -> List[RerankResult]:
        """Retrieve and optionally rerank documents."""
        
        # Get vector store if not provided
        if self.vector_store is None:
            self.vector_store = await get_vector_store()
        
        async with tracer.trace("retrieve", query_length=len(query)):
            # Hybrid search
            results = await self.vector_store.hybrid_search(
                query_vector=query_vector,
                query_text=query,
                limit=self.top_k,
                filter=filter,
            )
            
            if not results:
                return []
            
            # Rerank if enabled
            if use_reranker and self.reranker:
                results = await self.reranker.rerank(query, results, self.rerank_top_k)
            
            return results
    
    async def retrieve_simple(
        self,
        query_vector: List[float],
        filter: Optional[Dict[str, Any]] = None,
        limit: int = None,
    ) -> List[SearchResult]:
        """Simple vector search without reranking."""
        if self.vector_store is None:
            self.vector_store = await get_vector_store()
        
        return await self.vector_store.search(
            query_vector=query_vector,
            limit=limit or self.top_k,
            filter=filter,
        )


# Global retriever instance
_retriever_instance: Optional[Retriever] = None


async def get_retriever() -> Retriever:
    """Get or create global retriever."""
    global _retriever_instance
    
    if _retriever_instance is None:
        # Try to use Cohere reranker if key available
        import os
        cohere_key = os.getenv("COHERE_API_KEY")
        reranker = get_reranker("cohere", api_key=cohere_key) if cohere_key else get_reranker("none")
        
        _retriever_instance = Retriever(reranker=reranker)
    
    return _retriever_instance