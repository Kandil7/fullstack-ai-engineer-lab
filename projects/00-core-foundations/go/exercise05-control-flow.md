# Exercise 05: Control Flow

> Master Go's control flow constructs: if, for, switch, defer, and labels.

## Goal

Write idiomatic Go control flow with short statements, type switches, defer stacks, and labeled breaks.

## Requirements

Create a Go program that demonstrates:
1. **If-else with short statement**: `if err := do(); err != nil {`
2. **Switch**: Expression switch, tagless switch (if-else chain)
3. **Type switch**: `switch v := i.(type)`
4. **For loops**: Standard, while-style, infinite with break, range
5. **Labels with break/continue**: Breaking out of outer loops
6. **Goto**: Rare but valid use cases
7. **Defer**: Stack order (LIFO), deferred function evaluation

## Expected Output

```
=== Exercise 05: Control Flow ===
--- 1. If-Else ---
x > 5
2*x > 15: 20

--- 2. Switch ---
Midweek
positive
string: hello
```

## Key Go Control Flow Facts

- **No while or do-while**: `for condition { }` replaces while
- **No ternary (`? :`)**: Use if-else
- **Switch cases don't fall through** by default (no `break` needed)
- **Defer runs when the surrounding function returns**, not when the block ends

## Defer Gotcha

```go
// Deferred function arguments are evaluated immediately, not when deferred runs
func main() {
    x := 1
    defer fmt.Println(x) // prints 1, not 2
    x = 2
}
```

## Next Step

Move to **Exercise 06: Functions**.
