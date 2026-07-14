# Glossary: LLM API Integration

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| API Key | Secret credential for authentication | Never hardcode in source |
| Token | Unit of text processing (~0.75 words) | Primary billing unit |
| Context Window | Maximum tokens model can process | Limits input + output |
| Streaming | Real-time token delivery | Better UX for long responses |
| Temperature | Randomness control (0-2) | 0 = deterministic |
| Max Tokens | Response length limit | Controls output size |
| Rate Limit | Requests per minute/hour | Implement backoff |
| Prompt | Input text to the model | Foundation of all interactions |
| Completion | Model's generated response | The output you receive |
| Embedding | Vector representation of text | Used for similarity search |
| Fine-tuning | Customizing model on your data | Requires training data |
| Inference | Running the model to generate output | What API calls do |

---

## Detailed Definitions

### API Key

**Definition:** A unique string used to authenticate your application with an LLM provider. It identifies your account and tracks usage/billing.

**Example:**
```python
import os
import openai

# Reading from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Using with client
client = openai.OpenAI(api_key=api_key)
```

**Related Terms:** Authentication, Bearer Token, Rate Limit

**Security Notes:**
- Store in environment variables or secret managers
- Never commit to version control
- Rotate keys if compromised
- Use separate keys for development and production

---

### Token

**Definition:** The basic unit of text that LLMs process. One token is approximately 0.75 words or 4 characters in English. Tokens are used for both billing and context limits.

**Example:**
```python
import tiktoken

# Count tokens for a specific model
encoding = tiktoken.encoding_for_model("gpt-4")

text = "Hello, how are you today?"
tokens = encoding.encode(text)
print(f"Text: {text}")
print(f"Tokens: {tokens}")
print(f"Token count: {len(tokens)}")  # ~7 tokens

# Decode tokens back to text
decoded = encoding.decode(tokens)
print(f"Decoded: {decoded}")
```

**Related Terms:** Context Window, Prompt, Completion, Pricing

**Key Facts:**
- 1 token ≈ 0.75 words (English)
- 1 token ≈ 4 characters (English)
- Pricing is per-token (input and output separately)
- Different models tokenize differently

---

### Context Window

**Definition:** The maximum number of tokens a model can process in a single request, including both input (prompt) and output (completion).

**Example:**
```python
# Check model context window
models = {
    "gpt-4": 8192,
    "gpt-4-turbo": 128000,
    "gpt-4o": 128000,
    "claude-3-opus": 200000,
    "claude-3-haiku": 200000
}

# Calculate available tokens for output
def available_output_tokens(model, prompt_tokens):
    context_window = models.get(model, 4096)
    return context_window - prompt_tokens - 100  # 100 for safety margin

available = available_output_tokens("gpt-4", 500)
print(f"Available output tokens: {available}")  # 7592
```

**Related Terms:** Token, Prompt, Completion, Max Tokens

**Why It Matters:**
- Exceeding the limit causes API errors
- Need to chunk long documents
- Affects how much context you can provide
- Influences cost calculations

---

### Streaming

**Definition:** Receiving model output incrementally as it's generated, rather than waiting for the complete response. Tokens are delivered as they're produced.

**Example:**
```python
from openai import OpenAI

client = OpenAI()

# Non-streaming (waits for complete response)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}]
)
print(response.choices[0].message.content)

# Streaming (real-time tokens)
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**Related Terms:** Chunk, Delta, Real-time, UX

**When to Use:**
- User-facing applications
- Long responses
- When time-to-first-token matters

---

### Temperature

**Definition:** A parameter (0-2) that controls the randomness of model output. Lower values produce more deterministic, focused responses. Higher values produce more creative, diverse outputs.

**Example:**
```python
# Deterministic output (factual tasks)
response_factual = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    temperature=0.0
)

# Balanced output (general use)
response_balanced = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a greeting"}],
    temperature=0.7
)

