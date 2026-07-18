package main

import (
	"testing"
)

func TestPersonGreet(t *testing.T) {
	p := Person{Name: "Alice", Age: 30}
	expected := "Hello, my name is Alice and I am 30 years old."
	if p.Greet() != expected {
		t.Errorf("Person.Greet() = %q; want %q", p.Greet(), expected)
	}
}

func TestEmployeeGreet(t *testing.T) {
	e := Employee{
		Person:     Person{Name: "Bob", Age: 28},
		EmployeeID: "EMP-001",
		Department: "Engineering",
	}
	expected := "Hello, I'm Bob (ID: EMP-001), 28 years old, working in Engineering."
	if e.Greet() != expected {
		t.Errorf("Employee.Greet() = %q; want %q", e.Greet(), expected)
	}
}

func TestGreetPerson(t *testing.T) {
	// Test that GreetPerson works with any Greeter
	p := Person{Name: "Test", Age: 25}
	GreetPerson(p) // Should not panic

	e := Employee{
		Person:     Person{Name: "TestEmp", Age: 30},
		EmployeeID: "TEST-001",
		Department: "TestDept",
	}
	GreetPerson(e) // Should not panic
}

func BenchmarkPersonGreet(b *testing.B) {
	p := Person{Name: "Benchmark", Age: 100}
	for i := 0; i < b.N; i++ {
		_ = p.Greet()
	}
}

func BenchmarkEmployeeGreet(b *testing.B) {
	e := Employee{
		Person:     Person{Name: "Benchmark", Age: 100},
		EmployeeID: "BENCH-001",
		Department: "Benchmarking",
	}
	for i := 0; i < b.N; i++ {
		_ = e.Greet()
	}
}
