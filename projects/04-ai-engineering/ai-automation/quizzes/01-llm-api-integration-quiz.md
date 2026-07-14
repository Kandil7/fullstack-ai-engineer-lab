# Quiz 01: LLM API Integration

## Topic Overview
This quiz covers the fundamentals of integrating Large Language Models (LLMs) into applications. Topics include API authentication, request/response handling, streaming, token management, rate limiting, error handling, and multi-provider integration patterns.

---

## Questions

### Question 1
**What is the primary purpose of the `temperature` parameter in LLM API calls?**

- A) To control the maximum number of tokens generated
- B) To control the randomness/creativity of the output
- C) To set the API timeout duration
- D) To define the model version to use

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The `temperature` parameter (typically 0.0 to 2.0) controls the randomness of token selection. Lower values (e.g., 0.1) make the output more deterministic and focused, while higher values (e.g., 1.5) increase creativity and randomness. It does not affect token limits, timeouts, or model selection.
</details>

---

### Question 2
**Which HTTP status code indicates you've exceeded your API rate limit?**

- A) 400 Bad Request
- B) 401 Unauthorized
- C) 429 Too Many Requests
- D) 500 Internal Server Error

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** HTTP 429 is the standard status code for rate limiting. When an API rate limit is exceeded, the server returns 429 to indicate too many requests in a given time window. 400 indicates malformed requests, 401 indicates authentication failures, and 500 indicates server-side errors.
</details>

---

### Question 3
**What is "tokenization" in the context of LLM APIs?**

- A) Encrypting the API key for security
- B) Splitting input text into token units for the model
- C) Compressing the API response payload
- D) Converting the model output to JSON format

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Tokenization is the process of breaking text into smaller units called tokens. LLMs process input as tokens rather than raw text. Common tokenizers include BPE (Byte-Pair Encoding). Understanding tokenization is crucial because pricing and context limits are measured in tokens, not words.
</details>

---

### Question 4
**When using streaming API responses, what format is commonly used to deliver incremental tokens?**

- A) XML
- B) WebSocket frames only
- C) Server-Sent Events (SSE)
- D) gRPC bidirectional streams

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Server-Sent Events (SSE) is the most common format for streaming LLM responses. SSE allows the server to push data to the client over a single HTTP connection. While WebSockets can be used, SSE is simpler and sufficient for one-way streaming. Most LLM providers (OpenAI, Anthropic) use SSE for streaming endpoints.
</details>

---

### Question 5
**What is "prompt caching" in LLM API integration?**

- A) Storing API keys in a secure cache
- B) Caching repeated prompts to avoid redundant API calls
- C) Saving model weights locally for faster inference
- D) Caching browser responses for web applications

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt caching stores results for repeated or similar prompts to reduce API calls and costs. When the same or very similar prompt is sent again, the cached response is returned without making a new API call. This is particularly useful for chat applications with repeated system prompts.
</details>

---

### Question 6
**Which authentication method is most secure for storing API keys in a production application?**

- A) Hardcoding keys directly in source code
- B) Storing keys in a public Git repository
- C) Using environment variables or a secrets manager
- D) Embedding keys in the frontend JavaScript

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Environment variables and dedicated secrets managers (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) are the most secure methods. Hardcoding keys, storing them in public repos, or embedding them in frontend code exposes them to unauthorized access. Secrets managers provide encryption, access control, and audit logging.
</details>

---

### Question 7
**What does the `max_tokens` parameter control in an LLM API request?**

- A) The maximum input length the model accepts
- B) The maximum number of tokens in the generated response
- C) The total token budget for the entire conversation
- D) The maximum number of API calls per minute

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The `max_tokens` parameter sets the upper limit on the number of tokens the model will generate in its response. It does not affect input length. Note that the total context window includes both input and output tokens, so `max_tokens` should be set considering the available context window after accounting for input tokens.
</details>

---

### Question 8
**When implementing retry logic for LLM API calls, what is the recommended approach?**

