# Case Study: Extraction — Glossary 25

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Extraction | Pipeline | Turning unstructured text into structured records |
| Field Accuracy | Quality | Correctness of a field on a labeled set |
| Human Queue | Reconcile | Failed records routed for human review |
| Reconciliation | Reconcile | The loop fixing bad extractions |
| Repair | Reconcile | Re-extracting with more context |
| Schema | Design | The typed contract for extracted records |
| Validation | Quality | Checking records before persistence |
| Cross-Field | Validation | Consistency checks between fields |

## Detailed Definitions
### Extraction
**Definition**: Mapping documents to schema-compliant records.
**Related**: Schema

### Field Accuracy
**Definition**: The fraction of a field's values correct on labeled data.
**Related**: Validation

### Human Queue
**Definition**: The review path for records machines cannot fix.
**Related**: Reconciliation

### Reconciliation
**Definition**: The loop: re-extract, validate, escalate - improving over
time.
**Related**: Human Queue

### Repair
**Definition**: Re-running extraction with additional context or prompts.
**Related**: Reconciliation

### Schema
**Definition**: Field names, types, and required flags - designed first.
**Related**: Extraction

### Validation
**Definition**: Type/range/required checks before persistence.
**Related**: Field Accuracy

### Cross-Field
**Definition**: Checks that related fields are consistent (e.g. date ≤ today).
**Related**: Validation

## Key Concepts Summary
### The Order
- Schema → extract → validate → persist → reconcile

### The Rules
- Schema first, prompt second
- Never persist unvalidated records

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Schema — ___
2. Validation — ___
3. Reconciliation — ___
4. Human queue — ___
5. Repair — ___

**Answers:** 1-b, 2-e, 3-c, 4-a, 5-d where a=human review path, b=typed
contract, c=fix loop, d=re-extract with context, e=pre-persist checks.
