# Quiz 07: Agent Communication

> **Topic Overview**: Agent communication encompasses the protocols, formats, and patterns that enable agents to exchange information with users and other agents. This quiz covers message formats, API communication patterns, structured output, streaming, natural language interfaces, and protocols like MCP for standardized agent interaction.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 20 |
| Correct Answers | 0 |
| Score | 0% |
| Difficulty Rating | — |

---

## Questions

### Question 1 — Easy

**What is "structured output" in agent communication?**

- A) Output organized in paragraphs
- B) Responses formatted according to a predefined schema (JSON, XML, etc.) for reliable parsing
- C) Output with proper grammar
- D) Output that follows a specific writing style

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Structured output formats agent responses according to a predefined schema (like JSON Schema). This makes responses machine-readable, enabling reliable parsing and downstream processing. It's essential when agents need to produce data that other systems consume.

</details>

---

### Question 2 — Easy

**What is "streaming" in agent communication?**

- A) Watching videos on the agent
- B) Sending the agent's response token-by-token as it's generated, rather than waiting for the complete response
- C) Streaming audio from the agent
- D) Data streaming between databases

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Streaming sends the agent's response incrementally as tokens are generated. This provides real-time feedback to users, reduces perceived latency, and allows the application to process partial results. It's the standard for most LLM API interactions.

</details>

---

### Question 3 — Easy

**What is an "API endpoint" in agent communication?**

- A) The final result of an API call
- B) A specific URL path where the agent's API can be accessed
- C) The end of the agent's processing pipeline
- D) A termination signal for the agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An API endpoint is a specific URL path (like `/api/v1/agent/chat`) where the agent's API can be accessed. Each endpoint typically handles a specific type of request—chat, tool execution, status checks, etc.

</details>

---

### Question 4 — Easy

**What is the "system prompt" in agent communication?**

- A) A prompt displayed on the system tray
- B) A pre-configured instruction that sets the agent's role, capabilities, and behavioral guidelines
- C) A prompt for system administrators
- D) The default prompt when no user input is given

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The system prompt is a pre-configured instruction that establishes the agent's role, personality, capabilities, and behavioral guidelines. It's sent with every request and shapes how the agent responds to user inputs and tool calls.

</details>

---

### Question 5 — Medium

**What is "MCP" (Model Context Protocol)?**

- A) A database protocol
- B) A standardized protocol for connecting LLMs to external tools, data sources, and services
- C) A security protocol
- D) A message compression protocol

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Model Context Protocol (MCP) is a standardized protocol for connecting LLMs to external tools, data sources, and services. It defines how tools, resources, and prompts are exposed to LLMs, enabling interoperability across different systems.

</details>

---

### Question 6 — Medium

**What is "message history" management in agent communication?**

- A) Storing all messages forever
- B) Strategically managing which messages to include in the context window to maintain relevance and stay within limits
- C) Deleting all old messages
- D) Only keeping the last message

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Message history management involves strategically deciding which messages to include in the context window—keeping recent messages in full, summarizing older ones, and removing irrelevant content. This balances context richness with context window limits.

</details>

---

### Question 7 — Medium

**What is a "function calling response" in agent communication?**

- A) A text response to the user
- B) A structured message from the LLM indicating which tool to call and with what arguments
- C) An error message
- D) A system status update

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A function calling response is a structured message from the LLM that specifies which tool to call (by name) and what arguments to pass. The application intercepts this, executes the tool, and returns the result—enabling the LLM to interact with external systems.

</details>

---

### Question 8 — Medium

**What is "rate limiting" in agent communication?**

- A) Limiting the agent's response speed
- B) Restricting the number of API requests a client can make within a given time period
- C) Limiting the number of users
- D) Slowing down the agent's reasoning

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rate limiting restricts how many API requests a client can make within a time period (e.g., 100 requests per minute). This prevents abuse, ensures fair resource allocation, and protects the agent's infrastructure from being overwhelmed.

</details>

---

### Question 9 — Medium

**What is "retry logic" in agent communication?**

- A) Never retrying failed requests
- B) Automatically retrying failed API requests with appropriate backoff strategies
- C) Repeating the same request indefinitely
- D) Asking the user to retry manually

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Retry logic automatically retries failed API requests using strategies like exponential backoff (increasing wait time between retries) and jitter (adding randomness). This handles transient failures like network glitches or rate limits without user intervention.

</details>

---

### Question 10 — Medium

**What is "context injection" in agent communication?**

- A) Injecting code into the agent
- B) Dynamically adding relevant information (like tool results, retrieved documents, or conversation history) into the LLM's context
- C) Injecting viruses into the agent
- D) Adding new tools to the agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Context injection dynamically adds relevant information into the LLM's context window. This can include tool results, retrieved documents, conversation history, system instructions, or any other information the agent needs to make informed decisions.

</details>

---

### Question 11 — Hard

**What is "protocol negotiation" in multi-agent communication?**

