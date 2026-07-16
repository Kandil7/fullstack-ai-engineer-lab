# AI Security Quiz: API Security

## Topic Overview

API security for AI systems involves protecting the interfaces through which clients interact with models and services. This quiz covers secure API design, rate limiting, input validation, encryption, and common attack vectors targeting AI APIs.

### Key Concepts
- API authentication and authorization
- Rate limiting and throttling
- Input validation and sanitization
- HTTPS and transport security
- API versioning and deprecation

---

## Quiz

### Question 1 — Easy
**Why is HTTPS required for AI APIs?**

- A) It makes responses faster
- B) It encrypts data in transit, preventing interception
- C) It's optional for security
- D) It reduces server costs

**Answer: B**

**Explanation:** HTTPS encrypts all data transmitted between client and server, preventing man-in-the-middle attacks, data interception, and credential theft.

---

### Question 2 — Easy
**What is rate limiting in API security?**

- A) Limiting the number of users
- B) Restricting the number of API requests per time period
- C) Limiting response size
- D) Restricting model parameters

**Answer: B**

**Explanation:** Rate limiting controls how many requests a client can make within a time window, preventing abuse, denial-of-service attacks, and excessive resource consumption.

---

### Question 3 — Easy
**Which HTTP status code indicates rate limiting has been exceeded?**

- A) 200 OK
- B) 404 Not Found
- C) 429 Too Many Requests
- D) 500 Internal Server Error

**Answer: C**

**Explanation:** 429 Too Many Requests is the standard HTTP status code returned when a client exceeds the rate limit, typically accompanied by retry-after headers.

---

### Question 4 — Medium
**What is "API key rotation"?**

- A) Changing the API endpoint URL
- B) Regularly replacing API keys to limit exposure from compromised credentials
- C) Rotating the server hardware
- D) Changing the API version

**Answer: B**

**Explanation:** API key rotation involves regularly generating new keys and deprecating old ones, limiting the window of opportunity if a key is leaked or compromised.

---

### Question 5 — Medium
**What is "input validation" for API endpoints?**

- A) Checking the API key format
- B) Verifying request data matches expected schema before processing
- C) Validating the server configuration
- D) Checking network connectivity

**Answer: B**

**Explanation:** Input validation ensures incoming requests contain valid data types, formats, and values, preventing injection attacks and malformed data from causing errors or vulnerabilities.

---

### Question 6 — Medium
**Why should API responses include minimal information?**

- A) To reduce response time only
- B) To limit information leakage that could aid attackers
- C) To reduce server costs
- D) To make responses faster

**Answer: B**

**Explanation:** Verbose error messages and detailed system information can reveal internal architecture, vulnerabilities, and configuration details that attackers can exploit.

---

### Question 7 — Medium
**What is "CORS" (Cross-Origin Resource Sharing) in API security?**

- A) A type of encryption
- B) A mechanism that controls which origins can access API resources
- C) A database security feature
- D) A network protocol

**Answer: B**

**Explanation:** CORS defines which external domains can make requests to your API, preventing unauthorized cross-origin access to AI services and data.

---

### Question 8 — Medium
**What is an "API versioning" best practice?**

- A) Never update APIs
- B) Include version in URL path or headers with graceful deprecation
- C) Force all clients to update simultaneously
- D) Remove old versions immediately

**Answer: B**

**Explanation:** Versioning (e.g., `/v1/models`) allows API evolution without breaking existing clients, with deprecated versions maintained for a transition period.

---

### Question 9 — Hard
**What is a "server-side request forgery" (SSRF) attack on AI APIs?**

- A) Forging server certificates
- B) Tricking the API into making requests to internal services
- C) Spoofing client IP addresses
- D) Modifying request headers

**Answer: B**

**Explanation:** SSRF attacks manipulate APIs to make requests to internal or unintended resources, potentially accessing internal services, metadata endpoints, or other protected systems.

---

