# Quiz 07: AI Deployment

## Topic Overview
This quiz covers deploying AI applications to production, including containerization, scaling, monitoring, cost optimization, security, CI/CD pipelines, and production readiness. Topics span infrastructure, operations, and best practices for running AI systems at scale.

---

## Questions

### Question 1
**What is "model serving" in AI deployment?**

- A) Training the model on new data
- B) Providing an API endpoint to make predictions with a trained model
- C) Distributing the model to users
- D) Selling the model to customers

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Model serving is the process of deploying a trained model as an accessible service (typically via REST API) that can receive inputs and return predictions. Model serving solutions handle request routing, batch processing, versioning, and scaling. Popular options include TensorFlow Serving, TorchServe, and cloud-based solutions like AWS SageMaker.
</details>

---

### Question 2
**What is the difference between "batch inference" and "real-time inference"?**

- A) Batch is faster; real-time is slower
- B) Batch processes data in bulk offline; real-time processes individual requests immediately
- C) Batch uses GPU; real-time uses CPU
- D) They are the same thing

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Batch inference processes large volumes of data offline (e.g., nightly report generation), optimizing for throughput. Real-time inference processes individual requests immediately (e.g., chatbot responses), optimizing for latency. Batch is more cost-efficient for non-urgent workloads; real-time is essential for interactive applications.
</details>

---

### Question 3
**What is "containerization" in AI deployment?**

- A) Compressing the model into a container
- B) Packaging the application and dependencies into isolated containers (e.g., Docker)
- C) Storing the model in a data container
- D) Using container data structures in code

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Containerization packages an application and all its dependencies into a standardized unit (container) that runs consistently across environments. Docker is the most common containerization technology. Containers ensure that AI applications work the same on development laptops, staging servers, and production environments, eliminating "works on my machine" issues.
</details>

---

### Question 4
**What is "horizontal scaling" in AI deployment?**

- A) Scaling the model's architecture horizontally
- B) Adding more machines/instances to handle increased load
- C) Scaling the input data horizontally
- D) Increasing the resources on a single machine

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Horizontal scaling (scaling out) adds more machines or instances to distribute load, as opposed to vertical scaling (scaling up) which increases resources on a single machine. Horizontal scaling is preferred for AI workloads because it provides better fault tolerance, cost efficiency, and can handle larger loads than any single machine.
</details>

---

### Question 5
**What is "auto-scaling" in cloud-based AI deployment?**

- A) Automatically training the model
- B) Automatically adjusting the number of instances based on demand
- C) Automatically scaling the model's parameters
- D) Automatically updating the model

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Auto-scaling automatically adjusts the number of computing instances based on current demand. When traffic increases, more instances are added; when traffic decreases, instances are removed. This ensures optimal performance during peak loads while minimizing costs during quiet periods. Most cloud providers (AWS, GCP, Azure) offer auto-scaling services.
</details>

---

### Question 6
**What is "canary deployment" in AI systems?**

- A) Deploying the model in a canary environment
- B) Gradually rolling out changes to a small percentage of users before full deployment
- C) Using canary tokens for authentication
- D) Deploying only to canary (test) users

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Canary deployment gradually rolls out a new model version to a small percentage of users (e.g., 5%) before full deployment. This allows monitoring for issues with minimal impact. If problems are detected, the rollout is stopped and rolled back. This reduces deployment risk compared to all-at-once deployments.
</details>

---

### Question 7
**What is "blue-green deployment" in AI systems?**

- A) Deploying with blue and green colored interfaces
- B) Maintaining two identical environments and switching traffic between them
- C) Using blue and green API keys
- D) Deploying to two different cloud providers

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Blue-green deployment maintains two identical production environments (blue and green). The current version runs in one environment while the new version is deployed to the other. Once validated, traffic is instantly switched to the new environment. If issues arise, traffic is switched back instantly. This provides zero-downtime deployments and instant rollbacks.
</details>

---

### Question 8
**What is "model versioning" and why is it important?**

- A) Versioning the training code
- B) Tracking different versions of deployed models for rollback and comparison
- C) Versioning the API endpoints
- D) Versioning the user data

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Model versioning tracks different versions of deployed models, enabling rollback to previous versions if issues arise, comparison of performance between versions, and audit trails. Versioning is essential for reproducibility, debugging, and compliance. Many ML platforms (MLflow, Weights & Biases) provide built-in versioning.
</details>

---

### Question 9
**What is "observability" in AI system deployment?**

- A) Making the system visible to users
- B) The ability to understand the internal state of the system from its external outputs
- C) Observing the user's behavior
- D) Making the system open-source

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Observability provides insights into the internal state of AI systems through logs, metrics, and traces. It enables debugging, performance optimization, and anomaly detection. Key observability tools include Prometheus (metrics), Grafana (visualization), Jaeger (tracing), and ELK stack (logging). Observability is essential for maintaining reliable production AI systems.
</details>

---

### Question 10
**What is "latency" in the context of AI deployment?**

- A) The model's training time
- B) The time between sending a request and receiving a response
- C) The model's memory usage
- D) The network bandwidth

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Latency measures the total time from sending a request to receiving a complete response. It includes network time, preprocessing, model inference, and postprocessing. For real-time applications, low latency is critical. Key metrics include Time to First Token (TTFT) for streaming and total response time.
</details>

---

### Question 11
**What is "throughput" in AI deployment?**

