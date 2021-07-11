from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paymentAPI.settings')

app = Celery('paymentAPI')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "update_accounts": {
        "task": "payment.tasks.update_accounts",
        "schedule": crontab(minute='*/5')
    }
}
