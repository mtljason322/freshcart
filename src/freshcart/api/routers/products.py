from __future__ import annotations

# SUPPRIMER: from datetime import date
from typing import List, Literal  # <-- on réintroduit List pour mypy compat

from fastapi import APIRouter, Depends, HTTPException, Request, status

from freshcart.api.schemas import ProductCreate, ProductOut
from freshcart.domain.inventory import Inventory
from freshcart.domain.products import PerishableProduct, Product

router = APIRouter(prefix="/products", tags=["products"])


def get_inventory(request: Request) -> Inventory:
    inv = getattr(request.app.state, "inventory", None)
    if inv is None:
        raise RuntimeError("Inventory is not initialized on app.state")
    return inv


def to_product_out(p: Product) -> ProductOut:
    type_value: Literal["regular", "perishable"]
    if hasattr(p, "expiry_date"):
        type_value = "perishable"
        expiry = getattr(p, "expiry_date")
    else:
        type_value = "regular"
        expiry = None

    return ProductOut(
        sku=p.sku,
        name=p.name,
        type=type_value,
        price=p.price,
        final_price=p.final_price(),
        expiry_date=expiry,
    )


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate, inv: Inventory = Depends(get_inventory)
) -> ProductOut:
    if any(it.sku == payload.sku for it in inv.all()):
        raise HTTPException(status_code=400, detail="SKU already exists")

    if payload.type == "regular":
        p = Product(payload.sku, payload.name, payload.initial_price)
    else:
        assert payload.expiry_date is not None, "expiry_date validated by Pydantic"
        p = PerishableProduct(
            payload.sku,
            payload.name,
            payload.initial_price,
            expiry_date=payload.expiry_date,
        )

    inv.add(p)
    return to_product_out(p)


@router.get("", response_model=List[ProductOut])  # <-- List[...] au lieu de list[...]
def list_products(inv: Inventory = Depends(get_inventory)) -> List[ProductOut]:
    items = sorted(inv.all())
    return [to_product_out(p) for p in items]
