package main

import "fmt"

type Counter struct {
	count int
}

// Value receiver - operates on copy
func (c Counter) IncrementValue() {
	c.count++
	fmt.Printf("  Inside IncrementValue: %d\n", c.count)
}

// Pointer receiver - operates on original
func (c *Counter) IncrementPointer() {
	c.count++
	fmt.Printf("  Inside IncrementPointer: %d\n", c.count)
}

func main() {
	fmt.Println("=== Exercise 03: Pointers and Memory ===")

	// 1. Basic pointer operations
	fmt.Println("--- 1. Basic Pointer Operations ---")
	var x int = 42
	var p *int = &x
	fmt.Printf("Value of x: %d\n", x)
	fmt.Printf("Address of x (&x): %p\n", &x)
	fmt.Printf("Value of p (address): %p\n", p)
	fmt.Printf("Value pointed to by p (*p): %d\n", *p)

	// Modify through pointer
	*p = 100
	fmt.Printf("After *p = 100, x = %d\n", x)

	// 2. Pointer to struct
	fmt.Println("\n--- 2. Pointer to Struct ---")
	type Point struct {
		X, Y int
	}
	pt := Point{X: 10, Y: 20}
	ptr := &pt
	fmt.Println("Original point directly access fields through pointer (no need for (*ptr).X)")
	fmt.Printf("pt.X = %d, ptr.X = %d\n", pt.X, ptr.X)
	ptr.Y = 30 // modifies original
	fmt.Printf("After ptr.Y = 30, pt.Y = %d\n", pt.Y)

	// 3. new() vs make() - new allocates memory, returns pointer
	fmt.Println("\n--- 3. new() vs &struct{} ---")
	p1 := new(Point) // returns *Point, zero-valued
	fmt.Printf("new(Point): %+v\n", p1)
	p2 := &Point{X: 5, Y: 5} // composite literal, returns *Point
	fmt.Printf("&Point{X:5, Y:5}: %+v\n", p2)

	// 4. Pointer to slice vs slice
	fmt.Println("\n--- 4. Pointer to Slice vs Slice ---")
	s := []int{1, 2, 3}
	sp := &s
	fmt.Printf("Slice s: %v, len=%d, cap=%d\n", s, len(s), cap(s))
	fmt.Printf("Pointer *sp: %v, len=%d, cap=%d\n", *sp, len(*sp), cap(*sp))
	// Modifying slice through pointer
	*sp = append(*sp, 4)
	fmt.Printf("After append through pointer, s: %v\n", s)

	// 5. Function with pointer receiver vs value receiver
	fmt.Println("\n--- 5. Pointer vs Value Receiver ---")

	c1 := Counter{count: 0}
	fmt.Println("Value receiver (doesn't modify original):")
	c1.IncrementValue()
	c1.IncrementValue()
	fmt.Printf("After two calls, c1.count = %d (unchanged!)\n", c1.count)

	c2 := Counter{count: 0}
	fmt.Println("Pointer receiver (modifies original):")
	c2.IncrementPointer()
	c2.IncrementPointer()
	fmt.Printf("After two calls, c2.count = %d (modified!)\n", c2.count)

	// 6. Nil pointers
	fmt.Println("\n--- 6. Nil Pointers ---")
	var nilPtr *int
	fmt.Printf("Nil pointer value: %v\n", nilPtr)
	// *nilPtr = 10 // This would panic!
	if nilPtr == nil {
		fmt.Println("Pointer is nil, safe to check before dereferencing")
	}

	// 7. Pointer to pointer (double pointer)
	fmt.Println("\n--- 7. Double Pointer ---")
	val := 100
	ptr1 := &val
	ptr2 := &ptr1
	fmt.Printf("val = %d, *ptr1 = %d, **ptr2 = %d\n", val, *ptr1, **ptr2)
	**ptr2 = 200
	fmt.Printf("After **ptr2 = 200, val = %d\n", val)

	// 8. Escape analysis - when does Go allocate on heap?
	fmt.Println("\n--- 8. Heap vs Stack (Escape Analysis) ---")
	// Run with: go build -gcflags='-m' to see escape analysis
	local := 42
	_ = &local // Taking address may cause heap allocation
	fmt.Println("Local variable address taken - may escape to heap")
}
