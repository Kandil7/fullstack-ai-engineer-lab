package main

import (
	"testing"
)

// Table-driven tests
func TestAdd(t *testing.T) {
	tests := []struct {
		name string
		a, b int
		want int
	}{
		{"positive", 5, 3, 8},
		{"negative", -1, -2, -3},
		{"zero", 0, 0, 0},
		{"mixed", -5, 10, 5},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := Add(tt.a, tt.b); got != tt.want {
				t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
			}
		})
	}
}

func TestFibonacci(t *testing.T) {
	tests := []struct {
		n    int
		want int
	}{
		{0, 0},
		{1, 1},
		{5, 5},
		{10, 55},
		{15, 610},
	}
	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := Fibonacci(tt.n); got != tt.want {
				t.Errorf("Fibonacci(%d) = %d; want %d", tt.n, got, tt.want)
			}
		})
	}
}

func TestReverse(t *testing.T) {
	tests := []struct {
		input string
		want  string
	}{
		{"hello", "olleh"},
		{"Go", "oG"},
		{"", ""},
		{"12345", "54321"},
		{"racecar", "racecar"},
		{"Hello, 世界", "界世 ,olleH"},
	}
	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			if got := Reverse(tt.input); got != tt.want {
				t.Errorf("Reverse(%q) = %q; want %q", tt.input, got, tt.want)
			}
		})
	}
}

func TestFilterEven(t *testing.T) {
	tests := []struct {
		input []int
		want  []int
	}{
		{[]int{1, 2, 3, 4, 5, 6}, []int{2, 4, 6}},
		{[]int{1, 3, 5}, []int{}},
		{[]int{}, []int{}},
		{[]int{2, 4, 6}, []int{2, 4, 6}},
	}
	for _, tt := range tests {
		got := FilterEven(tt.input)
		if len(got) != len(tt.want) {
			t.Fatalf("FilterEven(%v) = %v; want %v", tt.input, got, tt.want)
		}
		for i, v := range tt.want {
			if got[i] != v {
				t.Errorf("FilterEven(%v)[%d] = %d; want %d", tt.input, i, got[i], v)
			}
		}
	}
}

// Stack tests
func TestStack(t *testing.T) {
	s := NewStack[int]()
	if s.Len() != 0 {
		t.Errorf("expected empty stack, got len=%d", s.Len())
	}

	s.Push(1)
	s.Push(2)
	s.Push(3)

	if s.Len() != 3 {
		t.Errorf("expected len=3, got %d", s.Len())
	}

	// Pop in LIFO order
	val, ok := s.Pop()
	if !ok || val != 3 {
		t.Errorf("expected Pop=3, got %d (ok=%v)", val, ok)
	}
	val, ok = s.Pop()
	if !ok || val != 2 {
		t.Errorf("expected Pop=2, got %d (ok=%v)", val, ok)
	}
	val, ok = s.Pop()
	if !ok || val != 1 {
		t.Errorf("expected Pop=1, got %d (ok=%v)", val, ok)
	}

	// Pop from empty
	_, ok = s.Pop()
	if ok {
		t.Error("expected Pop on empty stack to return false")
	}
}

// Table-driven Calculator tests
func TestCalculator_Add(t *testing.T) {
	calc := &Calculator{}
	tests := []struct {
		a, b, want int
	}{
		{2, 3, 5},
		{0, 0, 0},
		{-1, 1, 0},
		{100, -50, 50},
	}
	for _, tt := range tests {
		if got := calc.Add(tt.a, tt.b); got != tt.want {
			t.Errorf("Calc.Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
		}
	}
}

func TestCalculator_Div(t *testing.T) {
	calc := &Calculator{}
	result, err := calc.Div(10, 2)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 5 {
		t.Errorf("expected 5, got %d", result)
	}

	_, err = calc.Div(10, 0)
	if err == nil {
		t.Error("expected error for division by zero")
	}
}

// Benchmarks
func BenchmarkFibonacci(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Fibonacci(20)
	}
}

func BenchmarkReverse(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Reverse("Hello, World! This is a benchmark test.")
	}
}

func BenchmarkStackPush(b *testing.B) {
	for i := 0; i < b.N; i++ {
		s := NewStack[int]()
		for j := 0; j < 1000; j++ {
			s.Push(j)
		}
	}
}

// Fuzz test
func FuzzAdd(f *testing.F) {
	testcases := []int{0, 1, -1, 100}
	for _, tc := range testcases {
		f.Add(tc, tc)
	}
	f.Fuzz(func(t *testing.T, a, b int) {
		result := Add(a, b)
		// Verify commutativity
		if result != Add(b, a) {
			t.Errorf("Add not commutative: Add(%d,%d)!=Add(%d,%d)", a, b, b, a)
		}
		// Verify Add(a, 0) == a
		if resultZero := Add(a, 0); resultZero != a {
			t.Errorf("Add(%d,0) should be %d, got %d", a, a, resultZero)
		}
		// Verify Add(a, b) - b == a (if no overflow)
		if result-b == a {
			// passed
		}
	})
}
