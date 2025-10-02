"""
Freshcart - package principal
Expose les objets importants pour éviter les imports trop longs.
"""

# from freshcart.domain.products import Product
# on pourra faire :
# from freshcart import Product


from .domain.inventory import Inventory, ProductNotFoundError
from .domain.products import PerishableProduct, Product

__all__ = [
    "Product",
    "PerishableProduct",
    "Inventory",
    "ProductNotFoundError",
]
