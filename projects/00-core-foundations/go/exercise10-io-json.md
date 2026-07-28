# Exercise 10: I/O and JSON

> Master file I/O, the `io.Reader`/`io.Writer` interfaces, and JSON marshaling/unmarshaling.

## Goal

Read/write files, work with streaming I/O, and serialize/deserialize JSON with custom types.

## Requirements

Create a Go program that demonstrates:
1. **File I/O**: `os.ReadFile`, `os.WriteFile`, file permissions
2. **`io.Reader`**: Reading from strings, files into a buffer
3. **`io.Writer`**: Writing to strings.Builder, files
4. **JSON marshal**: `json.Marshal`, `json.MarshalIndent` with struct tags
5. **JSON unmarshal**: Parse JSON string into Go struct
6. **JSON streaming**: `json.Decoder` for newline-delimited JSON
7. **Custom JSON marshaling**: Implement `MarshalJSON`/`UnmarshalJSON`
8. **Directory operations**: `os.ReadDir`, `os.CreateTemp`, file info
9. **Standard streams**: `os.Stdout`, `os.Stderr` as writers

## Expected Output

```
=== Exercise 10: I/O and JSON ===
--- 1. Standard Input/Output ---
Enter your name: Alice
Hello, Alice

--- 2. File I/O ---
File written
File content:
Hello, Go!
```

## JSON Struct Tags

```go
type User struct {
    ID        int      `json:"id"`
    Name      string   `json:"name"`
    Email     string   `json:"email,omitempty"`  // Omit if empty
    Password  string   `json:"-"`                // Always omit
}
```

## Next Step

Move to **Exercise 11: Testing**.
