# Lecture 02: Prompt Engineering

## Topic Overview

Prompt engineering is the art and science of designing effective inputs for Large Language Models. It's the single most impactful skill in AI automation—good prompts can mean the difference between a useless output and a production-ready solution. This lecture covers techniques from basic to advanced, including chain-of-thought reasoning, few-shot learning, and systematic prompt optimization.

**Duration:** 3-4 hours  
**Difficulty:** Beginner to Advanced  
**Prerequisites:** Lecture 01 (LLM API Integration)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Design** effective prompts using proven frameworks
2. **Implement** chain-of-thought (CoT) reasoning in prompts
3. **Use** few-shot and zero-shot techniques appropriately
4. **Apply** role-playing and persona techniques
5. **Structure** complex prompts for multi-step tasks
6. **Evaluate** prompt quality systematically
7. **Optimize** prompts for cost and performance
8. **Debug** common prompt failures

---

## Key Concepts

### 1. The Anatomy of a Good Prompt

Every effective prompt has these components:

```
┌─────────────────────────────────────────────────┐
│  ROLE (Who the AI should be)                    │
│  CONTEXT (Background information)               │
│  INSTRUCTIONS (What to do)                      │
│  INPUT DATA (What to process)                   │
│  OUTPUT FORMAT (How to respond)                 │
│  CONSTRAINTS (Rules and limits)                 │
└─────────────────────────────────────────────────┘
```

**Example:**
```python
prompt = """
ROLE: You are a senior data analyst with 10 years of experience.

CONTEXT: We have quarterly sales data for our e-commerce platform.
The data includes: date, product_category, revenue, units_sold, region.

INSTRUCTIONS: Analyze the data and identify:
1. Top 3 performing categories
2. Seasonal trends
3. Regional differences
4. Year-over-year growth

INPUT DATA:
Q1: Electronics $1.2M (15K units), Clothing $800K (25K units)
Q2: Electronics $900K (12K units), Clothing $1.1M (35K units)
Q3: Electronics $1.5M (18K units), Clothing $700K (20K units)
Q4: Electronics $2.0M (25K units), Clothing $1.3M (40K units)

OUTPUT FORMAT: Executive summary with bullet points, followed by
detailed analysis with specific numbers and percentages.

CONSTRAINTS:
- Use only provided data
- Include confidence levels for predictions
- Flag any data quality concerns
"""
```

### 2. Zero-Shot vs Few-Shot Prompting

**Zero-Shot:** No examples provided; relies on the model's pre-training.

```python
# Zero-shot
prompt = """
Classify the sentiment of this review as positive, negative, or neutral:

"The product arrived quickly and works great, but the packaging was damaged."
"""
```

**Few-Shot:** Examples provided to guide the model's behavior.

```python
# Few-shot
prompt = """
Classify the sentiment of reviews as positive, negative, or neutral.

Examples:
Review: "Absolutely love this product! Best purchase ever."
Sentiment: positive

Review: "Terrible quality. Broke after one use."
Sentiment: negative

Review: "It's okay, does what it's supposed to do."
Sentiment: neutral

Review: "The product arrived quickly and works great, but the packaging was damaged."
Sentiment: """
```

**When to use which:**
- **Zero-shot:** Simple, well-defined tasks
- **Few-shot:** Complex tasks, specific output formats, edge cases

### 3. Chain-of-Thought (CoT) Prompting

CoT forces the model to show its reasoning process, dramatically improving accuracy on complex tasks.

```python
# Standard prompt (may give wrong answer)
prompt = "If a train travels 60 mph for 2.5 hours, how far does it go?"

# CoT prompt (shows reasoning)
prompt = """
Solve this step by step:

If a train travels 60 mph for 2.5 hours, how far does it go?

Let's think through this:
1. What is the formula for distance?
2. What values do we have?
3. How do we calculate?

Show your reasoning at each step, then give the final answer.
"""
```

**CoT Variations:**

