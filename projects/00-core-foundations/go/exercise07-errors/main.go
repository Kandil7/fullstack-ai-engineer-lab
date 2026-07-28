package main

import (
	"errors"
	"fmt"
	"os"
)

func main() {
	fmt.Println("=== Exercise 06: Error Handling ===")

	// 1. Basic error handling
	fmt.Println("--- 1. Basic Error Handling ---")
	result, err := divide(10, 2)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("10 / 2 =", result)
	}

	// Division by zero
	_, err = divide(10, 0)
	if err != nil {
		fmt.Println("Expected error:", err)
	}

	// 2. Sentinel errors
	fmt.Println("\n--- 2. Sentinel Errors ---")
	err = doSomething()
	if errors.Is(err, ErrNotFound) {
		fmt.Println("Item not found (sentinel check)")
	} else if errors.Is(err, ErrPermission) {
		fmt.Println("Permission denied")
	}

	// 3. Error wrapping
	fmt.Println("\n--- 3. Error Wrapping ---")
	err = processFile("nonexistent.txt")
	if err != nil {
		fmt.Println("Wrapped error:", err)
		// Unwrap to check root cause
		if errors.Is(err, os.ErrNotExist) {
			fmt.Println("Root cause: file doesn't exist")
		}
	}

	// 4. Custom error types
	fmt.Println("\n--- 4. Custom Error Types ---")
	err = validateUser("")
	if err != nil {
		var ve *ValidationError
		if errors.As(err, &ve) {
			fmt.Printf("Validation failed for field: %s, reason: %s\n", ve.Field, ve.Reason)
		}
	}

	// 5. Multiple error wrapping (errors.Join in Go 1.20+)
	fmt.Println("\n--- 5. Multiple Errors (Go 1.20+) ---")
	err1 := errors.New("error 1")
	err2 := errors.New("error 2")
	combined := errors.Join(err1, err2)
	fmt.Println("Combined:", combined)
	if errors.Is(combined, err1) {
		fmt.Println("Contains err1")
	}

	// 6. Panic and recover
	fmt.Println("\n--- 6. Panic and Recover ---")
	safeOperation()
	fmt.Println("After panic recovery, program continues")

	// 7. Best practices
	fmt.Println("\n--- 7. Best Practices ---")
	// Check errors immediately
	_ = doWork()

	// Don't ignore errors!
	// Bad: _ = doWork()
	// Good:
	if err := doWork(); err != nil {
		fmt.Println("Work failed:", err)
	}

	// Add context when wrapping
	err = readConfig()
	if err != nil {
		// Wrap with context
		err = fmt.Errorf("reading config: %w", err)
		fmt.Println("With context:", err)
	}
}

func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}
	return a / b, nil
}

// Sentinel errors
var (
	ErrNotFound   = errors.New("not found")
	ErrPermission = errors.New("permission denied")
)

func doSomething() error {
	return ErrNotFound
}

// Error wrapping
func processFile(filename string) error {
	_, err := os.Open(filename)
	if err != nil {
		return fmt.Errorf("opening %s: %w", filename, err)
	}
	return nil
}

// Custom error type
type ValidationError struct {
	Field  string
	Reason string
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("validation error on field %s: %s", e.Field, e.Reason)
}

func validateUser(email string) error {
	if email == "" {
		return &ValidationError{Field: "email", Reason: "required"}
	}
	if len(email) < 3 {
		return &ValidationError{Field: "email", Reason: "too short"}
	}
	return nil
}

func safeOperation() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered from panic:", r)
		}
	}()
	panic("something went wrong!")
}

func doWork() error {
	return errors.New("work failed")
}

func readConfig() error {
	return os.ErrNotExist
}
