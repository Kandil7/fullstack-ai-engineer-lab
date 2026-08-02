"""
DevMate - AI Assistant for Code Repositories

A production-grade RAG + Agent system with evaluation, observability, and MCP support.
"""

from devmate.config import settings
from devmate.llm.client import LLMClient
from devmate.obs.tracing import tracer
from devmate.obs.cost import cost_tracker

__version__ = "0.1.0"

__all__ = [
    "settings",
    "LLMClient",
    "tracer",
    "cost_tracker",
]