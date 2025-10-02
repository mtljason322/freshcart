"""
Router /inventory

Expose :
- GET /inventory/value : somme des final_price() de l'inventaire
"""

from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, Depends, Request

from freshcart.domain.inventory import Inventory

router = APIRouter(prefix="/inventory", tags=["inventory"])


def get_inventory(request: Request) -> Inventory:
    inv = getattr(request.app.state, "inventory", None)
    if inv is None:
        raise RuntimeError("Inventory is not initialized on app.state")
    return inv


@router.get("/value", response_model=Dict[str, float])
def get_total_value(inv: Inventory = Depends(get_inventory)) -> dict[str, float]:
    """Retourne la somme des final_price() (arrondie côté domaine)."""
    return {"total_value": inv.total_value()}
