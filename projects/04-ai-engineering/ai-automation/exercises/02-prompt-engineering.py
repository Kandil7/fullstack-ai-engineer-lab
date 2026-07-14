"""
Exercise 02: Prompt Engineering
=================================
Master advanced prompt engineering techniques: zero-shot, few-shot,
chain-of-thought, tree-of-thought, self-consistency, prompt templates,
output parsing, and systematic prompt testing.

Prerequisites:
    pip install openai groq python-dotenv pydantic

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
    GROQ_API_KEY=gsk_...
"""

import os
import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, TypeVar, Type
from enum import Enum

T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. LLM Abstraction (simple, for prompt testing)
# ---------------------------------------------------------------------------

def llm_call(prompt: str, *, system: str = "", temperature: float = 0.7,
             max_tokens: int = 1024, model: str = "gpt-4o-mini") -> str:
    """Simple LLM call using OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
    )
    return response.choices[0].message.content or ""


def llm_call_groq(prompt: str, *, system: str = "", temperature: float = 0.7,
                   model: str = "llama-3.3-70b-versatile") -> str:
    """Simple LLM call using Groq API."""
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=1024,
        messages=messages,
    )
    return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# 2. Zero-Shot Prompting
# ---------------------------------------------------------------------------

class ZeroShot:
    """
    Zero-shot prompting: ask the model to perform a task without examples.
    
    When to use: Simple tasks where the model already understands the format.
    Key: Be explicit about the output format and constraints.
    """

    @staticmethod
    def classify(text: str, categories: list[str], model: str = "gpt-4o-mini") -> str:
        """Classify text into one of the given categories."""
        prompt = f"""Classify the following text into exactly one of these categories: {', '.join(categories)}

Text: "{text}"

Category:"""
        return llm_call(prompt, temperature=0, model=model).strip()

    @staticmethod
    def extract(text: str, fields: list[str], model: str = "gpt-4o-mini") -> dict:
        """Extract structured information from text."""
        fields_str = ", ".join(fields)
        prompt = f"""Extract the following fields from the text: {fields_str}

Return ONLY a JSON object with those keys. No explanation.

Text: "{text}"

JSON:"""
        response = llm_call(prompt, temperature=0, model=model)
        # Clean up response to extract JSON
        response = re.sub(r"```json\n?|\n?```", "", response).strip()
        return json.loads(response)

    @staticmethod
    def summarize(text: str, *, style: str = "concise", model: str = "gpt-4o-mini") -> str:
        """Summarize text in a specified style."""
        styles = {
            "concise": "Summarize in 1-2 sentences.",
            "detailed": "Summarize in 3-5 bullet points.",
            "technical": "Summarize for a technical audience, including key concepts.",
        }
        instruction = styles.get(style, styles["concise"])
        prompt = f"""{instruction}

Text: "{text}"

Summary:"""
        return llm_call(prompt, temperature=0.3, model=model)


# ---------------------------------------------------------------------------
# 3. Few-Shot Prompting
# ---------------------------------------------------------------------------

class FewShot:
    """
    Few-shot prompting: provide examples before the actual query.
    
    When to use: When you need specific output formatting or style
    that's hard to describe in instructions alone.
    """

    @staticmethod
    def sentiment_analysis(text: str, model: str = "gpt-4o-mini") -> str:
        """Classify sentiment with examples."""
        prompt = f"""Classify the sentiment of each review as positive, negative, or neutral.

Review: "This product is amazing! Best purchase ever."
Sentiment: positive

Review: "Terrible quality, broke after one day."
Sentiment: negative

Review: "It's okay, nothing special."
Sentiment: neutral

Review: "Absolutely love it! Would recommend to everyone."
Sentiment: positive

Review: "{text}"
Sentiment:"""
        return llm_call(prompt, temperature=0, model=model).strip().lower()

    @staticmethod
    def style_transfer(text: str, target_style: str, model: str = "gpt-4o-mini") -> str:
        """Rewrite text in a different style with examples."""
        prompt = f"""Rewrite the text in {target_style} style.

Original: "The weather is nice today."
{target_style}: "What a glorious day it is! The sun shines upon us like a warm embrace."

Original: "I went to the store."
{target_style}: "I ventured forth to the marketplace of goods."

