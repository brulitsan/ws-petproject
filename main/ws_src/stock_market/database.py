from collections import OrderedDict
from typing import Any

from stock_market.exceptions import CurrencyPriceException, ProductPriceException
from ws_src.common.choices import BaseOrderStatus, BaseOrderType
from ws_src.stock_market.models import Order, Product, ProductCategories
from ws_src.stock_market.schemas import AutoOperationsOrderSchema, ProductSchema
from ws_src.users.database import update_user_balance
from ws_src.users.models import User


def get_quantity(order: Order) -> Any:
    products = order.product
    product_price = products.last_price
    quantity = order.transaction_price / product_price
    return quantity


def processing_quantity(order: OrderedDict) -> str:
    product = order.get("product")
    order["quantity"] = order["transaction_price"] / product.last_price
    return order["quantity"]


def update_or_create_products(product_data: dict) -> None:
    item = ProductSchema(**product_data)
    ProductCategories.objects.get_or_create(name=item.symbol)
    Product.objects.update_or_create(
        symbol=item.symbol,
        defaults=item.model_dump()
    )


def auto_operations(user: User, order_dto: AutoOperationsOrderSchema):
    match order_dto.type:
        case BaseOrderType.AUTO_SALE:
            validate_order_sale(user, order_dto)
            order_dto.status = BaseOrderStatus.success
        case BaseOrderType.AUTO_PURCHASE:
            validate_order_purchase(user, order_dto)
            order_dto.status = BaseOrderStatus.success
    return order_dto


def validate_order_sale(user: User, order_dto: AutoOperationsOrderSchema) -> None:
    if order_dto.currency_price > order_dto.product.last_price:
        update_user_balance(user, order_dto)
        raise ProductPriceException
    order_dto.status = BaseOrderStatus.in_process


def validate_order_purchase(user: User, order_dto: AutoOperationsOrderSchema) -> None:
    if order_dto.currency_price < order_dto.product.last_price:
        update_user_balance(user, order_dto)
        raise CurrencyPriceException
    order_dto.status = BaseOrderStatus.in_process
