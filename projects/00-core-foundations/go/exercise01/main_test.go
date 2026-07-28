package main

import "testing"

func TestAdd(t *testing.T) {
	// Table-driven tests
	tests := []struct {
		a, b, expected int
	}{
		{2, 3, 5},
		{0, 0, 0},
		{-1, 1, 0},
		{100, 200, 300},
		{-5, -3, -8},
	}

	for _, tt := range tests {
		result := add(tt.a, tt.b)
		if result != tt.expected {
			t.Errorf("add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
		}
	}
}

func TestToUpper(t *testing.T) {
	tests := []struct {
		input, expected string
	}{
		{"hello", "HELLO"},
		{"Go", "GO"},
		{"123", "123"},
		{"already UPPER", "ALREADY UPPER"},
		{"", ""},
	}

	for _, tt := range tests {
		result := toUpper(tt.input)
		if result != tt.expected {
			t.Errorf("toUpper(%q) = %q; want %q", tt.input, result, tt.expected)
		}
	}
}

func BenchmarkAdd(b *testing.B) {
	for i := 0; i < b.N; i++ {
		add(5, 3)
	}
}

func BenchmarkToUpper(b *testing.B) {
	for i := 0; i < b.N; i++ {
		toUpper("hello world")
	}
}
