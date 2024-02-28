import asyncio

from kafka import KafkaConsumer, KafkaProducer


async def send_currency_info_request(text: str):
    producer = KafkaProducer(bootstrap_servers=["kafka:9092"])
    producer.send("take_crypto_requests", value=text.encode())
    producer.flush()


async def kafka_consumer():
    consumer = KafkaConsumer(
        "send_crypto_info",
        bootstrap_servers=["kafka:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    for message in consumer:  # надо сделать так, чтобы включалась при запуске приложения
        print(message.value)


asyncio.run(kafka_consumer())
