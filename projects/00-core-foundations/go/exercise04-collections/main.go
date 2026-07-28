package main

import "fmt"

func main() {
	fmt.Println("=== Exercise 04: Collections (Slices, Maps, Arrays) ===")

	// 1. Arrays - fixed size
	fmt.Println("--- 1. Arrays ---")
	var arr [5]int
	arr[0] = 10
	arr[4] = 50
	fmt.Printf("Array: %v, len=%d, cap=%d\n", arr, len(arr), cap(arr))

	// Array literal
	arr2 := [3]string{"a", "b", "c"}
	fmt.Println("Array literal:", arr2)

	// 2. Slices - dynamic arrays
	fmt.Println("\n--- 2. Slices ---")
	s := []int{1, 2, 3}
	fmt.Printf("Slice: %v, len=%d, cap=%d\n", s, len(s), cap(s))

	// Slice operations
	s = append(s, 4, 5)
	fmt.Println("After append:", s)

	// Slicing
	s2 := s[1:4]
	fmt.Println("Slice [1:4]:", s2)

	// Make slice
	s3 := make([]int, 3, 5) // len=3, cap=5
	fmt.Printf("make([]int, 3, 5): %v, len=%d, cap=%d\n", s3, len(s3), cap(s3))

	// Copy slice
	s4 := make([]int, len(s))
	copy(s4, s)
	fmt.Println("Copied slice:", s4)

	// 3. Two-dimensional slices
	fmt.Println("\n--- 3. 2D Slices ---")
	matrix := [][]int{
		{1, 2, 3},
		{4, 5, 6},
	}
	fmt.Println("Matrix:", matrix)

	// 4. Maps
	fmt.Println("\n--- 4. Maps ---")
	m := make(map[string]int)
	m["apple"] = 5
	m["banana"] = 3
	fmt.Println("Map:", m)

	// Map literal
	m2 := map[string]int{
		"red":   1,
		"green": 2,
		"blue":  3,
	}
	fmt.Println("Map literal:", m2)

	// Map operations
	val, ok := m["apple"]
	fmt.Printf("m[\"apple\"] = %d, exists=%v\n", val, ok)

	delete(m, "banana")
	fmt.Println("After delete:", m)

	// Iterating maps (random order)
	fmt.Println("Iterating map:")
	for k, v := range m2 {
		fmt.Printf("  %s: %d\n", k, v)
	}

	// 5. Map with slice values
	fmt.Println("\n--- 5. Map of Slices ---")
	grouped := map[string][]int{
		"evens": {2, 4, 6, 8},
		"odds":  {1, 3, 5, 7},
	}
	fmt.Println("Grouped:", grouped)

	// 6. Range over slice/map
	fmt.Println("\n--- 6. Range ---")
	for i, v := range s {
		fmt.Printf("  Index %d: %d\n", i, v)
	}

	// Range over map (key only)
	for k := range m2 {
		fmt.Println("  Key:", k)
	}

	// 7. String as rune slice
	fmt.Println("\n--- 7. Strings and Runes ---")
	str := "Hello, 世界"
	fmt.Printf("String: %s, len=%d\n", str, len(str))
	runes := []rune(str)
	fmt.Printf("Runes: %v, len=%d\n", runes, len(runes))
	for i, r := range str {
		fmt.Printf("  Index %d: %c (U+%04X)\n", i, r, r)
	}

	// 8. Bytes vs Runes
	fmt.Println("\n--- 8. Bytes vs Runes ---")
	b := []byte(str)
	fmt.Printf("Bytes: %v, len=%d\n", b, len(b))
}
