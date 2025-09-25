# On importe date/timedelta pour fabriquer des dates dynamiques (aujourd’hui + x jours)
from datetime import date, timedelta

# pytest : framework de test (on l’a installé avec pip)
import pytest

# On importe nos classes à tester
from freshcart.domain.products import Product, PerishableProduct


# -------------------------------------------------------------------
# 1) Test de la propriété "price" avec validation
# -------------------------------------------------------------------
def test_price_property_validation():
    # On crée un produit normal
    p = Product("SKU-1", "Café", 8.0)

    # Vérifie que le prix est bien celui donné
    assert p.price == 8.0

    # On change le prix → devrait être arrondi à 2 décimales
    p.price = 10.249
    assert p.price == 10.25

    # Cas invalide : prix négatif → devrait lever une erreur
    with pytest.raises(ValueError):
        p.price = -1


# -------------------------------------------------------------------
# 2) Test de l'affichage et de l'ordre (tri)
# -------------------------------------------------------------------
def test_str_and_ordering():
    # Deux produits avec prix différents
    p1 = Product("A", "ProdA", 5.0)
    p2 = Product("B", "ProdB", 7.0)

    # __str__ → doit contenir le nom du produit
    assert "ProdA" in str(p1)

    # Tri par prix → p1 (5.0) doit être avant p2 (7.0)
    assert sorted([p2, p1])[0] == p1


# -------------------------------------------------------------------
# 3) Test du produit périssable (expiration + réduction)
# -------------------------------------------------------------------
def test_perishable_is_expired_and_discount():
    # Produit déjà périmé hier
    expired = PerishableProduct(
        "E1", "Yaourt", 3.0, expiry_date=date.today() - timedelta(days=1)
    )

    # Produit qui expire dans 2 jours
    soon = PerishableProduct(
        "S1", "Lait", 4.0, expiry_date=date.today() + timedelta(days=2)
    )

    # Produit qui expire dans 10 jours
    later = PerishableProduct(
        "L1", "Fromage", 6.0, expiry_date=date.today() + timedelta(days=10)
    )

    # ---- Cas 1 : périmé ----
    assert expired.is_expired is True
    assert expired.final_price() == 0.0  # valeur nulle car déjà périmé

    # ---- Cas 2 : expire bientôt (<= 3 jours) ----
    assert soon.is_expired is False
    assert soon.final_price() == 2.0  # réduction -50% sur 4.0

    # ---- Cas 3 : expiration lointaine (> 3 jours) ----
    assert later.final_price() == 6.0  # prix normal, aucune réduction


def test_regular_product_final_price():
    p = Product("SKU-REG2", "Thé", 5.5)
    # Appelle explicitement la méthode final_price()
    assert p.final_price() == 5.5
