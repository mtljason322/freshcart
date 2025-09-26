# __future__ import annotations :
# permet d'utiliser les annotations de type (ex: Product dans Product)
# sans guillemets. Améliore la compatibilité avec les versions futures.
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Protocol


# -------------------------------------------------------------------
# 1) Duck typing : définir un contrat Pricable
# -------------------------------------------------------------------
# Toute classe qui implémente final_price() -> float sera considérée
# comme un Pricable, même sans hériter explicitement d'une base.
class Pricable(Protocol):
    def final_price(self) -> float:
        ...


# -------------------------------------------------------------------
# 2) Classe Product
# -------------------------------------------------------------------
# order=True génère __lt__/__le__/__gt__/__ge__ pour le tri.
@dataclass(order=True)
class Product(Pricable):
    # sort_index : utilisé pour le tri, pas affiché.
    sort_index: float = field(init=False, repr=False, compare=True)

    sku: str
    name: str
    _price: float = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        # Valide et initialise via le setter (empêche prix négatif).
        self.price = self._price
        self.sort_index = self._price

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            # Validation métier : pas de prix négatif.
            raise ValueError("price cannot be negative")
        self._price = round(float(value), 2)
        # Maintenir l’ordre de tri cohérent.
        self.sort_index = self._price

    def final_price(self) -> float:
        # Peut être redéfini par les sous-classes (polymorphisme).
        return self.price

    def __str__(self) -> str:
        return f"{self.name} ({self.sku}) - {self.price:.2f}$"


# -------------------------------------------------------------------
# 3) Classe PerishableProduct (hérite de Product)
# -------------------------------------------------------------------
@dataclass(order=True)
class PerishableProduct(Product):
    # On ne compare pas expiry_date pour l'ordre.
    expiry_date: date = field(compare=False)

    @property
    def is_expired(self) -> bool:
        return date.today() > self.expiry_date

    def days_left(self) -> int:
        return (self.expiry_date - date.today()).days

    def final_price(self) -> float:
        if self.is_expired:
            return 0.0
        if self.days_left() <= 3:
            return round(self.price * 0.5, 2)
        return self.price
