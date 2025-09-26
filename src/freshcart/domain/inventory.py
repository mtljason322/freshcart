from typing import Any, Callable, List, TypeVar

from freshcart.domain.products import Product

# Type générique pour le décorateur
F = TypeVar("F", bound=Callable[..., Any])


class ProductNotFoundError(Exception):
    """Levée quand on cherche un produit absent de l'inventaire."""
    pass


def log_call(func: F) -> F:
    """Décorateur qui logge le nom de la fonction lors de l'appel."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # NOTE: args[0] est souvent 'self' si on décore une méthode.
        print(f"[LOG] Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


class Inventory:
    def __init__(self) -> None:
        self._items: List[Product] = []

    @log_call
    def add(self, product: Product) -> None:
        self._items.append(product)

    def remove(self, sku: str) -> None:
        for p in self._items:
            if p.sku == sku:
                self._items.remove(p)
                return
        raise ProductNotFoundError(f"Produit {sku} introuvable")

    def all(self) -> List[Product]:
        return list(self._items)

    def expired(self) -> List[Product]:
        return [
            p for p in self._items
            if hasattr(p, "is_expired") and getattr(p, "is_expired")
        ]

    def total_value(self) -> float:
        return round(sum(p.final_price() for p in self._items), 2)
