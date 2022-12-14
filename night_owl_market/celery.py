import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'night_owl_market.settings')

broker = os.getenv("BROKER", "127.0.0.1")


app = Celery('night_owl_market',
             broker=f'redis://{broker}:6379/1',
             backend=f'redis://{broker}:6379/2')

app.conf.update(
    result_expires=3600,
)

app.conf.task_routes = {
    'market.tasks.import_message_to_db': {'queue': 'msg_to_db'},
    'chat.tasks.create_message': {'queue': 'msg_to_group'}
}

app.autodiscover_tasks()