- A) Agents arguing about which protocol to use
- B) The process by which agents agree on a communication format, encoding, and rules before exchanging information
- C) Negotiating API pricing
- D) Agents deciding who speaks first

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Protocol negotiation is the process where agents determine compatible communication formats, encodings, and rules. This ensures interoperability—allowing agents built with different frameworks or by different developers to communicate effectively.

</details>

---

### Question 12 — Hard

**What is "semantic versioning" in agent communication protocols?**

- A) Giving versions meaningful names
- B) A versioning scheme (MAJOR.MINOR.PATCH) that communicates the nature of changes and backward compatibility
- C) Versioning based on semantic meaning of the content
- D) Using semantic web standards for versioning

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Semantic versioning uses MAJOR.MINOR.PATCH format: MAJOR changes break backward compatibility, MINOR adds functionality in a backward-compatible way, and PATCH makes backward-compatible fixes. This helps agents and clients understand compatibility implications.

</details>

---

### Question 13 — Hard

**What is "message queuing" in agent communication?**

- A) Agents standing in line to send messages
- B) A system that stores messages asynchronously, allowing agents to send and receive messages at different rates
- C) A queue of pending tool calls
- D) A priority list for user messages

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Message queuing systems (like RabbitMQ, Kafka, or SQS) store messages asynchronously between producers and consumers. This decouples agents, allowing them to operate at different rates and providing reliability when agents are temporarily unavailable.

</details>

---

### Question 14 — Hard

**What is "event-driven communication" in multi-agent systems?**

- A) Communication triggered by specific events rather than polling or direct requests
- B) Agents communicating only during specific events
- C) Communication that only happens during emergencies
- D) Event logging for agent communication

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Event-driven communication uses a publish-subscribe or event-bus model where agents emit events and other agents subscribe to events they care about. This is more efficient than polling and enables reactive, loosely-coupled agent architectures.

</details>

---

### Question 15 — Hard

**What is "content negotiation" in agent APIs?**

- A) Agents negotiating what content to produce
- B) The process where client and server agree on data format (JSON, XML, etc.) for communication
- C) Negotiating licensing terms for content
- D) Agents deciding what to include in their response

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Content negotiation is an HTTP mechanism where client and server agree on data format through headers like `Accept` and `Content-Type`. This allows the same API endpoint to serve different formats based on client capabilities.

</details>

---

### Question 16 — Easy

**What is a "chat completion" in agent communication?**

- A) Finishing the chat application
- B) The API call that sends messages to an LLM and receives a generated response
- C) Completing a chat session
- D) The final message in a conversation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A chat completion is the API call that sends a conversation (system message, user messages, assistant messages, tool results) to an LLM and receives a generated response. This is the fundamental interaction in LLM-based agent communication.

</details>

---

### Question 17 — Medium

**What is "token counting" and why is it important in agent communication?**

- A) Counting the number of words
- B) Tracking the number of tokens used in requests to manage costs and stay within context limits
- C) Counting API calls
- D) Counting the number of tools used

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Token counting tracks the number of tokens (subword units) in requests and responses. This is critical for managing API costs (LLMs charge per token), staying within context window limits, and optimizing prompt efficiency.

</details>

---

### Question 18 — Medium

**What is "output streaming" vs "output buffering"?**

- A) Streaming is faster; buffering is slower
- B) Streaming sends tokens as they're generated; buffering waits for the complete response
- C) They are the same thing
- D) Buffering is always preferred

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Output streaming sends tokens incrementally as they're generated, providing real-time feedback. Output buffering waits for the complete response before sending. Streaming is preferred for user-facing applications; buffering may be used for batch processing.

</details>

---

### Question 19 — Hard

**What is "graceful degradation" in agent communication?**

- A) The agent slowly getting worse over time
- B) The system continuing to provide partial functionality when some components fail
- C) The agent's response quality degrading gracefully
- D) The agent gracefully declining to answer

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Graceful degradation means the agent system continues to provide partial functionality when some components fail. For example, if a specialized agent is unavailable, the system falls back to a general agent rather than completely failing.

</details>

---

### Question 20 — Easy

**What is the purpose of an "API key" in agent communication?**

- A) To encrypt all communication
- B) To authenticate and authorize API requests, ensuring only valid clients can access the agent
- C) To compress API responses
- D) To speed up API calls

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: API keys authenticate and authorize API requests. They identify the client, verify permissions, and track usage for billing and rate limiting. Without proper authentication, the agent's API would be vulnerable to abuse.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Easy |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | B | Medium |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | A | Hard |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | B | Medium |
| 18 | B | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | Excellent communication protocols knowledge |
| 14-17 | Proficient | Strong understanding; explore advanced protocols |
| 10-13 | Developing | Good foundation; implement communication patterns |
| 6-9 | Beginner | Review API and communication fundamentals |
| 0-5 | Novice | Start with basic API communication concepts |

---

**Previous Quiz**: [06 - Multi-Agent Orchestration](06-multi-agent-orchestration-quiz.md) | **Next Quiz**: [08 - Agent Evaluation](08-agent-evaluation-quiz.md)
