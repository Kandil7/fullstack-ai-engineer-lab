# Exercise 06: Functions

> Master Go functions: variadic, closures, first-class functions, and the function-vs-method distinction.

## Goal

Write idiomatic Go functions using variadic parameters, closures with captures, function types, and method receivers.

## Requirements

Create a Go program that demonstrates:
1. **Basic function**: Simple parameters and return
2. **Multiple return values**: Idiomatic Go pattern
3. **Named return values**: "Naked" returns
4. **Variadic functions**: `func sum(nums ...int) int`
5. **First-class functions**: Assign to variable, pass as parameter
6. **Closures**: Capturing variables, counter pattern
7. **Defer in functions**: Modifying named return values
8. **Function types**: Type aliases, map of functions
9. **Methods vs functions**: Value receiver, pointer receiver

## Expected Output

```
=== Exercise 06: Functions ===
--- 1. Basic Function ---
add(3, 5) = 8

--- 2. Multiple Return Values ---
17 / 5 = 3 remainder 5
```

## Key Concepts

- **Multiple returns**: Go functions can return multiple values (commonly `(result, error)`)
- **Named returns**: Pre-declare return variable names for clarity
- **Variadic**: `...T` collects remaining arguments into a slice
- **Closure**: A function that captures variables from its enclosing scope
- **Method**: A function with a receiver parameter

## Closure Pitfall

```go
for i := 0; i < 3; i++ {
    go func() { fmt.Println(i) }() // Prints 3, 3, 3—not 0, 1, 2!
}
// Fix: capture a copy
for i := 0; i < 3; i++ {
    i := i  // shadow with a new variable
    go func() { fmt.Println(i) }()
}
```

## Next Step

Move to **Exercise 07: Error Handling**.
