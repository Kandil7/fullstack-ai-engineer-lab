# Exercise 06: Bash Scripting

> Write shell scripts with variables, conditionals, loops, and functions.

## Goal

Write production-quality bash scripts with error handling and best practices.

## Instructions

### 1. Variables and Parameters

```bash
#!/bin/bash

# Variables (no spaces around =)
NAME="World"
echo "Hello, $NAME!"

# Command substitution
FILES=$(ls -la)
echo "Files: $FILES"

# Special variables
echo "Script: $0"
echo "Args: $1, $2, $3"
echo "Arg count: $#"
echo "All args: $@"
echo "Exit code of last command: $?"
```

### 2. Conditionals

```bash
#!/bin/bash

FILE="test.txt"

# File tests
if [ -f "$FILE" ]; then
    echo "$FILE exists"
fi

if [ -d "$DIR" ]; then
    echo "$DIR is a directory"
fi

# String comparison
if [ "$NAME" = "World" ]; then
    echo "Hello, World!"
fi

if [ -z "$EMPTY" ]; then
    echo "Variable is empty"
fi

# Numeric comparison
AGE=25
if [ "$AGE" -ge 18 ]; then
    echo "Adult"
fi

# Logical operators
if [ -f "$FILE" ] && [ -r "$FILE" ]; then
    echo "File exists and is readable"
fi
```

### 3. Loops

```bash
#!/bin/bash

# For loop over list
for fruit in apple banana cherry; do
    echo "Fruit: $fruit"
done

# For loop with range (Bash 3.0+)
for i in {1..5}; do
    echo "Number: $i"
done

# While loop
COUNT=0
while [ "$COUNT" -lt 5 ]; do
    echo "Count: $COUNT"
    ((COUNT++))
done

# While read line
while IFS= read -r line; do
    echo "Line: $line"
done < input.txt

# Iterate over files
for file in *.go; do
    echo "Go file: $file"
done
```

### 4. Functions

```bash
#!/bin/bash

# Define function
function greet() {
    local name="$1"  # local scope
    echo "Hello, $name!"
}

greet "Alice"
greet "Bob"

# Function with return value
function add() {
    local sum=$(( $1 + $2 ))
    echo "$sum"  # Use echo to "return" values
}

result=$(add 5 3)
echo "5 + 3 = $result"
```

### 5. Error Handling

```bash
#!/bin/bash
set -e          # Exit on error
set -u          # Error on undefined variables
set -o pipefail # Catch pipe errors

# Or combine:
set -euo pipefail

# Trap errors
trap 'echo "Error on line $LINENO"; exit 1' ERR

# Trap exit
trap 'echo "Script finished"; cleanup' EXIT

function cleanup() {
    rm -f /tmp/tempfile
}
```

### 6. Complete Example Script

Save this as `deploy.sh`:

```bash
#!/bin/bash
set -euo pipefail

APP_DIR="/var/www/app"
BACKUP_DIR="/tmp/backup"

echo "Starting deployment..."

# Check prerequisites
if [ ! -d "$APP_DIR" ]; then
    echo "Error: $APP_DIR does not exist"
    exit 1
fi

# Backup
echo "Backing up..."
cp -r "$APP_DIR" "$BACKUP_DIR/backup-$(date +%Y%m%d)"

# Deploy
echo "Deploying..."
cp -r ./dist/* "$APP_DIR/"

# Verify
if [ -f "$APP_DIR/index.html" ]; then
    echo "Deployment successful!"
else
    echo "Deployment failed - rolling back..."
    cp -r "$BACKUP_DIR/backup-$(date +%Y%m%d)/*" "$APP_DIR/"
    exit 1
fi
```

## Self-Check

- What does `set -euo pipefail` do?
- How do you make a variable local to a function?
- What's the difference between `$@` and `$*`?

## Key Commands Reference

| Pattern | Purpose |
|---------|---------|
| `$1`, `$2` | Script arguments |
| `$?` | Last exit code |
| `[ -f file ]` | Check file exists |
| `[ -z "$var" ]` | Check variable empty |
| `$(( expr ))` | Arithmetic |
| `$(command)` | Command substitution |
| `set -euo pipefail` | Strict mode |
| `local x=1` | Local variable |
