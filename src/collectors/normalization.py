from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

REQUIRED_FIELDS = (
    "source_code",
    "source_job_id",
    "title",
    "company",
    "location",
    "url",
)

def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())

def normalize_tags(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        parts = [normalize_text(entry) for entry in value if normalize_text(entry)]
        return ", ".join(parts)
    if isinstance(value, dict):
        return normalize_text(
            value.get("name")
            or value.get("title")
            or value.get("tag")
            or value.get("skill")
        )
    return normalize_text(value)

def coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.isdigit():
            return int(text)
        numbers = [int(n) for n in re.findall(r"\d+", text)]
        if numbers:
            return numbers[-1]
    return None

def coerce_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
        except ValueError:
            pass
        for sep in ("-", ".", "/"):
            parts = text.split(sep)
            if len(parts) == 3 and all(part.isdigit() for part in parts):
                year, month, day = map(int, parts)
                if year < 100:
                    year += 2000
                try:
                    return date(year, month, day)
                except ValueError:
                    return None
    return None

def normalize_item(
    item: Dict[str, Any],
    source_code: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    normalized: Dict[str, Any] = {
        "source_code": normalize_text(item.get("source_code") or source_code),
        "source_job_id": normalize_text(item.get("source_job_id")),
        "title": normalize_text(item.get("title")),
        "company": normalize_text(item.get("company")),
        "location": normalize_text(item.get("location")),
        "employment_type": normalize_text(item.get("employment_type")),
        "experience_level": normalize_text(item.get("experience_level")),
        "experience_max_years": coerce_int(item.get("experience_max_years")),
        "posting_date": coerce_date(item.get("posting_date")),
        "closing_date": coerce_date(item.get("closing_date")),
        "url": normalize_text(item.get("url")),
        "description_snippet": normalize_text(item.get("description_snippet")),
        "tags": normalize_tags(item.get("tags")),
        "source_category_path": normalize_text(item.get("source_category_path")),
    }

    missing = [field for field in REQUIRED_FIELDS if not normalized.get(field)]
    if missing:
        return None, f"missing required fields: {', '.join(missing)}"

    return normalized, None

def normalize_items(
    items: Iterable[Dict[str, Any]],
    source_code: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    normalized: List[Dict[str, Any]] = []
    errors: List[str] = []

    for index, item in enumerate(items or []):
        if not isinstance(item, dict):
            errors.append(f"item[{index}] invalid type")
            continue
        normalized_item, error = normalize_item(item, source_code=source_code)
        if error:
            errors.append(f"item[{index}] {error}")
            continue
        normalized.append(normalized_item)

    return normalized, errors