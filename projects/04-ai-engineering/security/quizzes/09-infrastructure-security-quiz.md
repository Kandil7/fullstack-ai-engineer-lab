# AI Security Quiz: Infrastructure Security

## Topic Overview

Infrastructure security for AI systems involves protecting the underlying compute, storage, networking, and orchestration layers that support AI workloads. This quiz covers container security, cloud configurations, network protection, and operational security practices.

### Key Concepts
- Container and orchestration security
- Cloud infrastructure hardening
- Network segmentation and firewalls
- Secret management
- Incident response

---

## Quiz

### Question 1 — Easy
**Why is container security important for AI systems?**

- A) Containers are always secure
- B) Containers can expose vulnerabilities that compromise the entire AI pipeline
- C) Containers slow down models
- D) Containers are only for development

**Answer: B**

**Explanation:** Containers package AI applications with their dependencies, and vulnerabilities in container images or configurations can provide attackers access to the entire AI system.

---

### Question 2 — Easy
**What is "secret management" in infrastructure security?**

- A) Keeping documentation confidential
- B) Securely storing and managing credentials, keys, and sensitive configuration
- C) Hiding server locations
- D) Encrypting user passwords only

**Answer: B**

**Explanation:** Secret management involves securely storing, accessing, and rotating sensitive credentials like API keys, database passwords, and certificates using dedicated tools like HashiCorp Vault.

---

### Question 3 — Easy
**What is "network segmentation"?**

- A) Dividing the network into isolated zones
- B) Combining all network traffic into one channel
- C) Removing network firewalls
- D) Using a single network for all services

**Answer: A**

**Explanation:** Network segmentation divides infrastructure into isolated zones, limiting lateral movement if one segment is compromised and containing potential breaches.

---

### Question 4 — Medium
**What is a "container escape" attack?**

- A) Leaving a container running
- B) Breaking out of container isolation to access the host system
- C) Stopping a container
- D) Moving containers between servers

**Answer: B**

**Explanation:** Container escape exploits vulnerabilities to break out of container isolation, gaining access to the host system and potentially other containers, compromising the entire infrastructure.

---

### Question 5 — Medium
**Why should AI containers run as non-root users?**

- A) Root users are slower
- B) Root access inside containers increases the impact of container escape
- C) Non-root users use less memory
- D) Root users can't access GPUs

**Answer: B**

**Explanation:** Running as root inside containers means that if an attacker escapes the container, they gain root access to the host, significantly increasing the blast radius.

---

### Question 6 — Medium
**What is "infrastructure as code" (IaC) security?**

- A) Coding best practices only
- B) Scanning and securing infrastructure definitions before deployment
- C) Writing documentation for infrastructure
- D) Managing physical servers

**Answer: B**

**Explanation:** IaC security involves scanning infrastructure definitions (Terraform, CloudFormation) for misconfigurations, vulnerabilities, and policy violations before deployment.

---

### Question 7 — Medium
**What is the "shared responsibility model" in cloud AI security?**

- A) All security is the cloud provider's responsibility
- B) Security responsibilities are divided between cloud provider and customer
- C) Customers have no security responsibilities
- D) Security is everyone's and no one's responsibility

**Answer: B**

**Explanation:** Cloud providers secure the infrastructure layer, while customers secure their applications, data, and configurations, requiring understanding of which responsibilities fall where.

---

### Question 8 — Medium
**What is "image scanning" in container security?**

- A) Scanning physical containers
- B) Analyzing container images for known vulnerabilities and malware
- C) Taking photos of containers
- D) Monitoring container performance

**Answer: B**

**Explanation:** Image scanning analyzes container images for known vulnerabilities, malware, misconfigurations, and policy violations before deployment, preventing deployment of compromised images.

---

### Question 9 — Hard
**What is a "supply chain attack" in AI infrastructure?**

- A) Attacks on physical supply chains
- B) Compromising trusted dependencies, tools, or images used in the AI pipeline
- C) Stealing physical hardware
- D) Network-level attacks only

**Answer: B**

