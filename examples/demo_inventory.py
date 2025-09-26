from datetime import date, timedelta

from freshcart import Inventory, PerishableProduct, Product


def main() -> None:
    inv = Inventory()

    cafe = Product("SKU001", "Café", 8.0)
    lait = PerishableProduct(
        "SKU002",
        "Lait",
        4.0,
        expiry_date=date.today() + timedelta(days=2),  # kw-only
    )
    sucre = Product("SKU003", "Sucre", 2.0)

    inv.add(cafe)
    inv.add(lait)
    inv.add(sucre)

    print("Tous les produits :", inv.all())
    print("Périmés :", inv.expired())
    print("Valeur totale (final_price) :", inv.total_value())


if __name__ == "__main__":
    main()
