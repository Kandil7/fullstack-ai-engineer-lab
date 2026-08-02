"""
FastAPI application with lifespan, routing, and middleware.
"""

import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from devmate.config import settings
from devmate.llm.client import llm_client
from devmate.llm.schemas import (
    RAGRequest, RAGResponse, AskRequest, AskResponse,
    HealthResponse, ErrorResponse, IngestRequest, IngestResponse,
    EmbeddingRequest, EmbeddingResponse,
)
from devmate.retrieve.rag import get_rag_pipeline, RAGRequest as InternalRAGRequest
from devmate.obs.tracing import tracer
from devmate.obs.cost import cost_tracker
from devmate.ingest.chunker import DocumentLoader, get_chunker


# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.version if hasattr(settings, 'version') else '0.1.0'}")
    
    # Initialize clients
    try:
        # This will initialize vector store, retriever, etc.
        await get_rag_pipeline()
        print("RAG pipeline initialized")
    except Exception as e:
        print(f"Warning: Failed to initialize RAG pipeline: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down...")
    await llm_client.close()


# Create FastAPI app
app = FastAPI(
    title="DevMate API",
    description="AI Assistant for Code Repositories - RAG + Agents + MCP",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = request_id
    
    with tracer.trace("http.request", method=request.method, path=request.url.path) as span:
        span.set_attribute("request_id", request_id)
        
        start_time = datetime.utcnow()
        response = await call_next(request)
        latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        span.set_attribute("status_code", response.status_code)
        span.set_attribute("latency_ms", latency_ms)
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{latency_ms:.2f}ms"
        
        return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    
    with tracer.trace("http.error", error_type=type(exc).__name__) as span:
        span.set_status("error", str(exc))
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else None,
            request_id=request_id,
        ).model_dump(),
    )


# Health endpoints
@app.get("/health", response_model=HealthResponse)
async def health():
    """Liveness probe."""
    return HealthResponse(
        status="healthy",
        components={"api": "ok"},
    )


@app.get("/ready")
async def ready():
    """Readiness probe - checks dependencies."""
    components = {"api": "ok"}
    
    # Check Qdrant
    try:
        from devmate.index.vector_store import get_vector_store
        vs = await get_vector_store()
        count = await vs.count()
        components["qdrant"] = f"ok ({count} vectors)"
    except Exception as e:
        components["qdrant"] = f"error: {e}"
    
    # Check Redis
    try:
        import redis.asyncio as redis
        r = redis.from_url(settings.redis_connection_url)
        await r.ping()
        await r.close()
        components["redis"] = "ok"
    except Exception as e:
        components["redis"] = f"error: {e}"
    
    # Check LLM
    try:
        provider = llm_client.get_provider()
        components["llm"] = f"ok ({provider.provider_name.value})"
    except Exception as e:
        components["llm"] = f"error: {e}"
    
    all_healthy = all("ok" in v for v in components.values())
    
    return {
        "status": "ready" if all_healthy else "degraded",
        "components": components,
    }


# Ask endpoint (simple Q&A with RAG)
@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """Ask a question - returns streaming or full response."""
    rag_pipeline = await get_rag_pipeline()
    
    rag_request = InternalRAGRequest(
        query=request.question,
        stream=request.stream,
    )
    
    if request.stream:
        async def generate():
            result = await rag_pipeline.query(rag_request)
            async for chunk in result:
                yield f"data: {chunk.content}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"X-Conversation-ID": request.conversation_id or str(uuid.uuid4())},
        )
    else:
        result = await rag_pipeline.query(rag_request)
        
        sources = []
        for ctx in result.contexts:
            sources.append({
                "id": ctx.id,
                "content": ctx.content[:200] + "..." if len(ctx.content) > 200 else ctx.content,
                "metadata": ctx.metadata,
                "score": ctx.score,
            })
        
        return AskResponse(
            answer=result.answer,
            conversation_id=request.conversation_id or str(uuid.uuid4()),
            sources=sources,
        )


