# 🧮 Project 01: CLI Calculator

A full-featured command-line calculator with scientific operations, memory, and history.

## What This Project Practices

| Skill | Phase | Details |
|-------|-------|---------|
| Functions | Phase 1 | Modular operation functions |
| Control Flow | Phase 1 | Menu loop, conditionals |
| User Input | Phase 1 | `input()` parsing |
| Error Handling | Phase 1 | `try/except ValueError` |
| Classes & OOP | Phase 1 | `Calculator` class |
| String Formatting | Phase 1 | f-strings, `.format()` |
| Math Module | Phase 1 | `math.sin()`, `math.factorial()` |
| RegEx | Phase 1 | Pattern matching for expressions |
| Type Hints | Phase 2 | Function annotations |

## How to Run

```bash
python projects/01-calculator/main.py
```

## Features

- **Basic**: `+`, `-`, `*`, `/`, `^`, `%`
- **Scientific**: `sin()`, `cos()`, `tan()`, `log()`, `sqrt()`, `n!`
- **Constants**: `pi`, `e`
- **Memory**: `mstore`, `mrecall`, `madd`, `mclear`
- **History**: Last 10 calculations with `history`
- **Angle modes**: `deg`, `rad`

## Example Session

```
>> 2 + 3
  = 5
>> sin(90)
  = 1.0
>> 5!
  = 120
>> history
   1. 2+3 = 5.0
   2. sin(90) = 1.0
   3. 5! = 120
>> quit
```
