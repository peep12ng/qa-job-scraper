from celery import shared_task
from django.conf import settings

from collectors.playwright_client import PlaywrightClient, PlaywrightConfig

@shared_task
def playwright_smoke(url: str):
    config = PlaywrightConfig(
        browser=settings.PLAYWRIGHT_BROWSER,
        headless=settings.PLAYWRIGHT_HEADLESS,
        timeout_ms=settings.PLAYWRIGHT_TIMEOUT_MS,
    )
    with PlaywrightClient(config) as client:
        title, html = client.fetch(url)
    return {"url": url, "title": title, "bytes": len(html)}