### Question 10 — Hard
**How does "request signing" enhance API security?**

- A) It compresses requests
- B) It verifies request integrity and authenticity using cryptographic signatures
- C) It encrypts request content
- D) It caches requests

**Answer: B**

**Explanation:** Request signing uses cryptographic signatures to verify that requests haven't been tampered with and are from authenticated sources, preventing replay and modification attacks.

---

### Question 11 — Hard
**What is a "ZIP bomb" attack on an AI API?**

- A) Compressing API responses
- B) Sending a small compressed file that expands to exhaust resources when decompressed
- C) Flooding the network
- D) Using ZIP files for authentication

**Answer: B**

**Explanation:** ZIP bombs are malicious compressed files that appear small but expand to enormous sizes, exhausting memory and storage when the API attempts to process them.

---

### Question 12 — Hard
**What is "time-of-check to time-of-use" (TOCTOU) in API security?**

- A) A timing attack
- B) A race condition where validation and usage occur at different times
- C) A clock synchronization issue
- D) A timeout configuration problem

**Answer: B**

**Explanation:** TOCTOU vulnerabilities occur when there's a gap between validating a condition and using it, allowing attackers to change the state between check and use.

---

### Question 13 — Easy
**What is an "API endpoint"?**

- A) The physical server location
- B) A specific URL path where an API function can be accessed
- C) The database connection
- D) The firewall configuration

**Answer: B**

**Explanation:** API endpoints are specific URLs (like `/v1/chat/completions`) that accept requests and return responses, serving as the interface between clients and AI services.

---

### Question 14 — Medium
**What is "request throttling" in API security?**

- A) Slowing down all users
- B) Gradually reducing request rates for clients approaching limits
- C) Blocking all requests
- D) Increasing response times

**Answer: B**

**Explanation:** Throttling provides a softer limit than hard rate limiting, gradually reducing allowed request rates as clients approach their limits, allowing graceful degradation.

---

### Question 15 — Medium
**Why should API keys be stored in environment variables, not code?**

- A) Environment variables are faster
- B) Code may be committed to version control, exposing keys
- C) Environment variables are encrypted by default
- D) Code can't access environment variables

**Answer: B**

**Explanation:** Storing keys in code risks exposure through version control, code reviews, or breaches. Environment variables keep secrets separate from the codebase.

---

### Question 16 — Easy
**What is "API throttling" different from rate limiting?**

- A) They're exactly the same
- B) Throttling slows requests; rate limiting blocks them
- C) Rate limiting is for internal use only
- D) Throttling is more secure

**Answer: B**

**Explanation:** While similar, throttling typically slows down requests approaching limits (allowing some through), while rate limiting blocks requests entirely once limits are exceeded.

---

### Question 17 — Hard
**What is "XML External Entity" (XXE) injection in API attacks?**

- A) A type of SQL injection
- B) Exploiting XML parsers to access internal files or services
- C) Injecting malicious JavaScript
- D) A network protocol attack

**Answer: B**

**Explanation:** XXE attacks exploit XML parsers that process external entity references, potentially accessing internal files, performing SSRF attacks, or causing denial of service.

---

### Question 18 — Medium
**What is the purpose of "API documentation security"?**

- A) Making documentation look professional
- B) Ensuring documentation doesn't expose sensitive implementation details
- C) Making documentation longer
- D) Adding more examples

**Answer: B**

**Explanation:** API documentation should provide enough detail for developers while avoiding exposure of internal architecture, security mechanisms, or sensitive configuration details.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong API security knowledge.
- **12-14 correct (67-82%):** Good foundation, review hard topics.
- **9-11 correct (50-66%):** Needs improvement, study the explanations.
- **Below 9 (<50%):** Review the topic overview and retake.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | C | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Hard |
| 10 | B | Hard |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | B | Easy |
| 14 | B | Medium |
| 15 | B | Medium |
| 16 | B | Easy |
| 17 | B | Hard |
| 18 | B | Medium |
