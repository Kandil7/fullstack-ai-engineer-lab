"""
Pydantic schemas for LLM structured outputs and API contracts.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class TokenUsage(BaseModel):
    """Token usage for a request."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMRequest(BaseModel):
    """Request to LLM API."""
    messages: List[Dict[str, str]]
    model: str
    max_tokens: int = 4096
    temperature: float = 0.1
    stream: bool = False
    response_format: Optional[Dict[str, Any]] = None


class LLMResponse(BaseModel):
    """Response from LLM API."""
    content: str
    usage: TokenUsage
    model: str
    latency_ms: float


class RAGContext(BaseModel):
    """A single context chunk for RAG."""
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float


class RAGRequest(BaseModel):
    """RAG query request."""
    query: str
    conversation_history: List[Dict[str, str]] = []
    filter: Optional[Dict[str, Any]] = None
    use_reranker: bool = True
    stream: bool = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class RAGResponse(BaseModel):
    """RAG query response."""
    answer: str
    contexts: List[RAGContext]
    usage: Dict[str, Any]
    latency_ms: float
    request_id: str


class IngestRequest(BaseModel):
    """Repository ingestion request."""
    repo_path: str
    chunker: str = "fixed"
    chunk_size: int = 512
    chunk_overlap: int = 50
    exclude_patterns: List[str] = []


class IngestResponse(BaseModel):
    """Ingestion response."""
    documents_ingested: int
    chunks_created: int
    elapsed_ms: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "0.1.0"
    components: Dict[str, str] = {}


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None


class AskRequest(BaseModel):
    """Simple ask endpoint request."""
    question: str
    stream: bool = True
    conversation_id: Optional[str] = None


class AskResponse(BaseModel):
    """Simple ask endpoint response."""
    answer: str
    conversation_id: str
    sources: List[Dict[str, Any]] = []


class EmbeddingRequest(BaseModel):
    """Embedding generation request."""
    texts: List[str]
    model: Optional[str] = None


class EmbeddingResponse(BaseModel):
    """Embedding generation response."""
    embeddings: List[List[float]]
    usage: TokenUsage
    model: str


class RerankRequest(BaseModel):
    """Rerank request."""
    query: str
    documents: List[str]
    top_k: int = 5


class RerankResponse(BaseModel):
    """Rerank response."""
    results: List[Dict[str, Any]]


class AgentRunRequest(BaseModel):
    """Agent execution request."""
    goal: str
    tools: List[str] = []
    max_steps: int = 10


class AgentRunResponse(BaseModel):
    """Agent execution response."""
    result: str
    steps: List[Dict[str, Any]]
    success: bool


class MCPToolCall(BaseModel):
    """MCP tool call request."""
    name: str
    arguments: Dict[str, Any]


class MCPToolResult(BaseModel):
    """MCP tool call result."""
    content: Any
    is_error: bool = False


# Prompt templates schemas
class PromptTemplate(BaseModel):
    """Versioned prompt template."""
    name: str
    version: str
    template: str
    variables: List[str] = []
    description: str = ""


class PromptRenderRequest(BaseModel):
    """Prompt rendering request."""
    template_name: str
    variables: Dict[str, Any]
    version: Optional[str] = None


class PromptRenderResponse(BaseModel):
    """Prompt rendering response."""
    rendered: str
    template: PromptTemplate
    tokens_estimate: int