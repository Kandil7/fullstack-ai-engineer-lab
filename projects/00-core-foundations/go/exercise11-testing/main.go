package main

import "fmt"

// Add adds two integers
func Add(a, b int) int {
	return a + b
}

// Fibonacci calculates nth Fibonacci number recursively (inefficient on purpose for benchmarking)
func Fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return Fibonacci(n-1) + Fibonacci(n-2)
}

// Reverse reverses a string
func Reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// FilterEven returns only even numbers from slice
func FilterEven(nums []int) []int {
	var result []int
	for _, n := range nums {
		if n%2 == 0 {
			result = append(result, n)
		}
	}
	return result
}

// Stack is a simple generic stack implementation
type Stack[T any] struct {
	items []T
}

func NewStack[T any]() *Stack[T] {
	return &Stack[T]{items: make([]T, 0)}
}

func (s *Stack[T]) Push(item T) {
	s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
	if len(s.items) == 0 {
		var zero T
		return zero, false
	}
	item := s.items[len(s.items)-1]
	s.items = s.items[:len(s.items)-1]
	return item, true
}

func (s *Stack[T]) Len() int {
	return len(s.items)
}

// Calculator demonstrates table-driven tests with different operations
type Calculator struct{}

func (c *Calculator) Add(a, b int) int { return a + b }
func (c *Calculator) Sub(a, b int) int { return a - b }
func (c *Calculator) Mul(a, b int) int { return a * b }
func (c *Calculator) Div(a, b int) (int, error) {
	if b == 0 {
		return 0, ErrDivByZero
	}
	return a / b, nil
}

var ErrDivByZero = NewError("division by zero")

type Error string

func (e Error) Error() string {
	return string(e)
}

func NewError(msg string) Error {
	return Error(msg)
}

func main() {
	fmt.Println("=== Exercise 11: Testing ====")
	fmt.Println()
	fmt.Println("This exercise is designed to be tested, not run directly.")
	fmt.Println("Run: go test -v")
	fmt.Println("     go test -bench=.")
	fmt.Println("     go test -fuzz=FuzzAdd -fuzztime=5s")
	fmt.Println()
	fmt.Println("Demo:")
	fmt.Printf("  Add(5, 3) = %d\n", Add(5, 3))
	fmt.Printf("  Fibonacci(10) = %d\n", Fibonacci(10))
	fmt.Printf("  Reverse(\"hello\") = %s\n", Reverse("hello"))
	fmt.Printf("  FilterEven([1,2,3,4,5,6]) = %v\n", FilterEven([]int{1, 2, 3, 4, 5, 6}))

	s := NewStack[int]()
	s.Push(1)
	s.Push(2)
	fmt.Printf("  Stack len: %d\n", s.Len())
	val, _ := s.Pop()
	fmt.Printf("  Stack pop: %d\n", val)

	calc := &Calculator{}
	fmt.Printf("  Calc Div(10, 2) = %d\n", func() int { r, _ := calc.Div(10, 2); return r }())
}
