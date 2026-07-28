# Exercise 08: Linux Text Processing

> Process text files with grep, sed, awk, cut, sort, uniq, and pipes.

## Goal

Master the Linux text processing pipeline: regex searching, text transformation, column extraction, sorting, and deduplication.

## Instructions

### 1. grep — Search Patterns

```bash
# Create a sample file
cat > sample.txt << EOF
apple 5 0.50
banana 3 0.30
cherry 10 0.75
apple 2 0.50
date 7 0.25
EOF

# Basic search
grep "apple" sample.txt

# Line count
grep -c "apple" sample.txt

# Case-insensitive
grep -i "APPLE" sample.txt

# Show line numbers
grep -n "apple" sample.txt

# Invert match
grep -v "apple" sample.txt

# Regular expressions
grep "^[ab]" sample.txt      # Starts with a or b
grep "0\\.[0-9][0-9]$"      # Ends with two decimal places
grep "e$" sample.txt         # Ends with 'e'
```

### 2. sed — Stream Editor

```bash
# Replace text (first occurrence per line)
sed 's/apple/orange/' sample.txt

# Replace all occurrences (global)
sed 's/apple/orange/g' sample.txt

# Replace in-place
sed -i 's/apple/orange/g' sample.txt

# Delete lines matching pattern
sed '/banana/d' sample.txt

# Print specific lines
sed -n '2,4p' sample.txt

# Multiple commands
sed -e 's/apple/orange/g' -e '/banana/d' sample.txt
```

### 3. awk — Field Processing

```bash
# Print specific columns
awk '{print $1, $2}' sample.txt

# Print lines where column 2 > 5
awk '$2 > 5 {print $1, $2}' sample.txt

# Calculate sum
awk '{sum += $2} END {print "Total:", sum}' sample.txt

# Formatted output
awk '{printf "%-10s %3d $%5.2f\n", $1, $2, $3}' sample.txt

# Column separators (e.g., CSV)
awk -F',' '{print $1, $2}' data.csv
```

### 4. cut — Extract Columns

```bash
# Characters by position
cut -c1-5 sample.txt

# Fields by delimiter
cut -d' ' -f1,3 sample.txt

# Skip first line (for headers)
tail -n +2 data.csv | cut -d',' -f1,3
```

### 5. sort and uniq

```bash
# Sort alphabetically
sort sample.txt

# Sort numerically by column 2
sort -k2 -n sample.txt

# Sort by column 3 numerically (reverse)
sort -k3 -nr sample.txt

# Unique lines (requires sorted input)
sort sample.txt | uniq
sort sample.txt | uniq -c      # Count occurrences
sort sample.txt | uniq -d      # Only duplicates
```

### 6. The Pipeline

```bash
# Real-world pipeline: find top 5 memory-consuming processes
ps aux | sort -k4 -nr | head -5

# Count Go source files per directory
find . -name "*.go" | cut -d'/' -f2 | sort | uniq -c | sort -rn

# Find most common words in a file
cat text.txt | tr ' ' '\n' | sort | uniq -c | sort -rn | head -10

# Extract and process JSON-like data
grep "ERROR" app.log | cut -d' ' -f3- | sort | uniq -c | sort -rn
```

## Self-Check

- What does `grep -r` do?
- How do you replace text in-place with sed?
- What's the difference between `sort -n` and `sort` without `-n`?

## Key Commands Reference

| Command | Example | Purpose |
|---------|---------|---------|
| `grep` | `grep -r "TODO" .` | Search patterns |
| `sed` | `sed 's/old/new/g' file` | Stream edit |
| `awk` | `awk '{print $1}' file` | Field processing |
| `cut` | `cut -d',' -f1 file` | Extract columns |
| `sort` | `sort -k2 -n file` | Sort lines |
| `uniq` | `sort file \| uniq -c` | Unique + count |
