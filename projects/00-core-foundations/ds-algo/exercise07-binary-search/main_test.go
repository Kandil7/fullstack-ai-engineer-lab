package main

import "testing"

func TestBinarySearchIterative(t *testing.T) {
	arr := []int{1, 3, 5, 7, 9, 11, 13, 15}
	tests := []struct {
		target, expected int
	}{
		{7, 3},
		{1, 0},
		{15, 7},
		{99, -1},
		{0, -1},
	}
	for _, tt := range tests {
		if got := binarySearchIterative(arr, tt.target); got != tt.expected {
			t.Errorf("binarySearchIterative(%v, %d) = %d; want %d",
				arr, tt.target, got, tt.expected)
		}
	}
}

func TestBinarySearchIterative_Empty(t *testing.T) {
	if got := binarySearchIterative([]int{}, 5); got != -1 {
		t.Errorf("expected -1 for empty array, got %d", got)
	}
}

func TestBinarySearchRecursive(t *testing.T) {
	arr := []int{1, 3, 5, 7, 9, 11, 13, 15}
	if got := binarySearchRecursive(arr, 7, 0, len(arr)-1); got != 3 {
		t.Errorf("expected 3, got %d", got)
	}
	if got := binarySearchRecursive(arr, 99, 0, len(arr)-1); got != -1 {
		t.Errorf("expected -1, got %d", got)
	}
}

func TestSearchRotatedArray(t *testing.T) {
	arr := []int{4, 5, 6, 7, 0, 1, 2}
	tests := []struct {
		target, expected int
	}{
		{0, 4},
		{3, -1},
		{4, 0},
		{2, 6},
		{7, 3},
	}
	for _, tt := range tests {
		if got := searchRotatedArray(arr, tt.target); got != tt.expected {
			t.Errorf("searchRotatedArray(%v, %d) = %d; want %d",
				arr, tt.target, got, tt.expected)
		}
	}
}

func TestFindPeakElement(t *testing.T) {
	tests := []struct {
		arr      []int
		expected int // any peak is valid, just check value > neighbors
	}{
		{[]int{1, 2, 3, 1}, 2},
		{[]int{1, 2, 1, 3, 5, 6, 4}, 5}, // arr[5] = 6 is a peak
		{[]int{1}, 0},
		{[]int{1, 2}, 1},
	}
	for _, tt := range tests {
		got := findPeakElement(tt.arr)
		if tt.expected >= 0 && tt.arr[got] != tt.arr[tt.expected] {
			// Just check it's a valid peak (>= neighbors)
			isPeak := true
			if got > 0 && tt.arr[got] < tt.arr[got-1] {
				isPeak = false
			}
			if got < len(tt.arr)-1 && tt.arr[got] < tt.arr[got+1] {
				isPeak = false
			}
			if !isPeak {
				t.Errorf("findPeakElement(%v) = %d (val=%d), not a peak", tt.arr, got, tt.arr[got])
			}
		}
	}
}

func TestSqrt(t *testing.T) {
	tests := []struct {
		x, expected int
	}{
		{0, 0},
		{1, 1},
		{4, 2},
		{8, 2}, // floor sqrt
		{16, 4},
		{25, 5},
		{100, 10},
		{-1, -1},
	}
	for _, tt := range tests {
		if got := sqrt(tt.x); got != tt.expected {
			t.Errorf("sqrt(%d) = %d; want %d", tt.x, got, tt.expected)
		}
	}
}
