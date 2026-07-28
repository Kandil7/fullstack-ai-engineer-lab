package main

import (
	"fmt"
	"math/rand"
	"reflect"
	"testing"
)

func TestBubbleSort(t *testing.T) {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	expected := []int{11, 12, 22, 25, 34, 64, 90}
	BubbleSort(arr)
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestSelectionSort(t *testing.T) {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	expected := []int{11, 12, 22, 25, 34, 64, 90}
	SelectionSort(arr)
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestInsertionSort(t *testing.T) {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	expected := []int{11, 12, 22, 25, 34, 64, 90}
	InsertionSort(arr)
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestMergeSort(t *testing.T) {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	expected := []int{3, 9, 10, 27, 38, 43, 82}
	result := MergeSort(arr)
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}

func TestQuickSort(t *testing.T) {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	expected := []int{11, 12, 22, 25, 34, 64, 90}
	QuickSort(arr)
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestSortEmpty(t *testing.T) {
	var arr []int
	QuickSort(arr)
	if len(arr) != 0 {
		t.Error("expected empty slice to remain empty")
	}
}

func TestSortSingle(t *testing.T) {
	arr := []int{1}
	QuickSort(arr)
	if arr[0] != 1 {
		t.Error("expected single element to remain unchanged")
	}
}

func TestSortAlreadySorted(t *testing.T) {
	arr := []int{1, 2, 3, 4, 5}
	QuickSort(arr)
	expected := []int{1, 2, 3, 4, 5}
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestSortReversed(t *testing.T) {
	arr := []int{5, 4, 3, 2, 1}
	QuickSort(arr)
	expected := []int{1, 2, 3, 4, 5}
	if !reflect.DeepEqual(arr, expected) {
		t.Errorf("expected %v, got %v", expected, arr)
	}
}

func TestIsSorted(t *testing.T) {
	if !isSorted([]int{1, 2, 3, 4, 5}) {
		t.Error("expected sorted")
	}
	if isSorted([]int{5, 4, 3, 2, 1}) {
		t.Error("expected not sorted")
	}
	if !isSorted([]int{}) {
		t.Error("expected empty to be sorted")
	}
	if !isSorted([]int{1}) {
		t.Error("expected single element to be sorted")
	}
}

// Benchmarks
var benchSizes = []int{10, 100, 1000}

func generateRandomSlice(n int) []int {
	s := make([]int, n)
	for i := range s {
		s[i] = rand.Intn(n)
	}
	return s
}

func BenchmarkBubbleSort(b *testing.B) {
	for _, n := range benchSizes {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			data := generateRandomSlice(n)
			b.ResetTimer()
			for i := 0; i < b.N; i++ {
				arr := make([]int, len(data))
				copy(arr, data)
				BubbleSort(arr)
			}
		})
	}
}

func BenchmarkQuickSort(b *testing.B) {
	for _, n := range benchSizes {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			data := generateRandomSlice(n)
			b.ResetTimer()
			for i := 0; i < b.N; i++ {
				arr := make([]int, len(data))
				copy(arr, data)
				QuickSort(arr)
			}
		})
	}
}
