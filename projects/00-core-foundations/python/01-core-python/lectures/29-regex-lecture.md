# Regular Expressions (Regex) in Python

## Topic 29: Mastering Pattern Matching with Regex

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what regular expressions are and why they matter
2. Use the `re` module to search, match, and manipulate strings
3. Write regex patterns using metacharacters, quantifiers, and character classes
4. Capture and extract data using groups
5. Compile patterns for better performance
6. Apply regex in real-world scenarios like validation and parsing

---

## 1. What Are Regular Expressions?

Regular expressions (regex) are sequences of characters that define **search patterns**. They provide a powerful way to find, match, and replace text within strings.

### Why Use Regex?

- **Pattern Matching**: Find specific patterns in text
- **Text Validation**: Check if input matches a required format
- **Data Extraction**: Pull out specific parts from strings
- **Text Transformation**: Replace or modify text based on patterns
- **Search & Replace**: Complex find-and-replace operations

### Real-World Applications

```python
# Validate email addresses
# Extract phone numbers from text
# Parse log files
# Scrape data from web pages
# Validate form inputs
```

---

## 2. The `re` Module

Python provides the built-in `re` module for working with regular expressions.

### Basic Import

```python
import re

# All regex functions are accessed through the re module
text = "Hello, World!"
pattern = r"World"

# Check if pattern exists in text
match = re.search(pattern, text)
if match:
    print(f"Found: {match.group()}")  # Output: Found: World
```

### Raw Strings (r-strings)

Always use raw strings (`r""`) for regex patterns:

```python
# Without raw string - backslashes need escaping
pattern1 = "\\d+"    # Matches digits

# With raw string - backslashes are literal
pattern2 = r"\d+"    # Same pattern, cleaner syntax

# Both work the same way
print(re.findall(pattern1, "abc123def"))  # ['123']
print(re.findall(pattern2, "abc123def"))  # ['123']
```

---

## 3. Core Regex Functions

### `re.search()` - Search Anywhere

Finds the **first** occurrence of the pattern anywhere in the string.

```python
import re

text = "The price is 42 dollars"

# Search for digits
match = re.search(r'\d+', text)

if match:
    print(f"Found: {match.group()}")    # Found: 42
    print(f"Position: {match.start()}")  # Position: 14
    print(f"End: {match.end()}")         # End: 16
```

### `re.match()` - Match at Start

Matches only at the **beginning** of the string.

```python
import re

text = "Hello, World!"

# This will match
match = re.match(r'Hello', text)
print(match.group())  # Hello

# This will NOT match (pattern not at start)
match = re.match(r'World', text)
print(match)  # None
```

### `re.findall()` - Find All Matches

Returns a **list** of all non-overlapping matches.

```python
import re

text = "2 apples, 3 oranges, 5 bananas"

# Find all numbers
numbers = re.findall(r'\d+', text)
print(numbers)  # ['2', '3', '5']

# Find all words
words = re.findall(r'[a-z]+', text.lower())
print(words)  # ['apples', 'oranges', 'bananas']
```

### `re.finditer()` - Iterator of Matches

Returns an **iterator** yielding match objects.

```python
import re

text = "2 apples, 3 oranges, 5 bananas"

for match in re.finditer(r'\d+', text):
    print(f"Number {match.group()} at position {match.start()}")
# Number 2 at position 0
# Number 3 at position 9
# Number 5 at position 19
```

### `re.sub()` - Substitute Matches

Replaces occurrences of the pattern with a replacement string.

```python
import re

text = "Call me at 555-123-4567 or 555-987-6543"

# Replace phone numbers with a placeholder
redacted = re.sub(r'\d{3}-\d{3}-\d{4}', '[PHONE]', text)
print(redacted)  # Call me at [PHONE] or [PHONE]

# Using a function for dynamic replacement
def double_number(match):
    return str(int(match.group()) * 2)

result = re.sub(r'\d+', double_number, "a1 b2 c3")
print(result)  # a2 b4 c6
```

### `re.split()` - Split by Pattern

Splits the string at regex matches.

```python
import re

text = "apple; orange, banana  cherry"

# Split by semicolon, comma, or multiple spaces
parts = re.split(r'[;,]\s*|\s{2,}', text)
print(parts)  # ['apple', 'orange', 'banana', 'cherry']
```

---

## 4. Metacharacters

Metacharacters have special meaning in regex patterns.

### Common Metacharacters

