# Quiz 06: AI Evaluation

## Topic Overview
This quiz covers AI evaluation methods, including hallucination detection, answer quality assessment, RAG evaluation metrics, benchmark datasets, human evaluation, and automated evaluation pipelines. Topics span both traditional NLP metrics and modern LLM-specific evaluation approaches.

---

## Questions

### Question 1
**What is "hallucination" in the context of LLM evaluation?**

- A) The model running too slowly
- B) The model generating factually incorrect or fabricated information
- C) The model producing output in the wrong language
- D) The model failing to complete the request

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Hallucination occurs when an LLM generates information that is factually incorrect, fabricated, or not supported by the provided context. The model may present false information with high confidence, making hallucinations particularly dangerous. Detection and mitigation of hallucinations are critical for reliable AI applications.
</details>

---

### Question 2
**What is "faithfulness" in RAG evaluation?**

- A) How faithful the user is to the system
- B) Whether the generated answer is supported by the retrieved context
- C) How consistent the answers are over time
- D) The accuracy of the retrieval system

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Faithfulness measures whether the generated response is grounded in and supported by the retrieved context. A faithful answer doesn't introduce information not present in the retrieved documents. This metric is crucial for ensuring that RAG systems produce reliable, verifiable answers.
</details>

---

### Question 3
**What is the "RAGAS" framework?**

- A) A RAG implementation library
- B) A framework for evaluating RAG systems using automated metrics
- C) A model training framework
- D) A vector database management tool

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** RAGAS (Retrieval Augmented Generation Assessment) is a framework for evaluating RAG systems. It provides automated metrics including faithfulness, answer relevancy, context precision, and context recall. RAGAS uses LLM-as-judge approaches to evaluate quality without requiring expensive human annotations.
</details>

---

### Question 4
**What is "context recall" in RAG evaluation?**

- A) How many documents are retrieved
- B) The proportion of relevant information from the ground truth that appears in the retrieved context
- C) How often the context is recalled from cache
- D) The number of times context is re-retrieved

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Context recall measures what percentage of the ground truth information is present in the retrieved context. High recall means the retrieval system is finding most of the relevant information. Low recall indicates the system is missing important documents. This metric complements precision, which measures how many retrieved documents are actually relevant.
</details>

---

### Question 5
**What is "answer relevancy" in RAG evaluation?**

- A) How relevant the answer is to the user's query
- B) How relevant the retrieved documents are to the answer
- C) How relevant the query is to the documents
- D) How relevant the model is to the task

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Answer relevancy measures how well the generated answer addresses the user's query. A relevant answer directly responds to the question, provides the requested information, and stays on topic. This is evaluated by checking if the answer's content aligns with the query's intent and information needs.
</details>

---

### Question 6
**What is "LLM-as-judge" in AI evaluation?**

- A) Using a human judge to evaluate LLM outputs
- B) Using one LLM to evaluate the outputs of another LLM
- C) Judging which LLM is the best
- D) A court case involving LLMs

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** LLM-as-judge uses a powerful LLM to evaluate the outputs of other models. The judge LLM scores or ranks responses based on criteria like accuracy, helpfulness, safety, or faithfulness. This approach scales evaluation beyond human capacity while maintaining reasonable quality, though it requires careful prompt design and calibration.
</details>

---

### Question 7
**What is the "ground truth" in AI evaluation?**

- A) The model's true capabilities
- B) The correct or expected answers used as a reference for evaluation
- C) The actual API response time
- D) The ground truth about the model's training data

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Ground truth refers to the correct or expected answers used as a reference standard for evaluating model performance. Creating high-quality ground truth datasets is essential for reliable evaluation. Ground truth can be manually annotated, derived from authoritative sources, or generated by domain experts.
</details>

---

### Question 8
**What is "precision" in the context of information retrieval?**

- A) The speed of retrieval
- B) The proportion of retrieved documents that are relevant
- C) The total number of documents retrieved
- D) The accuracy of the embedding model

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Precision measures what proportion of the retrieved documents are actually relevant to the query. High precision means most retrieved documents are useful. Precision is calculated as: relevant documents retrieved / total documents retrieved. It's a key metric for evaluating retrieval quality in RAG systems.
</details>

---

### Question 9
**What is "recall" in information retrieval?**

- A) Recalling information from the model's training data
- B) The proportion of relevant documents that were successfully retrieved
- C) The total number of relevant documents in the database
- D) The model's ability to remember past queries

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Recall measures what proportion of all relevant documents were successfully retrieved. High recall means the system found most of the relevant information. Recall is calculated as: relevant documents retrieved / total relevant documents. It's complementary to precision and both are needed to evaluate retrieval quality.
</details>

---

### Question 10
**What is the "F1 score" in AI evaluation?**

- A) A score for the first model in a comparison
- B) The harmonic mean of precision and recall
- C) The first evaluation metric
- D) A score based on response speed

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** F1 score is the harmonic mean of precision and recall, providing a single metric that balances both concerns. It ranges from 0 (worst) to 1 (best). F1 is useful when you need to balance precision and recall, as it penalizes extreme values more than the arithmetic mean.
</details>

---

### Question 11
**What is "ROUGE" in AI evaluation?**

- A) A type of LLM
- B) A set of metrics for evaluating text summarization quality
- C) A vector database
- D) An embedding model

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics for evaluating automatic summarization. ROUGE-N measures n-gram overlap, ROUGE-L measures longest common subsequence, and ROUGE-S measures skip-bigram overlap. While originally for summarization, ROUGE is also used to evaluate RAG answer quality.
</details>

