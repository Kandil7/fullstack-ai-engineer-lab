"""
W3Schools Python Tutorial - 29: Python RegEx
=============================================
Topics: re module, pattern matching, findall, search, split, sub

Run: python 29-regex.py
Reference: https://www.w3schools.com/python/python_regex.asp
"""

# ============================================================
# What is RegEx?
# ============================================================
# RegEx (Regular Expressions) are sequences of characters that
# define search patterns. Python's re module provides regex support.

import re

# ============================================================
# The findall() Function
# ============================================================
# Example 1: Find all matches
print("--- findall() ---")

text = "The rain in Spain stays mainly in the plain"

# Find all lowercase 'i'
matches = re.findall("ain", text)
print(f"'ain' found: {matches}")
print(f"Count: {len(matches)}")

# Find all words starting with 's' or 'S'
matches = re.findall(r"\bS\w+", text)
print(f"Words starting with S: {matches}")

# Find all digits
text2 = "I have 2 cats and 3 dogs"
numbers = re.findall(r"\d+", text2)
print(f"Numbers: {numbers}")

# Output:
# 'ain' found: ['ain', 'ain', 'ain', 'ain']
# Count: 4
# Words starting with S: ['Spain', 'stays']
# Numbers: ['2', '3']

# ============================================================
# The search() Function
# ============================================================
# Example 2: Find first match
print("\n--- search() ---")

text = "The rain in Spain"

# Search for pattern
match = re.search("Spain", text)
if match:
    print(f"Found: '{match.group()}' at position {match.start()}-{match.end()}")

# Search with pattern
match = re.search(r"\b\w{5}\b", text)  # 5-letter word
if match:
    print(f"First 5-letter word: '{match.group()}'")

# Output:
# Found: 'Spain' at position 14-19
# First 5-letter word: 'rain'

# ============================================================
# The split() Function
# ============================================================
# Example 3: Split string by pattern
print("\n--- split() ---")

text = "one1two2three3four4"

# Split by digits
parts = re.split(r"\d+", text)
print(f"Split by digits: {parts}")

# Split by multiple delimiters
text2 = "apple;banana,cherry orange"
parts = re.split(r"[;, ]+", text2)
print(f"Split by ;,comma,space: {parts}")

# Output:
# Split by digits: ['one', 'two', 'three', 'four', '']
# Split by ;,comma,space: ['apple', 'banana', 'cherry', 'orange']

# ============================================================
# The sub() Function
# ============================================================
# Example 4: Replace matches
print("\n--- sub() ---")

text = "The rain in Spain stays mainly in the plain"

# Replace 'ain' with 'AIN'
result = re.sub("ain", "AIN", text)
print(f"Replace 'ain': {result}")

# Replace with function
def double_match(match):
    return match.group().upper() * 2

result = re.sub(r"\b\w{4}\b", double_match, text)
print(f"Double uppercase 4-letter words: {result}")

# Replace digits
text2 = "My phone is 123-456-7890"
result = re.sub(r"\d", "*", text2)
print(f"Mask digits: {result}")

# Output:
# Replace 'ain': The rAIN in SpAIN stAIns mAINly in the plAIN
# Mask digits: My phone is ***-***-****

# ============================================================
# Common RegEx Patterns
# ============================================================
# Example 5: Useful patterns
print("\n--- Common Patterns ---")

text = "Email: test@example.com, Phone: (555) 123-4567, Date: 2024-01-15"

# Email pattern
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print(f"Emails: {emails}")

# Phone pattern (simple)
phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
print(f"Phones: {phones}")

# Date pattern
dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
print(f"Dates: {dates}")

# Output:
# Emails: ['test@example.com']
# Phones: ['(555) 123-4567']
# Dates: ['2024-01-15']

# ============================================================
# RegEx Special Characters
# ============================================================
# Example 6: Special character patterns
print("\n--- Special Characters ---")

text = "The price is $19.99 and tax is 8.5%"

# \d - digit
digits = re.findall(r"\d+", text)
print(f"Digits: {digits}")

# \w - word character (letter, digit, underscore)
words = re.findall(r"\w+", text)
print(f"Words: {words}")

# \s - whitespace
parts = re.split(r"\s+", text)
print(f"Split by whitespace: {parts}")

