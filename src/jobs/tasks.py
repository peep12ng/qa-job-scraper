import time

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from typing import List

from collectors.core.fixture_loader import load_latest_fixture
from collectors.core.normalization import normalize_items
from collectors.core.registry import get_sources
from collectors.core.playwright_client import PlaywrightClient, PlaywrightConfig
from jobs.models import RunLog
from jobs.services.job_store import ensure_source, store_items

def _format_errors(errors, limit: int = 20, max_chars: int = 2000) -> str:
    if not errors:
        return ""
    message = "; ".join(errors[:limit])
    if len(message) > max_chars:
        return message[: max_chars - 3] + "..."
    return message

def _extract_items(payload):
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload.get("items") or []
    if isinstance(payload, list):
        return payload
    return None

def _backoff_seconds(attempt: int, base: float = 1.0, factor: float = 2.0, max_delay: float = 8.0) -> float:
    return min(max_delay, base * (factor ** attempt))

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

@shared_task
def scheduled_collect():
    summaries = []
    max_attempts = 3

    for source in get_sources(active_only=True):
        started_at = timezone.now()
        source_obj = ensure_source(
            source.code,
            name=source.name,
            base_url=source.base_url,
            priority=source.priority,
        )

        fixture_path = ""
        stored = 0
        skipped = 0
        all_errors: List[str] = []
        status = RunLog.STATUS_FAIL
        attempt_errors: List[str] = []
        completed = False

        for attempt in range(max_attempts):
            try:
                payload, fixture_path, error = load_latest_fixture(source.code)
                if error:
                    raise RuntimeError(error)

                extracted = _extract_items(payload)
                if extracted is None:
                    raise RuntimeError("invalid fixture payload")

                normalized, normalize_errors = normalize_items(items=extracted, source_code=source.code)
                stored, skipped, store_errors = store_items(normalized)

                all_errors = normalize_errors + store_errors
                if stored == 0 and (all_errors or skipped > 0):
                    status = RunLog.STATUS_FAIL
                elif all_errors or skipped > 0:
                    status = RunLog.STATUS_PARTIAL
                else:
                    status = RunLog.STATUS_SUCCESS

                completed = True
                break
            except Exception as exc:
                attempt_errors.append(f"attempt {attempt + 1}: {exc}")
                if attempt < max_attempts - 1:
                    time.sleep(_backoff_seconds(attempt))

        if not completed:
            all_errors = attempt_errors
            status = RunLog.STATUS_FAIL

        RunLog.objects.create(
            source=source_obj,
            status=status,
            started_at=started_at,
            finished_at=timezone.now(),
            items_collected=stored,
            error_message=_format_errors(all_errors),
        )

        summaries.append(
            {
                "source_code": source.code,
                "stored": stored,
                "skipped": skipped,
                "errors": len(all_errors),
                "status": status,
                "fixture": fixture_path or "",
            }
        )

    return summaries
