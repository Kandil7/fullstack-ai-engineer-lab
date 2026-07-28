# Exercise 11: Testing

> Master Go testing: table-driven tests, benchmarks, subtests, fuzzing, and mocking.

## Goal

Write comprehensive tests using Go's standard `testing` package including benchmarks and fuzzing.

## Requirements

Create a Go program that includes functions to test and write tests for:
1. **Table-driven tests**: Test multiple cases with a slice of test structs
2. **Subtests**: `t.Run("name", func(t *testing.T) {})` for hierarchical tests
3. **Benchmarks**: `BenchmarkXxx(b *testing.B)` for performance measurement
4. **Test coverage**: `go test -cover` to measure coverage
5. **Fuzzing**: `FuzzXxx(f *testing.F)` for random input testing
6. **Test helpers**: `t.Helper()` for cleaner error messages
7. **Skipping tests**: `t.Skip()` for platform-specific or slow tests

## Key Commands

```bash
go test -v                  # Verbose test output
go test -run TestName       # Run specific test
go test -bench=. -benchmem  # Run benchmarks with memory stats
go test -cover -coverprofile=coverage.out  # Coverage report
go test -fuzz=FuzzAdd       # Fuzz testing (30s default)
go test -v ./...            # Test all packages in module
```

## Expected Test Output

```
=== RUN   TestAdd
=== RUN   TestAdd/case_0
=== RUN   TestAdd/case_1
--- PASS: TestAdd (0.00s)
    --- PASS: TestAdd/case_0 (0.00s)
    --- PASS: TestAdd/case_1 (0.00s)
```

## Next Step

Move to **Exercise 12: CLI Tool (Capstone)**.
