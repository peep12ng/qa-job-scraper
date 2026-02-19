import os

os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret")
os.environ.setdefault("DJANGO_DEBUG", "true")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "*")
os.environ.setdefault("DB_ENGINE", "sqlite")
os.environ.setdefault("SCRAPE_INTERVAL_HOURS", "12")
os.environ.setdefault("SCRAPE_TIMEZONE", "UTC")
os.environ.setdefault("PLAYWRIGHT_BROWSER", "chromium")

from .base import * # noqa: F401,F403