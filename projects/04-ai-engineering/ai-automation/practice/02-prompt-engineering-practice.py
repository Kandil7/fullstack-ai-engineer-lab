"""
Practice Problems — Module 02: Prompt Engineering (NO SOLUTIONS)
================================================================
Solve these yourself! No hints, no solutions.

Run: python 02-prompt-engineering-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai python-dotenv pydantic
"""


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Zero-Shot Classifier
# Write a function that takes a text and a list of labels, and uses
# zero-shot prompting to classify the text into one of the labels.
# Return the chosen label.
# Example: classify("The stock market crashed today", ["finance", "sports", "politics"])
#   → "finance"
def problem_01():
    pass  # Write your code here


# Problem 2: Few-Shot Sentiment Analyzer
# Write a function that uses few-shot prompting (3 examples) to analyze
# sentiment of a review. Return "positive", "negative", or "neutral".
# Include the examples directly in the prompt.
def problem_02():
    pass  # Write your code here


# Problem 3: Structured Data Extractor
# Write a function that takes a paragraph of text and extracts a person's
# information into a dict with keys: name, age, occupation, location.
# Use zero-shot prompting with a clear output format instruction.
# Return the dict (parsed from JSON).
def problem_03():
    pass  # Write your code here


# Problem 4: Summarizer with Constraints
# Write a function that summarizes text in exactly 3 bullet points.
# Each bullet must start with "- " and be under 20 words.
# Use explicit constraints in the prompt.
def problem_04():
    pass  # Write your code here


# Problem 5: Translation Prompt
# Write a function that translates text to a target language.
# The prompt should specify: "Translate the following text to {language}.
# Output ONLY the translation, nothing else."
# Return the translated text.
def problem_05():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Chain-of-Thought Solver
# Write a function that solves a math word problem using chain-of-thought.
# The prompt should instruct the model to "think step by step" and
# show its reasoning before giving the final answer.
# Extract and return both the reasoning steps and the final answer.
def problem_06():
    pass  # Write your code here


# Problem 7: Prompt Template System
# Build a PromptTemplate class that:
# - Takes a template string with {variables}
# - Has a fill(**kwargs) method that substitutes variables
# - Validates that all required variables are provided
# - Raises ValueError if a required variable is missing
# Example: PromptTemplate("Summarize {topic} in {style} style").fill(topic="AI", style="formal")
def problem_07():
    pass  # Write your code here


# Problem 8: JSON Output Parser
# Write a function that calls an LLM and parses the response as JSON.
# The prompt should instruct the model to respond with valid JSON only.
# Handle cases where:
# - The response contains markdown code fences (```json...```)
# - The JSON is malformed (retry once with "Please fix the JSON")
# - A required field is missing (return None)
# Return the parsed dict or None.
def problem_08():
    pass  # Write your code here


# Problem 9: Self-Consistency Evaluator
# Write a function that asks the same question N times (with temperature > 0)
# and takes the majority answer. This implements the self-consistency technique.
# Example: solve("What is 2+2?", n=5) → if 4/5 say "4", return "4"
def problem_09():
    pass  # Write your code here


# Problem 10: Prompt Regression Tester
# Write a function that tests a prompt against a test suite.
# Input: a prompt template and a list of test cases, each with:
#   {"input": str, "expected_contains": str, "should_not_contain": str}
# Run each test case through the LLM and check if the response
# contains expected text and does NOT contain forbidden text.
# Return a report dict with pass/fail for each test.
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Prompt Chain Executor
# Build a PromptChain class that:
# - Takes a list of PromptStep objects (each with a template and parser)
# - Executes them sequentially, passing output of step N as input to step N+1
# - Each step can have a "condition" function that determines if it should run
# - Tracks the full execution trace (input/output per step)
# - Returns the final output and the trace
class PromptChain:
    def __init__(self):
        pass  # Write your code here

    def add_step(self, name, template, parser=None, condition=None):
        pass  # Write your code here

    def run(self, initial_input: str) -> dict:
        pass  # Write your code here


# Problem 12: Prompt Optimizer
# Write a function that optimizes a prompt by:
# 1. Taking a base prompt and a quality metric function
# 2. Generating 5 variations (add examples, rephrase, add constraints)
# 3. Testing each variation against the metric
# 4. Returning the best-performing prompt and its score
# This is automatic prompt engineering (APE).
def problem_12():
    pass  # Write your code here


# Problem 13: Multi-Role Debate
# Write a function that simulates a debate between 3 LLM "roles":
# - Optimist: argues the positive side
# - Pessimist: argues the negative side
# - Judge: summarizes both sides and gives a balanced conclusion
# Each role gets the previous roles' responses as context.
# Return all three responses.
def problem_13():
    pass  # Write your code here


# Problem 14: Token-Budget-Aware Prompter
# Write a function that:
# 1. Takes a prompt, context documents, and a max token budget
# 2. Estimates token count of prompt + context
# 3. Truncates context to fit within budget (keeping most relevant parts)
# 4. Sends the budget-aware prompt to the LLM
# 5. Returns the response and how many tokens were used from the budget
# Use a simple tokenizer estimation (1 token ≈ 4 chars for English).
def problem_14():
    pass  # Write your code here


# Problem 15: Prompt Security Auditor
# Write a function that audits a prompt for security issues:
# 1. Detects prompt injection attempts (instructions overriding system prompt)
# 2. Detects jailbreak patterns (DAN, role-play bypasses)
# 3. Detects data exfiltration attempts (asking for system prompt, API keys)
# 4. Detects excessive token usage (potential DoS)
# Return a security report with findings and risk level (low/medium/high/critical).
def problem_15():
    pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 02: Prompt Engineering — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("Zero-Shot Classifier", "Easy", 20),
        2: ("Few-Shot Sentiment Analyzer", "Easy", 20),
        3: ("Structured Data Extractor", "Easy", 20),
        4: ("Summarizer with Constraints", "Easy", 20),
        5: ("Translation Prompt", "Easy", 20),
        6: ("Chain-of-Thought Solver", "Medium", 50),
        7: ("Prompt Template System", "Medium", 50),
        8: ("JSON Output Parser", "Medium", 50),
        9: ("Self-Consistency Evaluator", "Medium", 50),
        10: ("Prompt Regression Tester", "Medium", 50),
        11: ("Prompt Chain Executor", "Hard", 100),
        12: ("Prompt Optimizer", "Hard", 100),
        13: ("Multi-Role Debate", "Hard", 100),
        14: ("Token-Budget-Aware Prompter", "Hard", 100),
        15: ("Prompt Security Auditor", "Hard", 100),
    }

    total_xp = sum(p[2] for p in problems.values())
    print(f"Total Problems: {len(problems)}")
    print(f"Total XP: {total_xp}")
    print()

    for num, (name, diff, xp) in problems.items():
        print(f"  [{num:2d}] {name:<40} {diff:<8} +{xp} XP")

    print()
    print("Select a problem number to see its full description.")
    print("Solve each function by replacing 'pass' with your implementation.")
    print("No solutions are provided — figure it out yourself!")
    print("=" * 60)
