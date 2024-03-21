from celery import shared_task
from common.choices import BaseOrderStatus, BaseOrderType
from ws_src.stock_market.brocker import kafka_consumer
from ws_src.stock_market.database import auto_operations
from ws_src.stock_market.models import Order
from ws_src.stock_market.schemas import AutoOperationsOrderSchema


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
