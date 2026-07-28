package main

import "fmt"

// BINARY SEARCH VARIANTS

// binarySearchIterative — classic iterative binary search
func binarySearchIterative(arr []int, target int) int {
	low, high := 0, len(arr)-1
	for low <= high {
		mid := low + (high-low)/2 // prevent overflow
		if arr[mid] == target {
			return mid
		}
		if arr[mid] < target {
			low = mid + 1
		} else {
			high = mid - 1
		}
	}
	return -1
}

// binarySearchRecursive — recursive implementation
func binarySearchRecursive(arr []int, target, low, high int) int {
	if low > high {
		return -1
	}
	mid := low + (high-low)/2
	if arr[mid] == target {
		return mid
	}
	if arr[mid] < target {
		return binarySearchRecursive(arr, target, mid+1, high)
	}
	return binarySearchRecursive(arr, target, low, mid-1)
}

// searchRotatedArray — search in a rotated sorted array
func searchRotatedArray(arr []int, target int) int {
	low, high := 0, len(arr)-1
	for low <= high {
		mid := low + (high-low)/2
		if arr[mid] == target {
			return mid
		}
		// Left half is sorted
		if arr[low] <= arr[mid] {
			if target >= arr[low] && target < arr[mid] {
				high = mid - 1
			} else {
				low = mid + 1
			}
		} else { // Right half is sorted
			if target > arr[mid] && target <= arr[high] {
				low = mid + 1
			} else {
				high = mid - 1
			}
		}
	}
	return -1
}

// findPeakElement — finds a peak element (greater than neighbors)
func findPeakElement(arr []int) int {
	low, high := 0, len(arr)-1
	for low < high {
		mid := low + (high-low)/2
		if arr[mid] > arr[mid+1] {
			high = mid
		} else {
			low = mid + 1
		}
	}
	return low
}

// sqrt computes integer square root using binary search
func sqrt(x int) int {
	if x < 0 {
		return -1
	}
	if x < 2 {
		return x
	}
	low, high := 1, x/2
	for low <= high {
		mid := low + (high-low)/2
		sq := mid * mid
		if sq == x {
			return mid
		}
		if sq < x {
			low = mid + 1
		} else {
			high = mid - 1
		}
	}
	return high // floor sqrt
}

func main() {
	fmt.Println("=== Binary Search Exercise ===")
	fmt.Println()

	// Standard binary search
	fmt.Println("--- Standard Binary Search ---")
	sorted := []int{1, 3, 5, 7, 9, 11, 13, 15}
	for _, target := range []int{7, 1, 15, 99} {
		idx := binarySearchIterative(sorted, target)
		if idx != -1 {
			fmt.Printf("  Found %d at index %d\n", target, idx)
		} else {
			fmt.Printf("  %d not found\n", target)
		}
	}

	// Recursive
	fmt.Println("\n--- Recursive Binary Search ---")
	fmt.Printf("  binarySearchRecursive([...], 7) = %d\n",
		binarySearchRecursive(sorted, 7, 0, len(sorted)-1))

	// Rotated array
	fmt.Println("\n--- Rotated Array Search ---")
	rotated := []int{4, 5, 6, 7, 0, 1, 2}
	fmt.Printf("  rotated = %v\n", rotated)
	for _, target := range []int{0, 3, 4, 2} {
		fmt.Printf("  search for %d: index %d\n", target, searchRotatedArray(rotated, target))
	}

	// Peak element
	fmt.Println("\n--- Peak Element ---")
	peaks := []int{1, 2, 3, 1}
	fmt.Printf("  arr = %v, peak at index %d (val=%d)\n", peaks, findPeakElement(peaks), peaks[findPeakElement(peaks)])

	// Integer square root
	fmt.Println("\n--- Integer Square Root ---")
	for _, n := range []int{0, 1, 4, 8, 16, 25, 100} {
		fmt.Printf("  sqrt(%d) = %d\n", n, sqrt(n))
	}
}