```python
# Manual CoT
prompt = """
Step-by-step reasoning:
1. First, I need to identify...
2. Next, I should consider...
3. Then, I can calculate...
4. Finally, I conclude...

Now solve: [your question]
"""

# Zero-shot CoT (just add "Let's think step by step")
prompt = """
[Your question]

Let's think step by step.
"""

# Auto-CoT (model generates steps automatically)
prompt = """
Work through this problem step by step, showing your reasoning:

[Your complex problem]
"""
```

### 4. Role-Playing and Personas

Assigning roles dramatically changes output quality and style:

```python
# Generic response
prompt = "Explain how a database works."

# Expert persona
prompt = """
You are a database architect with 20 years of experience at major tech companies.
You've designed systems handling millions of queries per second.

Explain how a database works to a junior developer who understands basic programming
but has never worked with databases. Use analogies from everyday life.
"""

# Multiple personas (for debate/perspective)
prompt = """
Three experts discuss whether to use SQL or NoSQL:

Expert 1 (Database Administrator): Advocates for SQL
Expert 2 (Startup CTO): Advocates for NoSQL
Expert 3 (Enterprise Architect): Provides balanced view

Each expert should:
- State their position
- Provide 3 supporting arguments
- Address counterarguments
- Give a final recommendation

Format as a structured debate.
"""
```

### 5. Output Format Control

Control exactly how the model responds:

```python
# JSON output
prompt = """
Extract the following information from this text and return as JSON:

Text: "John Smith, age 35, works at Google as a Senior Engineer. 
He lives in San Francisco and has been with the company for 5 years."

Return JSON with this schema:
{
    "name": "string",
    "age": number,
    "company": "string",
    "role": "string",
    "location": "string",
    "years_at_company": number
}
"""

# Table output
prompt = """
Compare Python, JavaScript, and Go for web development.

Format your response as a markdown table with columns:
| Feature | Python | JavaScript | Go |

Include rows for: Learning curve, Performance, Ecosystem, Use Cases, Job Market
"""

# Structured output with sections
prompt = """
Analyze this code and provide feedback in this exact format:

## Code Quality
[Rate 1-10 and explain]

## Bugs Found
[List each bug with line number]

## Performance Issues
[Identify any performance concerns]

## Suggestions
[Numbered list of improvements]

## Refactored Code
[Improved version]
"""
```

### 6. Constraint-Based Prompting

Set explicit limits to guide output:

```python
prompt = """
Write a product description for wireless headphones.

CONSTRAINTS:
- Maximum 150 words
- Must mention: battery life, sound quality, comfort
- Tone: Professional but friendly
- No superlatives (best, greatest, most)
- Include one technical specification
- End with a call to action
"""
```

### 7. Iterative Prompt Refinement

Systematic approach to improving prompts:

```python
# Version 1: Basic
v1 = "Write a marketing email for our new product."

# Version 2: Add context
v2 = """
Write a marketing email for our new AI-powered code review tool.
Target audience: Senior developers
Key feature: Catches 40% more bugs than manual review
"""

# Version 3: Add structure
v3 = """
Write a marketing email for our new AI-powered code review tool.

Structure:
- Subject line (under 50 chars)
- Hook (first sentence)
- Problem statement
- Solution presentation
- Key benefits (3 max)
- Social proof
- Call to action

Tone: Professional, developer-focused, no hype
Length: Under 200 words
"""

# Version 4: Add examples
v4 = """
Write a marketing email for our new AI-powered code review tool.

[Version 3 content + example of a good marketing email for reference]
"""
```

---

## Code Examples

### Example 1: Prompt Template System

