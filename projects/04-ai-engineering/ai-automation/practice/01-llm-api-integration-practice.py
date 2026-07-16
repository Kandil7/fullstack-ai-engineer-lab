"""
Practice Problems — Module 01: LLM API Integration (NO SOLUTIONS)
==================================================================
Solve these yourself! No hints, no solutions.

Run: python 01-llm-api-integration-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai anthropic groq python-dotenv
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Generator


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Basic OpenAI Chat
# Write a function that sends a simple prompt to OpenAI's gpt-4o-mini
# and returns the response text. Use the openai library.
# Handle the case where OPENAI_API_KEY is not set.
def problem_01():
    pass  # Write your code here


# Problem 2: Multi-Message Conversation
# Write a function that takes a list of messages (each with "role" and "content")
# and sends them to OpenAI as a conversation. Return the assistant's reply.
# Example input: [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]
def problem_02():
    pass  # Write your code here


# Problem 3: Response Metadata Extractor
# Write a function that calls an LLM and returns a dict containing:
# - "text": the response content
# - "tokens_used": total tokens (prompt + completion)
# - "model": the model name used
# - "finish_reason": why the model stopped
def problem_03():
    pass  # Write your code here


# Problem 4: System Prompt Sender
# Write a function that sends a user prompt with a custom system prompt
# to OpenAI. The system prompt should set the assistant's behavior
# (e.g., "You are a pirate"). Return the response text.
def problem_04():
    pass  # Write your code here


# Problem 5: Temperature Comparison
# Write a function that sends the SAME prompt to an LLM with three
# different temperatures (0.0, 0.7, 1.5) and returns a dict mapping
# each temperature to its response text. This demonstrates deterministic
# vs creative outputs.
def problem_05():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Streaming Response
# Write a generator function that streams an OpenAI response token-by-token.
# Yield each token as it arrives. The caller should be able to do:
#   for token in stream_response("Tell me a story"):
#       print(token, end="")
def problem_06():
    pass  # Write your code here


# Problem 7: Retry with Exponential Backoff
# Write a function that calls an LLM with retry logic.
# If the API call fails (any exception), wait 1s, then 2s, then 4s,
# up to a maximum of 3 retries. If all retries fail, raise the last error.
# Return the successful response text.
def problem_07():
    pass  # Write your code here


# Problem 8: Token Cost Calculator
# Write a function that takes a model name and a response object
# (from openai) and calculates the exact cost in dollars.
# Use these prices per 1K tokens:
#   gpt-4o:       input=$0.0025, output=$0.01
#   gpt-4o-mini:  input=$0.00015, output=$0.0006
#   claude-sonnet-4-20250514: input=$0.003, output=$0.015
# Return {"input_cost": float, "output_cost": float, "total_cost": float}
def problem_08():
    pass  # Write your code here


# Problem 9: Multi-Provider Router
# Write a function that takes a prompt and a provider name ("openai", "anthropic",
# "groq") and routes the request to the correct API. Each provider has a different
# client library and message format. Return the response text.
# Handle the case where the provider is unknown.
def problem_09():
    pass  # Write your code here


# Problem 10: Response Validator
# Write a function that calls an LLM and validates the response against
# a schema. The schema is a dict like {"type": "object", "properties": {...}}.
# If the response is valid JSON matching the schema, return it parsed.
# If not, retry up to 2 times with a "Please respond in valid JSON" follow-up.
# If still invalid, return None.
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Function Calling Pipeline
# Write a complete function-calling pipeline:
# 1. Define 3 tools (calculator, weather, web_search) with schemas
# 2. Send a prompt that requires tool use
# 3. Parse the tool call from the response
# 4. Execute the tool (mock the actual functions)
# 5. Send the tool result back to the LLM
# 6. Return the final answer
# This is the core pattern behind all AI agents.
def problem_11():
    pass  # Write your code here


# Problem 12: Async Batch Processor
# Write an async function that processes a list of 100 prompts concurrently
# using asyncio.gather, with a semaphore limiting to 10 concurrent requests.
# Each request calls the OpenAI API. Return a list of responses in the same
# order as the input prompts. Track total tokens used across all requests.
async def problem_12():
    pass  # Write your code here


# Problem 13: Fallback Chain
# Write a function that tries multiple LLM providers in order:
#   1. Try OpenAI gpt-4o
#   2. If that fails, try Claude claude-sonnet-4-20250514
#   3. If that fails, try Groq llama-3.3-70b-versatile
#   4. If all fail, raise an exception with all error messages
# Each provider has a different client library and message format.
# Return the response text and which provider succeeded.
def problem_13():
    pass  # Write your code here


# Problem 14: LLM Client Class
# Build a complete LLMClient class that:
# - Supports OpenAI, Anthropic, and Groq
# - Tracks usage (tokens, cost) across all calls
# - Has sync and async methods
# - Supports streaming
# - Has configurable retry with exponential backoff
# - Can export usage stats to a JSON file
# - Has a context manager (__enter__/__exit__) for cleanup
class LLMClient:
    def __init__(self, default_provider: str = "openai"):
        pass  # Write your code here

    def chat(self, prompt: str, **kwargs) -> str:
        pass  # Write your code here

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        pass  # Write your code here

    async def achat(self, prompt: str, **kwargs) -> str:
        pass  # Write your code here

    def get_usage(self) -> dict:
        pass  # Write your code here

    def export_usage(self, path: str):
        pass  # Write your code here

    def __enter__(self):
        pass  # Write your code here

    def __exit__(self, *args):
        pass  # Write your code here


# Problem 15: Cost-Aware LLM Router
# Build a smart router that:
# - Takes a prompt and a budget (max cost in dollars)
# - Classifies the task complexity (simple/medium/complex)
# - Routes simple tasks to cheapest model (gpt-4o-mini)
# - Routes medium tasks to mid-tier (claude-haiku-4-20250514)
# - Routes complex tasks to best model (gpt-4o)
# - Tracks cumulative cost and rejects if budget exceeded
# - Returns the response AND the cost of this call
# - Has a method to get total spend vs budget remaining
def problem_15():
    pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 01: LLM API Integration — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("Basic OpenAI Chat", "Easy", 20),
        2: ("Multi-Message Conversation", "Easy", 20),
        3: ("Response Metadata Extractor", "Easy", 20),
        4: ("System Prompt Sender", "Easy", 20),
        5: ("Temperature Comparison", "Easy", 20),
        6: ("Streaming Response", "Medium", 50),
        7: ("Retry with Exponential Backoff", "Medium", 50),
        8: ("Token Cost Calculator", "Medium", 50),
        9: ("Multi-Provider Router", "Medium", 50),
        10: ("Response Validator", "Medium", 50),
        11: ("Function Calling Pipeline", "Hard", 100),
        12: ("Async Batch Processor", "Hard", 100),
        13: ("Fallback Chain", "Hard", 100),
        14: ("LLM Client Class", "Hard", 100),
        15: ("Cost-Aware LLM Router", "Hard", 100),
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