- A) The number of parameters in the model
- B) The number of requests processed per unit time
- C) The speed of the training process
- D) The amount of data processed per batch

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Throughput measures the number of requests an AI system can process per unit time (e.g., requests per second). High throughput is essential for handling large volumes of requests. Throughput is influenced by batch size, hardware resources, and model optimization. Balancing throughput and latency is a key deployment challenge.
</details>

---

### Question 12
**What is "model optimization" for deployment?**

- A) Optimizing the model's training process
- B) Techniques to reduce model size and improve inference speed
- C) Optimizing the model's hyperparameters
- D) Optimizing the model's accuracy

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Model optimization for deployment includes techniques like quantization (reducing precision), pruning (removing unnecessary weights), distillation (training smaller models to mimic larger ones), and compilation (optimizing for specific hardware). These techniques reduce model size, memory usage, and inference time while maintaining acceptable accuracy.
</details>

---

### Question 13
**What is "GPU inference" and when is it preferred?**

- A) Using GPU for training instead of inference
- B) Running model predictions on GPU hardware for faster processing
- C) Using GPU memory for data storage
- D) GPU-based data preprocessing

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** GPU inference runs model predictions on GPU hardware, which is significantly faster than CPU for parallelizable operations like matrix multiplications. GPUs are preferred for large models, real-time applications, and high-throughput workloads. GPU inference is more expensive but provides the speed needed for production AI applications.
</details>

---

### Question 14
**What is "model caching" in deployment?**

- A) Caching the model's training data
- B) Storing frequently accessed model outputs to avoid redundant computation
- C) Caching the model's source code
- D) Caching API authentication tokens

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Model caching stores predictions for previously seen inputs to avoid redundant computation. For deterministic models, the same input always produces the same output, so caching eliminates unnecessary inference. This improves latency and reduces costs, especially for popular queries or content that's accessed frequently.
</details>

---

### Question 15
**What is "CI/CD" in AI deployment?**

- A) Continuous Integration/Continuous Deployment
- B) Central Intelligence/Computer Database
- C) Code Integration/Code Deployment
- D) Cloud Infrastructure/Cloud Deployment

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** CI/CD (Continuous Integration/Continuous Deployment) is a development practice that automates the building, testing, and deployment of applications. In AI, CI/CD pipelines automate model training, evaluation, and deployment. This enables rapid, reliable updates while maintaining quality through automated testing and validation.
</details>

---

### Question 16
**What is "A/B testing" in AI deployment?**

- A) Testing with two API keys
- B) Comparing two model versions with real users to measure performance
- C) Testing with two different databases
- D) Testing the model's response to two different inputs

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A/B testing compares two model versions by randomly assigning users to each version and measuring performance metrics. It provides real-world evaluation data and can reveal differences that offline metrics miss. A/B testing is essential for validating improvements before full deployment and making data-driven deployment decisions.
</details>

---

### Question 17
**What is "cost optimization" in AI deployment?**

- A) Reducing the model's accuracy to save costs
- B) Strategies to minimize infrastructure costs while maintaining performance
- C) Optimizing the model's training cost
- D) Reducing the number of API calls

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Cost optimization balances performance with infrastructure costs. Strategies include: right-sizing instances, using spot/preemptible instances, auto-scaling, model optimization, caching, and choosing appropriate hardware (CPU vs GPU). Monitoring and alerting on costs helps prevent unexpected expenses while maintaining service quality.
</details>

---

### Question 18
**What is "disaster recovery" in AI deployment?**

- A) Recovering from a model's bad output
- B) Strategies to restore service after infrastructure failures or outages
- C) Recovering lost training data
- D) Recovering from API rate limits

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Disaster recovery (DR) encompasses strategies and procedures for restoring AI services after failures like infrastructure outages, data loss, or security incidents. DR includes backups, failover systems, redundant deployments, and recovery procedures. Regular DR testing ensures the organization can recover quickly when failures occur.
</details>

---

### Question 19
**What is "feature flagging" in AI deployment?**

- A) Flagging features in the model's output
- B) Using configuration flags to enable/disable features without redeployment
- C) Flagging important features in the data
- D) Creating feature documentation

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Feature flags allow enabling, disabling, or modifying features through configuration without code changes or redeployment. In AI, this enables gradual rollouts, A/B testing, and quick rollback. Feature flags provide flexibility and reduce deployment risk by allowing changes to be controlled independently of code releases.
</details>

---

### Question 20
**What is "SLA" in AI service deployment?**

- A) Service Level Agreement - guarantees for uptime, latency, and accuracy
- B) Service Level Analysis - measuring performance
- C) System Level Architecture - design patterns
- D) Software License Agreement - legal terms

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** SLA (Service Level Agreement) defines the guaranteed performance levels for an AI service, including uptime (e.g., 99.9%), latency (e.g., p95 < 200ms), accuracy (e.g., >95%), and support response times. SLAs set expectations for users and provide accountability. They're essential for production services where reliability is critical.
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
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Easy | | |
| 9 | Medium | | |
| 10 | Easy | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Easy | | |
| 14 | Medium | | |
| 15 | Easy | | |
| 16 | Medium | | |
| 17 | Medium | | |
| 18 | Medium | | |
| 19 | Medium | | |
| 20 | Easy | | |

**Score:** ____/20

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 8 | B | 15 | A |
| 2 | B | 9 | B | 16 | B |
| 3 | B | 10 | B | 17 | B |
| 4 | B | 11 | B | 18 | B |
| 5 | B | 12 | B | 19 | B |
| 6 | B | 13 | B | 20 | A |
| 7 | B | 14 | B | | |

---

*Generated for AI Automation Lab - Quiz 07 of 09*