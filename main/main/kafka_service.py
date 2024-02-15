from django.conf import settings
from kafka import KafkaProducer
from kafka.errors import KafkaError


def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer="utf-8"
    )


def send_text_to_kafka(data):
    producer = create_kafka_producer()
    try:
        producer.send(settings.KAFKA_TOPIC, data)
        producer.flush()
        return True
    except KafkaError:
        print(f"Error sending text to Kafka topic: {KafkaError}")
        return False
