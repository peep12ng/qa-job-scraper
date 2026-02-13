from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from jobs.models import JobPost, Source

def ensure_source(
    code: str,
    name: str | None = None,
    base_url: str | None = None,
    priority: int | None = None,
) -> Source:
    defaults = {
        "name": name or code,
        "priority": priority if priority is not None else 999,
        "base_url": base_url or "",
        "is_active": True,
    }
    source, created = Source.objects.get_or_create(code=code, defaults=defaults)
    if not created:
        updates = {}
        if name and not source.name:
            updates["name"] = name
        if base_url and not source.base_url:
            updates["base_url"] = base_url
        if priority is not None and source.priority != priority:
            updates["priority"] = priority
        if updates:
            for key, value in updates.items():
                setattr(source, key, value)
            source.save(update_fields=list(updates.keys()))
    return source

def store_items(items: Iterable[Dict[str, object]]) -> Tuple[int, int, List[str]]:
    stored = 0
    skipped = 0
    errors: List[str] = []

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            skipped += 1
            errors.append(f"item[{index}] invalid type")
            continue

        source_code = item.get("source_code")
        if not source_code:
            skipped += 1
            errors.append(f"item[{index}] missing source_code")
            continue

        source_job_id = item.get("source_job_id")
        if not source_job_id:
            skipped += 1
            errors.append(f"item[{index}] missing source_job_id")
            continue

        source = ensure_source(source_code)

        defaults = {
            "title": item.get("title", ""),
            "company": item.get("company", ""),
            "location": item.get("location", ""),
            "employment_type": item.get("employment_type", ""),
            "experience_level": item.get("experience_level", ""),
            "experience_max_years": item.get("experience_max_years"),
            "posting_date": item.get("posting_date"),
            "closing_date": item.get("closing_date"),
            "url": item.get("url", ""),
            "description_snippet": item.get("description_snippet", ""),
            "tags": item.get("tags", ""),
            "source_category_path": item.get("source_category_path", ""),
        }

        try:
            JobPost.objects.update_or_create(
                source=source,
                source_job_id=source_job_id,
                defaults=defaults,
            )
            stored += 1
        except Exception as exc:
            skipped += 1
            errors.append(f"item[{index}] db_error: {exc}")

    return stored, skipped, errors
