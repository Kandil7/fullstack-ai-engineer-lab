package main

import (
	"testing"
)

func TestAdd(t *testing.T) {
	tests := []struct {
		a, b, expected int
	}{
		{3, 5, 8},
		{0, 0, 0},
		{-1, 1, 0},
		{100, -50, 50},
	}
	for _, tt := range tests {
		result := add(tt.a, tt.b)
		if result != tt.expected {
			t.Errorf("add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
		}
	}
}

func TestDivmod(t *testing.T) {
	q, r := divmod(17, 5)
	if q != 3 || r != 2 {
		t.Errorf("divmod(17,5) = (%d, %d); want (3, 2)", q, r)
	}
}

func TestSplit(t *testing.T) {
	x, y := split(10)
	sum := x + y
	if sum != 10 {
		t.Errorf("split(10) = (%d, %d); sum should be 10", x, y)
	}
}

func TestSumVariadic(t *testing.T) {
	tests := []struct {
		nums     []int
		expected int
	}{
		{[]int{1, 2, 3}, 6},
		{[]int{}, 0},
		{[]int{10, -10, 5}, 5},
	}
	for _, tt := range tests {
		result := sum(tt.nums...)
		if result != tt.expected {
			t.Errorf("sum(%v) = %d; want %d", tt.nums, result, tt.expected)
		}
	}
}

func TestCounterClosure(t *testing.T) {
	counter := makeCounter()
	values := []int{counter(), counter(), counter()}
	expected := []int{1, 2, 3}
	for i, v := range expected {
		if values[i] != v {
			t.Errorf("counter() iteration %d = %d; want %d", i, values[i], v)
		}
	}
}

func TestDeferDemo(t *testing.T) {
	result := deferDemo()
	if result != 10 {
		t.Errorf("deferDemo() = %d; want 10 (defer doubles the return)", result)
	}
}

func TestPointScale(t *testing.T) {
	p := Point{X: 3, Y: 4}
	p.Scale(2)
	if p.X != 6 || p.Y != 8 {
		t.Errorf("After Scale(2): (%f, %f); want (6, 8)", p.X, p.Y)
	}
}

func TestApply(t *testing.T) {
	// apply just prints; verify it doesn't panic
	apply(3, square)
	apply(3, func(x int) int { return x * x * x })
}

func BenchmarkSum(b *testing.B) {
	nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	for i := 0; i < b.N; i++ {
		sum(nums...)
	}
}