```python
"""
A flexible prompt template system for reusable prompts.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
import re


@dataclass
class PromptTemplate:
    """Reusable prompt template with variable substitution."""
    
    template: str
    required_vars: list[str]
    optional_vars: Dict[str, str] = None
    
    def render(self, **kwargs) -> str:
        """Render template with provided variables."""
        
        # Check required variables
        missing = [v for v in self.required_vars if v not in kwargs]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        
        # Apply optional defaults
        if self.optional_vars:
            for key, default in self.optional_vars.items():
                if key not in kwargs:
                    kwargs[key] = default
        
        # Replace {var} placeholders
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f"{{{key}}}", str(value))
        
        return result


# Define templates
ANALYSIS_TEMPLATE = PromptTemplate(
    template="""
ROLE: You are a {role} with expertise in {domain}.

TASK: Analyze the following {content_type}:

{content}

ANALYSIS REQUIREMENTS:
1. Identify key {key_elements}
2. Evaluate {evaluation_criteria}
3. Provide actionable recommendations

OUTPUT FORMAT:
- Executive Summary (2-3 sentences)
- Detailed Findings (bullet points)
- Recommendations (numbered list)
- Risk Assessment (low/medium/high)

CONSTRAINTS:
- Be specific with numbers and evidence
- Avoid speculation without data
- Flag assumptions clearly
""",
    required_vars=["role", "domain", "content_type", "content", 
                   "key_elements", "evaluation_criteria"],
    optional_vars={"risk_level": "medium"}
)

# Usage
prompt = ANALYSIS_TEMPLATE.render(
    role="senior security analyst",
    domain="cybersecurity",
    content_type="network logs",
    content=open("network_logs.txt").read(),
    key_elements="anomalies and potential threats",
    evaluation_criteria="severity and impact"
)
```

### Example 2: Chain-of-Thought Problem Solver

```python
"""
Chain-of-Thought prompt generator for different problem types.
"""
from enum import Enum
from typing import Any


class ProblemType(Enum):
    MATHEMATICAL = "mathematical"
    LOGICAL = "logical"
    CODE_DEBUG = "code_debug"
    ANALYSIS = "analysis"
    CREATIVE = "creative"


class CoTPromptGenerator:
    """Generate chain-of-thought prompts for different problem types."""
    
    TEMPLATES = {
        ProblemType.MATHEMATICAL: """
Solve this mathematical problem step by step:

Problem: {problem}

Let me work through this systematically:

1. UNDERSTAND THE PROBLEM:
   - What am I asked to find?
   - What information is given?

2. IDENTIFY KEY CONCEPTS:
   - What formulas or principles apply?
   - What are the known variables?

3. SET UP THE SOLUTION:
   - Write the equations
   - Substitute known values

4. SOLVE STEP BY STEP:
   - Show each calculation
   - Explain what each step accomplishes

5. VERIFY THE ANSWER:
   - Does the answer make sense?
   - Can I check it another way?

Final Answer: [clearly stated]
""",
        
        ProblemType.CODE_DEBUG: """
Debug this code using systematic analysis:

```{language}
{code}
```

Problem description: {problem_description}

Let me analyze this step by step:

1. READ THE CODE CAREFULLY:
   - What is the intended behavior?
   - What are the inputs and outputs?

2. IDENTIFY THE SYMPTOM:
   - What is the actual behavior?
   - What error messages appear?
   - When does the bug occur?

3. FORM A HYPOTHESIS:
   - What could cause this behavior?
   - Consider: logic errors, off-by-one, null handling, race conditions

4. TRACE THE EXECUTION:
   - Walk through with example inputs
   - Track variable values at each step

5. TEST THE HYPOTHESIS:
   - Does the error match my theory?
   - What would fix it?

6. VERIFY THE FIX:
   - Does the fix address the root cause?
   - Are there edge cases to consider?

Bug identified: [description]
Root cause: [explanation]
Fix: [code change]
""",
        
        ProblemType.ANALYSIS: """
Analyze this situation systematically:

Context: {context}
Question: {question}

My analytical framework:

1. DEFINE THE PROBLEM:
   - What exactly needs to be determined?
   - What are the success criteria?

2. GATHER EVIDENCE:
   - What data/facts do we have?
   - What are the key variables?

3. IDENTIFY PATTERNS:
   - What trends emerge from the data?
   - What correlations exist?

4. GENERATE HYPOTHESES:
   - What are possible explanations?
   - What assumptions am I making?

5. EVALUATE HYPOTHESES:
   - Which explanation best fits the evidence?
   - What would disprove each hypothesis?

6. DRAW CONCLUSIONS:
   - What is the most likely answer?
   - What is my confidence level?
   - What additional information would increase confidence?

Conclusion: [summary]
Confidence: [high/medium/low with reasoning]
Recommendations: [actionable next steps]
""",
    }
    
    @classmethod
    def generate(cls, problem_type: ProblemType, **kwargs) -> str:
        """Generate a CoT prompt for the given problem type."""
        template = cls.TEMPLATES.get(problem_type)
        if not template:
            raise ValueError(f"Unknown problem type: {problem_type}")
        
        return template.format(**kwargs)


# Usage
cot_prompt = CoTPromptGenerator.generate(
    ProblemType.CODE_DEBUG,
    language="python",
    code="""
def find_max(arr):
    max_val = arr[0]
    for i in range(len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
""",
    problem_description="Function throws IndexError when array is empty"
)
```

