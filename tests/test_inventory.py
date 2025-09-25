# But du fichier :
# - Vérifier que le service Inventory fonctionne comme prévu.
# - Couvrir : ajout, suppression, listing, filtrage "expired", total_value.
# - Tester les cas heureux ET les erreurs (exception custom).

from datetime import date, timedelta
import pytest

from freshcart.domain.inventory import Inventory, ProductNotFoundError
from freshcart.domain.products import Product, PerishableProduct


def test_add_and_all():
    # Arrange : inventaire vide + 1 produit
    inv = Inventory()
    p = Product("S1", "Café", 8.0)

    # Act : on ajoute le produit
    inv.add(p)

    # Assert : la liste "all" contient bien notre produit
    items = inv.all()
    assert len(items) == 1
    assert items[0].name == "Café"
    # Bonus : "all" retourne une COPIE → modifier 'items' ne doit pas impacter l'interne
    items.clear()
    assert len(inv.all()) == 1  # l'inventaire original n'a pas bougé


def test_remove_success_and_failure():
    inv = Inventory()
    p = Product("S2", "Thé", 5.0)
    inv.add(p)

    # Cas 1 : suppression réussie
    inv.remove("S2")
    assert len(inv.all()) == 0

    # Cas 2 : suppression d'un SKU inexistant → doit lever une exception métier
    with pytest.raises(ProductNotFoundError):
        inv.remove("BADSKU")


def test_expired_and_total_value():
    inv = Inventory()

    # Produit périmé (hier) : is_expired=True, final_price=0.0
    expired = PerishableProduct("E1", "Yaourt", 3.0, expiry_date=date.today() - timedelta(days=1))
    # Produit frais (expire dans 10 jours) : final_price=price (=6.0)
    fresh = PerishableProduct("E2", "Lait", 4.0, expiry_date=date.today() + timedelta(days=10))
    # Produit normal (non périssable) : final_price=price (=2.0)
    normal = Product("N1", "Sucre", 2.0)

    inv.add(expired)
    inv.add(fresh)
    inv.add(normal)

    # Vérifier le filtrage 'expired'
    expired_list = inv.expired()
    assert expired in expired_list
    assert fresh not in expired_list
    assert normal not in expired_list  # normal n'a pas is_expired

    # Vérifier la somme polymorphe des prix finaux :
    # - expired.final_price() = 0.0
    # - fresh.final_price()   = 4.0
    # - normal.final_price()  = 2.0
    # total = 0 + 4 + 2 = 6.0
    assert inv.total_value() == 6.0
