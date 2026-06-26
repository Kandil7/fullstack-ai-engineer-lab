# Exercise 01: Hello World + Basic Types

> Complete the Go Tour basics, then write this exercise yourself.

## Goal

Practice Go fundamentals: variables, types, imports, basic functions.

## Requirements

Create a Go program that:

1. Declares variables of different types (string, int, float64, bool)
2. Prints them with `fmt.Println`
3. Has a function that takes two numbers and returns their sum
4. Has a function that takes a string and returns it in uppercase
5. Has a main function that calls both and prints results

## Starter Code

```go
package main

import "fmt"

// Add your variables here

// Write a function that adds two integers
func add(a int, b int) int {
    // your code here
}

// Write a function that converts string to uppercase
func toUpper(s string) string {
    // your code here
}

func main() {
    // Test your functions here
    fmt.Println("Hello, Go!")
}
```

## Expected Output

```text
Hello, Go!
5 + 3 = 8
hello → HELLO
```

## Self-Check

After writing this, can you explain:
- What is `package main`?
- What is `import "fmt"`?
- What is the difference between `:=` and `=`?
- What is a function signature?

## Next Step

When this works, create `exercise02_test.go` and write a test for your `add` function.
