package main

import "fmt"

// Person struct with Name and Age fields
type Person struct {
	Name string
	Age  int
}

// Greeter interface with Greet() method
type Greeter interface {
	Greet() string
}

// Greet method for Person - implements Greeter interface
func (p Person) Greet() string {
	return fmt.Sprintf("Hello, my name is %s and I am %d years old.", p.Name, p.Age)
}

// GreetPerson takes a Greeter interface and prints greeting
func GreetPerson(g Greeter) {
	fmt.Println(g.Greet())
}

// Employee struct embedding Person (composition)
type Employee struct {
	Person
	EmployeeID string
	Department string
}

// Override Greet for Employee
func (e Employee) Greet() string {
	return fmt.Sprintf("Hello, I'm %s (ID: %s), %d years old, working in %s.", e.Name, e.EmployeeID, e.Age, e.Department)
}

func main() {
	fmt.Println("=== Exercise 02: Structs and Interfaces ===")

	// Create a Person
	p := Person{Name: "Alice", Age: 30}
	fmt.Printf("Person: %+v\n", p)
	GreetPerson(p)

	// Create an Employee (embedding Person)
	e := Employee{
		Person:     Person{Name: "Bob", Age: 28},
		EmployeeID: "EMP-001",
		Department: "Engineering",
	}
	fmt.Printf("Employee: %+v\n", e)
	GreetPerson(e)

	// Demonstrate interface slice
	people := []Greeter{p, e}
	fmt.Println("\n--- All Greeters ---")
	for _, person := range people {
		GreetPerson(person)
	}

	// Type assertion
	if emp, ok := people[1].(Employee); ok {
		fmt.Printf("\nType assertion worked: %s works in %s\n", emp.Name, emp.Department)
	}
}
