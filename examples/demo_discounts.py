from datetime import date, timedelta

from freshcart import PerishableProduct


def main() -> None:
    bientot = PerishableProduct(
        "SKU100", "Yaourt", 3.0, expiry_date=date.today() + timedelta(days=2)
    )
    plus_tard = PerishableProduct(
        "SKU101", "Fromage", 6.0, expiry_date=date.today() + timedelta(days=10)
    )
    perime = PerishableProduct(
        "SKU102", "Crème", 5.0, expiry_date=date.today() - timedelta(days=1)
    )

    for p in (bientot, plus_tard, perime):
        print(f"{p} | expired={getattr(p,'is_expired')} | final={p.final_price()}")


if __name__ == "__main__":
    main()