### Example 3: Prompt Evaluation Framework

```python
"""
Systematic prompt evaluation and comparison.
"""
from dataclasses import dataclass
from typing import List, Callable
import time
from openai import OpenAI


@dataclass
class EvalCase:
    """A test case for prompt evaluation."""
    input_data: str
    expected_behavior: str
    keywords: List[str]
    anti_keywords: List[str]


@dataclass
class EvalResult:
    """Result of evaluating a prompt on a test case."""
    prompt_version: str
    input_data: str
    output: str
    score: float
    keywords_found: int
    anti_keywords_found: int
    latency_ms: float
    tokens_used: int


class PromptEvaluator:
    """Evaluate and compare prompt versions."""
    
    def __init__(self, model: str = "gpt-4"):
        self.client = OpenAI()
        self.model = model
    
    def evaluate(
        self,
        prompt_template: str,
        test_cases: List[EvalCase],
        version_name: str = "v1"
    ) -> List[EvalResult]:
        """Evaluate a prompt template against test cases."""
        
        results = []
        
        for test in test_cases:
            # Format prompt
            prompt = prompt_template.format(input=test.input_data)
            
            # Call API
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            latency = (time.time() - start_time) * 1000
            
            output = response.choices[0].message.content
            
            # Score output
            keywords_found = sum(1 for kw in test.keywords 
                               if kw.lower() in output.lower())
            anti_keywords_found = sum(1 for kw in test.anti_keywords 
                                    if kw.lower() in output.lower())
            
            # Calculate score (0-1)
            keyword_score = keywords_found / max(len(test.keywords), 1)
            penalty = anti_keywords_found * 0.2
            score = max(0, min(1, keyword_score - penalty))
            
            results.append(EvalResult(
                prompt_version=version_name,
                input_data=test.input_data,
                output=output,
                score=score,
                keywords_found=keywords_found,
                anti_keywords_found=anti_keywords_found,
                latency_ms=latency,
                tokens_used=response.usage.total_tokens
            ))
        
        return results
    
    def compare(
        self,
        results_v1: List[EvalResult],
        results_v2: List[EvalResult]
    ) -> dict:
        """Compare two prompt versions."""
        
        avg_score_v1 = sum(r.score for r in results_v1) / len(results_v1)
        avg_score_v2 = sum(r.score for r in results_v2) / len(results_v2)
        
        avg_latency_v1 = sum(r.latency_ms for r in results_v1) / len(results_v1)
        avg_latency_v2 = sum(r.latency_ms for r in results_v2) / len(results_v2)
        
        avg_tokens_v1 = sum(r.tokens_used for r in results_v1) / len(results_v1)
        avg_tokens_v2 = sum(r.tokens_used for r in results_v2) / len(results_v2)
        
        return {
            "version_1": {
                "avg_score": avg_score_v1,
                "avg_latency_ms": avg_latency_v1,
                "avg_tokens": avg_tokens_v1
            },
            "version_2": {
                "avg_score": avg_score_v2,
                "avg_latency_ms": avg_latency_v2,
                "avg_tokens": avg_tokens_v2
            },
            "winner": "v1" if avg_score_v1 > avg_score_v2 else "v2",
            "improvement": abs(avg_score_v2 - avg_score_v1) / max(avg_score_v1, 0.01)
        }


# Usage
evaluator = PromptEvaluator()

# Define test cases
test_cases = [
    EvalCase(
        input_data="Python is too slow for web development",
        expected_behavior="Provide balanced view of Python performance",
        keywords=["async", "framework", "FastAPI", "performance"],
        anti_keywords=["slow", "terrible", "worst"]
    ),
    EvalCase(
        input_data="JavaScript is better than Python",
        expected_behavior="Avoid taking sides, highlight use cases",
        keywords=["different", "use cases", "ecosystem"],
        anti_keywords=["wrong", "stupid", "never"]
    )
]

# Evaluate two prompt versions
v1_template = "Respond to this opinion: {input}"
v2_template = """
You are a helpful technology consultant. Respond to this opinion:
{input}

Be balanced, professional, and provide evidence-based perspective.
Focus on use cases rather than declaring winners.
"""

results_v1 = evaluator.evaluate(v1_template, test_cases, "v1")
results_v2 = evaluator.evaluate(v2_template, test_cases, "v2")

comparison = evaluator.compare(results_v1, results_v2)
print(f"Winner: {comparison['winner']}")
print(f"Improvement: {comparison['improvement']:.1%}")
```

