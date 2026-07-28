# Exercise 04: Collections (Slices, Maps, Arrays)

> Master Go's collection types: arrays (fixed size) vs slices (dynamic) and maps (key-value).

## Goal

Understand the memory model of slices (ptr, len, cap), map operations, and string/rune handling.

## Requirements

Create a Go program that demonstrates:
1. **Arrays**: Fixed-size, value semantics
2. **Slices**: Dynamic, `append`, `make`, `copy`, slicing expressions
3. **Two-dimensional slices**: Matrix representation
4. **Maps**: Create, read, update, delete, comma-ok idiom
5. **Map with slice values**: Complex nested structures
6. **Range over slice/map**: Iteration with index/value
7. **Strings and runes**: `[]rune(str)`, UTF-8 encoding
8. **Bytes vs runes**: `[]byte(str)` and `[]rune(str)` differences

## Expected Output

```
=== Exercise 04: Collections ===
--- 1. Arrays ---
Array: [10 0 0 0 50], len=5, cap=5
Array literal: [a b c]

--- 2. Slices ---
Slice: [1 2 3], len=3, cap=3
After append: [1 2 3 4 5]
```

## Key Concepts

- **Array**: `[5]int` — fixed size, passed by value (copied!)
- **Slice**: `[]int` — dynamic, references backing array
- **Slice header**: pointer to backing array, length, capacity
- **`append`**: may allocate new backing array if capacity exceeded
- **Map**: `map[K]V` where K must be comparable
- **Comma-ok**: `val, ok := m["key"]` — safe lookup

## Pitfall to Watch

```go
// Modifying a slice in a function affects the caller's backing array
func main() {
    s := []int{1, 2, 3}
    modify(s)
    fmt.Println(s) // [1, 2, 100] — backing array modified!
}
func modify(s []int) {
    s[2] = 100
}
```

## Next Step

Move to **Exercise 05: Control Flow**.
