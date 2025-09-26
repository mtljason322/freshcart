# But : vérifier Inventory (ajout, retrait, listing, périmés, total).

from datetime import date, timedelta

import pytest

from freshcart.domain.inventory import Inventory, ProductNotFoundError
from freshcart.domain.products import PerishableProduct, Product


def test_add_and_all() -> None:
    inv = Inventory()
    p = Product("S1", "Café", 8.0)

    inv.add(p)

    items = inv.all()
    assert len(items) == 1
    assert items[0].name == "Café"

    # "all" retourne une copie : modifier 'items' n'affecte pas l'interne.
    items.clear()
    assert len(inv.all()) == 1


def test_remove_success_and_failure() -> None:
    inv = Inventory()
    p = Product("S2", "Thé", 5.0)
    inv.add(p)

    inv.remove("S2")
    assert len(inv.all()) == 0

    with pytest.raises(ProductNotFoundError):
        inv.remove("BADSKU")


def test_expired_and_total_value() -> None:
    inv = Inventory()

    expired = PerishableProduct(
        "E1",
        "Yaourt",
        3.0,
        expiry_date=date.today() - timedelta(days=1),
    )
    fresh = PerishableProduct(
        "E2",
        "Lait",
        4.0,
        expiry_date=date.today() + timedelta(days=10),
    )
    normal = Product("N1", "Sucre", 2.0)

    inv.add(expired)
    inv.add(fresh)
    inv.add(normal)

    expired_list = inv.expired()
    assert expired in expired_list
    assert fresh not in expired_list
    assert normal not in expired_list

    assert inv.total_value() == 6.0
