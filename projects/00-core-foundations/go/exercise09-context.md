# Exercise 09: Context

> Master Go's `context` package: timeouts, cancellation, values, and propagation through call chains.

## Goal

Use context for request-scoped values, deadline propagation, and graceful cancellation in concurrent programs.

## Requirements

Create a Go program that demonstrates:
1. **`context.WithTimeout`**: Automatically cancel after a duration
2. **`context.WithCancel`**: Manual cancellation signal
3. **`context.WithValue`**: Pass request-scoped data through the call chain
4. **Context propagation**: Pass ctx as first parameter through function calls
5. **Context select pattern**: Listen for both work completion and cancellation
6. **HTTP-like request handling**: Timeout per-request
7. **Multiple context sources**: Wait for first cancellation among multiple contexts
8. **Best practices**: ctx as first param, don't store in structs, always call cancel

## Expected Output

```
=== Exercise 09: Context ===
--- 1. Context with Timeout ---
Timeout: context deadline exceeded

--- 2. Context Cancellation ---
Cancel signal sent
Context cancelled: context canceled
```

## Key Rules

| Rule | Explanation |
|------|-------------|
| `ctx` is the **first parameter** | `func Do(ctx context.Context, ...)` |
| **Don't store context in structs** | Pass explicitly through function calls |
| **Always call `cancel()`** | Use `defer cancel()` immediately after creating |
| Don't pass nil context | Use `context.TODO()` if unsure |
| `context.Background()` at the root | Entry points (main, init, tests) |
| `context.TODO()` when unclear | Signals "I need to decide this later" |

## Next Step

Move to **Exercise 10: I/O and JSON**.
