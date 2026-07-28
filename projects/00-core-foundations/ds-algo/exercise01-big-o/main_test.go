package main

import (
	"reflect"
	"testing"
)

func TestConstantAccess(t *testing.T) {
	arr := []int{10, 20, 30}
	if val := constantAccess(arr, 1); val != 20 {
		t.Errorf("expected 20, got %d", val)
	}
}

func TestLinearSum(t *testing.T) {
	if sum := linearSum([]int{1, 2, 3, 4, 5}); sum != 15 {
		t.Errorf("expected 15, got %d", sum)
	}
	if sum := linearSum([]int{}); sum != 0 {
		t.Errorf("expected 0 for empty slice, got %d", sum)
	}
}

func TestLogarithmicBinarySearch(t *testing.T) {
	sorted := []int{1, 3, 5, 7, 9, 11, 13}
	tests := []struct {
		target, expected int
	}{
		{7, 3},
		{1, 0},
		{13, 6},
		{99, -1},
	}
	for _, tt := range tests {
		if idx := logarithmicBinarySearch(sorted, tt.target); idx != tt.expected {
			t.Errorf("search(%d) = %d; want %d", tt.target, idx, tt.expected)
		}
	}
}

func TestQuadraticBubbleSort(t *testing.T) {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	expected := []int{11, 12, 22, 25, 34, 64, 90}
	quadraticBubbleSort(arr)
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestLinearithmicMergeSort(t *testing.T) {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	expected := []int{3, 9, 10, 27, 38, 43, 82}
	result := linearithmicMergeSort(arr)
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}

func TestExponentialFib(t *testing.T) {
	tests := []struct{ n, expected int }{
		{0, 0},
		{1, 1},
		{5, 5},
		{10, 55},
	}
	for _, tt := range tests {
		if result := exponentialFib(tt.n); result != tt.expected {
			t.Errorf("fib(%d) = %d; want %d", tt.n, result, tt.expected)
		}
	}
}

func BenchmarkLinearSum(b *testing.B) {
	arr := make([]int, 1000)
	for i := range arr {
		arr[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		linearSum(arr)
	}
}

func BenchmarkExponentialFib(b *testing.B) {
	for i := 0; i < b.N; i++ {
		exponentialFib(20)
	}
}