**Explanation:** Supply chain attacks compromise trusted components (base images, libraries, tools) that the AI system depends on, potentially injecting malicious code into the development or deployment process.

---

### Question 10 — Hard
**What is "immutable infrastructure" and why is it secure?**

- A) Infrastructure that can never be changed
- B) Infrastructure replaced rather than modified, preventing configuration drift
- C) Infrastructure using read-only databases
- D) Infrastructure without backups

**Answer: B**

**Explanation:** Immutable infrastructure replaces servers and containers rather than modifying them, preventing configuration drift and ensuring consistent, reproducible, and auditable deployments.

---

### Question 11 — Hard
**What is "zero trust architecture" in AI infrastructure?**

- A) Trusting all users
- B) Never trusting any request, always verifying regardless of location
- C) Having zero security measures
- D) Trusting only internal users

**Answer: B**

**Explanation:** Zero trust assumes no request should be trusted by default, requiring verification of every access attempt regardless of whether it originates inside or outside the network boundary.

---

### Question 12 — Hard
**What is "blast radius" in infrastructure security?**

- A) The speed of an explosion
- B) The extent of damage when a security incident occurs
- C) The size of the infrastructure
- D) The number of users affected

**Answer: B**

**Explanation:** Blast radius measures how much of the system is affected when a component is compromised. Minimizing blast radius through isolation and segmentation limits damage from security incidents.

---

### Question 13 — Easy
**What is "patch management" in infrastructure security?**

- A) Applying bandages to servers
- B) Regularly updating software to fix known vulnerabilities
- C) Creating backup patches
- D) Managing user permissions

**Answer: B**

**Explanation:** Patch management involves timely application of security updates to operating systems, frameworks, and dependencies, closing known vulnerabilities that attackers could exploit.

---

### Question 14 — Medium
**Why should GPU access be restricted in AI infrastructure?**

- A) GPUs are expensive
- B) Unauthorized GPU access can enable cryptocurrency mining or model theft
- C) GPUs use too much power
- D) GPUs are always secure

**Answer: B**

**Explanation:** Unrestricted GPU access can be abused for unauthorized computations, cryptocurrency mining, or unauthorized model training, consuming resources and potentially exfiltrating data.

---

### Question 15 — Medium
**What is "cloud security posture management" (CSPM)?**

- A) Managing cloud user positions
- B) Continuously monitoring cloud configurations for security risks and compliance
- C) Setting up cloud servers
- D) Managing cloud costs

**Answer: B**

**Explanation:** CSPM tools continuously assess cloud infrastructure configurations against security best practices and compliance requirements, identifying and remediating misconfigurations.

---

### Question 16 — Easy
**What is "least privilege" in infrastructure security?**

- A) Giving maximum access
- B) Granting only the minimum permissions needed for each component
- C) Using the cheapest services
- D) Running everything on one server

**Answer: B**

**Explanation:** Least privilege ensures each component, service, and user only has the permissions necessary for their function, limiting potential damage from compromised elements.

---

### Question 17 — Hard
**What is a "side-channel attack" on AI infrastructure?**

- A) A channel on the side of a server
- B) Extracting information through indirect physical observations like power or timing
- C) A backup communication channel
- D) A secondary API endpoint

**Answer: B**

**Explanation:** Side-channel attacks extract sensitive information through indirect observations like power consumption, electromagnetic emissions, or timing variations, potentially revealing model secrets.

---

### Question 18 — Medium
**What is the purpose of "disaster recovery planning" for AI systems?**

- A) Planning for successful deployments
- B) Ensuring AI systems can recover from failures, attacks, or disasters
- C) Planning new feature development
- D) Managing technical debt

**Answer: B**

**Explanation:** Disaster recovery planning ensures AI systems can be restored and continue operating after failures, attacks, or disasters, minimizing downtime and data loss.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong infrastructure security knowledge.
- **12-14 correct (67-82%):** Good foundation, review hard topics.
- **9-11 correct (50-66%):** Needs improvement, study the explanations.
- **Below 9 (<50%):** Review the topic overview and retake.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | A | Easy |
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
