package main

import (
	"fmt"
	"strings"
)

// Declare variables of different types
var (
	appName   string  = "Go Exercises"
	version   int     = 1
	pi        float64 = 3.14159
	isReady   bool    = true
)

// add adds two integers and returns the sum
func add(a int, b int) int {
	return a + b
}

// toUpper converts a string to uppercase using strings.ToUpper
func toUpper(s string) string {
	return strings.ToUpper(s)
}

func main() {
	fmt.Println("=== Exercise 01: Hello World + Basic Types ===")
	fmt.Println()

	// Print variables
	fmt.Printf("Application: %s (v%d)\n", appName, version)
	fmt.Printf("Pi: %.5f\n", pi)
	fmt.Printf("Ready: %v\n", isReady)
	fmt.Println()

	// Test our functions
	sum := add(5, 3)
	fmt.Printf("%d + %d = %d\n", 5, 3, sum)

	upper := toUpper("hello")
	fmt.Printf("%s -> %s\n", "hello", upper)
	fmt.Println()

	// Demonstrate short variable declaration (:=)
	message := "Short declaration in Go"
	count := 42
	fmt.Printf("Message: %s (count: %d)\n", message, count)

	// Demonstrate zero values
	var (
		zeroInt    int
		zeroStr    string
		zeroBool   bool
		zeroFloat  float64
	)
	fmt.Println("\nZero values:")
	fmt.Printf("  int:    %d\n", zeroInt)
	fmt.Printf("  string: %q\n", zeroStr)
	fmt.Printf("  bool:   %v\n", zeroBool)
	fmt.Printf("  float64: %.1f\n", zeroFloat)

	fmt.Println("\n✅ Exercise 01 complete!")
}
