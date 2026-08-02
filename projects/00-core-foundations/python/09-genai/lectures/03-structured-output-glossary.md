# Structured Output — Glossary 03

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Fallback | Parsing | Safe path when output cannot be parsed |
| Function Calling | Output | Model returns typed function arguments |
| JSON Mode | Output | Instruction to emit valid JSON |
| Repair | Parsing | Fixing common JSON breakage (stray commas) |
| Schema | Output | The typed contract output must satisfy |
| Validation | Output | Checking parsed data against the schema |
| Tool | Output | A declared function the model may call |

## Detailed Definitions
### Fallback
**Definition**: The guaranteed path - parse, repair, then default - so no bad
output crashes the pipeline.
**Related**: Repair

### Function Calling
**Definition**: Supplying tool schemas; the model responds with typed argument
objects instead of free text.
**Related**: Tool

### JSON Mode
**Definition**: A request flag that biases the model to emit valid JSON.
**Related**: Validation

### Repair
**Definition**: Correcting common JSON defects like stray commas and unquoted
keys.
**Related**: Fallback

### Schema
**Definition**: The formal contract: fields, types, required flags.
**Related**: Validation

### Validation
**Definition**: Checking parsed data against the schema before use.
**Related**: Schema

### Tool
**Definition**: A declared function with a JSON schema the model can choose to
call.
**Related**: Function Calling

## Key Concepts Summary
### The Chain
- Generate → parse → repair → validate → use

### The Rules
- JSON mode ≠ schema compliance
- Parse is not validation

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Schema — ___
2. Function calling — ___
3. Fallback — ___
4. Validation — ___
5. Repair — ___

**Answers:** 1-d, 2-b, 3-e, 4-a, 5-c where a=check against contract, b=typed
argument output, c=fix broken JSON, d=typed contract, e=never-crash path.