# . - any character except newline
matches = re.findall(r"i.", text)
print(f"'i' followed by any char: {matches}")

# ^ - start of string
starts_with_the = re.findall(r"^The", text)
print(f"Starts with 'The': {starts_with_the}")

# $ - end of string
ends_with_99 = re.findall(r"99$", text)
print(f"Ends with '99': {ends_with_99}")

# ============================================================
# Quantifiers
# ============================================================
# Example 7: Quantifiers
print("\n--- Quantifiers ---")

text = "aa aab aaa aaaa aaaaa"

# * - zero or more
matches = re.findall(r"a*", text)
print(f"'a*' (zero or more): {matches}")

# + - one or more
matches = re.findall(r"a+", text)
print(f"'a+' (one or more): {matches}")

# ? - zero or one
matches = re.findall(r"a?", text)
print(f"'a?' (zero or one): {matches}")

# {n} - exactly n times
matches = re.findall(r"a{3}", text)
print(f"'a{{3}}' (exactly 3): {matches}")

# {n,m} - n to m times
matches = re.findall(r"a{2,4}", text)
print(f"'a{{2,4}}' (2 to 4): {matches}")

# ============================================================
# Groups and Capturing
# ============================================================
# Example 8: Groups
print("\n--- Groups ---")

text = "2024-01-15 14:30:45"

# Capture groups
match = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
if match:
    print(f"Full match: {match.group(0)}")
    print(f"Year: {match.group(1)}")
    print(f"Month: {match.group(2)}")
    print(f"Day: {match.group(3)}")
    print(f"All groups: {match.groups()}")

# Named groups
match = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
if match:
    print(f"\nNamed groups:")
    print(f"  Year: {match.group('year')}")
    print(f"  Month: {match.group('month')}")
    print(f"  Day: {match.group('day')}")

# Output:
# Full match: 2024-01-15
# Year: 2024
# Month: 01
# Day: 15
# All groups: ('2024', '01', '15')

# ============================================================
# Flags
# ============================================================
# Example 9: Using flags
print("\n--- Flags ---")

text = "Hello HELLO hello"

# re.IGNORECASE (re.I) - case insensitive
matches = re.findall(r"hello", text, re.IGNORECASE)
print(f"Case insensitive: {matches}")

# re.MULTILINE (re.M) - ^ and $ match each line
text2 = "line1\nline2\nline3"
matches = re.findall(r"^line\d$", text2, re.MULTILINE)
print(f"Multiline: {matches}")

# re.DOTALL (re.S) - . matches newline too
text3 = "line1\nline2"
matches = re.findall(r"line.", text3, re.DOTALL)
print(f"Dotall: {matches}")

# Output:
# Case insensitive: ['Hello', 'HELLO', 'hello']
# Multiline: ['line1', 'line2', 'line3']
# Dotall: ['line1\n', 'line2']

# ============================================================
# Practical Examples
# ============================================================
# Example 10: Real-world regex usage
print("\n--- Practical Examples ---")

# Validate email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

emails = ["test@example.com", "invalid@", "@invalid.com", "valid.email+tag@domain.co"]
for email in emails:
    print(f"  {email}: {'OK' if is_valid_email(email) else 'INVALID'}")

# Extract URLs
text = "Visit https://www.example.com or http://test.org/path?q=1"
urls = re.findall(r"https?://\S+", text)
print(f"\nURLs: {urls}")

# Clean text
dirty_text = "  Hello   World!!!  This   is   messy  "
clean = re.sub(r"\s+", " ", dirty_text).strip()
print(f"\nCleaned: '{clean}'")

# Find hashtags
text = "Check out #python and #regex for more info #coding"
hashtags = re.findall(r"#\w+", text)
print(f"Hashtags: {hashtags}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. re.findall(): find all matches")
print("2. re.search(): find first match")
print("3. re.split(): split by pattern")
print("4. re.sub(): replace matches")
print("5. Patterns: \\d (digit), \\w (word), \\s (whitespace)")
print("6. Quantifiers: * (0+), + (1+), ? (0/1), {n} (exact)")
print("7. Groups: () capture, (?P<name>...) named")
print("8. Flags: re.IGNORECASE, re.MULTILINE, re.DOTALL")