- A) Retry immediately without any delay
- B) Use exponential backoff with jitter
- C) Retry a fixed number of times with constant delay
- D) Never retry failed API calls

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Exponential backoff with jitter is the recommended approach. It starts with a short delay and increases exponentially (e.g., 1s, 2s, 4s, 8s) while adding random jitter to prevent thundering herd problems. This approach respects rate limits while recovering from transient failures. Always set a maximum retry count and handle permanent failures gracefully.
</details>

---

### Question 9
**What is the purpose of "system prompts" in LLM API conversations?**

- A) To authenticate the user's API key
- B) To set the model's behavior, personality, and constraints
- C) To specify the API endpoint URL
- D) To define the tokenization algorithm

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** System prompts define the model's role, behavior, tone, and constraints. They are typically sent at the beginning of a conversation and influence all subsequent responses. System prompts are essential for creating consistent, reliable AI assistants with specific capabilities or limitations.
</details>

---

### Question 10
**What is "function calling" in modern LLM APIs?**

- A) Calling external functions in the programming language
- B) Allowing the model to request structured function invocations
- C) Defining the model's internal neural network functions
- D) Creating API endpoints for the model

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Function calling allows the LLM to generate structured JSON requests that map to predefined functions. Instead of generating free-form text, the model outputs structured data indicating which function to call and with what parameters. This enables LLMs to interact with external tools, databases, and APIs in a controlled, predictable way.
</details>

---

### Question 11
**Which of the following is NOT a common LLM API provider?**

- A) OpenAI
- B) Anthropic
- C) TensorFlow.js
- D) Google Vertex AI

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** TensorFlow.js is a JavaScript library for machine learning that runs in browsers and Node.js. It is not an LLM API provider. OpenAI, Anthropic, and Google Vertex AI are all major providers offering LLM APIs for text generation, embeddings, and other AI capabilities.
</details>

---

### Question 12
**What is "streaming completion" in LLM APIs?**

- A) Completing the model training in real-time
- B) Receiving response tokens incrementally as they are generated
- C) Completing the entire API response at once
- D) Auto-completing API endpoint URLs

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Streaming completion sends tokens one by one (or in small batches) as the model generates them, rather than waiting for the complete response. This reduces perceived latency for users since they start seeing output immediately. It's implemented via Server-Sent Events (SSE) or similar streaming protocols.
</details>

---

### Question 13
**What is the "context window" in LLM API terms?**

- A) The API response time window
- B) The maximum number of tokens the model can process (input + output)
- C) The rate limit window for API calls
- D) The time window for prompt caching

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The context window is the maximum number of tokens the model can handle in a single request, including both input and output tokens. Different models have different context window sizes (e.g., 4K, 8K, 32K, 128K tokens). Exceeding the context window will result in errors or truncation.
</details>

---

### Question 14
**When handling API errors, which HTTP status code indicates an invalid API key?**

- A) 400 Bad Request
- B) 401 Unauthorized
- C) 403 Forbidden
- D) 429 Too Many Requests

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** HTTP 401 Unauthorized indicates authentication failure, which occurs when the API key is invalid, expired, or missing. HTTP 403 Forbidden indicates the key is valid but lacks permission for the requested operation. HTTP 400 indicates malformed request syntax, and 429 indicates rate limiting.
</details>

---

### Question 15
**What is "token pricing" in LLM API integration?**

- A) Setting the price for your application's API
- B) Paying per API call regardless of input/output size
- C) Charging based on the number of tokens processed (input + output)
- D) Fixed monthly subscription for unlimited usage

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** LLM APIs typically charge based on token usage, with different rates for input and output tokens. This means longer prompts and longer responses cost more. Understanding token pricing is essential for budgeting and optimizing API usage in production applications.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Easy | | |
| 7 | Easy | | |
| 8 | Medium | | |
| 9 | Easy | | |
| 10 | Medium | | |
| 11 | Easy | | |
| 12 | Medium | | |
| 13 | Medium | | |
| 14 | Easy | | |
| 15 | Easy | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 6 | C | 11 | C |
| 2 | C | 7 | B | 12 | B |
| 3 | B | 8 | B | 13 | B |
| 4 | C | 9 | B | 14 | B |
| 5 | B | 10 | B | 15 | C |

---

*Generated for AI Automation Lab - Quiz 01 of 09*