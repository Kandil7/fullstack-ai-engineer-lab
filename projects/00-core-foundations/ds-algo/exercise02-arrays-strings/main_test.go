package main

import (
	"reflect"
	"testing"
)

func TestIsPalindrome(t *testing.T) {
	tests := []struct {
		input string
		want  bool
	}{
		{"racecar", true},
		{"hello", false},
		{"a", true},
		{"", true},
		{"golang", false},
	}
	for _, tt := range tests {
		if got := isPalindrome(tt.input); got != tt.want {
			t.Errorf("isPalindrome(%q) = %v; want %v", tt.input, got, tt.want)
		}
	}
}

func TestReverseString(t *testing.T) {
	tests := []struct {
		input, want string
	}{
		{"hello", "olleh"},
		{"Go", "oG"},
		{"", ""},
		{"a", "a"},
	}
	for _, tt := range tests {
		if got := reverseString(tt.input); got != tt.want {
			t.Errorf("reverseString(%q) = %q; want %q", tt.input, got, tt.want)
		}
	}
}

func TestMaxSubarraySum(t *testing.T) {
	tests := []struct {
		arr []int
		k   int
		want int
	}{
		{[]int{2, 1, 5, 1, 3, 2}, 3, 9},
		{[]int{1, 2, 3, 4, 5}, 2, 9},
		{[]int{1, 2, 3}, 5, 0},    // k > len
		{[]int{1, 2, 3}, 0, 0},    // k = 0
	}
	for _, tt := range tests {
		if got := maxSubarraySum(tt.arr, tt.k); got != tt.want {
			t.Errorf("maxSubarraySum(%v, %d) = %d; want %d", tt.arr, tt.k, got, tt.want)
		}
	}
}

func TestRemoveDuplicates(t *testing.T) {
	arr := []int{0, 0, 1, 1, 1, 2, 2, 3, 3, 4}
	got := removeDuplicates(arr)
	want := []int{0, 1, 2, 3, 4}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("removeDuplicates = %v; want %v", got, want)
	}
}

func TestRotateArray(t *testing.T) {
	tests := []struct {
		arr []int
		k   int
		want []int
	}{
		{[]int{1, 2, 3, 4, 5, 6, 7}, 3, []int{5, 6, 7, 1, 2, 3, 4}},
		{[]int{-1, -100, 3, 99}, 2, []int{3, 99, -1, -100}},
		{[]int{1, 2}, 3, []int{2, 1}}, // k > len
	}
	for _, tt := range tests {
		rotateArray(tt.arr, tt.k)
		if !reflect.DeepEqual(tt.arr, tt.want) {
			t.Errorf("rotateArray(%v, %d) = %v; want %v", tt.arr, tt.k, tt.arr, tt.want)
		}
	}
}
