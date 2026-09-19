"""
Pydantic schemas for LLM structured outputs and API contracts.
"""

from typing import Any

from pydantic import BaseModel


class TokenUsage(BaseModel):
    """Token usage for a request."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMRequest(BaseModel):
    """Request to LLM API."""

    messages: list[dict[str, str]]
    model: str
    max_tokens: int = 4096
    temperature: float = 0.1
    stream: bool = False
    response_format: dict[str, Any] | None = None


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
    metadata: dict[str, Any]
    score: float


class RAGRequest(BaseModel):
    """RAG query request."""

    query: str
    conversation_history: list[dict[str, str]] = []
    filter: dict[str, Any] | None = None
    use_reranker: bool = True
    stream: bool = False
    max_tokens: int | None = None
    temperature: float | None = None


class RAGResponse(BaseModel):
    """RAG query response."""

    answer: str
    contexts: list[RAGContext]
    usage: dict[str, Any]
    latency_ms: float
    request_id: str


class IngestRequest(BaseModel):
    """Repository ingestion request."""

    repo_path: str
    chunker: str = "fixed"
    chunk_size: int = 512
    chunk_overlap: int = 50
    exclude_patterns: list[str] = []


class IngestResponse(BaseModel):
    """Ingestion response."""

    documents_ingested: int
    chunks_created: int
    elapsed_ms: float


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str = "0.1.0"
    components: dict[str, str] = {}


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: str | None = None
    request_id: str | None = None


class AskRequest(BaseModel):
    """Simple ask endpoint request."""

    question: str
    stream: bool = True
    conversation_id: str | None = None


class AskResponse(BaseModel):
    """Simple ask endpoint response."""

    answer: str
    conversation_id: str
    sources: list[dict[str, Any]] = []


class EmbeddingRequest(BaseModel):
    """Embedding generation request."""

    texts: list[str]
    model: str | None = None


class EmbeddingResponse(BaseModel):
    """Embedding generation response."""

    embeddings: list[list[float]]
    usage: TokenUsage
    model: str


class RerankRequest(BaseModel):
    """Rerank request."""

    query: str
    documents: list[str]
    top_k: int = 5


class RerankResponse(BaseModel):
    """Rerank response."""

    results: list[dict[str, Any]]


class AgentRunRequest(BaseModel):
    """Agent execution request."""

    goal: str
    tools: list[str] = []
    max_steps: int = 10


class AgentRunResponse(BaseModel):
    """Agent execution response."""

    result: str
    steps: list[dict[str, Any]]
    success: bool


class MCPToolCall(BaseModel):
    """MCP tool call request."""

    name: str
    arguments: dict[str, Any]


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
    variables: list[str] = []
    description: str = ""


class PromptRenderRequest(BaseModel):
    """Prompt rendering request."""

    template_name: str
    variables: dict[str, Any]
    version: str | None = None


class PromptRenderResponse(BaseModel):
    """Prompt rendering response."""

    rendered: str
    template: PromptTemplate
    tokens_estimate: int
