from collections import OrderedDict
from typing import Any

from ws_src.stock_market.models import Order, Product, ProductCategories

from .schemas import ProductSchema


def get_quantity(obj: Order) -> Any:
    products = Product.objects.filter(id=obj.product_id)
    if not products:
        raise ValueError(f"No product with id {obj.product_id}")
    product = products[0]
    product_price = product.last_price
    quantity = obj.transaction_price / product_price
    return quantity


def processing_quantity(attrs: OrderedDict) -> OrderedDict:
    product = attrs.get("product")
    attrs["quantity"] = attrs["transaction_price"] / product.last_price
    return attrs


def update_or_create_products(product_data: list[dict]) -> None:
    for item in product_data:
        item = ProductSchema(**item)
        ProductCategories.objects.get_or_create(name=item.symbol)
        Product.objects.update_or_create(id=item.id, defaults=item.model_dump())