| Character | Description | Example |
|-----------|-------------|---------|
| `.` | Any character (except newline) | `h.t` matches "hat", "hot", "hit" |
| `^` | Start of string | `^Hello` matches "Hello..." |
| `$` | End of string | `world$` matches "...world" |
| `*` | Zero or more | `ab*c` matches "ac", "abc", "abbc" |
| `+` | One or more | `ab+c` matches "abc", "abbc" (not "ac") |
| `?` | Zero or one (optional) | `colou?r` matches "color", "colour" |
| `\|` | OR (alternation) | `cat\|dog` matches "cat" or "dog" |
| `()` | Group | `(ab)+` matches "ab", "abab" |
| `[]` | Character class | `[aeiou]` matches any vowel |
| `{}` | Quantifier | `a{3}` matches exactly "aaa" |
| `\` | Escape special char | `\.` matches literal "." |

### Examples

```python
import re

# . (any character)
print(re.findall(r'h.t', 'hat hot hit hut'))  # ['hat', 'hot', 'hit', 'hut']

# ^ (start of string)
print(re.findall(r'^\w+', 'Hello World'))  # ['Hello']

# $ (end of string)
print(re.findall(r'\w+$', 'Hello World'))  # ['World']

# * (zero or more)
print(re.findall(r'go*d', 'gd god good goood'))  # ['gd', 'god', 'good', 'goood']

# + (one or more)
print(re.findall(r'go+d', 'gd god good goood'))  # ['god', 'good', 'goood']

# ? (zero or one)
print(re.findall(r'colou?r', 'color colour'))  # ['color', 'colour']

# | (alternation)
print(re.findall(r'cat|dog', 'I have a cat and a dog'))  # ['cat', 'dog']
```

---

## 5. Character Classes

Character classes match specific types of characters.

### Built-in Character Classes

| Class | Description | Equivalent |
|-------|-------------|------------|
| `\d` | Any digit | `[0-9]` |
| `\D` | Any non-digit | `[^0-9]` |
| `\w` | Word character | `[a-zA-Z0-9_]` |
| `\W` | Non-word character | `[^a-zA-Z0-9_]` |
| `\s` | Whitespace | `[ \t\n\r\f\v]` |
| `\S` | Non-whitespace | `[^ \t\n\r\f\v]` |

### Examples

```python
import re

text = "Phone: (555) 123-4567, Email: test@example.com"

# Find digits
print(re.findall(r'\d+', text))  # ['555', '123', '4567']

# Find word characters
print(re.findall(r'\w+', text))  # ['Phone', '555', '123', '4567', 'Email', 'test', 'example', 'com']

# Find non-word characters (special chars)
print(re.findall(r'\W+', text))  # [': ', '() ', '-', ', ', ': ', '@', '.']

# Find whitespace
print(re.findall(r'\s+', text))  # [' ', ' ', ' ', ' ', ' ', ' ', ' ']
```

### Custom Character Classes

```python
import re

# Vowels only
print(re.findall(r'[aeiou]', 'Hello World'))  # ['e', 'o', 'o']

# Range: lowercase letters
print(re.findall(r'[a-z]', 'Hello World'))  # ['e', 'l', 'l', 'o', 'o', 'r', 'l', 'd']

# Range: digits
print(re.findall(r'[0-9]', 'abc123def456'))  # ['1', '2', '3', '4', '5', '6']

# Negated class (not vowels)
print(re.findall(r'[^aeiou]', 'Hello'))  # ['H', 'l', 'l']

# Combined ranges
print(re.findall(r'[a-zA-Z0-9]', 'Hello World 123!'))  # ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd', '1', '2', '3']
```

---

## 6. Quantifiers

Quantifiers specify how many times a character or group can appear.

### Quantifier Types

| Quantifier | Description | Example |
|------------|-------------|---------|
| `{n}` | Exactly n times | `a{3}` = "aaa" |
| `{n,}` | At least n times | `a{2,}` = "aa", "aaa", etc. |
| `{n,m}` | Between n and m times | `a{2,4}` = "aa", "aaa", "aaaa" |
| `*` | Zero or more (same as `{0,}`) | `a*` = "", "a", "aa", etc. |
| `+` | One or more (same as `{1,}`) | `a+` = "a", "aa", etc. |
| `?` | Zero or one (same as `{0,1}`) | `a?` = "", "a" |

### Greedy vs Lazy (Non-Greedy)

```python
import re

text = '<div>Hello</div><div>World</div>'

# Greedy (default) - matches as much as possible
greedy = re.findall(r'<div>.*</div>', text)
print(greedy)  # ['<div>Hello</div><div>World</div>']

