
from collections import OrderedDict
from typing import Any

from ws_src.stock_market.models import Order, Product, ProductCategories

from .schemas import ProductSchema


def get_quantity(order: Order) -> Any:
    products = order.product
    product_price = products.last_price
    quantity = order.transaction_price / product_price
    return quantity


def processing_quantity(order: OrderedDict) -> OrderedDict:
    product = order.get("product")
    order["quantity"] = order["transaction_price"] / product.last_price
    return order


def update_or_create_products(product_data: dict) -> None:
    item = ProductSchema(**product_data)
    ProductCategories.objects.get_or_create(name=item.symbol)
    Product.objects.update_or_create(
        symbol=item.symbol,
        defaults=item.model_dump()
    )