# Creative output (brainstorming)
response_creative = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a poem"}],
    temperature=1.2
)
```

**Related Terms:** Top P, Frequency Penalty, Creativity

**Guidelines:**
- `0.0`: Best for factual Q&A, code generation
- `0.3-0.5`: Good for focused tasks
- `0.7`: General purpose
- `0.9-1.2`: Creative writing, brainstorming
- `1.5+`: Very diverse, may be incoherent

---

### Max Tokens

**Definition:** A parameter that limits the maximum number of tokens in the model's response. This controls output length and affects cost.

**Example:**
```python
# Short response
response_short = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain Python"}],
    max_tokens=100  # ~75 words
)

# Long response
response_long = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain Python"}],
    max_tokens=2000  # ~1500 words
)

# Check if response was truncated
if response.choices[0].finish_reason == "length":
    print("Response was truncated - increase max_tokens")
```

**Related Terms:** Token, Context Window, Finish Reason

**Key Points:**
- Counted separately from input tokens
- Affects cost (output tokens are more expensive)
- Use "length" finish_reason to detect truncation

---

### Rate Limit

**Definition:** A restriction on the number of API requests you can make within a time period (usually per minute or per day). Exceeding limits results in 429 errors.

**Example:**
```python
import time
from openai import RateLimitError

def call_with_rate_limit_handling(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt * 1  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

**Related Terms:** Backoff, Throttling, Quota, 429 Error

**Typical Limits:**
- Free tier: 3-5 RPM (requests per minute)
- Pay-as-you-go: 50-500 RPM
- Enterprise: Custom limits

---

### Prompt

**Definition:** The input text you send to an LLM to get a response. It includes instructions, context, questions, and any text you want the model to process.

**Example:**
```python
# Simple prompt
prompt = "Explain quantum computing in simple terms."

# Structured prompt with system message
messages = [
    {
        "role": "system",
        "content": "You are a physics teacher who explains concepts simply."
    },
    {
        "role": "user",
        "content": "What is quantum entanglement?"
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
```

**Related Terms:** System Message, User Message, Completion, Chain-of-Thought

**Best Practices:**
- Be specific and clear
- Provide context when needed
- Use examples for complex tasks
- Structure with roles (system/user/assistant)

---

### Completion

**Definition:** The text generated by the model in response to your prompt. It's the output of the API call.

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is AI?"}]
)

# Access the completion
completion = response.choices[0].message.content
print(completion)  # "AI, or artificial intelligence, is..."

# Access metadata
print(f"Model: {response.model}")
print(f"Tokens used: {response.usage.total_tokens}")
print(f"Finish reason: {response.choices[0].finish_reason}")
```

**Related Terms:** Response, Output, Finish Reason, Usage

**Finish Reasons:**
- `stop`: Natural completion (model finished)
- `length`: Hit max_tokens limit
- `content_filter`: Content was filtered
- `null`: Streaming in progress

---

### Embedding

**Definition:** A numerical vector representation of text that captures semantic meaning. Similar texts have similar embeddings, enabling similarity search.

**Example:**
```python
from openai import OpenAI

client = OpenAI()

# Generate embedding
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="The cat sat on the mat"
)

