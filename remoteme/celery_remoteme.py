import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "remoteme.settings")


app = Celery("remoteme")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "parser-5-min-after-midnight": {
        "task": "jobs.tasks.load_hh_data",
        "schedule": crontab(minute=5, hour=0),
    },
}

app.conf.timezone = settings.TIME_ZONE


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
