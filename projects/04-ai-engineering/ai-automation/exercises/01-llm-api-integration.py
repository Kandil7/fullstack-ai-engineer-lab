"""
Exercise 01: LLM API Integration
==================================
Master working with multiple LLM providers: OpenAI, Claude, and Groq.
Learn multi-provider abstraction, streaming, function calling, cost tracking,
and error handling for production AI applications.

Prerequisites:
    pip install openai anthropic groq python-dotenv

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
    ANTHROPIC_API_KEY=sk-ant-...
    GROQ_API_KEY=gsk_...
"""

import os
import time
import json
from dataclasses import dataclass, field
from typing import Generator, Optional
from enum import Enum

# ---------------------------------------------------------------------------
# 1. Configuration & Constants
# ---------------------------------------------------------------------------

class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"


@dataclass
class LLMConfig:
    """Configuration for an LLM provider."""
    provider: Provider
    model: str
    api_key: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1024

    def __post_init__(self):
        env_keys = {
            Provider.OPENAI: "OPENAI_API_KEY",
            Provider.ANTHROPIC: "ANTHROPIC_API_KEY",
            Provider.GROQ: "GROQ_API_KEY",
        }
        if self.api_key is None:
            env_var = env_keys.get(self.provider, "")
            self.api_key = os.getenv(env_var)


@dataclass
class UsageStats:
    """Track token usage and costs across calls."""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_calls: int = 0
    total_cost: float = 0.0
    _cost_per_1k_tokens: dict = field(default_factory=lambda: {
        "gpt-4o": {"input": 0.0025, "output": 0.01},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
        "claude-haiku-4-20250514": {"input": 0.0008, "output": 0.004},
        "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079},
        "mixtral-8x7b-32768": {"input": 0.00024, "output": 0.00024},
    })

    def record(self, model: str, input_tokens: int, output_tokens: int):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_calls += 1

        prices = self._cost_per_1k_tokens.get(model, {"input": 0.001, "output": 0.003})
        cost = (input_tokens / 1000 * prices["input"]) + (output_tokens / 1000 * prices["output"])
        self.total_cost += cost

    def summary(self) -> str:
        return (
            f"Calls: {self.total_calls} | "
            f"Input: {self.total_input_tokens:,} tokens | "
            f"Output: {self.total_output_tokens:,} tokens | "
            f"Cost: ${self.total_cost:.4f}"
        )


# Global usage tracker
usage = UsageStats()


# ---------------------------------------------------------------------------
# 2. OpenAI Integration
# ---------------------------------------------------------------------------

def openai_chat(prompt: str, *, system: str = "You are a helpful assistant.",
                config: LLMConfig | None = None) -> str:
    """Send a chat completion request to OpenAI."""
    from openai import OpenAI

    config = config or LLMConfig(Provider.OPENAI, "gpt-4o-mini")
    client = OpenAI(api_key=config.api_key)

    response = client.chat.completions.create(
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    msg = response.choices[0].message.content or ""
    usage.record(config.model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return msg


def openai_stream(prompt: str, *, system: str = "You are a helpful assistant.",
                  model: str = "gpt-4o-mini") -> Generator[str, None, None]:
    """Stream OpenAI responses token-by-token."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    stream = client.chat.completions.create(
        model=model,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content


def openai_function_call(prompt: str, tools: list[dict]) -> dict:
    """Demonstrate OpenAI function/tool calling."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant with access to tools."},
            {"role": "user", "content": prompt},
        ],
        tools=tools,
        tool_choice="auto",
    )

    choice = response.choices[0]
    if choice.message.tool_calls:
        tool_call = choice.message.tool_calls[0]
        return {
            "tool": tool_call.function.name,
            "args": json.loads(tool_call.function.arguments),
        }
    return {"text": choice.message.content}


# ---------------------------------------------------------------------------
# 3. Claude (Anthropic) Integration
# ---------------------------------------------------------------------------

def claude_chat(prompt: str, *, system: str = "You are a helpful assistant.",
                model: str = "claude-sonnet-4-20250514") -> str:
    """Send a message to Claude."""
    from anthropic import Anthropic

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    usage.record(model, response.usage.input_tokens, response.usage.output_tokens)
    return text


