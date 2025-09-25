# But du module :
# - Définir un service "Inventory" qui gère une collection de produits.
# - Illustrer : exceptions custom, décorateur simple, compréhensions de listes,
#   et duck typing via la méthode polymorphe `final_price()`.

from __future__ import annotations

from typing import List
from freshcart.domain.products import Product, Pricable


# -----------------------------------------------------------
# 1) Exception custom : métier
# -----------------------------------------------------------
# Pourquoi ? En entreprise, on n'utilise pas des ValueError génériques pour tout.
# On crée des exceptions "métier" qui documentent clairement l'intention.
class ProductNotFoundError(Exception):
    """Levée quand on cherche un produit qui n'existe pas dans l'inventaire."""


# -----------------------------------------------------------
# 2) Décorateur simple pour tracer l'appel d'une fonction
# -----------------------------------------------------------
# Objectif : te montrer la mécanique d'un décorateur (fonction qui "enveloppe" une autre fonction).
# Ici, on logge sur la sortie standard ; plus tard, on branchera un vrai logger (logging).
def log_call(func):
    """Décorateur qui logge le nom de la fonction au moment de l'appel."""

    def wrapper(*args, **kwargs):
        # NOTE: args[0] est souvent 'self' si on décore une méthode d'instance.
        print(f"[LOG] Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# -----------------------------------------------------------
# 3) Service d'inventaire
# -----------------------------------------------------------
# Design :
# - Stocker des objets Product (ou sous-classes).
# - Fournir des opérations simples (ajout, suppression, listing).
# - Offrir des vues filtrées (ex: produits périmés).
# - Calculer une valeur totale grâce au polymorphisme (final_price()).
class Inventory:
    def __init__(self) -> None:
        # Choix : liste en mémoire (simple pour commencer).
        # Plus tard : on branchera une base de données (SQLite/Postgres).
        self._items: List[Product] = []

    @log_call  # ← décorateur : logge l'appel d'ajout (exemple pédagogique)
    def add(self, product: Product) -> None:
        """Ajoute un produit à l'inventaire.

        Args:
            product: instance de Product (ou sous-classe)
        """
        self._items.append(product)

    def remove(self, sku: str) -> None:
        """Supprime un produit par son identifiant (SKU).

        Stratégie :
        - On parcourt la liste (O(n), suffisant pour l'exemple).
        - Si trouvé → on supprime et on retourne.
        - Sinon → on lève une exception métier.
        """
        for p in self._items:
            if p.sku == sku:
                self._items.remove(p)
                return
        raise ProductNotFoundError(f"Produit {sku} introuvable")

    def all(self) -> List[Product]:
        """Retourne une copie de la liste des produits.

        Pourquoi une copie ? Éviter qu'un appelant modifie la liste interne
        sans passer par les méthodes du service.
        """
        return list(self._items)

    def expired(self) -> List[Product]:
        """Retourne les produits périmés (si la classe les expose).

        Points pédagogiques :
        - Duck typing/feature detection : on teste `hasattr(p, "is_expired")`.
        - Si un objet possède la propriété is_expired et qu'elle vaut True,
          on le retient.
        """
        return [p for p in self._items if hasattr(p, "is_expired") and p.is_expired]

    def total_value(self) -> float:
        """Somme des prix finaux de tous les produits (arrondi à 2 décimales).

        Polymorphisme :
        - On n'a PAS besoin de savoir si 'p' est Product ou PerishableProduct.
        - On appelle simplement p.final_price() (contrat Pricable).
        - Chaque classe s'occupe de sa logique de prix (normal, promo, périmé).
        """
        return round(sum(p.final_price() for p in self._items), 2)
