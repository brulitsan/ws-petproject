import json

from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer

from .database import update_or_create_products


def send_currency_info_request(text: str):
    producer = KafkaProducer(bootstrap_servers=[settings.KAFKA_BROKER_PATH])
    producer.send("take_crypto_requests", value=text.encode())
    producer.flush()


def kafka_consumer():
    print("Kafka consumer started.")
    consumer = KafkaConsumer(
        "send_crypto_info",
        group_id="my_group_id",
        bootstrap_servers=[settings.KAFKA_BROKER_PATH],
        auto_offset_reset='earliest'
    )
    while True:
        message = consumer.poll(timeout_ms=1000)
        if message is not None:
            for topic_partition, records in message.items():  # pylint: disable=unused-variable
                for record in records:
                    value = record.value.decode()
                    value = json.loads(value)
                    for product_value in value:
                        update_or_create_products(product_value)
            consumer.commit()
