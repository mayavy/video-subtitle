"""Celery application for the django Project."""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery('project')  # rabbitmq-server
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
