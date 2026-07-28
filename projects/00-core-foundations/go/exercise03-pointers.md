# Exercise 03: Pointers and Memory

> Master Go pointers, memory allocation, and the critical difference between value and pointer receivers.

## Goal

Understand pointer semantics, heap vs stack allocation, and when to use pointers.

## Requirements

Create a Go program that demonstrates:
1. **Basic pointer operations**: `&` (address-of) and `*` (dereference)
2. **Pointers to structs**: Access fields through a pointer (automatic dereference)
3. **`new()` vs composite literals**: `new(Point)` vs `&Point{X: 1}`
4. **Value vs pointer receivers**: Show mutation behavior difference
5. **Nil pointers**: Check before dereferencing
6. **Double pointers**: `**T` pattern

## Expected Output

```
=== Exercise 03: Pointers and Memory ===
--- 1. Basic Pointer Operations ---
Value of x: 42
Address of x (&x): 0x...
Value of p (address): 0x...
Value pointed to by p (*p): 42
After *p = 100, x = 100
```

## Key Concepts

- `&` takes the address of a variable → produces a pointer
- `*` dereferences a pointer → reads the value at that address
- Go **automatically dereferences** struct pointers: `ptr.Field` works, no need for `(*ptr).Field`
- **Value receiver**: operates on a copy — original unchanged
- **Pointer receiver**: operates on original — modifications persist

## Test Your Understanding

```go
// What does this print?
func main() {
    n := 42
    defer func() { fmt.Println(n) }()
    n = 100
}
```

## Next Step

Move to **Exercise 04: Collections**.
