
from ws_src.common.choices import BaseOrderStatus, BaseOrderType
from ws_src.stock_market.models import Product, ProductCategories
from ws_src.stock_market.schemas import AutoOperationsOrderSchema, ProductSchema
from ws_src.users.database import update_user_balance
from ws_src.users.models import User


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
        case BaseOrderType.AUTO_PURCHASE:
            validate_order_purchase(user, order_dto)
    return order_dto


def validate_order_sale(user: User, order_dto: AutoOperationsOrderSchema) -> None:
    if order_dto.currency_price > order_dto.product.last_price:
        update_user_balance(user, order_dto)
    order_dto.status = BaseOrderStatus.in_process


def validate_order_purchase(user: User, order_dto: AutoOperationsOrderSchema) -> None:
    if order_dto.currency_price < order_dto.product.last_price:
        update_user_balance(user, order_dto)
    order_dto.status = BaseOrderStatus.in_process
