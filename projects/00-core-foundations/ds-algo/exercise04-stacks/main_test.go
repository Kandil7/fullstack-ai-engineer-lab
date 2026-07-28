package main

import (
	"reflect"
	"testing"
)

func TestStack(t *testing.T) {
	s := NewStack()
	if !s.IsEmpty() {
		t.Error("expected new stack to be empty")
	}
	s.Push(1)
	s.Push(2)
	s.Push(3)

	val, ok := s.Pop()
	if !ok || val != 3 {
		t.Errorf("expected Pop() = 3, got %d", val)
	}
	val, ok = s.Peek()
	if !ok || val != 2 {
		t.Errorf("expected Peek() = 2, got %d", val)
	}
}

func TestStackEmptyPop(t *testing.T) {
	s := NewStack()
	_, ok := s.Pop()
	if ok {
		t.Error("expected Pop() on empty stack to return false")
	}
	_, ok = s.Peek()
	if ok {
		t.Error("expected Peek() on empty stack to return false")
	}
}

func TestIsValidBrackets(t *testing.T) {
	tests := []struct {
		input string
		want  bool
	}{
		{"()", true},
		{"()[]{}", true},
		{"(]", false},
		{"([)]", false},
		{"{[]}", true},
		{"", true},
		{"(", false},
		{")", false},
	}
	for _, tt := range tests {
		if got := isValidBrackets(tt.input); got != tt.want {
			t.Errorf("isValidBrackets(%q) = %v; want %v", tt.input, got, tt.want)
		}
	}
}

func TestNextGreaterElement(t *testing.T) {
	arr := []int{4, 5, 2, 25}
	want := []int{5, 25, 25, -1}
	got := nextGreaterElement(arr)
	if !reflect.DeepEqual(got, want) {
		t.Errorf("nextGreaterElement(%v) = %v; want %v", arr, got, want)
	}
}

func TestDecimalToBinary(t *testing.T) {
	tests := []struct {
		n    int
		want string
	}{
		{0, "0"},
		{1, "1"},
		{5, "101"},
		{10, "1010"},
		{42, "101010"},
		{255, "11111111"},
	}
	for _, tt := range tests {
		if got := decimalToBinary(tt.n); got != tt.want {
			t.Errorf("decimalToBinary(%d) = %s; want %s", tt.n, got, tt.want)
		}
	}
}
