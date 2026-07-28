package main

import (
	"testing"
)

func TestSlice_Append(t *testing.T) {
	s := []int{1, 2, 3}
	s = append(s, 4, 5)
	expected := []int{1, 2, 3, 4, 5}

	if len(s) != len(expected) {
		t.Fatalf("expected len %d, got %d", len(expected), len(s))
	}
	for i, v := range expected {
		if s[i] != v {
			t.Errorf("expected s[%d] = %d, got %d", i, v, s[i])
		}
	}
}

func TestSlice_Copy(t *testing.T) {
	src := []int{1, 2, 3}
	dst := make([]int, len(src))
	copy(dst, src)

	src[0] = 99
	if dst[0] == 99 {
		t.Error("copy should create independent slice")
	}
}

func TestMap_CRUD(t *testing.T) {
	m := make(map[string]int)
	m["apple"] = 5

	// Read
	if val, ok := m["apple"]; !ok || val != 5 {
		t.Errorf("expected m[apple] = 5, got %d (exists=%v)", val, ok)
	}

	// Update
	m["apple"] = 10
	if m["apple"] != 10 {
		t.Errorf("expected m[apple] = 10 after update, got %d", m["apple"])
	}

	// Delete
	delete(m, "apple")
	if _, ok := m["apple"]; ok {
		t.Error("expected apple to be deleted")
	}

	// Missing key
	val, ok := m["nonexistent"]
	if ok || val != 0 {
		t.Errorf("expected (0, false) for missing key, got (%d, %v)", val, ok)
	}
}

func TestString_Runes(t *testing.T) {
	str := "Hello, 世界"
	runes := []rune(str)
	expectedLen := 9 // H,e,l,l,o,,, ,世,界

	if len(runes) != expectedLen {
		t.Errorf("expected %d runes, got %d (byte len=%d)", expectedLen, len(runes), len(str))
	}
}

func TestArray_FixedSize(t *testing.T) {
	var arr [5]int
	if len(arr) != 5 {
		t.Errorf("expected array len 5, got %d", len(arr))
	}
}

func TestSlice_EmptyVsNil(t *testing.T) {
	var nilSlice []int
	emptySlice := []int{}

	if nilSlice != nil {
		t.Error("expected var slice to be nil")
	}
	if emptySlice == nil {
		t.Error("expected literal slice to be non-nil")
	}
}