Original: "The meeting went well."
{target_style}: "The assembly proved most fruitful in its proceedings."

Original: "{text}"
{target_style}:"""
        return llm_call(prompt, temperature=0.7, model=model)

    @staticmethod
    def json_extraction(text: str, schema: dict, model: str = "gpt-4o-mini") -> dict:
        """Extract structured data with schema examples."""
        example_inputs = {
            "name": "John Smith",
            "email": "john@example.com",
            "age": "30",
        }

        prompt = f"""Extract information matching this schema: {json.dumps(schema)}

Example:
Input: "Contact John Smith at john@example.com, age 30"
Output: {json.dumps(example_inputs)}

Input: "{text}"
Output:"""
        response = llm_call(prompt, temperature=0, model=model)
        response = re.sub(r"```json\n?|\n?```", "", response).strip()
        return json.loads(response)


# ---------------------------------------------------------------------------
# 4. Chain-of-Thought (CoT) Prompting
# ---------------------------------------------------------------------------

class ChainOfThought:
    """
    Chain-of-thought prompting: ask the model to reason step-by-step.
    
    When to use: Complex reasoning, math, logic puzzles, multi-step problems.
    Key: "Let's think step by step" is the classic CoT trigger.
    """

    @staticmethod
    def basic(question: str, model: str = "gpt-4o-mini") -> str:
        """Standard chain-of-thought."""
        prompt = f"""{question}

Let's think step by step:"""
        return llm_call(prompt, temperature=0.3, model=model)

    @staticmethod
    def structured(question: str, model: str = "gpt-4o-mini") -> str:
        """Structured CoT with explicit reasoning steps."""
        prompt = f"""Answer the following question with clear reasoning steps.

Question: {question}

Step 1 - Understand the problem:
Step 2 - Identify key information:
Step 3 - Work through the solution:
Step 4 - Verify the answer:
Step 5 - Final answer:"""
        return llm_call(prompt, temperature=0.3, model=model)

    @staticmethod
    def math_problem(question: str, model: str = "gpt-4o-mini") -> str:
        """Math-specific CoT with verification."""
        prompt = f"""Solve this math problem step by step.

Problem: {question}

Given:
Reasoning:
Calculation:
Verification:
Answer:"""
        return llm_call(prompt, temperature=0, model=model)

    @staticmethod
    def code_review(code: str, model: str = "gpt-4o-mini") -> str:
        """CoT for code review."""
        prompt = f"""Review this code step by step.

Code:
```python
{code}
```

Step 1 - Read and understand the code:
Step 2 - Check for bugs and errors:
Step 3 - Evaluate performance:
Step 4 - Check security:
Step 5 - Suggest improvements:
Step 6 - Overall assessment:"""
        return llm_call(prompt, temperature=0.3, model=model)


# ---------------------------------------------------------------------------
# 5. Tree-of-Thought (ToT) Prompting
# ---------------------------------------------------------------------------

class TreeOfThought:
    """
    Tree-of-thought: explore multiple reasoning paths, evaluate them,
    and choose the best one.
    
    When to use: When there are multiple valid approaches and you want
    the model to evaluate alternatives before committing.
    """

    @staticmethod
    def solve(problem: str, *, num_paths: int = 3, model: str = "gpt-4o-mini") -> str:
        """Generate multiple solution paths and select the best."""
        prompt = f"""Problem: {problem}

Generate {num_paths} different approaches to solve this problem.

Approach 1: [reasoning]
Approach 2: [reasoning]
Approach 3: [reasoning]

For each approach, rate its feasibility (1-10) and identify pros/cons.

Then, select the BEST approach and provide the final answer.

Evaluation:"""
        return llm_call(prompt, temperature=0.5, model=model)

    @staticmethod
    def creative_writing(topic: str, *, num_ideas: int = 3, model: str = "gpt-4o-mini") -> str:
        """Generate multiple creative ideas and pick the best."""
        prompt = f"""Topic: {topic}

Generate {num_ideas} different creative ideas:

Idea 1: [detailed concept]
Idea 2: [detailed concept]
Idea 3: [detailed concept]

Evaluate each for: creativity (1-10), feasibility (1-10), impact (1-10).

Best idea (highest combined score): [selected idea]
Expanded version of the best idea:"""
        return llm_call(prompt, temperature=0.8, model=model)


