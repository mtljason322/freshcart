from datetime import date, timedelta
from freshcart.domain.products import Product, PerishableProduct

def main():
    p1 = Product("SKU001", "Café", 8.0)
    p2 = PerishableProduct("SKU002", "Lait", 4.0, expiry_date=date.today()+timedelta(days=2))

    print("Produit normal :", p1)
    print("Prix final café :", p1.final_price())

    print("Produit périssable :", p2)
    print("Prix final lait :", p2.final_price())

if __name__ == "__main__":
    main()
