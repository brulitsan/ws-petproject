import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'start_kafka_consumer': {
        'task': 'ws_src.stock_market.tasks.start_kafka_consumer',
        'schedule': 10.0,
    },
    'automatic_operations': {
        'task': 'ws_src.stock_market.tasks.automatic_operations',
        'schedule': 5.0,
    },
    'send_emails': {
        'task': 'ws_src.stock_market.tasks.send_emails',
        'schedule': 260.0,
    },
}