---

## Common Mistakes to Avoid

### 1. Being Too Vague
```python
# ❌ BAD: Vague prompt
"Write about AI"

# ✅ GOOD: Specific prompt
"Write a 500-word technical blog post explaining how transformer 
architecture works, targeted at software developers with basic ML 
knowledge. Include one code example."
```

### 2. Ignoring Output Format
```python
# ❌ BAD: No format specification
"Analyze this data"

# ✅ GOOD: Explicit format
"""
Analyze this data and return:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Recommendations (numbered list)
4. Confidence Level (high/medium/low)
"""
```

### 3. Not Using Examples
```python
# ❌ BAD: No examples for complex tasks
"Extract entities from text"

# ✅ GOOD: Few-shot with examples
"""
Extract entities from text.

Example:
Text: "Apple released iPhone 15 in September 2023"
Entities: Company: Apple, Product: iPhone 15, Date: September 2023

Now extract from: [your text]
"""
```

### 4. Overloading the Prompt
```python
# ❌ BAD: Too many tasks in one prompt
"""
Analyze the data, write a report, create charts, 
and email it to the team.
"""

# ✅ GOOD: Decompose into steps
"""
Step 1: Analyze the data and identify key insights
Step 2: Write an executive summary
Step 3: Create bullet points for the report
"""
```

---

## Best Practices

1. **Be specific** about what you want (length, format, tone, audience)
2. **Use examples** for complex or ambiguous tasks
3. **Apply CoT** for reasoning-heavy problems
4. **Set constraints** to guide output (word limits, required elements)
5. **Iterate systematically** - change one variable at a time
6. **Test with edge cases** - unusual inputs reveal prompt weaknesses
7. **Version control prompts** - track what works
8. **Measure quality** - don't rely on gut feeling
9. **Consider cost** - simpler prompts are cheaper
10. **Document prompt patterns** that work for your domain

---

## Practice Exercises

### Exercise 1: Email Generator
Create a prompt that generates professional emails for different scenarios (follow-up, introduction, apology). Test with at least 5 different scenarios.

### Exercise 2: Code Reviewer
Build a prompt that reviews Python code and provides feedback on:
- Code quality
- Performance
- Security
- Best practices

Include specific scoring criteria.

### Exercise 3: Data Extractor
Design a prompt that extracts structured data from unstructured text. Test with:
- Business cards
- Meeting notes
- Product reviews

### Exercise 4: Prompt Chainer
Create two prompts where the output of the first becomes the input of the second:
1. Summarize a long document
2. Generate questions based on the summary

### Exercise 5: A/B Test Framework
Write code that tests two prompt versions on 10 test cases and statistically determines which performs better.

---

## Summary

Prompt engineering is a critical skill for AI automation:

1. **Structure matters** - Use role, context, instructions, format
2. **CoT improves accuracy** - Force reasoning for complex tasks
3. **Examples clarify intent** - Few-shot for ambiguous tasks
4. **Iteration is key** - Systematic refinement beats one-shot attempts
5. **Evaluation is essential** - Measure, don't guess
6. **Constraints help** - Guide output with specific limits

**Next lecture:** Vector Embeddings - How to represent text as numbers.
