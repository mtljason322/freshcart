# But : couvrir propriété/validation, tri, périssable, final_price.

from datetime import date, timedelta

import pytest

from freshcart.domain.products import PerishableProduct, Product


def test_price_property_validation() -> None:
    p = Product("SKU-1", "Café", 8.0)
    assert p.price == 8.0

    p.price = 10.249  # arrondi à 2 décimales
    assert p.price == 10.25

    with pytest.raises(ValueError):
        p.price = -1


def test_str_and_ordering() -> None:
    p1 = Product("A", "ProdA", 5.0)
    p2 = Product("B", "ProdB", 7.0)
    assert "ProdA" in str(p1)
    assert sorted([p2, p1])[0] == p1


def test_perishable_is_expired_and_discount() -> None:
    expired = PerishableProduct(
        "E1",
        "Yaourt",
        3.0,
        expiry_date=date.today() - timedelta(days=1),
    )
    soon = PerishableProduct(
        "S1",
        "Lait",
        4.0,
        expiry_date=date.today() + timedelta(days=2),
    )
    later = PerishableProduct(
        "L1",
        "Fromage",
        6.0,
        expiry_date=date.today() + timedelta(days=10),
    )

    assert expired.is_expired is True
    assert expired.final_price() == 0.0

    assert soon.is_expired is False
    assert soon.final_price() == 2.0

    assert later.final_price() == 6.0


def test_regular_product_final_price() -> None:
    p = Product("SKU-REG2", "Thé", 5.5)
    assert p.final_price() == 5.5
