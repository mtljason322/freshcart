from datetime import date, timedelta
from freshcart.domain.products import Product, PerishableProduct

def test_regular_product_price_is_unchanged():
    p = Product("SKU-REG", "Café", 8.0)
    assert p.final_price() == 8.0

def test_perishable_product_discount_when_close_to_expiry():
    p = PerishableProduct("SKU-PER", "Lait", 4.0, expiry_date=date.today() + timedelta(days=2))
    assert p.final_price() == 2.0  # -50% si <= 3 jours

def test_perishable_no_discount_when_not_close():
    p = PerishableProduct("SKU-PER2", "Yaourt", 4.0, expiry_date=date.today() + timedelta(days=10))
    assert p.final_price() == 4.0
