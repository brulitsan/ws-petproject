from decimal import Decimal

from rest_framework.exceptions import ValidationError

from ws_src.common.choices import BaseOrderType
from .models import UserProduct


def update_user_balance(user, order_dto):
    transaction_price_decimal = Decimal(str(order_dto.transaction_price))
    if order_dto.type == BaseOrderType.SALE:
        if user.balance < transaction_price_decimal:
            raise ValidationError('Недостаточно средств для совершения покупки.')
        else:
            user.balance -= transaction_price_decimal
    elif order_dto.type == BaseOrderType.PURCHASE:
        if update_or_create_user_product(user, order_dto) is not None:
            user.balance += transaction_price_decimal
    user.save(update_fields=['balance'])


def update_or_create_user_product(user, order_dto):
    quantity = Decimal(str(order_dto.quantity))
    price = Decimal(str(order_dto.transaction_price))
    user_product, created = UserProduct.objects.get_or_create(
        user_id=user.id,
        user_product_id=order_dto.product_id,
        defaults={
            'quantity': quantity,
            'price': price
        }
    )
    if order_dto.type == BaseOrderType.SALE:
        if not created:
            user_product.quantity += quantity
            user_product.price += price
    elif order_dto.type == BaseOrderType.PURCHASE:
        if user_product.quantity < quantity or user_product.price < price:
            raise ValidationError('invalid quantity or price')
        else:
            user_product.quantity -= quantity
            user_product.price -= price
    user_product.save(update_fields=['quantity', 'price'])
    return user_product


