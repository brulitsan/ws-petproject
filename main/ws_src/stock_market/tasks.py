from celery import shared_task
from common.choices import BaseOrderStatus, BaseOrderType
from ws_src.stock_market.brocker import kafka_consumer
from ws_src.stock_market.database import auto_operations
from ws_src.stock_market.models import Order
from ws_src.stock_market.schemas import AutoOperationsOrderSchema

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

NOTIFICATION_PERIOD = settings.NOTIFICATION_PERIOD
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


@shared_task()
def start_kafka_consumer():
    kafka_consumer()


@shared_task()
def automatic_operations():
    orders = Order.objects.select_related('product', 'user').filter(
        status=BaseOrderStatus.in_process,
        type__in=[BaseOrderType.AUTO_PURCHASE, BaseOrderType.AUTO_SALE]
    )
    for order in orders:
        order_dto = AutoOperationsOrderSchema.model_validate(order)
        auto_operations(user=order.user, order_dto=order_dto)


@shared_task()
def send_emails() -> None:
    updated_orders = (
        Order.objects.filter(
            updated_at__gte=timezone.now() - NOTIFICATION_PERIOD
        ).select_related('product', 'user').all()
    )
    message = ""
    for order in updated_orders:
        if order.status == BaseOrderStatus.success:
            if order.type == BaseOrderType.AUTO_SALE:
                message = f'Currency {order.product.symbol} sealed!'
            if order.type == BaseOrderType.AUTO_PURCHASE:
                message = f'Currency {order.product.symbol} purchased!'
            from_email = EMAIL_HOST_USER
            to_email_list = [order.user.email]
            send_mail(
                "automatic operations",
                message,
                from_email,
                to_email_list,
                fail_silently=False,
            )