# ---------------------------------------------------------------------------
# 6. Self-Consistency
# ---------------------------------------------------------------------------

class SelfConsistency:
    """
    Self-consistency: generate multiple answers and take the majority vote.
    
    When to use: When accuracy matters more than speed.
    Key: Higher temperature = more diverse reasoning paths.
    """

    def __init__(self, num_samples: int = 5, temperature: float = 0.7):
        self.num_samples = num_samples
        self.temperature = temperature

    def vote(self, question: str, *, model: str = "gpt-4o-mini") -> dict:
        """Generate multiple answers and vote on the most common one."""
        answers = []

        for i in range(self.num_samples):
            prompt = f"""{question}

Think step by step, then give your final answer on the last line.
Final answer:"""
            response = llm_call(prompt, temperature=self.temperature, model=model)
            # Extract the last non-empty line as the answer
            lines = [l.strip() for l in response.strip().split("\n") if l.strip()]
            answer = lines[-1] if lines else response
            answers.append(answer)
            print(f"  Sample {i + 1}: {answer}")

        # Count votes
        from collections import Counter
        vote_counts = Counter(answers)
        most_common, count = vote_counts.most_common(1)[0]

        return {
            "answer": most_common,
            "confidence": count / self.num_samples,
            "all_answers": answers,
            "vote_distribution": dict(vote_counts),
        }


# ---------------------------------------------------------------------------
# 7. Prompt Templates
# ---------------------------------------------------------------------------

class PromptTemplate:
    """Reusable prompt template with variable substitution."""

    def __init__(self, template: str, required_vars: list[str] | None = None):
        self.template = template
        self.required_vars = required_vars or self._extract_vars(template)

    def _extract_vars(self, template: str) -> list[str]:
        """Extract {variable} names from template."""
        return list(set(re.findall(r"\{(\w+)\}", template)))

    def render(self, **kwargs) -> str:
        """Render the template with given variables."""
        missing = set(self.required_vars) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        return self.template.format(**kwargs)

    def __call__(self, **kwargs) -> str:
        return self.render(**kwargs)


# Pre-built templates
TEMPLATES = {
    "summarize": PromptTemplate(
        "Summarize the following text for a {audience} audience in {style}.\n\nText: {text}\n\nSummary:"
    ),
    "classify": PromptTemplate(
        "Classify the following text into one of: {categories}\n\nText: {text}\n\nCategory:"
    ),
    "extract": PromptTemplate(
        "Extract {fields} from the following text.\n\nText: {text}\n\nReturn as JSON:"
    ),
    "rewrite": PromptTemplate(
        "Rewrite the following text to be {style}.\n\nOriginal: {text}\n\nRewritten:"
    ),
    "explain": PromptTemplate(
        "Explain {topic} to a {level} audience.\n\nKey points:\n- Point 1\n- Point 2\n- Point 3\n\nExplanation:"
    ),
    "code_review": PromptTemplate(
        "Review this {language} code for {focus}.\n\n```{language}\n{code}\n```\n\nReview:"
    ),
}


# ---------------------------------------------------------------------------
# 8. Output Parsing
# ---------------------------------------------------------------------------

class OutputParser:
    """Parse structured output from LLM responses."""

    @staticmethod
    def json_from_text(text: str) -> dict | list:
        """Extract JSON from LLM text response."""
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try extracting from code block
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))

        # Try finding JSON-like content
        match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))

        raise ValueError(f"No JSON found in response:\n{text}")

    @staticmethod
    def list_from_text(text: str) -> list[str]:
        """Extract a list from LLM text (bullet points, numbered, etc.)."""
        items = []
        for line in text.strip().split("\n"):
            line = line.strip()
            # Remove bullet points or numbers
            cleaned = re.sub(r"^[\-\*\d\.\)]+\s*", "", line).strip()
            if cleaned:
                items.append(cleaned)
        return items

    @staticmethod
    def key_value_pairs(text: str) -> dict[str, str]:
        """Extract key-value pairs from LLM output."""
        pairs = {}
        for line in text.strip().split("\n"):
            line = line.strip()
            if ":" in line:
                key, _, value = line.partition(":")
                key = re.sub(r"^[\-\*]+", "", key).strip().lower()
                value = value.strip()
                if key and value:
                    pairs[key] = value
        return pairs

    @staticmethod
    def parse_with_schema(text: str, schema: dict) -> dict:
        """Parse LLM output against a Pydantic-like schema."""
        parsed = OutputParser.json_from_text(text)

        validated = {}
        for field_name, field_type in schema.items():
            if field_name in parsed:
                value = parsed[field_name]
                if field_type == "str":
                    validated[field_name] = str(value)
                elif field_type == "int":
                    validated[field_name] = int(value)
                elif field_type == "float":
                    validated[field_name] = float(value)
                elif field_type == "bool":
                    validated[field_name] = bool(value)
                elif field_type == "list":
                    validated[field_name] = list(value) if not isinstance(value, list) else value
                else:
                    validated[field_name] = value

        return validated


