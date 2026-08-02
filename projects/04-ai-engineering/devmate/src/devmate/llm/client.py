"""
LLM Client with streaming, retries, cost tracking, and structured outputs.
"""

import asyncio
import json
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional, Type, TypeVar, Union
from contextlib import asynccontextmanager

import httpx
import tiktoken
from pydantic import BaseModel, ValidationError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type,
)

from devmate.config import settings
from devmate.obs.tracing import tracer
from devmate.obs.cost import cost_tracker, TokenUsage


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class LLMError(Exception):
    """Base exception for LLM errors."""
    pass


class LLMRateLimitError(LLMError):
    """Rate limit exceeded."""
    pass


class LLMAuthError(LLMError):
    """Authentication failed."""
    pass


class LLMTimeoutError(LLMError):
    """Request timeout."""
    pass


class LLMValidationError(LLMError):
    """Response validation failed."""
    pass


T = TypeVar("T", bound=BaseModel)


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    usage: TokenUsage
    model: str
    provider: LLMProvider
    latency_ms: float
    raw_response: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "usage": self.usage.to_dict(),
            "model": self.model,
            "provider": self.provider.value,
            "latency_ms": self.latency_ms,
        }


@dataclass
class StreamingChunk:
    """A chunk from a streaming response."""
    content: str
    is_final: bool = False
    usage: Optional[TokenUsage] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @property
    @abstractmethod
    def provider_name(self) -> LLMProvider:
        pass
    
    @abstractmethod
    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int,
        temperature: float,
        stream: bool = False,
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> Union[LLMResponse, AsyncIterator[StreamingChunk]]:
        pass
    
    @abstractmethod
    def count_tokens(self, text: str, model: str) -> int:
        pass


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider."""
    
    @property
    def provider_name(self) -> LLMProvider:
        return LLMProvider.ANTHROPIC
    
    def __init__(self):
        self.api_key = settings.anthropic_api_key
        if not self.api_key:
            raise LLMAuthError("ANTHROPIC_API_KEY not set")
        self.base_url = "https://api.anthropic.com/v1"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )
    
    def count_tokens(self, text: str, model: str) -> int:
        """Estimate tokens using tiktoken (approximation for Anthropic)."""
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception:
            return len(text) // 4  # Rough approximation
    
    @retry(
        wait=wait_exponential_jitter(initial=1, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        reraise=True,
    )
    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int,
        temperature: float,
        stream: bool = False,
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> Union[LLMResponse, AsyncIterator[StreamingChunk]]:
        """Complete a chat request with Anthropic."""
        
        # Separate system message
        system_prompt = ""
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_messages.append(msg)
        
        payload = {
            "model": model,
            "messages": user_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        # Add structured output if requested
        if response_model:
            schema = response_model.model_json_schema()
            payload["tools"] = [{
                "name": "structured_output",
                "description": "Return structured output matching the schema",
                "input_schema": schema,
            }]
            payload["tool_choice"] = {"type": "tool", "name": "structured_output"}
        
        start_time = time.perf_counter()
        
        async with tracer.trace("llm.complete", provider=self.provider_name.value, model=model) as span:
            try:
                if stream:
                    return self._stream_complete(payload, model, start_time)
                else:
                    return await self._complete_once(payload, model, start_time, response_model)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise LLMRateLimitError(f"Rate limited: {e.response.text}")
                elif e.response.status_code == 401:
                    raise LLMAuthError(f"Authentication failed: {e.response.text}")
                raise LLMError(f"API error: {e.response.status_code} - {e.response.text}")
    
    async def _complete_once(
        self,
        payload: Dict[str, Any],
        model: str,
        start_time: float,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> LLMResponse:
        """Single completion request."""
        response = await self.client.post("/messages", json=payload)
        response.raise_for_status()
        data = response.json()
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        # Extract content
        content = ""
        if "content" in data:
            for block in data["content"]:
                if block["type"] == "text":
                    content += block["text"]
                elif block["type"] == "tool_use" and response_model:
                    # Handle structured output
                    try:
                        validated = response_model(**block["input"])
                        content = validated.model_dump_json()
                    except ValidationError as e:
                        raise LLMValidationError(f"Structured output validation failed: {e}")
        
        # Extract usage
        usage_data = data.get("usage", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("input_tokens", 0),
            completion_tokens=usage_data.get("output_tokens", 0),
            total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
        )
        
        llm_response = LLMResponse(
            content=content,
            usage=usage,
            model=model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            raw_response=data,
        )
        
        # Track cost
        cost_tracker.record_usage(self.provider_name.value, model, usage, latency_ms)
        
        span.set_attribute("usage.prompt_tokens", usage.prompt_tokens)
        span.set_attribute("usage.completion_tokens", usage.completion_tokens)
        span.set_attribute("latency_ms", latency_ms)
        
        return llm_response
    
    async def _stream_complete(
        self,
        payload: Dict[str, Any],
        model: str,
        start_time: float,
    ) -> AsyncIterator[StreamingChunk]:
        """Streaming completion."""
        async with self.client.stream("POST", "/messages", json=payload) as response:
            response.raise_for_status()
            
            accumulated_content = ""
            usage = TokenUsage(0, 0, 0)
            
            async for line in response.aiter_lines():
                if not line.startswith("data: "):
                    continue
                
                data_str = line[6:]  # Remove "data: "
                if data_str.strip() == "[DONE]":
                    break
                
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    continue
                
                if data.get("type") == "content_block_delta":
                    delta = data.get("delta", {})
                    if delta.get("type") == "text_delta":
                        text = delta.get("text", "")
                        accumulated_content += text
                        yield StreamingChunk(content=text, is_final=False)
                
                elif data.get("type") == "message_delta":
                    usage_data = data.get("usage", {})
                    usage = TokenUsage(
                        prompt_tokens=usage_data.get("input_tokens", 0),
                        completion_tokens=usage_data.get("output_tokens", 0),
                        total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
                    )
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            cost_tracker.record_usage(self.provider_name.value, model, usage, latency_ms)
            
            yield StreamingChunk(content="", is_final=True, usage=usage)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider."""
    
    @property
    def provider_name(self) -> LLMProvider:
        return LLMProvider.OPENAI
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        if not self.api_key:
            raise LLMAuthError("OPENAI_API_KEY not set")
        self.base_url = "https://api.openai.com/v1"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )
    
    def count_tokens(self, text: str, model: str) -> int:
        """Count tokens using tiktoken."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    
    @retry(
        wait=wait_exponential_jitter(initial=1, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        reraise=True,
    )
    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int,
        temperature: float,
        stream: bool = False,
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> Union[LLMResponse, AsyncIterator[StreamingChunk]]:
        """Complete a chat request with OpenAI."""
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
        }
        
        if response_model:
            schema = response_model.model_json_schema()
            payload["tools"] = [{
                "type": "function",
                "function": {
                    "name": "structured_output",
                    "description": "Return structured output matching the schema",
                    "parameters": schema,
                }
            }]
            payload["tool_choice"] = {"type": "function", "function": {"name": "structured_output"}}
        
        start_time = time.perf_counter()
        
        async with tracer.trace("llm.complete", provider=self.provider_name.value, model=model) as span:
            try:
                if stream:
                    return self._stream_complete(payload, model, start_time)
                else:
                    return await self._complete_once(payload, model, start_time, response_model)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise LLMRateLimitError(f"Rate limited: {e.response.text}")
                elif e.response.status_code == 401:
                    raise LLMAuthError(f"Authentication failed: {e.response.text}")
                raise LLMError(f"API error: {e.response.status_code} - {e.response.text}")
    
    async def _complete_once(
        self,
        payload: Dict[str, Any],
        model: str,
        start_time: float,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> LLMResponse:
        """Single completion request."""
        response = await self.client.post("/chat/completions", json=payload)
        response.raise_for_status()
        data = response.json()
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        choice = data["choices"][0]
        content = choice["message"].get("content", "")
        
        # Handle structured output
        if response_model and choice["message"].get("tool_calls"):
            tool_call = choice["message"]["tool_calls"][0]
            args = json.loads(tool_call["function"]["arguments"])
            try:
                validated = response_model(**args)
                content = validated.model_dump_json()
            except ValidationError as e:
                raise LLMValidationError(f"Structured output validation failed: {e}")
        
        usage_data = data.get("usage", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0),
        )
        
        llm_response = LLMResponse(
            content=content,
            usage=usage,
            model=model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            raw_response=data,
        )
        
        cost_tracker.record_usage(self.provider_name.value, model, usage, latency_ms)
        
        span.set_attribute("usage.prompt_tokens", usage.prompt_tokens)
        span.set_attribute("usage.completion_tokens", usage.completion_tokens)
        span.set_attribute("latency_ms", latency_ms)
        
        return llm_response
    
    async def _stream_complete(
        self,
        payload: Dict[str, Any],
        model: str,
        start_time: float,
    ) -> AsyncIterator[StreamingChunk]:
        """Streaming completion."""
        async with self.client.stream("POST", "/chat/completions", json=payload) as response:
            response.raise_for_status()
            
            accumulated_content = ""
            usage = TokenUsage(0, 0, 0)
            
            async for line in response.aiter_lines():
                if not line.startswith("data: "):
                    continue
                
                data_str = line[6:]
                if data_str.strip() == "[DONE]":
                    break
                
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    continue
                
                choices = data.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    if "content" in delta and delta["content"]:
                        text = delta["content"]
                        accumulated_content += text
                        yield StreamingChunk(content=text, is_final=False)
                
                # Check for usage in final chunk
                if "usage" in data:
                    usage_data = data["usage"]
                    usage = TokenUsage(
                        prompt_tokens=usage_data.get("prompt_tokens", 0),
                        completion_tokens=usage_data.get("completion_tokens", 0),
                        total_tokens=usage_data.get("total_tokens", 0),
                    )
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            cost_tracker.record_usage(self.provider_name.value, model, usage, latency_ms)
            
            yield StreamingChunk(content="", is_final=True, usage=usage)


class LLMClient:
    """Unified LLM client with provider abstraction, fallbacks, and observability."""
    
    def __init__(self):
        self.providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self._init_providers()
        self.fallback_chain: List[LLMProvider] = [
            LLMProvider.ANTHROPIC,
            LLMProvider.OPENAI,
        ]
    
    def _init_providers(self):
        """Initialize available providers."""
        if settings.anthropic_api_key:
            try:
                self.providers[LLMProvider.ANTHROPIC] = AnthropicProvider()
            except Exception as e:
                print(f"Failed to init Anthropic: {e}")
        
        if settings.openai_api_key:
            try:
                self.providers[LLMProvider.OPENAI] = OpenAIProvider()
            except Exception as e:
                print(f"Failed to init OpenAI: {e}")
        
        if not self.providers:
            raise LLMAuthError("No LLM providers configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY")
    
    def get_provider(self, provider: Optional[LLMProvider] = None) -> BaseLLMProvider:
        """Get provider instance, defaulting to configured default."""
        if provider is None:
            provider = LLMProvider(settings.default_llm_provider)
        
        if provider not in self.providers:
            # Try fallback
            for fallback in self.fallback_chain:
                if fallback in self.providers:
                    print(f"Falling back to {fallback.value}")
                    return self.providers[fallback]
            raise LLMError(f"Provider {provider.value} not available and no fallback found")
        
        return self.providers[provider]
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stream: bool = False,
        response_model: Optional[Type[T]] = None,
        provider: Optional[LLMProvider] = None,
        **kwargs,
    ) -> Union[LLMResponse, AsyncIterator[StreamingChunk]]:
        """Complete with automatic fallback on failure."""
        
        model = model or settings.default_model
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature if temperature is not None else settings.temperature
        
        last_error = None
        
        for provider_name in [provider] + [p for p in self.fallback_chain if p != provider]:
            if provider_name is None:
                continue
            
            try:
                llm_provider = self.get_provider(provider_name)
                return await llm_provider.complete(
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=stream,
                    response_model=response_model,
                    **kwargs,
                )
            except (LLMRateLimitError, LLMAuthError, LLMTimeoutError, httpx.TimeoutException) as e:
                last_error = e
                print(f"Provider {provider_name.value} failed: {e}, trying fallback...")
                continue
            except Exception as e:
                last_error = e
                # Don't fallback on validation errors or other non-retryable errors
                if isinstance(e, LLMValidationError):
                    raise
                print(f"Provider {provider_name.value} failed unexpectedly: {e}, trying fallback...")
                continue
        
        raise LLMError(f"All providers failed. Last error: {last_error}")
    
    def count_tokens(self, text: str, model: Optional[str] = None, provider: Optional[LLMProvider] = None) -> int:
        """Count tokens using the specified or default provider."""
        llm_provider = self.get_provider(provider)
        return llm_provider.count_tokens(text, model or settings.default_model)
    
    async def close(self):
        """Close all provider clients."""
        for provider in self.providers.values():
            if hasattr(provider, 'client'):
                await provider.client.aclose()


# Global client instance — created lazily so that *importing* devmate never
# requires API keys. Without this, every module that imports devmate.llm.client
# crashed at import time in key-less environments (unit tests, docs tooling).
_llm_client_instance: Optional["LLMClient"] = None


def get_llm_client() -> "LLMClient":
    """Create (once) and return the global LLM client."""
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = LLMClient()
    return _llm_client_instance


class _LazyLLMClient:
    """Attribute proxy that instantiates the real client on first use.

    Preserves the existing ``llm_client.complete(...)`` call sites while deferring
    the (key-requiring) construction until the client is actually needed.
    """

    def __getattr__(self, name: str) -> Any:
        return getattr(get_llm_client(), name)


llm_client: Any = _LazyLLMClient()