def claude_stream(prompt: str, *, system: str = "You are a helpful assistant.",
                  model: str = "claude-haiku-4-20250514") -> Generator[str, None, None]:
    """Stream Claude responses."""
    from anthropic import Anthropic

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    with client.messages.stream(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def claude_tool_use(prompt: str, tools: list[dict]) -> dict:
    """Demonstrate Claude's tool use capability."""
    from anthropic import Anthropic

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
    )

    for block in response.content:
        if block.type == "tool_use":
            return {"tool": block.name, "args": block.input}

    return {"text": response.content[0].text}


# ---------------------------------------------------------------------------
# 4. Groq Integration
# ---------------------------------------------------------------------------

def groq_chat(prompt: str, *, system: str = "You are a helpful assistant.",
              model: str = "llama-3.3-70b-versatile") -> str:
    """Send a chat completion request to Groq (fast inference)."""
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        temperature=0.7,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    msg = response.choices[0].message.content or ""
    usage.record(model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return msg


def groq_stream(prompt: str, *, model: str = "llama-3.3-70b-versatile") -> Generator[str, None, None]:
    """Stream Groq responses."""
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    stream = client.chat.completions.create(
        model=model,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content


# ---------------------------------------------------------------------------
# 5. Multi-Provider Abstraction Layer
# ---------------------------------------------------------------------------

class LLMClient:
    """
    Unified interface for multiple LLM providers.
    
    Usage:
        client = LLMClient(Provider.OPENAI, "gpt-4o-mini")
        response = client.chat("What is AI?")
        
        client = LLMClient(Provider.GROQ, "llama-3.3-70b-versatile")
        response = client.chat("What is AI?")
    """

    def __init__(self, provider: Provider, model: str, api_key: str | None = None):
        self.config = LLMConfig(provider, model, api_key)
        self.provider = provider

    def chat(self, prompt: str, *, system: str = "You are a helpful assistant.") -> str:
        """Send a chat request via the configured provider."""
        dispatch = {
            Provider.OPENAI: lambda: openai_chat(prompt, system=system, config=self.config),
            Provider.ANTHROPIC: lambda: claude_chat(prompt, system=system, model=self.config.model),
            Provider.GROQ: lambda: groq_chat(prompt, system=system, model=self.config.model),
        }

        handler = dispatch.get(self.provider)
        if handler is None:
            raise ValueError(f"Unsupported provider: {self.provider}")

        start = time.time()
        result = handler()
        elapsed = time.time() - start
        print(f"[{self.provider.value}] Response in {elapsed:.2f}s")
        return result

    def stream(self, prompt: str, *, system: str = "You are a helpful assistant.") -> Generator[str, None, None]:
        """Stream a response via the configured provider."""
        if self.provider == Provider.OPENAI:
            yield from openai_stream(prompt, system=system, model=self.config.model)
        elif self.provider == Provider.ANTHROPIC:
            yield from claude_stream(prompt, system=system, model=self.config.model)
        elif self.provider == Provider.GROQ:
            yield from groq_stream(prompt, system=system, model=self.config.model)
        else:
            raise ValueError(f"Streaming not supported for: {self.provider}")

    def function_call(self, prompt: str, tools: list[dict]) -> dict:
        """Send a function calling request."""
        if self.provider == Provider.OPENAI:
            return openai_function_call(prompt, tools)
        elif self.provider == Provider.ANTHROPIC:
            return claude_tool_use(prompt, tools)
        else:
            raise ValueError(f"Function calling not supported for: {self.provider}")


# ---------------------------------------------------------------------------
# 6. Error Handling & Retry Logic
# ---------------------------------------------------------------------------

class LLMError(Exception):
    """Base exception for LLM integration errors."""


class RateLimitError(LLMError):
    """Raised when rate limited by the provider."""


class AuthenticationError(LLMError):
    """Raised when API key is invalid or missing."""


def retry_with_backoff(func, *, max_retries: int = 3, base_delay: float = 1.0):
    """
    Retry an LLM call with exponential backoff.
    
    Example:
        result = retry_with_backoff(lambda: openai_chat("Hello"))
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            error_msg = str(e).lower()
            if "rate_limit" in error_msg or "429" in error_msg:
                delay = base_delay * (2 ** attempt)
                print(f"Rate limited. Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                last_exception = RateLimitError(str(e))
            elif "unauthorized" in error_msg or "401" in error_msg:
                raise AuthenticationError(f"Invalid API key: {e}") from e
            else:
                delay = base_delay * (2 ** attempt)
                print(f"Error: {e}. Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                last_exception = LLMError(str(e))

    raise last_exception or LLMError("Max retries exceeded")


# ---------------------------------------------------------------------------
# 7. Example Usage & Demo
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search a knowledge base for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "top_k": {"type": "integer", "description": "Number of results"},
                },
                "required": ["query"],
            },
        },
    },
]


def demo_basic_chat():
    """Demo: Basic chat with different providers."""
    print("=" * 60)
    print("DEMO 1: Basic Chat")
    print("=" * 60)

    client = LLMClient(Provider.GROQ, "llama-3.3-70b-versatile")
    response = client.chat("Explain what a vector database is in 2 sentences.")
    print(f"Response: {response}\n")


def demo_streaming():
    """Demo: Streaming responses."""
    print("=" * 60)
    print("DEMO 2: Streaming")
    print("=" * 60)

    client = LLMClient(Provider.GROQ, "llama-3.3-70b-versatile")
    print("Response: ", end="")
    for token in client.stream("Write a haiku about machine learning."):
        print(token, end="", flush=True)
    print("\n")


def demo_function_calling():
    """Demo: Function/tool calling."""
    print("=" * 60)
    print("DEMO 3: Function Calling")
    print("=" * 60)

    client = LLMClient(Provider.OPENAI, "gpt-4o-mini")
    result = client.function_call(
        "What's the weather in San Francisco?",
        tools=TOOL_DEFINITIONS,
    )
    print(f"Tool call result: {json.dumps(result, indent=2)}\n")


def demo_cost_tracking():
    """Demo: Cost tracking across multiple calls."""
    print("=" * 60)
    print("DEMO 4: Cost Tracking")
    print("=" * 60)

    client = LLMClient(Provider.GROQ, "llama-3.3-70b-versatile")
    prompts = [
        "What is RAG?",
        "What are embeddings?",
        "What is fine-tuning?",
    ]

    for p in prompts:
        client.chat(p)

    print(f"\nUsage Stats: {usage.summary()}\n")


def demo_error_handling():
    """Demo: Error handling with retry logic."""
    print("=" * 60)
    print("DEMO 5: Error Handling")
    print("=" * 60)

    # Simulated call that would fail on first attempt
    def unreliable_call():
        if not os.getenv("GROQ_API_KEY"):
            raise LLMError("GROQ_API_KEY not set in environment")
        return groq_chat("Hello")

    try:
        result = retry_with_backoff(unreliable_call, max_retries=2)
        print(f"Result: {result}\n")
    except LLMError as e:
        print(f"Expected error (no API key): {e}\n")


# ---------------------------------------------------------------------------
# 8. Provider Comparison
# ---------------------------------------------------------------------------

def compare_providers(prompt: str):
    """Compare responses from all available providers."""
    print("=" * 60)
    print(f"COMPARISON: '{prompt}'")
    print("=" * 60)

    providers = [
        (Provider.GROQ, "llama-3.3-70b-versatile"),
        # Uncomment if you have the keys:
        # (Provider.OPENAI, "gpt-4o-mini"),
        # (Provider.ANTHROPIC, "claude-haiku-4-20250514"),
    ]

    for provider, model in providers:
        try:
            client = LLMClient(provider, model)
            start = time.time()
            response = client.chat(prompt)
            elapsed = time.time() - start
            print(f"\n--- {provider.value} ({model}) [{elapsed:.2f}s] ---")
            print(response[:200] + "..." if len(response) > 200 else response)
        except Exception as e:
            print(f"\n--- {provider.value}: Error - {e} ---")

    print(f"\n{usage.summary()}")


# ---------------------------------------------------------------------------
# 9. Main Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("LLM API Integration Exercises")
    print("=" * 60)
    print()

    # Run demos (uncomment those you have API keys for)
    demo_error_handling()

    # Uncomment if you have GROQ_API_KEY:
    # demo_basic_chat()
    # demo_streaming()
    # demo_cost_tracking()

    # Uncomment if you have OPENAI_API_KEY:
    # demo_function_calling()

    # Uncomment to compare providers:
    # compare_providers("What is retrieval-augmented generation?")

    print("\nDone! Uncomment demos above to run with your API keys.")
