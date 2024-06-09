
from typing import List, Optional
from web.models import Category, Product, Order
from django.contrib.auth.models import User

def get_category(category_id: int) -> Optional[Category]:
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return None

def get_categories() -> List[Category]:
    return list(Category.objects.all())

def get_product(product_id: int) -> Optional[Product]:
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

def get_products() -> List[Product]:
    return list(Product.objects.all())

def get_order(order_id: int) -> Optional[Order]:
    try:
        return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None

def get_orders() -> List[Order]:
    return list(Order.objects.all())

# Add more CRUD functions as needed