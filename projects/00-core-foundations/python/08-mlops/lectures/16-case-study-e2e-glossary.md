# End to End MLOps — Glossary 16

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Champion | Governance | The currently deployed, best-known model |
| Challenger | Governance | A candidate model being evaluated against the champion |
| Drift Alert | Monitoring | A signal that production data left the expected distribution |
| Gate | Governance | A binary promote/stay check between pipeline stages |
| Lineage | Governance | Provenance record: data, config, metrics behind an artifact |
| Release Gate | Governance | A specific gate that must pass for promotion |
| Rollback | Governance | Returning to the previous champion after a bad deploy |
| Runbook | Operations | Written procedure for responding to an incident |

## Detailed Definitions
### Champion
**Definition**: The model currently serving production traffic.
**Related**: Challenger, Rollback

### Challenger
**Definition**: A candidate model tested against the champion before promotion.
**Related**: Champion

### Drift Alert
**Definition**: Automated warning when live data no longer matches training
data within tolerance.
**Related**: Runbook

### Gate
**Definition**: A check with a pass/fail outcome that decides whether an
artifact moves to the next stage.
**Related**: Release Gate

### Lineage
**Definition**: The full provenance of an artifact - dataset hash, config,
code version, metrics.
```python
lineage = {"data_hash": h, "config": cfg, "metric": m}
```
**Related**: Rollback

### Release Gate
**Definition**: A gate applied specifically at promotion time (e.g. registry
promote requires passing metrics + shadow test).
**Related**: Gate

### Rollback
**Definition**: The operational path back to the last known-good champion.
**Related**: Champion, Lineage

### Runbook
**Definition**: The documented procedure for handling an alert or incident.
**Related**: Drift Alert

## Key Concepts Summary
### The Loop
- Monitor → retrain → evaluate → promote → monitor

### The Rules
- Nothing moves without passing a gate
- Rollback is designed before deploy
- Lineage follows every artifact

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Champion — ___
2. Gate — ___
3. Lineage — ___
4. Rollback — ___
5. Runbook — ___

**Answers:** 1-b, 2-e, 3-a, 4-d, 5-c where a=provenance record, b=deployed
best model, c=incident procedure, d=return to last good model, e=promote/stay
check.
