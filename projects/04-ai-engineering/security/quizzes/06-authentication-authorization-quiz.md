# AI Security Quiz: Authentication & Authorization

## Topic Overview

Authentication and authorization ensure that AI systems are accessed only by legitimate users with appropriate permissions. This quiz covers identity verification, access control models, API security, and secure credential management for AI applications.

### Key Concepts
- Authentication mechanisms (API keys, OAuth, JWT)
- Role-based access control (RBAC)
- Principle of least privilege
- Token security and management
- Multi-factor authentication

---

## Quiz

### Question 1 — Easy
**What is the difference between authentication and authorization?**

- A) They are the same thing
- B) Authentication verifies identity; authorization determines permissions
- C) Authentication grants access; authorization verifies identity
- D) Authorization is for humans only

**Answer: B**

**Explanation:** Authentication confirms who you are (identity verification), while authorization determines what you're allowed to do (permission checking) after identity is established.

---

### Question 2 — Easy
**Which of these is a common authentication method for AI APIs?**

- A) Shared passwords
- B) API keys with rate limiting
- C) No authentication needed
- D) Public access only

**Answer: B**

**Explanation:** API keys provide a simple, scalable authentication method for AI APIs, typically combined with rate limiting to prevent abuse and track usage.

---

### Question 3 — Easy
**What is the "principle of least privilege"?**

- A) Giving users maximum access
- B) Granting only the minimum permissions needed to perform a task
- C) Using the cheapest authentication method
- D) Limiting user count

**Answer: B**

**Explanation:** Least privilege means users and systems only get the access they absolutely need, limiting potential damage from compromised accounts or insider threats.

---

### Question 4 — Medium
**What does RBAC stand for in access control?**

- A) Random-Based Access Control
- B) Role-Based Access Control
- C) Read-Only Based Access Control
- D) Remote-Based Authentication Control

**Answer: B**

**Explanation:** Role-Based Access Control assigns permissions based on user roles rather than individual users, simplifying access management and ensuring consistent permission policies.

---

### Question 5 — Medium
**What is a JWT (JSON Web Token)?**

- A) A password storage format
- B) A compact, URL-safe token for securely transmitting information between parties
- C) A type of encryption key
- D) A database query language

**Answer: B**

**Explanation:** JWTs are self-contained tokens that carry claims about an entity, commonly used for API authentication because they can be verified without database lookups.

---

### Question 6 — Medium
**Why should API keys not be hardcoded in application code?**

- A) They slow down the application
- B) Code may be exposed, leaking credentials to attackers
- C) Hardcoded keys are less secure
- D) Hardcoded keys don't work

**Answer: B**

**Explanation:** Hardcoded credentials in source code can be exposed through version control, code reviews, or breaches, giving attackers direct access to AI services.

---

### Question 7 — Medium
**What is OAuth 2.0 primarily used for?**

- A) Password storage
- B) Delegated authorization allowing third-party access without sharing credentials
- C) Data encryption
- D) Model training

**Answer: B**

**Explanation:** OAuth 2.0 enables applications to obtain limited access to user accounts on third-party services without exposing passwords, providing a secure delegation mechanism.

---

### Question 8 — Medium
**What makes a strong API key?**

- A) Short and simple
- B) Long, random, and unique per application
- C) Based on the application name
- D) Using default values

**Answer: B**

**Explanation:** Strong API keys are cryptographically random, sufficiently long (at least 256 bits), and unique per application or user to prevent guessing and limit blast radius.

---

### Question 9 — Hard
**What is "token rotation" and why is it important?**

- A) Changing the token format periodically
- B) Regularly regenerating tokens to limit exposure from compromised credentials
- C) Rotating tokens between different users
- D) Changing token storage locations

**Answer: B**

**Explanation:** Token rotation regularly generates new tokens and invalidates old ones, limiting the window of opportunity if a token is compromised.

---

### Question 10 — Hard
**What is an "API gateway" in the context of AI security?**

- A) A physical security gate
- B) A server that manages, authenticates, and secures API traffic
- C) A type of firewall
- D) A load balancer only

**Answer: B**

**Explanation:** API gateways handle authentication, rate limiting, request validation, and security policies, providing a centralized control point for AI service access.

---

### Question 11 — Hard
**What is "token replay attack" and how is it prevented?**

- A) Playing tokens like music
- B) Reusing captured tokens; prevented by short expiry and one-time use tokens
- C) Copying token formatting
- D) Token serialization

**Answer: B**

**Explanation:** Token replay attacks involve capturing and reusing valid tokens. Prevention includes short token lifetimes, nonce usage, and token binding to specific requests.

---

### Question 12 — Hard
**How does "mutual TLS" (mTLS) enhance API security?**

- A) It's twice as fast as regular TLS
- B) Both client and server authenticate each other using certificates
- C) It uses two different encryption algorithms
- D) It doubles the encryption strength

**Answer: B**

**Explanation:** mTLS provides bidirectional authentication where both the client and server verify each other's identity through certificates, preventing unauthorized clients from accessing the API.

---

### Question 13 — Easy
**What is an "access token" in authentication?**

- A) A physical key card
- B) A credential that grants temporary access to protected resources
- C) A permanent password
- D) A type of API key

**Answer: B**

**Explanation:** Access tokens are temporary credentials issued after successful authentication, granting limited access to specific resources for a defined period.

---

### Question 14 — Medium
**What is "single sign-on" (SSO)?**

- A) Signing in once per day
- B) Authenticating once and accessing multiple systems without re-authentication
- C) Using a single password for all accounts
- D) Signing in with one finger

**Answer: B**

**Explanation:** SSO allows users to authenticate once and access multiple related systems without re-entering credentials, improving both security (fewer passwords) and user experience.

---

### Question 15 — Medium
**What is a "refresh token" used for?**

- A) Refreshing the browser page
- B) Obtaining new access tokens without re-authentication
- C) Refreshing the database
- D) Updating the API key

**Answer: B**

**Explanation:** Refresh tokens are long-lived credentials used to obtain new access tokens when they expire, maintaining user sessions without requiring repeated authentication.

---

### Question 16 — Easy
**Why is multi-factor authentication (MFA) important?**

- A) It's required by all laws
- B) It adds additional verification layers, reducing compromise risk
- C) It makes login faster
- D) It's cheaper than single-factor

**Answer: B**

**Explanation:** MFA requires multiple forms of verification (password + code + biometric), making it significantly harder for attackers to gain access even if one factor is compromised.

---

### Question 17 — Hard
**What is "attribute-based access control" (ABAC)?**

- A) Controlling access based on file attributes
- B) Access decisions based on user attributes, resource attributes, and environment conditions
- C) A simpler version of RBAC
- D) Controlling access based on time only

**Answer: B**

**Explanation:** ABAC provides fine-grained access control by evaluating policies based on multiple attributes (user role, resource sensitivity, time of day, location), offering more flexibility than RBAC alone.

---

### Question 18 — Medium
**What is the risk of "token leakage" in AI systems?**

- A) Tokens become invalid
- B) Exposed tokens can be used to access protected resources unauthorized
- C) Tokens slow down the system
- D) Tokens increase costs

**Answer: B**

**Explanation:** Token leakage through logs, URLs, or storage can allow attackers to impersonate users and access AI services, making secure token handling critical.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong authentication knowledge.
- **12-14 correct (67-82%):** Good foundation, review hard topics.
- **9-11 correct (50-66%):** Needs improvement, study the explanations.
- **Below 9 (<50%):** Review the topic overview and retake.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
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
