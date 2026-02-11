import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa_job_scraper.settings.local")

app = Celery("qa_job_scraper")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
