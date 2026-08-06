"""
Pandas String Methods: .str accessor, regex, vectorized string ops
===================================================================

Comprehensive coverage of pandas string manipulation capabilities.
"""

import pandas as pd
import numpy as np
import re

np.random.seed(42)
df = pd.DataFrame({
    'id': range(1, 21),
    'email': [f'user{i}@example.com' for i in range(1, 21)],
    'full_name': [f'User {i} Name' for i in range(1, 21)],
    'phone': [f'+1-555-{np.random.randint(100,999)}-{np.random.randint(1000,9999):04d}' for _ in range(20)],
    'address': [f'{np.random.randint(100,9999)} Main St, City {i}, ST {np.random.randint(10000,99999)}' for i in range(1, 21)],
    'tags': [','.join(np.random.choice(['python', 'ml', 'data', 'ai', 'web', 'cloud', 'devops', 'sql'], 
                                         np.random.randint(1, 4), replace=False)) for _ in range(20)],
    'description': [f'This is a sample description for user {i} with some numbers {np.random.randint(100,999)}' for i in range(1, 21)],
    'code': [f'CODE-{np.random.randint(1000,9999)}-{np.random.choice(["A","B","C"])}' for _ in range(20)],
})

print("=" * 60)
print("1. BASIC STRING OPERATIONS")
print("=" * 60)

s = df['full_name']
print("Original:", s.head().tolist())
print()

# Case conversion
print("lower():", s.str.lower().head().tolist())
print("upper():", s.str.upper().head().tolist())
print("title():", s.str.title().head().tolist())
print("capitalize():", s.str.capitalize().head().tolist())
print("swapcase():", s.str.swapcase().head().tolist())
print()

# Strip whitespace
s_spaces = pd.Series(['  hello  ', '\tworld\n', '  pandas  '])
print("Original with spaces:", s_spaces.tolist())
print("strip():", s_spaces.str.strip().tolist())
print("lstrip():", s_spaces.str.lstrip().tolist())
print("rstrip():", s_spaces.str.rstrip().tolist())
print()

# Length
print("len():", s.str.len().head().tolist())
print()

# =============================================================================
# 2. SUBSTRING OPERATIONS
# =============================================================================

print("=" * 60)
print("2. SUBSTRING OPERATIONS")
print("=" * 60)

# Slicing
print("Slice [0:4]:", s.str[0:4].head().tolist())
print("Slice [-4:]:", s.str[-4:].head().tolist())
print()

# Contains
print("contains('User'):", s.str.contains('User').head().tolist())
print("contains('user', case=False):", s.str.contains('user', case=False).head().tolist())
print()

# Startswith / Endswith
print("startswith('User'):", s.str.startswith('User').head().tolist())
print("endswith('Name'):", s.str.endswith('Name').head().tolist())
print()

# Match (regex at start)
print("match(r'User \\d+'):", s.str.match(r'User \d+').head().tolist())
print()

# =============================================================================
# 3. EXTRACTING & PARSING
# =============================================================================

print("=" * 60)
print("3. EXTRACTING & PARSING WITH REGEX")
print("=" * 60)

# Extract first match - returns DataFrame
email_parts = df['email'].str.extract(r'(.+)@(.+)')
print("Email extract (user, domain):")
print(email_parts.head())
print()

# Extract with named groups
email_named = df['email'].str.extract(r'(?P<user>.+)@(?P<domain>.+)')
print("Named groups:")
print(email_named.head())
print()

# Extract all matches - returns DataFrame with MultiIndex
phone_all = df['phone'].str.extractall(r'(\d+)')
print("Extract all digit groups:")
print(phone_all.head(10))
print()

# Extract first match only (returns Series)
first_digits = df['phone'].str.extract(r'(\d+)', expand=False)
print("First digit group only:")
print(first_digits.head())
print()

# =============================================================================
# 4. SPLITTING & JOINING
# =============================================================================

print("=" * 60)
print("4. SPLITTING & JOINING")
print("=" * 60)

# Split on delimiter
tags_split = df['tags'].str.split(',', expand=True)
tags_split.columns = [f'tag_{i+1}' for i in range(tags_split.shape[1])]
print("Split tags into columns:")
print(tags_split.head())
print()

# Split with limit
print("Split with n=2:", df['tags'].str.split(',', n=2, expand=True).head())
print()

# Split on regex
addr_split = df['address'].str.split(r',\s*', expand=True)
print("Split address on comma:")
print(addr_split.head())
print()

# Join
print("Join tags with ' | ':", df['tags'].str.join(' | ').head().tolist())
print()

# =============================================================================
# 5. REPLACING
# =============================================================================

print("=" * 60)
print("5. REPLACING")
print("=" * 60)

# Simple replace
print("Replace 'User' -> 'Customer':", df['full_name'].str.replace('User', 'Customer').head().tolist())
print()

# Regex replace
print("Replace digits with X:", df['description'].str.replace(r'\d+', 'XXX', regex=True).head().tolist())
print()

# Replace with function
def mask_email(match):
    user, domain = match.groups()
    return f'{user[0]}***@{domain}'

print("Mask emails:", df['email'].str.replace(r'(.+)@(.+)', mask_email, regex=True).head().tolist())
print()

