from rest_framework.exceptions import ValidationError
from ws_src.common.choices import BaseOrderType
from ws_src.stock_market.schemas import OrderSchema
from ws_src.users.models import User, UserProduct


def update_user_balance(user: User, order_dto: OrderSchema) -> None:
    match order_dto.type:
        case BaseOrderType.SALE:
            validate_and_decrease_user_balance(user, order_dto)
            update_or_create_user_product(user, order_dto)
        case BaseOrderType.PURCHASE if update_or_create_user_product(user, order_dto):
            increase_user_balance(user, order_dto)


def validate_and_decrease_user_balance(user: User, order_dto: OrderSchema) -> None:
    if user.balance < order_dto.transaction_price:
        raise ValidationError("not enough funds to make a purchase")
    user.balance -= order_dto.transaction_price
    user.save(update_fields=["balance"])


def increase_user_balance(user: User, order_dto: OrderSchema) -> None:
    user.balance += order_dto.transaction_price
    user.save(update_fields=["balance"])


def update_or_create_user_product(user: User, order_dto: OrderSchema) -> UserProduct:
    user_product, created = get_or_create_user_product(user, order_dto)
    update_user_product_based_on_order_type(user_product, created, order_dto)
    return user_product


def get_or_create_user_product(user: User, order_dto: OrderSchema) -> UserProduct:
    return UserProduct.objects.get_or_create(
        user_id=user.id,
        user_product=order_dto.product,
        defaults={
            "quantity": order_dto.quantity,
            "price": order_dto.transaction_price
        },
    )


def update_user_product_based_on_order_type(
        user_product: UserProduct,
        created: bool,
        order_dto: OrderSchema
) -> None:
    match order_dto.type:
        case BaseOrderType.SALE if not created:
            increase_user_product_quantity_and_price(user_product, order_dto)
        case BaseOrderType.PURCHASE:
            validate_and_decrease_user_product(user_product, order_dto)


def increase_user_product_quantity_and_price(
        user_product: UserProduct,
        order_dto: OrderSchema,
) -> None:
    user_product.quantity += order_dto.quantity
    user_product.price += order_dto.transaction_price
    user_product.save(update_fields=["quantity", "price"])


def validate_and_decrease_user_product(
        user_product: UserProduct,
        order_dto: OrderSchema,
) -> None:
    if (user_product.quantity < order_dto.quantity
            or user_product.price < order_dto.transaction_price):
        raise ValidationError("invalid quantity or price")
    user_product.quantity -= order_dto.quantity
    user_product.price -= order_dto.transaction_price
    user_product.save(update_fields=["quantity", "price"])
