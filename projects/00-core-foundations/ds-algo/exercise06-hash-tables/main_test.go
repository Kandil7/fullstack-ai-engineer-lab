package main

import (
	"reflect"
	"testing"
)

func TestHashTable(t *testing.T) {
	ht := NewHashTable(10)

	// Put and Get
	ht.Put("key1", 100)
	val, ok := ht.Get("key1")
	if !ok || val != 100 {
		t.Errorf("expected (100, true), got (%d, %v)", val, ok)
	}

	// Update existing key
	ht.Put("key1", 200)
	val, ok = ht.Get("key1")
	if !ok || val != 200 {
		t.Errorf("expected (200, true) after update, got (%d, %v)", val, ok)
	}

	// Missing key
	_, ok = ht.Get("nonexistent")
	if ok {
		t.Error("expected false for missing key")
	}

	// Contains
	if !ht.Contains("key1") {
		t.Error("expected Contains to return true")
	}
	if ht.Contains("nonexistent") {
		t.Error("expected Contains to return false")
	}

	// Delete
	if !ht.Delete("key1") {
		t.Error("expected Delete to return true")
	}
	if ht.Contains("key1") {
		t.Error("expected Contains to return false after delete")
	}
	if ht.Delete("nonexistent") {
		t.Error("expected Delete to return false for missing key")
	}
}

func TestHashTableCollision(t *testing.T) {
	// Use small capacity to force collisions
	ht := NewHashTable(2)
	ht.Put("a", 1)
	ht.Put("b", 2)
	ht.Put("c", 3) // likely collides

	if val, _ := ht.Get("a"); val != 1 {
		t.Errorf("expected a=1, got %d", val)
	}
	if val, _ := ht.Get("b"); val != 2 {
		t.Errorf("expected b=2, got %d", val)
	}
	if val, _ := ht.Get("c"); val != 3 {
		t.Errorf("expected c=3, got %d", val)
	}
}

func TestTwoSum(t *testing.T) {
	tests := []struct {
		nums   []int
		target int
		want   []int
	}{
		{[]int{2, 7, 11, 15}, 9, []int{0, 1}},
		{[]int{3, 2, 4}, 6, []int{1, 2}},
		{[]int{3, 3}, 6, []int{0, 1}},
	}
	for _, tt := range tests {
		got := twoSum(tt.nums, tt.target)
		if !reflect.DeepEqual(got, tt.want) {
			t.Errorf("twoSum(%v, %d) = %v; want %v", tt.nums, tt.target, got, tt.want)
		}
	}
}

func TestTwoSumNoSolution(t *testing.T) {
	got := twoSum([]int{1, 2, 3}, 100)
	if got != nil {
		t.Errorf("expected nil, got %v", got)
	}
}

func TestFirstNonRepeating(t *testing.T) {
	tests := []struct {
		input string
		want  rune
	}{
		{"leetcode", 'l'},
		{"loveleetcode", 'v'},
		{"aabb", 0},
		{"", 0},
	}
	for _, tt := range tests {
		got := firstNonRepeating(tt.input)
		if got != tt.want {
			t.Errorf("firstNonRepeating(%q) = %c; want %c", tt.input, got, tt.want)
		}
	}
}