# RAG endpoint (full control)
@app.post("/ai/rag/query", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """Full RAG query with all options."""
    rag_pipeline = await get_rag_pipeline()
    
    internal_request = InternalRAGRequest(
        query=request.query,
        conversation_history=request.conversation_history,
        filter=request.filter,
        use_reranker=request.use_reranker,
        stream=request.stream,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    
    if request.stream:
        async def generate():
            result = await rag_pipeline.query(internal_request)
            async for chunk in result:
                yield f"data: {chunk.model_dump_json()}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    result = await rag_pipeline.query(internal_request)
    
    return RAGResponse(
        answer=result.answer,
        contexts=[
            {
                "id": ctx.id,
                "content": ctx.content,
                "metadata": ctx.metadata,
                "score": ctx.score,
            }
            for ctx in result.contexts
        ],
        usage=result.usage,
        latency_ms=result.latency_ms,
        request_id=result.request_id,
    )


# Ingestion endpoint
@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    """Ingest a repository or directory."""
    import time
    start_time = time.perf_counter()
    
    repo_path = Path(request.repo_path)
    if not repo_path.exists():
        raise HTTPException(404, f"Path not found: {request.repo_path}")
    
    # Get chunker
    chunker = get_chunker(request.chunker, chunk_size=request.chunk_size, overlap=request.chunk_overlap)
    loader = DocumentLoader(chunker=chunker)
    
    # Load documents
    documents = list(loader.load_repository(repo_path))
    
    # Ingest via RAG pipeline
    rag_pipeline = await get_rag_pipeline()
    chunks_created = await rag_pipeline.ingest_documents(documents)
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    return IngestResponse(
        documents_ingested=len(documents),
        chunks_created=chunks_created,
        elapsed_ms=elapsed_ms,
    )


# Embedding endpoint
@app.post("/ai/embeddings", response_model=EmbeddingResponse)
async def embeddings(request: EmbeddingRequest):
    """Generate embeddings for texts."""
    from devmate.index.embeddings import embedding_service
    
    result = await embedding_service.embed(request.texts)
    
    return EmbeddingResponse(
        embeddings=result.embeddings,
        usage=result.usage,
        model=result.model,
    )


# Cost/usage endpoint
@app.get("/ai/usage")
async def usage(since: str = None):
    """Get usage and cost statistics."""
    from datetime import datetime
    
    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            raise HTTPException(400, "Invalid date format. Use ISO format.")
    
    summary = cost_tracker.get_summary(since=since_dt)
    
    return {
        "total_requests": summary.total_requests,
        "total_tokens": summary.total_tokens,
        "total_cost_usd": round(summary.total_cost_usd, 6),
        "avg_latency_ms": round(summary.total_latency_ms / max(summary.total_requests, 1), 2),
        "by_model": {
            model: {
                "requests": int(data["requests"]),
                "tokens": int(data["tokens"]),
                "cost_usd": round(data["cost"], 6),
                "avg_latency_ms": round(data["latency_ms"] / max(data["requests"], 1), 2),
            }
            for model, data in summary.by_model.items()
        },
        "by_provider": {
            provider: {
                "requests": int(data["requests"]),
                "tokens": int(data["tokens"]),
                "cost_usd": round(data["cost"], 6),
                "avg_latency_ms": round(data["latency_ms"] / max(data["requests"], 1), 2),
            }
            for provider, data in summary.by_provider.items()
        },
    }


# Traces endpoint
@app.get("/traces")
async def traces(limit: int = 50):
    """Get recent traces."""
    recent = tracer.get_recent_traces(limit=limit)
    return {
        "traces": [t.to_dict() for t in recent],
    }


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "DevMate API",
        "version": "0.1.0",
        "description": "AI Assistant for Code Repositories",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "devmate.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )


# Import at bottom to avoid circular imports
from pathlib import Path