# Lazy (non-greedy) - matches as little as possible
lazy = re.findall(r'<div>.*?</div>', text)
print(lazy)  # ['<div>Hello</div>', '<div>World</div>']

# Add ? after quantifier to make it lazy
# *? for lazy zero-or-more
# +? for lazy one-or-more
# ?? for lazy zero-or-one
```

### Examples

```python
import re

# Exactly 3 digits
print(re.findall(r'\d{3}', '12 123 1234 12345'))  # ['123', '234', '234', '345']

# At least 3 digits
print(re.findall(r'\d{3,}', '12 123 1234 12345'))  # ['123', '1234', '12345']

# Between 3 and 5 digits
print(re.findall(r'\d{3,5}', '12 123 1234 12345'))  # ['123', '1234', '12345']

# Email validation pattern
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
emails = re.findall(email_pattern, 'Contact: test@example.com or user@domain.org')
print(emails)  # ['test@example.com', 'user@domain.org']
```

---

## 7. Groups and Capturing

Groups allow you to capture parts of a match.

### Basic Groups

```python
import re

# Simple group
text = "John Smith, Jane Doe"
names = re.findall(r'(\w+) (\w+)', text)
print(names)  # [('John', 'Smith'), ('Jane', 'Doe')]

# Access groups from match object
match = re.search(r'(\w+) (\w+)', text)
if match:
    print(match.group(0))  # Full match: "John Smith"
    print(match.group(1))  # First group: "John"
    print(match.group(2))  # Second group: "Smith"
```

### Named Groups

```python
import re

# Named groups using (?P<name>...)
text = "Date: 2024-01-15"
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', text)

if match:
    print(match.group('year'))   # 2024
    print(match.group('month'))  # 01
    print(match.group('day'))    # 15
```

### Non-Capturing Groups

```python
import re

# (?:...) groups without capturing
text = "http://example.com https://secure.com"
urls = re.findall(r'https?://(?:www\.)?([^/\s]+)', text)
print(urls)  # ['example.com', 'secure.com']

# Without non-capturing group, we'd get extra matches
urls_bad = re.findall(r'https?://(www\.)?([^/\s]+)', text)
print(urls_bad)  # [('www.', 'example.com'), (None, 'secure.com')]
```

### Group References

```python
import re

# Backreference: \1 refers to first group
text = "hello hello world world"
# Find repeated words
repeated = re.findall(r'(\w+)\s+\1', text)
print(repeated)  # ['hello', 'world']

# Using in substitution
text = "John Smith"
result = re.sub(r'(\w+) (\w+)', r'\2, \1', text)
print(result)  # Smith, John
```

---

## 8. Flags (Modifiers)

Flags modify how the regex pattern is interpreted.

### Common Flags

| Flag | Description |
|------|-------------|
| `re.IGNORECASE` (or `re.I`) | Case-insensitive matching |
| `re.MULTILINE` (or `re.M`) | `^` and `$` match line boundaries |
| `re.DOTALL` (or `re.S`) | `.` matches any character including newline |
| `re.VERBOSE` (or `re.X`) | Allow comments and whitespace in pattern |
| `re.ASCII` (or `re.A`) | ASCII-only matching |

### Examples

```python
import re

# IGNORECASE
text = "Hello HELLO hello"
print(re.findall(r'hello', text, re.IGNORECASE))  # ['Hello', 'HELLO', 'hello']

# MULTILINE
text = """First line
Second line
Third line"""
print(re.findall(r'^\w+', text, re.MULTILINE))  # ['First', 'Second', 'Third']

# DOTALL
text = """Line 1
Line 2"""
print(re.findall(r'Line.*?1', text, re.DOTALL))  # ['Line 1']

# VERBOSE (readable patterns)
phone_pattern = re.compile(r"""
    (\d{3})     # Area code
    [-.\s]?     # Optional separator
    (\d{3})     # First 3 digits
    [-.\s]?     # Optional separator
    (\d{4})     # Last 4 digits
""", re.VERBOSE)

match = phone_pattern.search("Call: 555-123-4567")
if match:
    print(match.group())  # 555-123-4567
```

---

## 9. Compiling Patterns

For repeated use, compile patterns for better performance.

```python
import re

# Compile a pattern once
email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Use multiple times
emails = [
    "test@example.com",
    "invalid@",
    "user@domain.org",
    "not-an-email"
]

