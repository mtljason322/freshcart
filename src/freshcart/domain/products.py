from dataclasses import dataclass
from datetime import date

@dataclass
class Product:
    sku: str #id unique
    name: str
    price: float


    def final_price(self) -> float:
        return self.price
    
@dataclass
class PerishableProduct(Product):
    expiry_date: date

    def final_price(self) -> float:
        days_left = (self.expiry_date - date.today()).days
        if days_left <= 3:
            return round(self.price * 0.5, 2)
        return self.price
