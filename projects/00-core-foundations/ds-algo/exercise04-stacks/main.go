package main

import "fmt"

// Stack implementation
type Stack struct {
	items []int
}

func NewStack() *Stack {
	return &Stack{items: make([]int, 0)}
}

func (s *Stack) Push(item int) {
	s.items = append(s.items, item)
}

func (s *Stack) Pop() (int, bool) {
	if len(s.items) == 0 {
		return 0, false
	}
	item := s.items[len(s.items)-1]
	s.items = s.items[:len(s.items)-1]
	return item, true
}

func (s *Stack) Peek() (int, bool) {
	if len(s.items) == 0 {
		return 0, false
	}
	return s.items[len(s.items)-1], true
}

func (s *Stack) IsEmpty() bool {
	return len(s.items) == 0
}

// isValidBrackets checks if brackets are properly matched
func isValidBrackets(s string) bool {
	runes := []rune(s)
	var stack []rune
	pairs := map[rune]rune{
		')': '(',
		'}': '{',
		']': '[',
	}

	for _, r := range runes {
		switch r {
		case '(', '{', '[':
			stack = append(stack, r)
		case ')', '}', ']':
			if len(stack) == 0 || stack[len(stack)-1] != pairs[r] {
				return false
			}
			stack = stack[:len(stack)-1]
		}
	}
	return len(stack) == 0
}

// nextGreaterElement finds the next greater element for each array element
func nextGreaterElement(arr []int) []int {
	result := make([]int, len(arr))
	for i := range result {
		result[i] = -1
	}
	stack := make([]int, 0) // store indices

	for i := 0; i < len(arr); i++ {
		for len(stack) > 0 && arr[i] > arr[stack[len(stack)-1]] {
			result[stack[len(stack)-1]] = arr[i]
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, i)
	}
	return result
}

// decimalToBinary converts a decimal number to binary using a stack
func decimalToBinary(n int) string {
	if n == 0 {
		return "0"
	}
	stack := NewStack()
	for n > 0 {
		stack.Push(n % 2)
		n /= 2
	}
	result := ""
	for !stack.IsEmpty() {
		val, _ := stack.Pop()
		result += fmt.Sprintf("%d", val)
	}
	return result
}

func main() {
	fmt.Println("=== Stacks Exercise ===")
	fmt.Println()

	// Bracket validation
	fmt.Println("--- Bracket Validation ---")
	tests := []string{
		"()",
		"()[]{}",
		"(]",
		"([)]",
		"{[]}",
	}
	for _, s := range tests {
		fmt.Printf("  isValidBrackets(%q) = %v\n", s, isValidBrackets(s))
	}

	// Next greater element
	fmt.Println("\n--- Next Greater Element ---")
	arr := []int{4, 5, 2, 25}
	fmt.Printf("  arr = %v\n", arr)
	fmt.Printf("  NGE = %v\n", nextGreaterElement(arr))

	// Decimal to binary
	fmt.Println("\n--- Decimal to Binary ---")
	for _, n := range []int{0, 1, 5, 10, 42, 255} {
		fmt.Printf("  decimalToBinary(%d) = %s\n", n, decimalToBinary(n))
	}
}