for email in emails:
    if email_pattern.match(email):
        print(f"Valid: {email}")
    else:
        print(f"Invalid: {email}")

# Output:
# Valid: test@example.com
# Invalid: invalid@
# Valid: user@domain.org
# Invalid: not-an-email
```

### Compiled Pattern Methods

```python
import re

pattern = re.compile(r'\d+')

# Same methods as re module
print(pattern.search("abc123"))  # Match object
print(pattern.findall("a1 b2"))  # ['1', '2']
print(pattern.sub("X", "a1b2"))  # aXbX
```

---

## 10. Common Mistakes to Avoid

### 1. Forgetting Raw Strings

```python
# BAD - double backslash needed
pattern = "\\d+"

# GOOD - raw string
pattern = r"\d+"
```

### 2. Greedy Matching Issues

```python
import re

text = '<b>bold</b> and <i>italic</i>'

# BAD - greedy, misses second tag
print(re.findall(r'<.*>', text))
# ['<b>bold</b> and <i>italic</i>']

# GOOD - lazy matching
print(re.findall(r'<.*?>', text))
# ['<b>', '</b>', '<i>', '</i>']
```

### 3. Not Anchoring When Needed

```python
import re

text = "abc123"

# BAD - matches anywhere
print(re.findall(r'\d', text))  # ['1', '2', '3']

# GOOD - if you want full string match
print(re.fullmatch(r'\w+\d+', text))  # Match object
```

### 4. Overusing Regex

```python
# BAD - regex for simple operations
text = "Hello World"
result = re.sub(r'\s+', '_', text)

# GOOD - string method is simpler
result = text.replace(" ", "_")
```

---

## 11. Best Practices

1. **Use raw strings** (`r""`) for all regex patterns
2. **Compile patterns** that are used multiple times
3. **Use non-capturing groups** `(?:...)` when you don't need the capture
4. **Add comments** with `re.VERBOSE` for complex patterns
5. **Prefer built-in methods** for simple operations
6. **Test patterns thoroughly** with edge cases
7. **Use named groups** for better readability
8. **Be specific** - avoid `.*` when you can match specific characters

---

## 12. Practice Exercises

### Exercise 1: Validate Phone Numbers

```python
import re

def validate_phone(phone):
    """Validate US phone numbers in various formats."""
    pattern = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return bool(re.match(pattern, phone))

# Test cases
print(validate_phone("555-123-4567"))     # True
print(validate_phone("(555) 123-4567"))   # True
print(validate_phone("555.123.4567"))     # True
print(validate_phone("5551234567"))       # True
print(validate_phone("123-45"))           # False
```

### Exercise 2: Extract Data from Text

```python
import re

def extract_log_info(log_line):
    """Extract timestamp and message from log line."""
    pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (.+)'
    match = re.match(pattern, log_line)
    if match:
        return match.group(1), match.group(2)
    return None

# Test
log = "[2024-01-15 10:30:45] Server started successfully"
timestamp, message = extract_log_info(log)
print(f"Time: {timestamp}")    # Time: 2024-01-15 10:30:45
print(f"Message: {message}")   # Message: Server started successfully
```

### Exercise 3: Find and Replace

```python
import re

def mask_sensitive(text):
    """Mask credit card numbers and SSNs."""
    # Mask credit cards (16 digits)
    text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 
                  '****-****-****-****', text)
    
    # Mask SSNs (9 digits with dashes)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 
                  '***-**-****', text)
    
    return text

# Test
sensitive = "Card: 4111-1111-1111-1111, SSN: 123-45-6789"
print(mask_sensitive(sensitive))
# Card: ****-****-****-****, SSN: ***-**-****
```

---

## 13. Summary

| Concept | Key Points |
|---------|------------|
| **Core Functions** | `search()`, `match()`, `findall()`, `sub()`, `split()` |
| **Metacharacters** | `.`, `^`, `$`, `*`, `+`, `?`, `\|`, `()` |
| **Character Classes** | `\d`, `\w`, `\s` and their uppercase negations |
| **Quantifiers** | `{n}`, `{n,}`, `{n,m}`, `*`, `+`, `?` |
| **Groups** | Basic `()`, named `(?P<name>...)`, non-capturing `(?:...)` |
| **Flags** | `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE` |
| **Compilation** | Use `re.compile()` for patterns used multiple times |

---

## Next Steps

- Practice regex patterns at [regex101.com](https://regex101.com/)
- Learn about more advanced patterns like lookaheads and lookbehinds
- Explore regex in other languages for comparison
