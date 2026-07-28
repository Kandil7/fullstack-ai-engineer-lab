# Exercise 02: Structs and Interfaces

> Practice Go structs, methods, interfaces, and composition.

## Goal

Master Go's type system: structs, methods, interfaces, and embedding.

## Requirements

Create a Go program that demonstrates:

1. **Struct Definition**: Define a `Person` struct with `Name` (string) and `Age` (int) fields
2. **Method on Struct**: Add a `Greet() string` method to `Person`
3. **Interface Definition**: Define a `Greeter` interface with `Greet() string`
4. **Interface Implementation**: Make `Person` implement `Greeter` implicitly
4. **Function Accepting Interface**: Write `GreetPerson(g Greeter)` that prints the greeting
5. **Composition/Embedding**: Create `Employee` struct that embeds `Person` and adds `EmployeeID` and `Department`
6. **Method Override**: Override `Greet()` on `Employee` to include employee info
7. **Polymorphism**: Store both `Person` and `Employee` in a `[]Greeter` slice and iterate
8. **Type Assertion**: Demonstrate type assertion to access embedded fields

## Expected Output

```text
=== Exercise 02: Structs and Interfaces ===
Person: {Name:Alice Age:30}
Hello, my name is Alice and I am 30 years old.
Employee: {Person:{Name:Bob Age:28} EmployeeID:EMP-001 Department:Engineering}
Hello, I'm Bob (ID: EMP-001), 28 years old, working in Engineering.

--- All Greeters ---
Hello, my name is Alice and I am 30 years old.
Hello, I'm Bob (ID: EMP-001), 28 years old, working in Engineering.

Type assertion worked: Bob works in Engineering
```

## Self-Check

After writing this, can you explain:

- What is the difference between a struct and an interface?
- How does Go implement interfaces implicitly?
- What is struct embedding vs inheritance?
- When would you use a pointer receiver vs value receiver?
- What is the empty interface `interface{}` (now `any`)?

## Next Step

When this works, move to **Exercise 03: Pointers and Memory**.