---

### Question 12
**What is "BLEU" score primarily used for?**

- A) Evaluating image generation
- B) Evaluating machine translation quality
- C) Evaluating code generation
- D) Evaluating model speed

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** BLEU (Bilingual Evaluation Understudy) is primarily used for evaluating machine translation quality. It measures the overlap between machine-generated text and human reference translations using modified n-gram precision. While originally for translation, BLEU is also used for other text generation tasks, though it has known limitations.
</details>

---

### Question 13
**What is "human evaluation" in AI assessment?**

- A) Using humans to train the model
- B) Having humans rate or compare AI outputs for quality assessment
- C) Evaluating the model's ability to interact with humans
- D) Testing the model's human-like behavior

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Human evaluation involves having human annotators rate or compare AI outputs based on quality criteria like helpfulness, accuracy, safety, and fluency. Despite advances in automated metrics, human evaluation remains the gold standard for assessing subjective qualities. It's expensive and time-consuming but essential for calibrating automated metrics.
</details>

---

### Question 14
**What is "A/B testing" in AI evaluation?**

- A) Testing two different API keys
- B) Comparing two versions of a model or system with real users
- C) Testing with two different programming languages
- D) Using two different databases

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A/B testing compares two versions (A and B) of a model, prompt, or system by randomly assigning users to each version and measuring performance. It provides real-world evaluation data and can reveal differences that offline metrics miss. A/B testing is essential for validating improvements before full deployment.
</details>

---

### Question 15
**What is "benchmark contamination" in AI evaluation?**

- A) Contamination of the training data
- B) When evaluation data appears in the model's training data, invalidating results
- C) Pollution of the evaluation environment
- D) Mixing different benchmark datasets

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Benchmark contamination occurs when evaluation data (or very similar data) appears in the model's training data. This means the model may have memorized the answers rather than demonstrating generalizable capabilities, making benchmark scores unreliable. Detecting and preventing contamination is crucial for fair evaluation.
</details>

---

### Question 16
**What is "toxicity" evaluation in AI safety?**

- A) Evaluating the model's toxicity in terms of harmful chemicals
- B) Measuring whether outputs contain harmful, offensive, or inappropriate content
- C) Testing the model's performance on toxic data
- D) Evaluating the model's environmental impact

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Toxicity evaluation measures whether model outputs contain harmful, offensive, biased, or inappropriate content. This includes hate speech, violence, sexual content, and other harmful categories. Automated toxicity classifiers and human evaluation are used to assess and mitigate harmful outputs.
</details>

---

### Question 17
**What is "perplexity" in language model evaluation?**

- A) How confused the model appears
- B) A measure of how well the model predicts the next token
- C) The model's processing speed
- D) The complexity of the prompt

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Perplexity measures how well a language model predicts the next token in a sequence. Lower perplexity indicates the model is more confident and accurate in its predictions. It's calculated as the exponentiated average negative log-likelihood of the tokens. While useful for comparing models, perplexity doesn't always correlate with task performance.
</details>

---

### Question 18
**What is the "DeepEval" framework?**

- A) A deep learning evaluation library
- B) An end-to-end evaluation framework for LLM applications including RAG and agents
- C) A framework for evaluating deep neural networks
- D) A tool for deep code analysis

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** DeepEval is an open-source evaluation framework for LLM applications. It provides metrics for RAG evaluation (faithfulness, relevancy, context precision/recall), hallucination detection, answer quality assessment, and agent evaluation. DeepEval supports both automated metrics and LLM-as-judge approaches.
</details>

---

### Question 19
**What is "latency" evaluation in AI systems?**

- A) Evaluating the model's response quality
- B) Measuring the time it takes for the model to generate a response
- C) Evaluating the model's ability to handle late requests
- D) Measuring the model's memory usage

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Latency evaluation measures response time, including time-to-first-token (TTFT) and total generation time. Low latency is critical for user experience, especially in interactive applications. Latency evaluation considers both average and percentile metrics (p50, p95, p99) to understand performance distribution.
</details>

---

### Question 20
**What is "evaluation drift" in AI assessment?**

- A) The model's performance degrading over time
- B) Evaluation metrics becoming less meaningful as models improve
- C) The drift of evaluation data from real-world usage
- D) The evaluation system becoming slower over time

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Evaluation drift occurs when established evaluation metrics become less meaningful as models improve. For example, simple accuracy may not distinguish between capable models, or metrics may not capture important nuances. This requires updating evaluation benchmarks and developing more sophisticated metrics that better assess model capabilities.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Easy | | |
| 6 | Medium | | |
| 7 | Easy | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Easy | | |
| 14 | Easy | | |
| 15 | Hard | | |
| 16 | Medium | | |
| 17 | Hard | | |
| 18 | Medium | | |
| 19 | Easy | | |
| 20 | Hard | | |

**Score:** ____/20

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 8 | B | 15 | B |
| 2 | B | 9 | B | 16 | B |
| 3 | B | 10 | B | 17 | B |
| 4 | B | 11 | B | 18 | B |
| 5 | A | 12 | B | 19 | B |
| 6 | B | 13 | B | 20 | B |
| 7 | B | 14 | B | | |

---

*Generated for AI Automation Lab - Quiz 06 of 09*