import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','my_auto.settings')

app = Celery('my_auto')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

