# Exercise 08: Concurrency

> Master Go concurrency: goroutines, channels, select, WaitGroup, Mutex, and pipeline patterns.

## Goal

Write safe concurrent programs using goroutines, channels for communication, and sync primitives for coordination.

## Requirements

Create a Go program that demonstrates:
1. **Basic goroutines**: Launch with `go`, non-deterministic execution
2. **Channels**: Unbuffered (synchronous) send/receive
3. **Buffered channels**: Non-blocking until full
4. **Channel directions**: `chan<- T` (send-only), `<-chan T` (receive-only)
5. **Select statement**: Wait on multiple channel operations with timeout
6. **Worker pool**: Fixed number of workers processing jobs from a channel
7. **Pipeline**: Generator → processor → collector stages
8. **Fan-out, Fan-in**: Distribute work across multiple goroutines, merge results
9. **`sync.WaitGroup`**: Wait for a collection of goroutines
10. **`sync.Mutex`**: Protect shared state
11. **`sync.Once`**: One-time initialization
12. **Cancellation**: Close a channel to signal goroutines to stop

## Expected Output

```
=== Exercise 08: Concurrency ===
--- 1. Basic Goroutine ---
  Goroutine 1: Hello 0
  Goroutine 2: Hello 0
  Goroutine 1: Hello 1
  ...
```

## Key Rules

1. **"Do not communicate by sharing memory; instead, share memory by communicating."**
2. **The sender should close the channel**, not the receiver
3. **Always know when your goroutine exits** — leaked goroutines are a real problem
4. **Use `sync.WaitGroup`** to wait for goroutines to finish
5. **Race conditions are undefined behavior** — always protect shared state with `sync.Mutex` or use channels
6. **Detect races at dev time**: `go run -race .`

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Deadlock from unbuffered channel with no receiver | Use buffered channel or ensure receiver is ready |
| Goroutine leak (goroutine waiting forever) | Add cancellation channel or timeout |
| Loop variable capture in goroutine | `go func(val := i) { ... }(i)` |
| Closing channel twice | Only sender closes; use `sync.Once` if needed |
| Writing to closed channel (panics) | Ensure only sender writes; use `select` with done channel |

## Next Step

Move to **Exercise 09: Context**.
