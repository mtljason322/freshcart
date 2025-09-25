# __future__ import annotations :
# permet d'utiliser les annotations de type (ex: "Product" dans Product) 
# sans avoir à les mettre entre guillemets → compatibilité future.
from __future__ import annotations

# dataclass : génère automatiquement __init__, __repr__, __eq__, etc.
from dataclasses import dataclass, field

# pour gérer les dates d'expiration
from datetime import date

# Protocol : sert à définir un "contrat" d'interface → duck typing
from typing import Protocol


# -------------------------------------------------------------------
# 1) Duck typing : définir un contrat Pricable
# -------------------------------------------------------------------
# Toute classe qui "implémente" une méthode final_price() -> float 
# sera considérée comme un Pricable, même sans héritage explicite.
class Pricable(Protocol):
    def final_price(self) -> float: ...
    # Ici on dit seulement "toute classe avec une méthode final_price renvoyant float est valide"


# -------------------------------------------------------------------
# 2) Classe Product
# -------------------------------------------------------------------
# order=True → dataclass génère automatiquement les méthodes de comparaison
# (__lt__, __le__, __gt__, __ge__) basées sur un champ spécial "sort_index".
@dataclass(order=True)
class Product(Pricable):  # On dit aussi que Product respecte le contrat Pricable
    # sort_index : utilisé uniquement pour le tri → pas affiché (repr=False), pas comparé par défaut
    sort_index: float = field(init=False, repr=False, compare=True)

    # Champs classiques
    sku: str
    name: str
    _price: float = field(repr=False, compare=False)  # <-- plus de default=0.0

    # _price : on le rend privé (avec _) et on ne l'affiche pas dans __repr__

    # Méthode spéciale appelée juste après __init__
    def __post_init__(self) -> None:
        # On valide et initialise le prix via le setter (validation incluse)
        self.price = self._price  
        # On définit l'indice de tri sur le prix
        self.sort_index = self._price


    # ---- Propriété "price" ----
    # Grâce à @property, on peut écrire p.price au lieu de p.get_price()
    @property
    def price(self) -> float:
        return self._price

    # Setter pour price → permet de faire p.price = 10
    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("price cannot be negative")  # validation → pas de prix négatif
        # arrondir à 2 décimales
        self._price = round(float(value), 2)
        # garder le sort_index cohérent (pour tri)
        self.sort_index = self._price

    # ---- Méthode métier ----
    # final_price peut être redéfini dans les classes enfants (polymorphisme)
    def final_price(self) -> float:
        return self.price

    # ---- Affichage convivial ----
    def __str__(self) -> str:
        return f"{self.name} ({self.sku}) - {self.price:.2f}$"


# -------------------------------------------------------------------
# 3) Classe PerishableProduct (hérite de Product)
# -------------------------------------------------------------------
# Représente un produit périssable avec date d’expiration
@dataclass(order=True)
class PerishableProduct(Product):
    # On ne compare pas expiry_date pour l'ordre → compare=False
    expiry_date: date = field(compare=False)

    # ---- Propriété calculée ----
    @property
    def is_expired(self) -> bool:
        # True si la date d'aujourd'hui dépasse expiry_date
        return date.today() > self.expiry_date

    # ---- Méthode utilitaire ----
    def days_left(self) -> int:
        # Différence entre la date d’expiration et aujourd’hui
        return (self.expiry_date - date.today()).days

    # ---- Redéfinition de final_price (polymorphisme) ----
    def final_price(self) -> float:
        if self.is_expired:
            return 0.0  # produit périmé → gratuit ou inutilisable
        if self.days_left() <= 3:
            return round(self.price * 0.5, 2)  # réduction de 50% si proche d’expirer
        return self.price
