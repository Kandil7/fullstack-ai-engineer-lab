# Quiz 10: Production Agents

> **Topic Overview**: Building production-grade AI agents requires addressing deployment, scalability, monitoring, cost optimization, and operational concerns. This quiz covers deployment strategies, observability, scaling patterns, cost management, error handling, CI/CD for agents, and best practices for running agents reliably in production environments.

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

**What is the primary challenge of deploying AI agents to production?**

- A) Agents are too simple for production
- B) Ensuring reliability, safety, and cost-effectiveness at scale with non-deterministic components
- C) Agents don't need deployment
- D) Production environments don't support agents

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Production agents must handle non-deterministic LLM outputs, manage costs, ensure safety, scale to many users, and maintain reliability—all simultaneously. This is significantly more complex than deploying traditional deterministic software.

</details>

---

### Question 2 — Easy

**What is "observability" in production agent systems?**

- A) Making the agent visible to users
- B) The ability to understand the internal state and behavior of the agent through its external outputs, logs, and metrics
- C) Making the agent's code open source
- D) A UI feature for viewing the agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Observability provides insight into the agent's internal state through logs, metrics, and traces. It enables debugging, performance monitoring, cost tracking, and understanding how the agent behaves in production.

</details>

---

### Question 3 — Easy

**What is "latency monitoring" in production agents?**

- A) Monitoring the agent's typing speed
- B) Tracking the time between user requests and agent responses across all interactions
- C) Monitoring the agent's network connection
- D) Tracking the agent's uptime

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Latency monitoring tracks response times across all interactions, identifying slow queries, performance degradation, and bottlenecks. This includes tracking LLM inference time, tool execution time, and end-to-end response latency.

</details>

---

### Question 4 — Easy

**What is "cost tracking" in production agent systems?**

- A) Counting the number of users
- B) Monitoring and tracking the API costs, compute costs, and infrastructure costs of running the agent
- C) Tracking the agent's development costs
- D) Counting the agent's features

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cost tracking monitors all costs associated with running the agent—LLM API token costs, tool API costs, compute infrastructure, storage, and network. This is essential for understanding economic viability and optimizing spending.

</details>

---

### Question 5 — Medium

**What is "horizontal scaling" for agent systems?**

- A) Making the agent wider on screen
- B) Adding more instances of the agent to handle increased load
- C) Making the agent's codebase larger
- D) Adding more features to the agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

</details>

**Explanation**: Horizontal scaling adds more instances of the agent to distribute load across multiple servers. This increases throughput and availability. It requires stateless design, load balancing, and shared state management for consistent behavior.

</details>

---

### Question 6 — Medium

**What is "circuit breaking" in production agent systems?**

- A) Breaking the agent's circuit board
- B) A pattern that stops calling a failing service to prevent cascading failures and allow recovery
- C) Breaking the agent's code
- D) Stopping the agent permanently

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Circuit breaking monitors service health and "opens the circuit" (stops calling) when failures exceed a threshold. This prevents cascading failures, allows the failing service to recover, and provides fallback behavior for the agent.

</details>

---

### Question 7 — Medium

**What is a "fallback strategy" in production agents?**

- A) A plan for when the agent falls behind schedule
- B) An alternative approach the agent uses when its primary method fails or is unavailable
- C) A backup server
- D) A plan for rolling back deployments

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fallback strategies provide alternative approaches when the primary method fails. For example, if a specialized agent is unavailable, fall back to a general agent. If a tool fails, use cached results or alternative tools. This ensures the agent continues functioning under degraded conditions.

</details>

---

### Question 8 — Medium

**What is "canary testing" for agent deployments?**

- A) Testing with canary birds
- B) Gradually routing a small percentage of traffic to the new version to detect issues before full deployment
- C) Testing only during the day
- D) Testing with the cheapest model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Canary testing routes a small percentage of traffic to the new agent version, monitoring for errors, performance degradation, or safety issues. If problems are detected, traffic is routed back to the stable version. This minimizes the blast radius of issues.

</details>

---

### Question 9 — Medium

**What is "log aggregation" in production agent systems?**

- A) Collecting all logs from multiple agent instances into a centralized system for analysis
- B) Writing all logs to a single file
- C) Aggregating log data into summaries
- D) Compressing log files

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Log aggregation collects logs from multiple agent instances, services, and components into a centralized system (like ELK stack, Datadog, or CloudWatch). This enables cross-instance analysis, debugging, and monitoring at scale.

</details>

---

### Question 10 — Medium

**What is "prompt versioning" in production agents?**

- A) Numbering the prompts in the system
- B) Managing multiple versions of system prompts and configurations to track changes and enable rollback
- C) Creating different prompt styles
- D) Translating prompts to different languages

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Prompt versioning tracks changes to system prompts, configurations, and agent behavior over time. It enables comparison between versions, rollback to previous versions if issues arise, and systematic testing of prompt changes.

</details>

---

### Question 11 — Hard

**What is "rate-based auto-scaling" for agent systems?**

