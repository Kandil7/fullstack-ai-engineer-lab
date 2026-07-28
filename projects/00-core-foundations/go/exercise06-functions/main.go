package main

import (
	"fmt"
)

func main() {
	fmt.Println("=== Exercise 06: Functions ===")

	// 1. Basic function
	fmt.Println("--- 1. Basic Function ---")
	fmt.Println("add(3, 5) =", add(3, 5))

	// 2. Multiple return values
	fmt.Println("\n--- 2. Multiple Return Values ---")
	q, r := divmod(17, 5)
	fmt.Printf("17 / 5 = %d remainder %d\n", q, r)

	// 3. Named return values
	fmt.Println("\n--- 3. Named Return Values ---")
	x, y := split(10)
	fmt.Printf("split(10) = (%d, %d)\n", x, y)

	// 4. Variadic functions
	fmt.Println("\n--- 4. Variadic Functions ---")
	fmt.Println("sum(1, 2, 3) =", sum(1, 2, 3))
	fmt.Println("sum(1..5) =", sum(1, 2, 3, 4, 5))
	nums := []int{10, 20, 30}
	fmt.Println("sum(slice...) =", sum(nums...))

	// 5. Function as value (first-class functions)
	fmt.Println("\n--- 5. Functions as Values ---")
	f := square
	fmt.Println("square(4) via variable:", f(4))

	// Function as parameter
	apply(3, square)
	apply(3, func(x int) int { return x * x * x })

	// 6. Closures
	fmt.Println("\n--- 6. Closures ---")
	counter := makeCounter()
	fmt.Println("counter():", counter())
	fmt.Println("counter():", counter())
	fmt.Println("counter():", counter())

	// Closure capturing loop variable (common pitfall)
	fmt.Println("Closures in loop:")
	funcs := make([]func(), 3)
	for i := 0; i < 3; i++ {
		val := i // capture current value
		funcs[i] = func() { fmt.Println("  captured:", val) }
	}
	for _, fn := range funcs {
		fn()
	}

	// 7. Defer in functions
	fmt.Println("\n--- 7. Defer ---")
	fmt.Println("deferDemo():", deferDemo())

	// 8. Function types
	fmt.Println("\n--- 8. Function Types ---")
	type MathFunc func(int, int) int
	var op MathFunc = add
	fmt.Println("MathFunc variable:", op(10, 5))

	ops := map[string]MathFunc{
		"add": add,
		"sub": func(a, b int) int { return a - b },
		"mul": func(a, b int) int { return a * b },
	}
	fmt.Println("Map of functions:", ops["add"](3, 4), ops["mul"](3, 4))

	// 9. Methods vs Functions
	fmt.Println("\n--- 9. Methods ---")
	p := Point{X: 3, Y: 4}
	fmt.Println("Point:", p)
	fmt.Println("Distance from origin:", p.Distance())

	// 10. Method with pointer receiver
	p.Scale(2)
	fmt.Println("After Scale(2):", p)
}

// Basic function
func add(a, b int) int {
	return a + b
}

// Multiple return values
func divmod(a, b int) (quotient, remainder int) {
	quotient = a / b
	remainder = a % b
	return
}

// Named return values
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

// Variadic function
func sum(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

// Function as parameter
func apply(x int, f func(int) int) {
	fmt.Printf("  apply(%d, f) = %d\n", x, f(x))
}

func square(x int) int {
	return x * x
}

// Closure
func makeCounter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

// Defer demonstration
func deferDemo() (result int) {
	defer func() { result *= 2 }()
	result = 5
	return // returns 10
}

// Struct with methods
type Point struct {
	X, Y float64
}

// Value receiver
func (p Point) Distance() float64 {
	return sqrt(p.X*p.X + p.Y*p.Y)
}

// Pointer receiver (modifies original)
func (p *Point) Scale(factor float64) {
	p.X *= factor
	p.Y *= factor
}

func sqrt(x float64) float64 {
	return x // simplified
}
