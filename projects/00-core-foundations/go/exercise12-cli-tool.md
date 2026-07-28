# Exercise 12: CLI Tool (Capstone)

> Build a production-quality JSON Transformer CLI tool with subcommands and flags.

## Goal

Combine everything you've learned: packages, error handling, I/O, JSON, and testing into a real CLI tool.

## Requirements

Build a CLI tool (`jsontool`) with these subcommands:

### `transform` — Transform fields in JSON data
```bash
go run . transform --input data.json --output result.json --field name --op upper
go run . transform --input data.json --field age --op add --value 5
```

Operations: `upper`, `lower`, `add`, `multiply`

### `filter` — Filter JSON array by field value
```bash
go run . filter --input data.json --field status --value active --output active.json
```

### `stats` — Show statistics about JSON data
```bash
go run . stats --input data.json
```
Shows: object count, array count, string count, number count, null count

## Implementation Hints

- Use the `flag` package (not a third-party CLI framework)
- Read JSON with `os.ReadFile`, parse with `json.Unmarshal`
- Use `json.MarshalIndent` for pretty output
- Traverse nested JSON with `interface{}` and type switches
- Write idempotent, composable helper functions

## Extension Ideas

- Add a `--pretty` flag for indented output
- Add a `--verbose` flag for debug logging
- Support nested field paths like `--field user.address.city`
- Add a `validate` command that checks JSON schema compliance
- Write unit tests for all transformation functions

## Next Step

🎉 Congratulations! Move to **Phase 01: Backend Go Services** (`projects/01-backend-go/`).
