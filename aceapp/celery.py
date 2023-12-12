
from celery import Celery
from django.conf import settings
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aceapp.settings.local')
# Create a Celery instance
app = Celery('aceapp')

# Load Celery settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')


# Define a schedule for the task (daily at 8:00 AM)
app.conf.beat_schedule = {
    'send-daily-emails': {
        'task': 'Sockets.celery.py.send_daily_emails',
        'schedule': crontab( minute=5),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Auto-discover tasks in all installed apps
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()