
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookShop.settings')

app = Celery('bookShop')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# testing
app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# celery beat
app.conf.beat_schedule = {
    'everyday-at-night': {
        'task': 'accounts.tasks.check_membership_status',
        'schedule': crontab(hour=0, minute=20),  #every night 12.00 AM
        'args': ()
    },
}
