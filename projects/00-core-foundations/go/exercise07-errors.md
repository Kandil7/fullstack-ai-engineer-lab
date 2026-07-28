# Exercise 07: Error Handling

> Master Go error handling: sentinel errors, wrapping, custom types, panic/recover, and best practices.

## Goal

Write production-quality error handling using Go 1.13+ error wrapping, sentinel errors, custom error types, and the panic/recover pattern.

## Requirements

Create a Go program that demonstrates:
1. **Basic error handling**: Functions returning `(result, error)` — the Go idiom
2. **Sentinel errors**: Package-level `var ErrXxx = errors.New(...)` for known outcomes
3. **Error wrapping**: `fmt.Errorf("context: %w", err)` to preserve the error chain
4. **`errors.Is()`**: Check if any error in the chain matches a sentinel
5. **`errors.As()`**: Extract a specific error type from the chain
6. **Custom error types**: Struct implementing `Error() string` with additional fields
7. **Multiple errors**: `errors.Join()` (Go 1.20+)
8. **Panic and recover**: Safe panic handling with defer
9. **Best practices**: Wrap with context, don't ignore errors, return early

## Expected Output

```
=== Exercise 07: Error Handling ===
--- 1. Basic Error Handling ---
10 / 2 = 5
Expected error: division by zero

--- 2. Sentinel Errors ---
Item not found (sentinel check)
```

## Key Patterns

| Pattern | When to Use |
|---------|-------------|
| `errors.New("msg")` | Static, parameterless errors (e.g., `ErrNotFound`) |
| `fmt.Errorf("%w", err)` | Wrapping a lower-level error with context |
| `errors.Is(err, target)` | Checking if error matches a sentinel anywhere in chain |
| `errors.As(err, &target)` | Extracting a custom error type from the chain |
| `recover()` | Catching panics in goroutines or at API boundaries |
| `errors.Join(err1, err2)` | Combining multiple independent errors (Go 1.20+) |

## Anti-Patterns

❌ `_ = doWork()` — ignoring errors  
❌ `return errors.New("failed")` without context — no root cause  
❌ Panicking in library code — let caller decide  
❌ `fmt.Errorf("failed: %s", err.Error())` — breaks error chain, use `%w`  

## Next Step

Move to **Exercise 08: Concurrency**.
