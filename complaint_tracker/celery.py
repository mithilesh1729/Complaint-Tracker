import os

from celery import Celery

# Tell Celery which Django settings to use
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "complaint_tracker.settings.dev",
)

# Create Celery application
app = Celery("complaint_tracker")

# Read configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks.py in installed apps
app.autodiscover_tasks()