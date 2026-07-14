# String Formatting Glossary

## Topic 31: Quick Reference Guide

---

## Glossary Terms

### A

#### Alignment
**Definition:** Positioning text within a field (left, right, center).
```python
print(f"{'left':<10}|")     # left      |
print(f"{'right':>10}|")    #      right|
print(f"{'center':^10}|")   #   center  |
```
**Related:** `<`, `>`, `^`, width, padding

---

### F

#### F-string (Formatted String Literal)
**Definition:** String prefix `f` enabling embedded expressions inside `{}`.
```python
name = "Alice"
print(f"Hello, {name}!")  # Hello, Alice!
print(f"2 + 2 = {2 + 2}")  # 2 + 2 = 4
```
**Related:** Format expressions, `str.format()`, `=`, debug specifier

#### Format Specification
**Definition:** Controls how values are formatted within `{}`.
```python
print(f"{3.14159:.2f}")   # 3.14
print(f"{1234:,}")        # 1,234
print(f"{'hi':^10}")      #     hi
```
**Related:** Precision, alignment, type, width

---

### I

#### Interpolation
**Definition:** Embedding values directly into a string.
```python
# String interpolation
name = "Alice"
print(f"Hello, {name}")  # Interpolates name variable
```
**Related:** F-strings, substitution, placeholder

---

### P

#### Padding
**Definition:** Adding characters (spaces, zeros) to fill a field to specified width.
```python
print(f"{42:05d}")       # 00042 (zero-padded)
print(f"{'hi':*^10}")    # ***hi**** (center-padded with *)
```
**Related:** Width, fill character, alignment

#### Placeholder
**Definition:** Markers in format strings that get replaced with values.
```python
# Different placeholder styles
print("Hello %s" % "World")      # %-style
print("Hello {}".format("World")) # str.format
print(f"Hello {name}")            # f-string
```
**Related:** `%s`, `{}`, interpolation, substitution

#### Precision
**Definition:** Number of decimal places for floats in format specs.
```python
print(f"{3.14159:.2f}")   # 3.14 (2 decimal places)
print(f"{0.1:.10f}")      # 0.1000000000 (10 decimal places)
```
**Related:** `.Nf`, format spec, float formatting

---

### S

#### str.format()
**Definition:** Method for string formatting using `{}` placeholders.
```python
# Positional
print("Hello {}".format("World"))

# Named
print("Hello {name}".format(name="World"))
```
**Related:** F-strings, placeholders, positional arguments

#### Substitution
**Definition:** Replacing placeholders with actual values.
```python
# Template substitution
from string import Template
t = Template("Hello $name")
print(t.substitute(name="World"))
```
**Related:** Interpolation, placeholders, Template

---

### T

#### Template String
**Definition:** Simple string substitution using `string.Template`.
```python
from string import Template
t = Template("$name is $age years old")
print(t.substitute(name="Alice", age=30))
```
**Related:** `$name` syntax, `safe_substitute()`, user patterns

---

### W

#### Width
**Definition:** Minimum field width for formatted output.
```python
print(f"{42:10}")       #         42 (10-char field)
print(f"{'hi':<10}|")   # hi        | (left-aligned in 10 chars)
```
**Related:** Alignment, padding, format spec

---

## Quick Reference Table

| Term | Syntax/Example | Description |
|------|----------------|-------------|
| **Alignment (left)** | `{:<10}` | Left-align in 10-char field |
| **Alignment (right)** | `{:>10}` | Right-align in 10-char field |
| **Alignment (center)** | `{:^10}` | Center in 10-char field |
| **Fill character** | `{:*^10}` | Fill with `*` |
| **Width** | `{:10}` | Minimum 10 characters |
| **Precision (float)** | `{:.2f}` | 2 decimal places |
| **Thousands sep** | `{:,.2f}` | Comma separator |
| **Percent** | `{:.1%}` | As percentage |
| **Scientific** | `{:.2e}` | Scientific notation |
| **Binary** | `{:b}` | Binary representation |
| **Hex** | `{:x}` | Lowercase hex |
| **Hex (uppercase)** | `{:X}` | Uppercase hex |
| **Octal** | `{:o}` | Octal representation |
| **Zero-pad** | `{:05d}` | Zero-padded integer |
| **Sign** | `{:+d}` | Show sign for positive |
| **Debug** | `{x=}` | Shows `x=value` |
| **Repr** | `{x!r}` | Uses `repr()` |
| **Str** | `{x!s}` | Uses `str()` |

---

## Format Spec Template

```
[[fill]align][sign][#][0][width][grouping][.precision][type]
```

| Position | Options | Example |
|----------|---------|---------|
| fill | any character | `*`, `_`, `0` |
| align | `<` `>` `^` `=` | `:<`, `:>`, `:^` |
| sign | `+` `-` ` ` | `+`, `-`, ` ` (space) |
| # | `#` | `#x`, `#o`, `#b` |
| 0 | `0` | `010d` |
| width | integer | `10`, `20` |
| grouping | `,` `_` | `:,`, `:_` |
| precision | `.N` | `.2f`, `.10s` |
| type | `d` `f` `e` `s` etc. | `d`, `f`, `e`, `x`, `b` |

---

## Number Type Codes

| Code | Name | Example |
|------|------|---------|
| `d` | Decimal integer | `f"{42:d}"` → `42` |
| `b` | Binary | `f"{10:b}"` → `1010` |
| `o` | Octal | `f"{8:o}"` → `10` |
| `x` | Hex (lower) | `f"{255:x}"` → `ff` |
| `X` | Hex (upper) | `f"{255:X}"` → `FF` |
| `c` | Character | `f"{65:c}"` → `A` |
| `e` | Scientific (lower) | `f"{1234:e}"` → `1.234000e+03` |
| `E` | Scientific (upper) | `f"{1234:E}"` → `1.234000E+03` |
| `f` | Fixed-point (lower) | `f"{3.14:f}"` → `3.140000` |
| `F` | Fixed-point (upper) | `f"{3.14:F}"` → `3.140000` |
| `g` | General (lower) | `f"{3.14:g}"` → `3.14` |
| `G` | General (upper) | `f"{3.14:G}"` → `3.14` |
| `%` | Percentage | `f"{0.15:%}"` → `15.000000%` |
| `s` | String | `f"{'hi':s}"` → `hi` |

---

## Pattern Examples

### Currency
```python
price = 1234.56
print(f"${price:,.2f}")    # $1,234.56
print(f"${price:.0f}")     # $1235
```

### Date/Time
```python
from datetime import datetime
now = datetime.now()
print(f"{now:%Y-%m-%d}")    # 2024-01-15
print(f"{now:%H:%M:%S}")    # 10:30:45
```

### Table Formatting
```python
data = [("Alice", 30), ("Bob", 25)]
for name, age in data:
    print(f"{name:<10} | {age:>5}")
# Alice      |    30
# Bob        |    25
```

### Debugging
```python
x = 42
print(f"{x=}")              # x=42
print(f"{x + 1=}")          # x + 1=43
print(f"{x!r=}")            # x!r=42
```
