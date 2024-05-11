from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nova.settings")

# Exmplo tasks
# TASKS = {
#     'update_performance': {
#         'task': 'track.tasks.update_performance',
#         'schedule': crontab(hour="*", minute="*", day_of_week="*")
#     },
# }

TASKS = {}

app = Celery('nova')
app.conf.CELERY_DEFAULT_QUEUE = 'default'
app.conf.CELERY_DEFAULT_EXCHANGE_TYPE = 'default'
app.conf.CELERY_DEFAULT_ROUTING_KEY = 'default'
app.conf.CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default', delivery_mode=1),
)

app.conf.beat_schedule = TASKS
app.conf.timezone = 'America/Manaus'

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
