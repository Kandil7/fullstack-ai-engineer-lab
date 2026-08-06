# Challenge 02: ddl-schema — Schema, Constraints & Migration

## 🥉 Bronze — Products Table (~20 min)

**Task:** Implement `create_products_table(conn)` that creates a
`products` table with:
- `id INTEGER PRIMARY KEY`
- `sku TEXT NOT NULL UNIQUE`
- `price REAL NOT NULL CHECK (price >= 0)`
- `stock INTEGER NOT NULL DEFAULT 0`

**Signature:**
```python
def create_products_table(conn: sqlite3.Connection) -> None:
```

**Requirements:**
- All four constraints must be enforced by the engine
- Return `None`

**Constraints:** n ≤ 10³.

| Input | Expectation |
|-------|-------------|
| `INSERT price = -5` | IntegrityError |
| `INSERT sku = NULL` | IntegrityError |
| `INSERT sku = 'A'` twice | IntegrityError |
| Omit `stock` | Becomes `0` |

---

## 🥈 Silver — Backfilled Column (~35 min)

**Task:** Implement `add_status_and_backfill(conn)` that adds a
nullable `status TEXT` column and backfills it in batches of 1000:
rows with `price > 50` get `'premium'`, the rest `'standard'`.

**Signature:**
```python
def add_status_and_backfill(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- `ALTER TABLE ... ADD COLUMN` (nullable) first
- Batch `UPDATE ... WHERE id BETWEEN ? AND ?` — never one giant UPDATE
- Return `{"rows": n, "premium": n}` after the backfill

**Constraints:** n ≤ 10⁴ rows. Batch size fixed at 1000.

| Setup | Expected |
|-------|----------|
| 2500 rows, 800 with price > 50 | `rows == 2500`, `premium == 800` |
| Empty table | `rows == 0`, `premium == 0` |

---

## 🥇 Gold — Cascading Audit Schema (~50 min)

**Task:** Implement `create_audit_schema(conn)` that builds an
orders/order_items schema where deleting an order cascades to its
items, plus a generated `total REAL` column on each item computed as
`qty * unit_price`, and `order_totals(order_id, total)` views per order.

**Signature:**
```python
def create_audit_schema(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- `orders(id PK)`; `order_items(id PK, order_id FK ON DELETE CASCADE, qty INT, unit_price REAL)`
- Generated column `total` = `qty * unit_price`
- Return `{"items": n, "generated": float}` after inserting a 2-item
  order (qty 2 x 10.0, qty 1 x 4.5) and deleting the order:
  `items == 0` proves the cascade; `generated == 14.5` proves the column

**Constraints:** n ≤ 10³. FK enforcement must be ON.

| Setup | Expected |
|-------|----------|
| Order with items `(2 x 10.0)` + `(1 x 4.5)` | `generated == 14.5` |
| Delete the order | `items == 0` |

**Follow-up:** Why add a generated column instead of computing totals in
Python? (Answer: the value cannot drift — the engine owns the invariant,
and every consumer reads the same truth.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/02-ddl-schema/test_challenge.py -v
```

## Test File Structure

```
challenges/02-ddl-schema/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
