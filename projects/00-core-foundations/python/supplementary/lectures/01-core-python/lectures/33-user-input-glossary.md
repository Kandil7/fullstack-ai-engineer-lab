# User Input Glossary

## Topic 33: Quick Reference Guide

---

## Glossary Terms

### A

#### argparse
**Definition:** Python module for parsing command-line arguments.
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, required=True)
args = parser.parse_args()
```
**Related:** sys.argv, CLI, argument parsing

---

### C

#### CLI (Command-Line Interface)
**Definition:** Interface for interacting with programs via text commands.
```python
# Program run from terminal
python script.py --name Alice --age 30
```
**Related:** Command line, terminal, arguments

#### Confirmation
**Definition:** Getting yes/no response from user.
```python
response = input("Continue? (y/n): ").lower()
confirmed = response in ['y', 'yes']
```
**Related:** User validation, prompts

---

### G

#### getpass
**Definition:** Module for secure password input (no echo).
```python
import getpass
password = getpass.getpass("Password: ")
```
**Related:** Password input, security, hidden input

---

### I

#### input()
**Definition:** Built-in function to read line from stdin.
```python
name = input("Enter name: ")
# Returns string
```
**Related:** stdin, prompts, user interaction

---

### P

#### Prompt
**Definition:** Text displayed to user requesting input.
```python
response = input("What is your name? ")  # "What is your name?" is prompt
```
**Related:** input(), user interface, UX

---

### S

#### sys.argv
**Definition:** List containing command-line arguments.
```python
import sys
# python script.py arg1 arg2
# sys.argv = ['script.py', 'arg1', 'arg2']
```
**Related:** argparse, command line, arguments

#### stdin
**Definition:** Standard input stream (keyboard by default).
```python
import sys
line = sys.stdin.readline()
```
**Related:** input(), stdout, streams

---

## Quick Reference Table

| Term | Function/Module | Description |
|------|-----------------|-------------|
| **input()** | Built-in | Read string from user |
| **getpass** | Module | Hidden password input |
| **sys.argv** | Module | Command-line arguments |
| **argparse** | Module | Argument parsing |
| **stdin** | sys | Standard input stream |
| **Prompt** | Concept | Text requesting input |
| **Type conversion** | int(), float() | Convert string input |
| **Validation** | Concept | Checking input validity |

---

## Input Patterns

### Pattern 1: Validated Input
```python
while True:
    try:
        age = int(input("Age: "))
        if 0 <= age <= 150:
            break
        print("Invalid age!")
    except ValueError:
        print("Enter a number!")
```

### Pattern 2: Default Value
```python
port_input = input("Port [8080]: ").strip()
port = int(port_input) if port_input else 8080
```

### Pattern 3: Menu
```python
print("1. Option A\n2. Option B\n3. Quit")
choice = input("Select: ")
```

### Pattern 4: Confirmation
```python
def confirm(prompt):
    while True:
        resp = input(f"{prompt} (y/n): ").lower()
        if resp in ['y', 'yes']: return True
        if resp in ['n', 'no']: return False
```

---

## Type Conversion Table

| Function | Purpose | Example |
|----------|---------|---------|
| `int()` | String to integer | `int("42")` → `42` |
| `float()` | String to float | `float("3.14")` → `3.14` |
| `str()` | Value to string | `str(42)` → `"42"` |
| `bool()` | Value to boolean | `bool("yes")` → `True` |
| `list()` | Iterable to list | `list("abc")` → `['a','b','c']` |
