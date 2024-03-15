from celery import shared_task
from stock_market.brocker import kafka_consumer


@shared_task()
def start_kafka_consumer():
    kafka_consumer()
    print(kafka_consumer())


# def start_kafka_consumer():
#     kafka_consumer_thread = threading.Thread(target=kafka_consumer)
#     kafka_consumer_thread.daemon = True
#     kafka_consumer_thread.start()
#
#
# start_kafka_consumer()
