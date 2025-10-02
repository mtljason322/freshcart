"""
Schemas Pydantic pour l'API FreshCart.

Rôle:
- Définir les contrats d'ENTRÉE (payloads) et de SORTIE (réponses).
- Pydantic valide automatiquement les données et alimente la doc Swagger.
"""

from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

# ---------- Entrées ----------


class ProductCreate(BaseModel):
    """
    Requête de création de produit.

    - initial_price >= 0 (validation)
    - type = "regular" | "perishable"
    - si "perishable" -> expiry_date est requis (validation "after")
    """

    sku: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    initial_price: float = Field(..., ge=0.0)
    type: Literal["regular", "perishable"] = "regular"
    expiry_date: Optional[date] = None

    # Exemple de validation champ par champ (v2)
    @field_validator("initial_price")
    @classmethod
    def _non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("initial_price must be >= 0")
        # On peut arrondir au passage, pour rester aligné avec le domaine
        return round(float(v), 2)

    # Validation dépendant de plusieurs champs (v2)
    @model_validator(mode="after")
    def _perishable_needs_expiry(self) -> "ProductCreate":
        if self.type == "perishable" and self.expiry_date is None:
            raise ValueError("expiry_date is required for perishable products")
        return self


# ---------- Sorties ----------


class ProductOut(BaseModel):
    """
    Réponse standardisée d'un produit renvoyé par l'API.
    On expose le prix courant ET le prix calculé `final_price`.
    """

    sku: str
    name: str
    type: Literal["regular", "perishable"]
    price: float
    final_price: float
    expiry_date: Optional[date] = None
