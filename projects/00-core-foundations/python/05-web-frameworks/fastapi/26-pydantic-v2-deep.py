"""
26 - Pydantic v2 Deep
=======================
Pydantic v2 internals: field/model validators, Field constraints,
computed fields, serialization aliases, strict mode, model_config,
TypeAdapter, and the v2 performance story (Rust core).

Run:      python 26-pydantic-v2-deep.py
Verify:   python 26-pydantic-v2-deep.py --verify
Reference: https://docs.pydantic.dev/latest/
"""

from __future__ import annotations

import sys

from pydantic import (
    BaseModel, Field, TypeAdapter, ValidationError,
    field_validator, model_validator, computed_field, ConfigDict,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ============================================================
# 1. Field constraints — the declarative validation surface
# ============================================================
class Product(BaseModel):
    """Field-level constraints replace hand-written if/raise checks."""

    name: str = Field(min_length=3, max_length=80)
    price: float = Field(gt=0, le=10_000, description="Unit price in EUR")
    stock: int = Field(ge=0)
    tags: list[str] = Field(default_factory=list, max_length=10)


p = Product(name="GPU Server", price=2_500.0, stock=4)
print("Example 1: Field constraints")
print(f"  valid: {p.name} @ {p.price} x {p.stock}")

try:
    Product(name="X", price=-1, stock=0)   # name too short, price negative
except ValidationError as e:
    print(f"  invalid -> {e.errors()[0]['loc'][0]}: {e.errors()[0]['msg']}")

# ============================================================
# 2. field_validator — per-field logic with mode='before'/'after'
# ============================================================
class Order(BaseModel):
    email: str
    qty: int = Field(gt=0)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("email must contain @")
        return v

    @field_validator("qty", mode="before")
    @classmethod
    def coerce_qty(cls, v):
        """mode='before' runs on the raw input before type coercion."""
        if isinstance(v, str):
            v = v.strip()
        return v


o = Order(email="  A@B.com ", qty="3")
print("\nExample 2: field validators")
print(f"  email normalized: {o.email!r}  qty coerced: {o.qty!r} ({type(o.qty).__name__})")

# ============================================================
# 3. model_validator — cross-field rules
# ============================================================
class Booking(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_range(self) -> "Booking":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self


b = Booking(start=10, end=14)
print("\nExample 3: model_validator (cross-field)")
print(f"  valid booking {b.start}->{b.end}")

try:
    Booking(start=14, end=10)
except ValidationError as e:
    print(f"  invalid -> {e.errors()[0]['msg']}")

# ============================================================
# 4. computed_field + serialization aliases + strict mode
# ============================================================
class Invoice(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=False)

    unit_price: float
    qty: int
    tax_rate: float = 0.2

    @computed_field
    @property
    def total(self) -> float:
        """Computed: present in model_dump/serialization, not required as input."""
        return round(self.unit_price * self.qty * (1 + self.tax_rate), 2)


inv = Invoice(unit_price=10.0, qty=3)
print("\nExample 4: computed fields + serialization")
print(f"  total: {inv.total}")
print(f"  dump: {inv.model_dump()}")

# strict mode: reject coercion (e.g. str '1' for an int field)
class StrictId(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: int


try:
    StrictId(user_id="42")     # str for int in strict mode
    print("  strict: accepted (unexpected)")
except ValidationError:
    print("  strict mode rejects str '42' for user_id: int")

# ============================================================
# 5. TypeAdapter — validate non-model types (a list of ints)
# ============================================================
IntList = TypeAdapter(list[int])
print("\nExample 5: TypeAdapter for non-model types")
print(f"  valid: {IntList.validate_python([1, 2, 3])}")
try:
    IntList.validate_python([1, "x"])
except ValidationError:
    print("  invalid element -> rejected")

# ============================================================
# 6. Serialization aliases — JSON field names differ from Python
# ============================================================
class LegacyAPI(BaseModel):
    user_id: int
    user_name: str = Field(serialization_alias="userName")


api = LegacyAPI(user_id=1, user_name="ada")
print("\nExample 6: serialization aliases")
print(f"  by_alias: {api.model_dump(by_alias=True)}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Field constraints are declarative validation")
print("- field_validator: per-field, before/after coercion")
print("- model_validator: cross-field invariants")
print("- computed_field: derived values in output only")
print("- strict mode + TypeAdapter cover the edges")
print("- v2 core is Rust-based: ~5-50x faster than v1 for big schemas")
print("=" * 60)


def _verify() -> None:
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    # Validators as the app's contract
    assert Product(name="Valid", price=1.0, stock=0).price == 1.0
    assert Order(email="A@B.com", qty=3).email == "a@b.com", "email normalization"
    assert Order(email="a@b.com", qty="5").qty == 5, "mode='before' coercion"
    assert Booking(start=1, end=2).end == 2

    # Rejections
    for bad in (lambda: Product(name="X", price=1, stock=1),
                lambda: Booking(start=2, end=1),
                lambda: StrictId(user_id="1")):
        try:
            bad()
            assert False, "expected ValidationError"
        except ValidationError:
            pass

    # Computed + serialization
    assert Invoice(unit_price=10, qty=3).total == 36.0, "computed total"
    assert LegacyAPI(user_id=1, user_name="ada").model_dump(by_alias=True)["userName"] == "ada"

    # TypeAdapter
    assert IntList.validate_python([1, 2, 3]) == [1, 2, 3]

    # End-to-end via TestClient: validation produces 422
    app = FastAPI()

    @app.post("/products", response_model=Product, status_code=201)
    def create_product(prod: Product) -> Product:
        return prod

    with TestClient(app) as client:
        r = client.post("/products", json={"name": "OK", "price": 5.0, "stock": 1})
        assert r.status_code == 201, "valid body must create"
        r = client.post("/products", json={"name": "X", "price": -1, "stock": 1})
        assert r.status_code == 422, "invalid body must 422"
        detail = r.json()["detail"]
        assert any(item["loc"] == ["body", "name"] for item in detail), "error pinpoints field"

    print("[OK] 26-pydantic-v2-deep: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("26-pydantic-v2-deep:app", host="127.0.0.1", port=8000)
    else:
        _verify()
