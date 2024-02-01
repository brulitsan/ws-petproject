from rest_framework.exceptions import ValidationError

from ws_src.stock_market.schemas import OrderSchema
from ws_src.common.choices import BaseOrderType
from ws_src.users.models import UserProduct, User


def update_user_balance(user: User, order_dto: OrderSchema):
    transaction_price = order_dto.transaction_price
    if order_dto.type == BaseOrderType.SALE:
        check_user_balance_for_sale(user, transaction_price)
        decrease_user_balance(user, transaction_price)
    elif order_dto.type == BaseOrderType.PURCHASE:
        if update_or_create_user_product(user, order_dto):
            increase_user_balance(user, transaction_price)
    user.save(update_fields=["balance"])


def check_user_balance_for_sale(user: User, transaction_price: float):
    if user.balance < transaction_price:
        raise ValidationError("not enough funds to make a purchase")


def decrease_user_balance(user: User, amount: float):
    user.balance -= amount


def increase_user_balance(user: User, amount: float):
    user.balance += amount


def update_or_create_user_product(user: User, order_dto: OrderSchema):
    user_product, created = get_or_create_user_product(user, order_dto)
    update_user_product_based_on_order_type(user_product, created, order_dto)
    user_product.save(update_fields=["quantity", "price"])
    return user_product


def get_or_create_user_product(user: User, order_dto: OrderSchema):
    return UserProduct.objects.get_or_create(
        user_id=user.id,
        user_product=order_dto.product,
        defaults={"quantity": order_dto.quantity, "price": order_dto.transaction_price},
    )


def update_user_product_based_on_order_type(user_product, created, order_dto):
    if order_dto.type == BaseOrderType.SALE:
        if not created:
            increase_user_product_quantity_and_price(
                user_product, order_dto.quantity, order_dto.transaction_price
            )
    elif order_dto.type == BaseOrderType.PURCHASE:
        validate_user_product_for_purchase(
            user_product, order_dto.quantity, order_dto.transaction_price
        )
        decrease_user_product_quantity_and_price(
            user_product, order_dto.quantity, order_dto.transaction_price
        )


def increase_user_product_quantity_and_price(user_product, quantity, price):
    user_product.quantity += quantity
    user_product.price += price


def decrease_user_product_quantity_and_price(user_product, quantity, price):
    user_product.quantity -= quantity
    user_product.price -= price


def validate_user_product_for_purchase(user_product, quantity, price):
    if user_product.quantity < quantity or user_product.price < price:
        raise ValidationError("invalid quantity or price")
