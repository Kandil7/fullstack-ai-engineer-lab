package main

import (
	"testing"
)

func TestControlFlow_IfElse(t *testing.T) {
	x := 10
	if x <= 5 {
		t.Error("expected x > 5")
	}
}

func TestControlFlow_Switch(t *testing.T) {
	day := "Monday"
	result := ""
	switch day {
	case "Monday":
		result = "weekday"
	case "Saturday", "Sunday":
		result = "weekend"
	default:
		result = "unknown"
	}
	if result != "weekday" {
		t.Errorf("expected weekday, got %s", result)
	}
}

func TestControlFlow_TypeSwitch(t *testing.T) {
	var v interface{} = "hello"
	switch val := v.(type) {
	case string:
		if val != "hello" {
			t.Errorf("expected string 'hello', got %s", val)
		}
	default:
		t.Error("expected type string")
	}
}

func TestControlFlow_ForLoop(t *testing.T) {
	sum := 0
	for i := 0; i < 5; i++ {
		sum += i
	}
	if sum != 10 {
		t.Errorf("expected sum=10, got %d", sum)
	}
}

func TestControlFlow_WhileStyle(t *testing.T) {
	n := 1
	for n < 100 {
		n *= 2
	}
	if n != 128 {
		t.Errorf("expected n=128, got %d", n)
	}
}

func TestControlFlow_DeferOrder(t *testing.T) {
	// Deferred functions run LIFO
	var order []int
	func() {
		defer func() { order = append(order, 1) }()
		defer func() { order = append(order, 2) }()
		defer func() { order = append(order, 3) }()
	}()

	expected := []int{3, 2, 1} // LIFO
	if len(order) != len(expected) {
		t.Fatalf("expected len %d, got %d", len(expected), len(order))
	}
	for i, v := range expected {
		if order[i] != v {
			t.Errorf("expected order[%d]=%d, got %d", i, v, order[i])
		}
	}
}

func TestControlFlow_NamedReturnDefer(t *testing.T) {
	result := double(5)
	if result != 12 {
		t.Errorf("expected double(5)=12 (because defer modifies), got %d", result)
	}
}
