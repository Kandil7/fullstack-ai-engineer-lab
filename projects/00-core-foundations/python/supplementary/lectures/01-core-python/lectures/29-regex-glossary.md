# Regular Expressions (Regex) Glossary

## Topic 29: Quick Reference Guide

---

## Glossary Terms

### A

#### Alternation
**Definition:** The `|` operator matches either the expression before or after it.
```python
import re
# Matches "cat" OR "dog"
re.findall(r'cat|dog', 'I have a cat and a dog')  # ['cat', 'dog']
```
**Related:** OR operator, grouping

#### Anchors
**Definition:** Characters that match positions rather than characters in the string.
```python
import re
# ^ matches start, $ matches end
re.findall(r'^Hello', 'Hello World')  # ['Hello']
re.findall(r'World$', 'Hello World')  # ['World']
```
**Related:** `^`, `$`, word boundary

---

### B

#### Backreference
**Definition:** A reference to a previously captured group using `\1`, `\2`, etc.
```python
import re
# Find repeated words
re.findall(r'(\w+)\s+\1', 'the the quick brown fox fox')  # ['the', 'fox']
```
**Related:** Groups, capturing, capture groups

#### Boundary
**Definition:** Position between words (letters, digits, underscore) and non-word characters.
```python
import re
# \b matches word boundary
re.findall(r'\bcat\b', 'the cat sat')  # ['cat']
re.findall(r'\bcat\b', 'concatenate')  # [] (no match - inside word)
```
**Related:** `\b`, `\B`, word boundary

---

### C

#### Capturing Group
**Definition:** A group enclosed in `()` that captures the matched text.
```python
import re
match = re.search(r'(\d+)-(\w+)', '123-abc')
print(match.group(1))  # 123
print(match.group(2))  # abc
```
**Related:** Groups, backreference, named groups

#### Character Class
**Definition:** A set of characters enclosed in `[]` that matches any one character in the set.
```python
import re
# Match any vowel
re.findall(r'[aeiou]', 'Hello World')  # ['e', 'o', 'o']

# Match any digit
re.findall(r'[0-9]', 'abc123')  # ['1', '2', '3']
```
**Related:** Ranges, negated classes, `\d`, `\w`, `\s`

---

### D

#### DOTALL Flag (`re.S`)
**Definition:** Makes `.` match any character including newline.
```python
import re
text = "Line 1\nLine 2"
re.findall(r'Line.1', text)  # [] (without flag)
re.findall(r'Line.1', text, re.DOTALL)  # ['Line 1']
```
**Related:** Flags, `re.S`, metacharacters

---

### F

#### Findall
**Definition:** Returns all non-overlapping matches as a list of strings or tuples.
```python
import re
re.findall(r'\d+', 'a1 b2 c3')  # ['1', '2', '3']

# With groups, returns list of tuples
re.findall(r'(\d+)-(\w+)', '1-a 2-b')  # [('1', 'a'), ('2', 'b')]
```
**Related:** `search()`, `match()`, `finditer()`

#### Flags (Modifiers)
**Definition:** Optional parameters that modify regex behavior.
```python
import re
# re.IGNORECASE - case insensitive
re.findall(r'hello', 'Hello HELLO', re.IGNORECASE)  # ['Hello', 'HELLO']

# re.MULTILINE - ^ and $ match line boundaries
# re.DOTALL - . matches newlines
# re.VERBOSE - allows comments in patterns
# re.ASCII - ASCII-only matching
```
**Related:** `re.I`, `re.M`, `re.S`, `re.X`

---

### G

#### Greedy Quantifier
**Definition:** Matches as many characters as possible (default behavior).
```python
import re
text = '<div>content</div>'
re.findall(r'<.*>', text)  # ['<div>content</div>'] (greedy)
```
**Related:** Lazy quantifier, quantifiers, `*`, `+`

---

### I

#### IGNORECASE Flag (`re.I`)
**Definition:** Makes matching case-insensitive.
```python
import re
re.findall(r'python', 'Python PYTHON', re.IGNORECASE)  # ['Python', 'PYTHON']
```
**Related:** Flags, case sensitivity