embedding = response.data[0].embedding
print(f"Vector dimensions: {len(embedding)}")  # 1536
print(f"First 5 values: {embedding[:5]}")
```

**Related Terms:** Vector, Similarity Search, RAG, Semantic

**Use Cases:**
- Semantic search
- Recommendation systems
- Clustering similar documents
- RAG (Retrieval-Augmented Generation)

---

### System Message

**Definition:** A special message role that sets the AI's behavior, personality, and constraints. It's processed before user messages and influences all subsequent responses.

**Example:**
```python
# System message sets behavior
messages = [
    {
        "role": "system",
        "content": """You are a senior Python developer.
        - Always provide code examples
        - Explain your reasoning
        - Follow PEP 8 style
        - Be concise but thorough"""
    },
    {
        "role": "user",
        "content": "How do I read a CSV file?"
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
```

**Related Terms:** Role, Behavior, Personality, Constraints

**Key Points:**
- Only one system message (first in list)
- Anthropic requires it as separate parameter
- Defines AI's identity and rules
- Persists across conversation

---

### Model

**Definition:** The specific language model version used for generation. Different models have different capabilities, context windows, and pricing.

**Example:**
```python
# Compare models
models = {
    "gpt-4": {
        "context": 8192,
        "cost_input": 0.03,
        "cost_output": 0.06,
        "strength": "Reasoning"
    },
    "gpt-4o": {
        "context": 128000,
        "cost_input": 0.005,
        "cost_output": 0.015,
        "strength": "Speed + Quality"
    },
    "gpt-3.5-turbo": {
        "context": 16385,
        "cost_input": 0.0005,
        "cost_output": 0.0015,
        "strength": "Cost Efficiency"
    }
}

# Choose based on needs
def select_model(task_type, max_budget=0.01):
    if task_type == "complex_reasoning":
        return "gpt-4"
    elif task_type == "simple_qa":
        return "gpt-3.5-turbo"
    else:
        return "gpt-4o"  # Best balance
```

**Related Terms:** Context Window, Pricing, Capabilities

**Model Selection Guide:**
- GPT-4: Complex reasoning, analysis
- GPT-4o: General purpose, fast
- GPT-3.5-turbo: Simple tasks, cost-sensitive
- Claude: Long context, nuanced responses

---

### Backoff

**Definition:** A strategy for retrying failed requests with increasing delays. Used to handle rate limits and transient errors without overwhelming the server.

**Example:**
```python
import time
import random

def exponential_backoff(attempt, base_delay=1, max_delay=60):
    """Calculate wait time with jitter."""
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter

# Usage
for attempt in range(5):
    try:
        response = make_api_call()
        break
    except RateLimitError:
        wait = exponential_backoff(attempt)
        print(f"Attempt {attempt + 1} failed. Waiting {wait:.1f}s")
        time.sleep(wait)
```

**Related Terms:** Rate Limit, Retry, Jitter, Throttling

**Why Jitter:**
- Prevents thundering herd problem
- Spreads retry load across time
- More reliable than fixed delays

---

### Finish Reason

**Definition:** A field in the API response indicating why the model stopped generating. Helps detect truncation or content filtering.

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a long essay"}],
    max_tokens=100  # Intentionally short
)

reason = response.choices[0].finish_reason

if reason == "stop":
    print("Completed normally")
elif reason == "length":
    print("Response truncated - increase max_tokens")
elif reason == "content_filter":
    print("Content was filtered")
elif reason == "tool_calls":
    print("Model wants to call a tool")
```

**Related Terms:** Max Tokens, Truncation, Content Filter

**Possible Values:**
- `stop`: Natural ending
- `length`: Hit token limit
- `content_filter`: Blocked content
- `tool_calls`: Function calling mode
- `null`: Still streaming

---

### Chunk

**Definition:** A segment of text, typically used when splitting long documents for processing or when receiving streaming output.

**Example:**
```python
def chunk_text(text, max_tokens=4000, overlap=200):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_count = 0
    
    for word in words:
        current_chunk.append(word)
        current_count += 1
        
        if current_count >= max_tokens:
            chunks.append(" ".join(current_chunk))
            # Keep overlap
            current_chunk = current_chunk[-overlap:]
            current_count = overlap
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

# Usage
long_document = read_file("huge.txt")
chunks = chunk_text(long_document)
print(f"Split into {len(chunks)} chunks")
```

**Related Terms:** Context Window, Token, Overlap, Processing

**Why Chunk:**
- Documents may exceed context window
- Enables parallel processing
- Overlap maintains context across chunks
- Required for RAG systems

---

## Summary

Understanding these terms is essential for effective LLM API integration:

1. **Authentication**: API keys, secure storage
2. **Tokens**: Units of processing and billing
3. **Context Window**: Maximum processing capacity
4. **Streaming**: Real-time response delivery
5. **Temperature**: Output randomness control
6. **Rate Limits**: Request throttling
7. **Prompts**: Input construction
8. **Completions**: Model output
9. **Embeddings**: Semantic vectors
10. **Error Handling**: Retries, backoff, recovery

**Next:** See Lecture 02 for prompt engineering techniques.
