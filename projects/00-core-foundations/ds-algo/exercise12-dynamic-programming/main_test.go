package main

import "testing"

func TestFibonacci(t *testing.T) {
	tests := []struct {
		n, expected int
	}{
		{0, 0},
		{1, 1},
		{5, 5},
		{10, 55},
		{20, 6765},
	}
	for _, tt := range tests {
		if got := Fibonacci(tt.n); got != tt.expected {
			t.Errorf("Fibonacci(%d) = %d; want %d", tt.n, got, tt.expected)
		}
	}
}

func TestFibTab(t *testing.T) {
	tests := []struct {
		n, expected int
	}{
		{0, 0},
		{1, 1},
		{10, 55},
		{30, 832040},
	}
	for _, tt := range tests {
		if got := fibTab(tt.n); got != tt.expected {
			t.Errorf("fibTab(%d) = %d; want %d", tt.n, got, tt.expected)
		}
	}
}

func TestKnapsack(t *testing.T) {
	weights := []int{2, 3, 4, 5}
	values := []int{3, 4, 5, 6}

	tests := []struct {
		W, expected int
	}{
		{5, 7},  // items 0 and 1 (2+3=5 weight, 3+4=7 value)
		{10, 13}, // items 0+1+3: 2+3+5=10 weight, 3+4+6=13 value
		{0, 0},
	}
	for _, tt := range tests {
		if got := knapsack(weights, values, tt.W); got != tt.expected {
			t.Errorf("knapsack(W=%d) = %d; want %d", tt.W, got, tt.expected)
		}
	}
}

func TestLCS(t *testing.T) {
	tests := []struct {
		a, b     string
		expected int
	}{
		{"ABCDGH", "AEDFHR", 3}, // ADH
		{"AGGTAB", "GXTXAYB", 4}, // GTAB
		{"", "ABC", 0},
		{"ABC", "", 0},
		{"A", "A", 1},
		{"ABC", "DEF", 0},
	}
	for _, tt := range tests {
		if got := LCS(tt.a, tt.b); got != tt.expected {
			t.Errorf("LCS(%q, %q) = %d; want %d", tt.a, tt.b, got, tt.expected)
		}
	}
}

func TestCoinChange(t *testing.T) {
	tests := []struct {
		coins    []int
		amount   int
		expected int
	}{
		{[]int{1, 2, 5}, 11, 3},  // 5+5+1
		{[]int{2}, 3, -1},        // impossible
		{[]int{1}, 0, 0},         // zero amount
		{[]int{1, 3, 4}, 6, 2},   // 3+3
	}
	for _, tt := range tests {
		if got := coinChange(tt.coins, tt.amount); got != tt.expected {
			t.Errorf("coinChange(%v, %d) = %d; want %d", tt.coins, tt.amount, got, tt.expected)
		}
	}
}

func BenchmarkFibonacci(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Fibonacci(30)
	}
}

func BenchmarkKnapsack(b *testing.B) {
	weights := []int{2, 3, 4, 5, 6, 7, 8, 9}
	values := []int{3, 4, 5, 6, 7, 8, 9, 10}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		knapsack(weights, values, 50)
	}
}
