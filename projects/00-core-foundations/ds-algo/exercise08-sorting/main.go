package main

import "fmt"

// SORTING ALGORITHMS

// BubbleSort — O(n²) simple but slow
func BubbleSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		swapped := false
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				swapped = true
			}
		}
		if !swapped {
			break // Already sorted
		}
	}
}

// SelectionSort — O(n²) finds minimum repeatedly
func SelectionSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		minIdx := i
		for j := i + 1; j < n; j++ {
			if arr[j] < arr[minIdx] {
				minIdx = j
			}
		}
		arr[i], arr[minIdx] = arr[minIdx], arr[i]
	}
}

// InsertionSort — O(n²) builds final array one element at a time
func InsertionSort(arr []int) {
	for i := 1; i < len(arr); i++ {
		key := arr[i]
		j := i - 1
		for j >= 0 && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = key
	}
}

// MergeSort — O(n log n) divide and conquer
func MergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}
	mid := len(arr) / 2
	left := MergeSort(arr[:mid])
	right := MergeSort(arr[mid:])
	return merge2(left, right)
}

func merge2(left, right []int) []int {
	result := make([]int, 0, len(left)+len(right))
	i, j := 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}
	result = append(result, left[i:]...)
	result = append(result, right[j:]...)
	return result
}

// QuickSort — O(n log n) average, in-place
func QuickSort(arr []int) {
	if len(arr) <= 1 {
		return
	}
	quickSortHelper(arr, 0, len(arr)-1)
}

func quickSortHelper(arr []int, low, high int) {
	if low < high {
		pivotIdx := partition(arr, low, high)
		quickSortHelper(arr, low, pivotIdx-1)
		quickSortHelper(arr, pivotIdx+1, high)
	}
}

func partition(arr []int, low, high int) int {
	pivot := arr[high]
	i := low - 1
	for j := low; j < high; j++ {
		if arr[j] < pivot {
			i++
			arr[i], arr[j] = arr[j], arr[i]
		}
	}
	arr[i+1], arr[high] = arr[high], arr[i+1]
	return i + 1
}

// isSorted checks if array is sorted
func isSorted(arr []int) bool {
	for i := 1; i < len(arr); i++ {
		if arr[i] < arr[i-1] {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println("=== Sorting Algorithms Exercise ===")
	fmt.Println()

	// Test all sorting algorithms
	sortFuncs := []struct {
		name string
		fn   func([]int)
	}{
		{"BubbleSort", BubbleSort},
		{"SelectionSort", SelectionSort},
		{"InsertionSort", InsertionSort},
		{"QuickSort", QuickSort},
	}

	input := []int{64, 34, 25, 12, 22, 11, 90}
	for _, sf := range sortFuncs {
		arr := make([]int, len(input))
		copy(arr, input)
		sf.fn(arr)
		fmt.Printf("  %s: %v (sorted=%v)\n", sf.name, arr, isSorted(arr))
	}

	// MergeSort (returns new slice)
	arrCopy := []int{38, 27, 43, 3, 9, 82, 10}
	sorted := MergeSort(arrCopy)
	fmt.Printf("  MergeSort: %v -> %v (sorted=%v)\n", arrCopy, sorted, isSorted(sorted))

	fmt.Println()
	fmt.Println("Tip: Run 'go test -bench=.' to compare performance!")
}