- A) Scaling based on the agent's accuracy rate
- B) Automatically adding or removing agent instances based on request rate and load metrics
- C) Scaling based on the rate of code changes
- D) Auto-scaling the agent's codebase

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rate-based auto-scaling automatically adjusts the number of agent instances based on request rates and load metrics. When traffic increases, new instances are spun up; when traffic decreases, instances are removed. This optimizes cost while maintaining performance.

</details>

---

### Question 12 — Hard

**What is "trace visualization" in agent observability?**

- A) Drawing the agent's architecture
- B) Visualizing the complete execution path of a request through all agent components, tools, and LLM calls
- C) Creating visual outputs
- D) Drawing graphs of agent metrics

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Trace visualization shows the complete execution path of a request—each LLM call, tool execution, decision point, and timing. This helps identify bottlenecks, understand agent behavior, and debug issues in complex multi-step workflows.

</details>

---

### Question 13 — Hard

**What is "incident response" for production agent failures?**

- A) Responding to customer complaints
- B) A structured process for detecting, diagnosing, containing, and recovering from agent failures in production
- C) Writing incident reports
- D) Deploying emergency patches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Incident response is a structured process for handling agent failures: detection (monitoring alerts), diagnosis (root cause analysis), containment (limiting damage), recovery (restoring service), and post-incident review (preventing recurrence). This minimizes downtime and impact.

</details>

---

### Question 14 — Hard

**What is "cost optimization" for production agent systems?**

- A) Making the agent as cheap as possible
- B) Strategies to reduce API costs while maintaining quality—model routing, caching, batching, and prompt optimization
- C) Using only free tools
- D) Eliminating all safety features to save money

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cost optimization reduces expenses while maintaining quality: model routing (using cheaper models for simple tasks), caching (storing and reusing results), batching (combining requests), and prompt optimization (reducing token usage). These strategies can significantly reduce costs.

</details>

---

### Question 15 — Hard

**What is "model routing" in production cost optimization?**

- A) Routing between different databases
- B) Dynamically selecting which LLM model to use based on task complexity, cost, and latency requirements
- C) Routing user requests to different agents
- D) Routing network traffic

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Model routing dynamically selects which LLM to use for each request based on task complexity, cost constraints, and latency requirements. Simple tasks use cheaper, faster models; complex tasks use more capable (and expensive) models. This optimizes cost without sacrificing quality.

</details>

---

### Question 16 — Easy

**What is a "health check" in production agent systems?**

- A) A medical checkup for the agent
- B) A periodic test that verifies the agent and its dependencies are functioning correctly
- C) A code review
- D) A security audit

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A health check periodically verifies the agent and its dependencies (LLM APIs, tools, databases) are functioning correctly. Health checks enable automated recovery—restarting failed instances—and alerting when services are degraded.

</details>

---

### Question 17 — Medium

**What is "graceful degradation" in production agents?**

- A) The agent gradually becoming less capable over time
- B) The system continuing to provide partial functionality when some components fail
- C) The agent's quality slowly improving
- D) The agent's performance degrading under load

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Graceful degradation ensures the agent continues providing value even when some components fail. For example, if a specialized tool is unavailable, the agent falls back to simpler alternatives. This maintains partial functionality rather than complete failure.

</details>

---

### Question 18 — Medium

**What is "CI/CD for agents"?**

- A) Continuous Integration / Continuous Deployment practices adapted for agent systems
- B) A database for agents
- C) A type of agent architecture
- D) A deployment platform

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: CI/CD for agents adapts continuous integration and deployment practices for agent systems. This includes automated testing of agent behavior, prompt regression testing, canary deployments, and automated rollback—ensuring changes don't break agent functionality.

</details>

---

### Question 19 — Hard

**What is "cost anomaly detection" in production agent systems?**

- A) Detecting unusual agent behavior
- B) Automatically identifying unexpected spikes or patterns in API costs that may indicate issues or abuse
- C) Finding the cheapest API provider
- D) Detecting anomalies in agent outputs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cost anomaly detection monitors API costs for unexpected spikes or patterns that may indicate prompt injection attacks, runaway loops, or infrastructure issues. Automated alerts enable rapid response to prevent excessive costs.

</details>

---

### Question 20 — Easy

**What is the most important metric for production agent reliability?**

- A) Total number of users
- B) Uptime percentage (availability)
- C) Agent's memory usage
- D) Number of features

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Uptime (availability) is the most fundamental reliability metric—it measures what percentage of time the agent is operational and accessible. Common targets are 99.9% (three nines) or higher, depending on the application's criticality.

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
| 9 | A | Medium |
| 10 | B | Medium |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | B | Hard |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | B | Medium |
| 18 | A | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | Excellent production engineering knowledge |
| 14-17 | Proficient | Strong understanding; implement monitoring and scaling |
| 10-13 | Developing | Good foundation; study production best practices |
| 6-9 | Beginner | Review deployment and operations concepts |
| 0-5 | Novice | Start with basic DevOps and production concepts |

---

**Previous Quiz**: [09 - Agent Safety](09-agent-safety-quiz.md) | **Back to Overview**: [README](README.md)