# ---------------------------------------------------------------------------
# 9. Prompt Testing Framework
# ---------------------------------------------------------------------------

@dataclass
class PromptTest:
    """A single test case for a prompt."""
    input_text: str
    expected_behavior: str
    validation_fn: callable | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class TestResult:
    """Result of running a prompt test."""
    test: PromptTest
    output: str
    passed: bool
    score: float = 0.0
    notes: str = ""


class PromptTester:
    """Framework for systematic prompt testing."""

    def __init__(self):
        self.results: list[TestResult] = []

    def test(self, prompt_fn: callable, tests: list[PromptTest], *,
             judge_model: str = "gpt-4o-mini") -> list[TestResult]:
        """Run all tests against a prompt function."""
        self.results = []

        for test in tests:
            output = prompt_fn(test.input_text)

            # Automated validation
            passed = True
            notes = ""
            if test.validation_fn:
                try:
                    passed = test.validation_fn(output)
                except Exception as e:
                    passed = False
                    notes = str(e)

            # LLM-as-judge evaluation
            judge_prompt = f"""Evaluate this output against the expected behavior.

Output: {output}
Expected: {test.expected_behavior}

Score 1-10 (10 = perfect match) and explain briefly in JSON:
{{"score": <number>, "reason": "<brief explanation>"}}"""

            try:
                judge_response = llm_call(judge_prompt, temperature=0, model=judge_model)
                import re
                json_match = re.search(r"\{.*\}", judge_response, re.DOTALL)
                if json_match:
                    judge_result = json.loads(json_match.group())
                    score = judge_result.get("score", 5) / 10
                else:
                    score = 0.5
            except Exception:
                score = 0.5 if passed else 0.0

            result = TestResult(test=test, output=output, passed=passed, score=score, notes=notes)
            self.results.append(result)

            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] Score: {score:.1f}/1.0 | {test.expected_behavior[:50]}...")

        return self.results

    def summary(self) -> dict:
        """Summarize test results."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0

        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "average_score": avg_score,
        }


# ---------------------------------------------------------------------------
# 10. Demo Functions
# ---------------------------------------------------------------------------

def demo_zero_shot():
    """Demo: Zero-shot prompting techniques."""
    print("=" * 60)
    print("DEMO 1: Zero-Shot Prompting")
    print("=" * 60)

    # Classification
    text = "The new product launch exceeded all expectations with record sales."
    category = ZeroShot.classify(text, ["positive", "negative", "neutral"])
    print(f"Text: {text}")
    print(f"Category: {category}\n")

    # Extraction
    text = "Contact Dr. Jane Smith at jane.smith@university.edu for the AI course starting January 15, 2025."
    data = ZeroShot.extract(text, ["name", "email", "course", "date"])
    print(f"Extracted: {json.dumps(data, indent=2)}\n")


def demo_few_shot():
    """Demo: Few-shot prompting."""
    print("=" * 60)
    print("DEMO 2: Few-Shot Prompting")
    print("=" * 60)

    text = "The service was slow but the food was delicious."
    sentiment = FewShot.sentiment_analysis(text)
    print(f"Text: {text}")
    print(f"Sentiment: {sentiment}\n")

    text = "I need to buy groceries and clean the house."
    result = FewShot.style_transfer(text, "Shakespearean English")
    print(f"Original: {text}")
    print(f"Shakespearean: {result}\n")


def demo_chain_of_thought():
    """Demo: Chain-of-thought prompting."""
    print("=" * 60)
    print("DEMO 3: Chain-of-Thought")
    print("=" * 60)

    question = "If I have 3 apples and give away 1, then buy 5 more, how many do I have?"
    result = ChainOfThought.math_problem(question)
    print(f"Question: {question}")
    print(f"Answer:\n{result}\n")


def demo_tree_of_thought():
    """Demo: Tree-of-thought prompting."""
    print("=" * 60)
    print("DEMO 4: Tree-of-Thought")
    print("=" * 60)

    problem = "Design a scalable chat system that handles 1 million concurrent users."
    result = TreeOfThought.solve(problem, num_paths=3)
    print(f"Result:\n{result}\n")


def demo_self_consistency():
    """Demo: Self-consistency voting."""
    print("=" * 60)
    print("DEMO 5: Self-Consistency")
    print("=" * 60)

    sc = SelfConsistency(num_samples=3, temperature=0.7)
    result = sc.vote("What is 15 * 12? Show your work.")
    print(f"\nFinal answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.0%}\n")


def demo_templates():
    """Demo: Prompt templates."""
    print("=" * 60)
    print("DEMO 6: Prompt Templates")
    print("=" * 60)

    # Using pre-built templates
    prompt = TEMPLATES["summarize"](
        audience="technical",
        style="bullet points",
        text="Python is a high-level programming language known for its simplicity and readability."
    )
    print(f"Rendered prompt:\n{prompt}\n")

    # Custom template
    custom = PromptTemplate(
        "Translate the following {source_lang} text to {target_lang}:\n{text}\nTranslation:"
    )
    prompt = custom(source_lang="English", target_lang="French", text="Hello, how are you?")
    print(f"Custom template:\n{prompt}\n")


def demo_output_parsing():
    """Demo: Output parsing."""
    print("=" * 60)
    print("DEMO 7: Output Parsing")
    print("=" * 60)

    # JSON extraction
    text = 'The result is: {"name": "Alice", "age": 30, "skills": ["Python", "AI"]}'
    data = OutputParser.json_from_text(text)
    print(f"Parsed JSON: {json.dumps(data, indent=2)}")

    # List extraction
    text = """Here are the steps:
    - Install dependencies
    - Configure database
    - Run migrations
    - Start server"""
    items = OutputParser.list_from_text(text)
    print(f"Parsed list: {items}")

    # Key-value pairs
    text = """Name: John Doe
    Role: AI Engineer
    Experience: 5 years"""
    pairs = OutputParser.key_value_pairs(text)
    print(f"Parsed KV: {pairs}\n")


def demo_prompt_testing():
    """Demo: Prompt testing framework."""
    print("=" * 60)
    print("DEMO 8: Prompt Testing")
    print("=" * 60)

    tester = PromptTester()

    # Define test cases
    tests = [
        PromptTest(
            input_text="The movie was fantastic with great acting.",
            expected_behavior="Should return 'positive' sentiment",
            validation_fn=lambda x: "positive" in x.lower(),
            tags=["sentiment", "positive"],
        ),
        PromptTest(
            input_text="I waited 2 hours and the food was cold.",
            expected_behavior="Should return 'negative' sentiment",
            validation_fn=lambda x: "negative" in x.lower(),
            tags=["sentiment", "negative"],
        ),
        PromptTest(
            input_text="The weather is okay today.",
            expected_behavior="Should return 'neutral' sentiment",
            validation_fn=lambda x: "neutral" in x.lower(),
            tags=["sentiment", "neutral"],
        ),
    ]

    # Run tests against a prompt
    results = tester.test(
        prompt_fn=FewShot.sentiment_analysis,
        tests=tests,
    )

    summary = tester.summary()
    print(f"\nSummary: {json.dumps(summary, indent=2)}")


# ---------------------------------------------------------------------------
# 11. Main Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Prompt Engineering Exercises")
    print("=" * 60)
    print()

    # Uncomment demos you want to run (requires API keys)
    # demo_zero_shot()
    # demo_few_shot()
    # demo_chain_of_thought()
    # demo_tree_of_thought()
    # demo_self_consistency()
    # demo_templates()
    # demo_output_parsing()
    # demo_prompt_testing()

    # Show template examples (no API key needed)
    demo_templates()
    demo_output_parsing()

    print("\nDone! Uncomment demos above to run with your API keys.")
