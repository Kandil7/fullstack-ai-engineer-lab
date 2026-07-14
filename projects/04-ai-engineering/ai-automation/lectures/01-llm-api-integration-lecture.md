# Lecture 01: LLM API Integration

## Topic Overview

Large Language Model (LLM) API integration is the foundational skill for building AI-powered applications. This lecture covers how to programmatically interact with LLM providers (OpenAI, Anthropic, Google, etc.), handle authentication, manage API calls, process responses, and implement robust error handling. You will learn the patterns that form the backbone of every AI automation system.

**Duration:** 2-3 hours  
**Difficulty:** Beginner to Intermediate  
**Prerequisites:** Basic Python/JavaScript, HTTP fundamentals, API basics

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand** the architecture of LLM APIs and how they differ from traditional REST APIs
2. **Authenticate** with major LLM providers (OpenAI, Anthropic, Google)
3. **Implement** synchronous and streaming API calls
4. **Handle** token limits, rate limits, and cost optimization
5. **Parse** and process LLM responses programmatically
6. **Build** a reusable LLM client abstraction layer
7. **Debug** common API integration issues
8. **Implement** retry logic, fallbacks, and error recovery

---

## Key Concepts

### 1. LLM API Architecture

LLM APIs follow a client-server model where:

- **Client** sends a prompt (text) to the API endpoint
- **Server** runs inference on a massive language model
- **Response** contains the generated text, metadata, and usage information

```
┌─────────────┐    HTTP Request     ┌─────────────────┐
│  Your App    │ ─────────────────► │  LLM Provider    │
│  (Client)    │ ◄───────────────── │  (Server)        │
└─────────────┘    HTTP Response    └─────────────────┘
```

**Key differences from traditional APIs:**
- Responses are non-deterministic (same input can produce different outputs)
- Tokens are the unit of billing, not requests
- Streaming is the norm, not the exception
- Context windows impose hard limits on input size

### 2. Authentication Patterns

Every LLM provider uses API keys for authentication. The key is sent in the request header:

**OpenAI:**
```python
import openai

client = openai.OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Anthropic:**
```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Google Gemini:**
```python
import google.generativeai as genai

genai.configure(api_key="AIza...")
model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Hello!")
```

### 3. Message Format and Roles

LLMs use a message-based format with specific roles:

| Role | Purpose | Example |
|------|---------|---------|
| `system` | Sets AI behavior and context | "You are a helpful assistant" |
| `user` | Human input | "What is Python?" |
| `assistant` | AI responses | "Python is a programming language..." |
| `tool` | Results from tool calls | `{"result": "42"}` |

```python
messages = [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "Explain list comprehensions."},
    {"role": "assistant", "content": "List comprehensions are..."},
    {"role": "user", "content": "Give me an example."}
]
```

### 4. Streaming vs Non-Streaming

**Non-Streaming (Synchronous):**
```python
# Waits for complete response
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
print(response.choices[0].message.content)
```

**Streaming:**
```python
# Returns tokens as they're generated
stream = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

**When to use streaming:**
- User-facing applications (better UX)
- Long responses
- Real-time feedback needed

**When to use non-streaming:**
- Background processing
- Short responses
- When you need the complete response before proceeding

### 5. Token Management

Tokens are the currency of LLM APIs. Understanding them is critical:

- **1 token ≈ 0.75 words** (English)
- **1 token ≈ 4 characters** (English)
- Pricing is per-token (input and output separately)

```python
# Count tokens before sending
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4")
tokens = encoding.encode("Hello, world!")
print(f"Token count: {len(tokens)}")  # ~4 tokens
```

**Token limits by model:**

| Model | Context Window | Max Output |
|-------|---------------|------------|
| GPT-4o | 128K tokens | 16K tokens |
| Claude Sonnet 4 | 200K tokens | 8K tokens |
| Gemini Pro | 1M tokens | 8K tokens |

### 6. Temperature and Parameters

Control output behavior with parameters:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7,      # 0 = deterministic, 2 = very random
    max_tokens=1000,       # Limit response length
    top_p=0.9,             # Nucleus sampling
    frequency_penalty=0.0, # Reduce repetition
    presence_penalty=0.0   # Encourage new topics
)
```

