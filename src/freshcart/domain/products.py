# __future__ import annotations :
# permet d'utiliser les annotations de type (ex: Product dans Product)
# sans guillemets. Améliore la compatibilité avec les versions futures.
from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from datetime import date
from typing import Protocol


# -------------------------------------------------------------------
# 1) Duck typing : définir un contrat Pricable
# -------------------------------------------------------------------
# Toute classe qui implémente final_price() -> float sera considérée
# comme un Pricable, même sans hériter explicitement d'une base.
class Pricable(Protocol):
    def final_price(self) -> float: ...


# -------------------------------------------------------------------
# 2) Classe Product
# -------------------------------------------------------------------
# order=True génère automatiquement les méthodes de comparaison
# (__lt__, __gt__, etc.) afin de trier les produits par prix.
@dataclass(order=True)
class Product(Pricable):
    # utilisé pour le tri naturel (par prix), pas affiché
    sort_index: float = field(init=False, repr=False, compare=True)

    # champs "publics" obligatoires
    sku: str  # identifiant unique
    name: str  # nom du produit

    # >>> "initial_price" est seulement un paramètre d'init (InitVar),
    # il N'EST PAS stocké directement comme attribut d'instance.
    # On le reçoit dans __post_init__, puis on passe par le setter.
    initial_price: InitVar[float]

    # stockage interne réel du prix
    _price: float = field(init=False, repr=False, compare=False)

    def __post_init__(self, initial_price: float) -> None:
        """
        Méthode appelée automatiquement après __init__.
        On utilise le setter 'price' pour appliquer la validation.
        """
        self._price = 0.0  # valeur temporaire
        self.price = initial_price  # passe par le setter (validation, arrondi)
        self.sort_index = self._price  # synchroniser l'ordre de tri

    # --- propriété "price" exposée proprement ---
    @property
    def price(self) -> float:
        """Accès en lecture au prix validé."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Accès en écriture avec validation métier."""
        if value < 0:
            raise ValueError("price cannot be negative")
        # arrondi à 2 décimales (ex: 3.456 -> 3.46)
        self._price = round(float(value), 2)
        # garder le champ 'sort_index' synchronisé pour le tri
        self.sort_index = self._price

    # --- logique métier (polymorphisme) ---
    def final_price(self) -> float:
        """
        Prix final (ici = prix normal).
        Peut être redéfini dans les sous-classes
        (ex: PerishableProduct applique des réductions).
        """
        return self.price

    def __str__(self) -> str:
        """Représentation lisible du produit."""
        return f"{self.name} ({self.sku}) - {self.price:.2f}$"


# -------------------------------------------------------------------
# 3) Classe PerishableProduct (hérite de Product)
# -------------------------------------------------------------------
@dataclass(order=True)
class PerishableProduct(Product):
    # On ne compare pas expiry_date pour l'ordre.
    expiry_date: date = field(compare=False, kw_only=True)

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