---

### L

#### Lazy Quantifier
**Definition:** Matches as few characters as possible (add `?` after quantifier).
```python
import re
text = '<div>content</div>'
re.findall(r'<.*?>', text)  # ['<div>', '</div>'] (lazy)
```
**Related:** Greedy quantifier, `*?`, `+?`, `??`

---

### M

#### Match Object
**Definition:** Object returned by `search()` or `match()` containing match details.
```python
import re
match = re.search(r'(\d+)', 'abc123def')
if match:
    print(match.group())   # 123 (full match)
    print(match.group(0))  # 123 (same as above)
    print(match.start())   # 3 (start index)
    print(match.end())     # 6 (end index)
    print(match.span())    # (3, 6)
```
**Related:** `group()`, `start()`, `end()`, `span()`

#### Metacharacters
**Definition:** Characters with special meaning in regex patterns.
```python
# . * + ? ^ $ ( ) [ ] { } | \
# Each has a special purpose
import re
re.findall(r'.', 'abc')  # ['a', 'b', 'c']
re.findall(r'\.', 'a.b')  # ['.']
```
**Related:** Escape, special characters, patterns

#### MULTILINE Flag (`re.M`)
**Definition:** Makes `^` and `$` match at line boundaries instead of string boundaries.
```python
import re
text = "Line 1\nLine 2"
re.findall(r'^\w+', text, re.MULTILINE)  # ['Line', 'Line']
```
**Related:** Flags, anchors, `re.M`

---

### N

#### Named Group
**Definition:** A capturing group with a name using `(?P<name>...)`.
```python
import re
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})', '2024-01')
print(match.group('year'))   # 2024
print(match.group('month'))  # 01
```
**Related:** Groups, capturing, `groupdict()`

---

### P

#### Pattern
**Definition:** The regular expression string that defines what to search for.
```python
import re
pattern = r'\d{3}-\d{4}'  # Matches phone numbers like 555-1234
match = re.search(pattern, 'Call 555-1234')
```
**Related:** Compile, raw strings, regex

#### Positive Lookahead
**Definition:** `(?=...)` asserts what follows matches, without consuming text.
```python
import re
# Find numbers followed by "px"
re.findall(r'\d+(?=px)', '10px 20em 30px')  # ['10', '30']
```
**Related:** Lookbehind, lookahead, assertions

#### Positive Lookbehind
**Definition:** `(?<=...)` asserts what precedes matches, without consuming text.
```python
import re
# Find numbers preceded by "$"
re.findall(r'(?<=\$)\d+', '$100 $200')  # ['100', '200']
```
**Related:** Lookahead, lookbehind, assertions

---

### Q

#### Quantifier
**Definition:** Specifies how many times the preceding element can occur.
```python
import re
# {n} - exactly n times
re.findall(r'a{3}', 'aa aaa aaaa')  # ['aaa', 'aaa']

# {n,} - at least n times
re.findall(r'a{2,}', 'a aa aaa')  # ['aa', 'aaa']

# {n,m} - between n and m times
re.findall(r'a{1,3}', 'aaaa')  # ['aaa', 'a']
```
**Related:** Greedy, lazy, `*`, `+`, `?`

---

### R

#### Raw String
**Definition:** String prefix `r` that treats backslashes as literal characters.
```python
# Without raw string
pattern1 = "\\d+"  # Two backslashes needed

# With raw string (recommended)
pattern2 = r"\d+"  # Clean syntax
```
**Related:** Patterns, backslash, escape

#### re.compile()
**Definition:** Compiles a regex pattern for reuse and performance.
```python
import re
pattern = re.compile(r'\d+')
pattern.findall('a1 b2')  # ['1', '2']
pattern.findall('c3 d4')  # ['3', '4']
```
**Related:** Pattern, performance, reuse

#### re.findall()
**Definition:** Returns all matches as a list.
```python
import re
re.findall(r'\b\w{4}\b', 'the cat dog fish')  # ['fish']
```
**Related:** `search()`, `match()`, `finditer()`