**Parameter guide:**
- `temperature=0`: Best for factual, deterministic tasks
- `temperature=0.7`: Good balance for general use
- `temperature=1.0+`: Creative, diverse outputs

### 7. Error Handling and Retries

LLM APIs can fail. Implement robust error handling:

```python
import time
from openai import RateLimitError, APIError, Timeout

def call_llm_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                timeout=30.0
            )
            return response
            
        except RateLimitError as e:
            wait_time = 2 ** attempt * 1  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            
        except Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            
        except APIError as e:
            print(f"API error: {e}")
            if attempt == max_retries - 1:
                raise
    
    raise Exception("Max retries exceeded")
```

---

## Code Examples

### Example 1: Basic LLM Client Wrapper

```python
"""
A reusable LLM client that supports multiple providers.
"""
import os
from dataclasses import dataclass
from typing import Optional
import openai
import anthropic


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    finish_reason: str


class LLMClient:
    """Unified client for multiple LLM providers."""
    
    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        self.provider = provider
        self.model = model or self._default_model()
        
        if provider == "openai":
            self.client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            self.client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _default_model(self) -> str:
        defaults = {
            "openai": "gpt-4",
            "anthropic": "claude-sonnet-4-20250514"
        }
        return defaults[self.provider]
    
    def generate(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None
    ) -> LLMResponse:
        """Generate a response from the LLM."""
        
        # Prepend system prompt if provided
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        if self.provider == "openai":
            return self._generate_openai(messages, temperature, max_tokens)
        elif self.provider == "anthropic":
            return self._generate_anthropic(messages, temperature, max_tokens)
    
    def _generate_openai(self, messages, temperature, max_tokens):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            finish_reason=response.choices[0].finish_reason
        )
    
    def _generate_anthropic(self, messages, temperature, max_tokens):
        # Anthropic requires system prompt as separate parameter
        system = None
        if messages and messages[0]["role"] == "system":
            system = messages[0]["content"]
            messages = messages[1:]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages
        )
        
        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            finish_reason=response.stop_reason
        )


# Usage
client = LLMClient(provider="openai")
response = client.generate(
    messages=[{"role": "user", "content": "Explain recursion in 3 sentences."}],
    temperature=0.5,
    max_tokens=200
)
print(response.content)
print(f"Tokens used: {response.input_tokens + response.output_tokens}")
```

### Example 2: Streaming with Progress Tracking

```python
"""
Streaming response with token counting and progress display.
"""
import sys
from openai import OpenAI

client = OpenAI()

def stream_with_progress(messages, model="gpt-4"):
    """Stream response with real-time token counting."""
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    
    full_response = ""
    token_count = 0
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            full_response += token
            token_count += 1
            
            # Display with progress
            sys.stdout.write(f"\r[Tokens: {token_count}] {token}")
            sys.stdout.flush()
    
    print()  # New line after streaming
    
    return {
        "content": full_response,
        "token_count": token_count,
        "model": model
    }

# Usage
result = stream_with_progress([
    {"role": "user", "content": "Write a short poem about coding."}
])
print(f"\n\nTotal tokens: {result['token_count']}")
```

### Example 3: Batch Processing with Rate Limit Handling