# Replace multiple
# NOTE: str.replace(pat, repl) needs an explicit repl per call; a dict shortcut
# no longer works, so chain one replace per mapping
replacements = {'python': 'Python', 'ml': 'ML', 'ai': 'AI'}
tags_replaced = df['tags']
for old, new in replacements.items():
    tags_replaced = tags_replaced.str.replace(old, new, regex=False)
print("Multiple replacements:", tags_replaced.head().tolist())
print()

# =============================================================================
# 6. PARSING STRUCTURED STRINGS
# =============================================================================

print("=" * 60)
print("6. PARSING STRUCTURED STRINGS")
print("=" * 60)

# Parse code: CODE-1234-A
code_parsed = df['code'].str.extract(r'CODE-(?P<num>\d+)-(?P<letter>[A-C])')
print("Parsed code:")
print(code_parsed.head())
print()

# Combine extracted columns
df['code_num'] = code_parsed['num'].astype(int)
df['code_letter'] = code_parsed['letter']
print("Added parsed columns:")
print(df[['code', 'code_num', 'code_letter']].head())
print()

# Parse address components
addr_parsed = df['address'].str.extract(r'(?P<street_num>\d+)\s+(?P<street>\w+\s\w+),\s+(?P<city>\w+\s\d+),\s+(?P<state>\w+)\s+(?P<zip>\d+)')
print("Parsed address:")
print(addr_parsed.head())
print()

# =============================================================================
# 7. ADVANCED PATTERNS
# =============================================================================

print("=" * 60)
print("7. ADVANCED PATTERNS")
print("=" * 60)

# Count occurrences
print("Count 'a' in name:", df['full_name'].str.count('a').head().tolist())
print("Count digits:", df['description'].str.count(r'\d').head().tolist())
print()

# Find all matches (returns list)
print("Find all digits:", df['description'].str.findall(r'\d+').head().tolist())
print()

# Find first match position
print("Find 'User' position:", df['full_name'].str.find('User').head().tolist())
print("Rfind 'User':", df['full_name'].str.rfind('User').head().tolist())
print()

# Pad strings
print("zfill(5):", pd.Series(['1', '22', '333']).str.zfill(5).tolist())
print("ljust(10, '-'):", pd.Series(['a', 'bb']).str.ljust(10, '-').tolist())
print("rjust(10, '0'):", pd.Series(['a', 'bb']).str.rjust(10, '0').tolist())
print("center(10, '*'):", pd.Series(['a', 'bb']).str.center(10, '*').tolist())
print()

# Wrap text
long_text = pd.Series(['This is a very long text that should be wrapped'])
print("Wrap width=20:", long_text.str.wrap(20).tolist())
print()

# =============================================================================
# 8. VECTORIZED COMPARISONS
# =============================================================================

print("=" * 60)
print("8. VECTORIZED COMPARISONS")
print("=" * 60)

# Vectorized comparisons: .str has no eq/ne/lt/le/gt/ge accessors — use the
# plain Series operators, which compare elementwise
s1 = pd.Series(['apple', 'banana', 'cherry'])
s2 = pd.Series(['apple', 'BANANA', 'date'])

print("eq (==):", (s1 == s2).tolist())
print("ne (!=):", (s1 != s2).tolist())
print("lt (<):", (s1 < s2).tolist())
print("le (<=):", (s1 <= s2).tolist())
print("gt (>):", (s1 > s2).tolist())
print("ge (>=):", (s1 >= s2).tolist())
print()

# =============================================================================
# 9. PRACTICAL EXAMPLES
# =============================================================================

print("=" * 60)
print("9. PRACTICAL EXAMPLES")
print("=" * 60)

# Example 1: Clean messy column names
messy_cols = pd.DataFrame(columns=['First Name', 'Last Name', 'Email Address', 'Phone Number'])
print("Messy columns:", messy_cols.columns.tolist())
clean_cols = messy_cols.columns.str.lower().str.replace(' ', '_')
print("Clean columns:", clean_cols.tolist())
print()

# Example 2: Extract domain from email for analysis
df['email_domain'] = df['email'].str.extract(r'@(.+)')
domain_counts = df['email_domain'].value_counts()
print("Email domains:")
print(domain_counts)
print()

# Example 3: Validate phone format
valid_phone = df['phone'].str.match(r'^\+\d-\d{3}-\d{3}-\d{4}$')
print("Valid phone format:", valid_phone.sum(), "/", len(df))
print()

# Example 4: Create slug from name
df['slug'] = df['full_name'].str.lower().str.replace(' ', '-').str.replace(r'[^\w-]', '', regex=True)
print("Slugs:")
print(df[['full_name', 'slug']].head())
print()

# Example 5: Parse log-like strings
logs = pd.Series([
    '2020-01-01 10:00:00 INFO User login',
    '2020-01-01 10:05:00 ERROR Database connection failed',
    '2020-01-01 10:10:00 WARN High memory usage',
])
log_parsed = logs.str.extract(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.+)')
print("Parsed logs:")
print(log_parsed)
print()

print("=" * 60)
print("END OF STRING METHODS")
print("=" * 60)