#### re.match()
**Definition:** Matches pattern only at the start of the string.
```python
import re
re.match(r'\d+', '123abc')  # Match
re.match(r'\d+', 'abc123')  # None
```
**Related:** `search()`, `findall()`

#### re.search()
**Definition:** Searches anywhere in the string for a match.
```python
import re
re.search(r'\d+', 'abc123')  # Match at position 3
```
**Related:** `match()`, `findall()`, `finditer()`

#### re.split()
**Definition:** Splits string by regex pattern.
```python
import re
re.split(r'[;,]', 'one;two,three')  # ['one', 'two', 'three']
```
**Related:** `str.split()`, `re.findall()`

#### re.sub()
**Definition:** Replaces matches with replacement string.
```python
import re
re.sub(r'\d+', 'X', 'a1b2c3')  # 'aXbXcX'
```
**Related:** `str.replace()`, `re.subn()`

---

### S

#### Search
**Definition:** Finding the first occurrence of a pattern in a string.
```python
import re
match = re.search(r'pattern', 'text with pattern here')
```
**Related:** `match()`, `findall()`, `finditer()`

---

### V

#### VERBOSE Flag (`re.X`)
**Definition:** Allows whitespace and comments in regex patterns.
```python
import re
pattern = re.compile(r"""
    ^           # Start of string
    \d{4}       # Year
    -           # Separator
    \d{2}       # Month
    -           # Separator
    \d{2}       # Day
    $           # End of string
""", re.VERBOSE)
```
**Related:** Flags, comments, readability

---

### W

#### Word Boundary
**Definition:** `\b` matches position between word and non-word characters.
```python
import re
# Match whole word "cat"
re.findall(r'\bcat\b', 'cat concatenate cat')  # ['cat', 'cat']
```
**Related:** `\b`, `\B`, anchors

---

## Quick Reference Table

| Term | Syntax/Function | Description |
|------|-----------------|-------------|
| **Alternation** | `a\|b` | Match a or b |
| **Anchor (start)** | `^` | Start of string |
| **Anchor (end)** | `$` | End of string |
| **Backreference** | `\1`, `\2` | Reference captured group |
| **Character class** | `[abc]` | Match a, b, or c |
| **Digit** | `\d` | `[0-9]` |
| **Non-digit** | `\D` | `[^0-9]` |
| **Word char** | `\w` | `[a-zA-Z0-9_]` |
| **Non-word char** | `\W` | `[^a-zA-Z0-9_]` |
| **Whitespace** | `\s` | `[ \t\n\r\f\v]` |
| **Non-whitespace** | `\S` | `[^ \t\n\r\f\v]` |
| **Zero or more** | `*` | Greedy quantifier |
| **One or more** | `+` | Greedy quantifier |
| **Zero or one** | `?` | Greedy quantifier |
| **Exactly n** | `{n}` | Quantifier |
| **At least n** | `{n,}` | Quantifier |
| **Between n-m** | `{n,m}` | Quantifier |
| **Group** | `(...)` | Capture group |
| **Non-capturing** | `(?:...)` | Group without capture |
| **Named group** | `(?P<name>...)` | Named capture |
| **Lookahead** | `(?=...)` | Assert what follows |
| **Lookbehind** | `(?<=...)` | Assert what precedes |
| **Case insensitive** | `re.I` | Ignore case flag |
| **Multiline** | `re.M` | `^` and `$` match lines |
| **Dotall** | `re.S` | `.` matches newlines |
| **Verbose** | `re.X` | Allow comments |
| **Compile** | `re.compile()` | Optimize pattern |
| **Find all** | `re.findall()` | Return all matches |
| **Search** | `re.search()` | Find first match |
| **Match** | `re.match()` | Match at start |
| **Substitute** | `re.sub()` | Replace matches |
| **Split** | `re.split()` | Split by pattern |

---

## Pattern Templates

### Email Validation
```python
r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
```

### Phone Number (US)
```python
r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
```

### Date (YYYY-MM-DD)
```python
r'\d{4}-\d{2}-\d{2}'
```

### URL
```python
r'https?://(?:www\.)?[^\s]+'
```

### IP Address
```python
r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
```