```python
"""
Process multiple prompts efficiently with rate limit handling.
"""
import time
from dataclasses import dataclass
from typing import List
import openai

client = openai.OpenAI()

@dataclass
class BatchResult:
    prompt: str
    response: str
    tokens_used: int
    success: bool
    error: str = None


def process_batch(
    prompts: List[str],
    model: str = "gpt-4",
    requests_per_minute: int = 20,
    max_retries: int = 3
) -> List[BatchResult]:
    """Process multiple prompts with rate limiting."""
    
    results = []
    delay_between_requests = 60 / requests_per_minute
    
    for i, prompt in enumerate(prompts):
        result = None
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                
                result = BatchResult(
                    prompt=prompt,
                    response=response.choices[0].message.content,
                    tokens_used=response.usage.total_tokens,
                    success=True
                )
                break
                
            except openai.RateLimitError:
                wait_time = 2 ** attempt * 5
                print(f"Rate limited at {i+1}/{len(prompts)}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                
            except Exception as e:
                result = BatchResult(
                    prompt=prompt,
                    response="",
                    tokens_used=0,
                    success=False,
                    error=str(e)
                )
                break
        
        if result is None:
            result = BatchResult(
                prompt=prompt,
                response="",
                tokens_used=0,
                success=False,
                error="Max retries exceeded"
            )
        
        results.append(result)
        print(f"[{i+1}/{len(prompts)}] {'✓' if result.success else '✗'}")
        
        # Rate limiting
        if i < len(prompts) - 1:
            time.sleep(delay_between_requests)
    
    return results


# Usage
prompts = [
    "Explain machine learning in one sentence.",
    "What is a neural network?",
    "Define deep learning.",
    "What is NLP?",
    "Explain computer vision."
]

results = process_batch(prompts)
total_tokens = sum(r.tokens_used for r in results)
success_count = sum(1 for r in results if r.success)

print(f"\nResults: {success_count}/{len(prompts)} successful")
print(f"Total tokens: {total_tokens}")
```

---

## Common Mistakes to Avoid

### 1. Not Handling Rate Limits
```python
# ❌ BAD: No rate limit handling
for prompt in prompts:
    response = client.chat.completions.create(...)
    
# ✅ GOOD: With backoff
for prompt in prompts:
    try:
        response = client.chat.completions.create(...)
    except RateLimitError:
        time.sleep(2 ** attempt)
```

### 2. Ignoring Token Limits
```python
# ❌ BAD: Sending too many tokens
long_text = read_entire_file("huge_document.txt")  # 100K+ tokens
response = client.chat.completions.create(
    messages=[{"role": "user", "content": long_text}]
)

# ✅ GOOD: Chunk and process
chunks = split_into_chunks(long_text, max_tokens=4000)
responses = [process_chunk(chunk) for chunk in chunks]
```

### 3. Not Using Streaming for UX
```python
# ❌ BAD: User waits 30 seconds with no feedback
response = client.chat.completions.create(...)
print(response.choices[0].message.content)

# ✅ GOOD: Stream for better UX
stream = client.chat.completions.create(..., stream=True)
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
```

### 4. Hardcoding API Keys
```python
# ❌ BAD: Hardcoded key
client = openai.OpenAI(api_key="sk-secret123")

# ✅ GOOD: Environment variable
import os
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

---

## Best Practices

1. **Use environment variables** for API keys - never commit secrets
2. **Implement retry logic** with exponential backoff for all API calls
3. **Cache responses** when possible to reduce costs
4. **Monitor token usage** to track and optimize costs
5. **Use streaming** for user-facing applications
6. **Set appropriate timeouts** to prevent hanging requests
7. **Log all API calls** for debugging and cost tracking
8. **Validate inputs** before sending to the API
9. **Handle all error types** (rate limits, timeouts, invalid requests)
10. **Use model fallbacks** (try cheaper models first)

---

## Practice Exercises

### Exercise 1: Multi-Provider Client
Build a client that can switch between OpenAI and Anthropic with a single configuration change. Test with the same prompt on both providers.

### Exercise 2: Cost Calculator
Create a function that calculates the cost of an API call before making it, based on token count and model pricing.

### Exercise 3: Response Cache
Implement a cache that stores API responses keyed by the hash of the prompt + parameters. Include TTL (time-to-live) for cache invalidation.

### Exercise 4: Streaming Logger
Build a streaming wrapper that logs every token to a file while streaming to the console.

### Exercise 5: Retry Dashboard
Create a monitoring system that tracks retry counts, success rates, and average latency across API calls.

---

## Summary

LLM API integration is the foundation of AI automation. Key takeaways:

1. **Authentication** varies by provider but follows similar patterns
2. **Streaming** is essential for good user experience
3. **Token management** directly impacts cost and capability
4. **Error handling** must account for rate limits, timeouts, and failures
5. **Abstraction** over providers enables flexibility and migration
6. **Cost optimization** requires understanding token pricing and caching

**Next lecture:** Prompt Engineering - How to communicate effectively with LLMs.
