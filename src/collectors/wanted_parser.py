from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

_NUMBER_RE = re.compile(r"(\d+)")

def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    return " ".join(text.split())

def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, list):
        return len(value) > 0
    return True

def _parse_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("1", "true", "yes", "y", "on"):
            return True
        if text in ("0", "false", "no", "n", "off"):
            return False
    return None

def _iter_sources(item: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    yield item
    for key in ("position", "job", "detail", "data"):
        value = item.get(key)
        if isinstance(value, dict):
            yield value

def _get_first_value(item: Dict[str, Any], keys: Iterable[str]) -> Any:
    for source in _iter_sources(item):
        for key in keys:
            if key in source and _has_value(source[key]):
                return source[key]
    return None

def _normalize_location(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return _clean_text(value)
    if isinstance(value, dict):
        for key in (
            "full_location",
            "fullLocation",
            "location",
            "name",
            "city",
            "region",
            "address",
        ):
            if _has_value(value.get(key)):
                return _clean_text(value.get(key))
        if _has_value(value.get("locations")):
            return _normalize_location(value.get("locations"))
        return ""
    if isinstance(value, list):
        parts = []
        for entry in value:
            part = _normalize_location(entry)
            if part:
                parts.append(part)
        return ", ".join(parts)
    return _clean_text(value)

def _extract_location(item: Dict[str, Any]) -> str:
    value = _get_first_value(
        item,
        [
            "location",
            "location_name",
            "locationName",
            "address",
            "region",
            "area",
            "areas",
            "locations",
        ],
    )
    return _normalize_location(value)

def _normalize_tags(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = [part.strip() for part in re.split(r"[,#/]", value) if part.strip()]
        return parts
    if isinstance(value, list):
        tags: List[str] = []
        for entry in value:
            if isinstance(entry, dict):
                tag = entry.get("title") or entry.get("name") or entry.get("tag") or entry.get("skill")
            else:
                tag = entry
            tag_text = _clean_text(tag)
            if tag_text:
                tags.append(tag_text)
        return tags
    if isinstance(value, dict):
        for key in ("title", "name", "tag", "skill"):
            tag_text = _clean_text(value.get(key))
            if tag_text:
                return [tag_text]
        return []
    tag_text = _clean_text(value)
    return [tag_text] if tag_text else []

def _extract_tags(item: Dict[str, Any]) -> tuple[str, str]:
    value = _get_first_value(
        item,
        [
            "skill_tags",
            "skillTags",
            "tags",
            "tag_list",
            "skills",
            "skill_list",
        ],
    )
    tags = _normalize_tags(value)
    return ", ".join(tags), (tags[0] if tags else "")

def _extract_company(item: Dict[str, Any]) -> str:
    value = _get_first_value(
        item,
        [
            "company",
            "company_name",
            "companyName",
            "company_name_ko",
            "companyNameKr",
            "company_ko",
        ],
    )
    if isinstance(value, dict):
        return _clean_text(
            value.get("name")
            or value.get("company_name")
            or value.get("companyName")
            or value.get("title")
            or ""
        )
    return _clean_text(value)

def _normalize_employment(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        parts = [_clean_text(entry) for entry in value if _clean_text(entry)]
        return ",".join(parts)
    if isinstance(value, dict):
        return _clean_text(value.get("name") or value.get("title") or value.get("type") or "")
    return _clean_text(value)

def _extract_employment_type(item: Dict[str, Any]) -> str:
    value = _get_first_value(
        item,
        [
            "employment_type",
            "employmentType",
            "contract_type",
            "contractType",
            "employment",
        ],
    )
    return _normalize_employment(value)

def _coerce_years(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        numbers = [int(n) for n in _NUMBER_RE.findall(value)]
        return max(numbers) if numbers else None
    if isinstance(value, list):
        numbers: List[int] = []
        for entry in value:
            year = _coerce_years(entry)
            if year is not None:
                numbers.append(year)
        return max(numbers) if numbers else None
    if isinstance(value, dict):
        for key in ("max", "max_year", "maxYears", "max_years", "to", "end", "year", "years"):
            if key in value:
                year = _coerce_years(value.get(key))
                if year is not None:
                    return year
    return None

def _extract_experience_max_years(item: Dict[str, Any]) -> Optional[int]:
    is_newbie = _parse_bool(_get_first_value(item, ["is_newbie", "isNewbie"]))
    if is_newbie is True:
        return 1

    annual_to = _coerce_years(_get_first_value(item, ["annual_to", "annualTo"]))
    if annual_to is not None:
        return annual_to
    annual_from = _coerce_years(_get_first_value(item, ["annual_from", "annualFrom"]))
    if annual_from is not None:
        return annual_from

    for key in (
        "max_year",
        "maxYears",
        "max_years",
        "max_experience",
        "maxExperience",
        "careerMax",
        "years",
        "year",
        "experience_years",
        "career_range",
        "careerRange",
    ):
        value = _get_first_value(item, [key])
        year = _coerce_years(value)
        if year is not None:
            return year
    value = _get_first_value(
        item,
        [
            "experience",
            "experience_level",
            "experienceLevel",
            "career",
            "careerLevel",
            "career_level",
        ],
    )
    return _coerce_years(value)

def _extract_experience_level(item: Dict[str, Any], max_years: Optional[int]) -> str:
    value = _get_first_value(
        item,
        [
            "experience_level",
            "experienceLevel",
            "career_level",
            "careerLevel",
            "experience",
            "career",
        ],
    )
    if isinstance(value, dict):
        value = value.get("label") or value.get("name") or value.get("title")
    text = _clean_text(value)
    if text:
        return text

    is_newbie = _parse_bool(_get_first_value(item, ["is_newbie", "isNewbie"]))
    if is_newbie is True:
        return "신입"

    annual_from = _coerce_years(_get_first_value(item, ["annual_from", "annualFrom"]))
    annual_to = _coerce_years(_get_first_value(item, ["annual_to", "annualTo"]))
    if annual_from is not None or annual_to is not None:
        if annual_from is not None and annual_to is not None:
            if annual_from == annual_to:
                return f"경력 {annual_to}년"
            return f"경력 {annual_from}~{annual_to}년"
        return f"경력 {annual_to or annual_from}년"

    if max_years is None:
        return ""
    if max_years <= 1:
        return "신입"
    return f"경력 {max_years}년"

def _parse_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 1_000_000_000_000:
            ts /= 1000.0
        try:
            return datetime.fromtimestamp(ts, tz=timezone.utc).date()
        except (OverflowError, OSError, ValueError):
            return None
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
                try:
                    return date(int(parts[0]), int(parts[1]), int(parts[2]))
                except ValueError:
                    return None
    return None

def _extract_description_snippet(item: Dict[str, Any]) -> str:
    value = _get_first_value(
        item,
        [
            "summary",
            "description",
            "intro",
            "position_description",
            "jobDescription",
        ],
    )
    if isinstance(value, dict):
        value = value.get("summary") or value.get("description")
    text = _clean_text(value)
    if len(text) > 200:
        return f"{text[:200]}..."
    return text

def _extract_source_category(item: Dict[str, Any], fallback: str) -> str:
    value = _get_first_value(
        item,
        [
            "job_category",
            "jobCategory",
            "category",
            "occupation",
            "job_group",
            "jobGroup",
        ],
    )
    if isinstance(value, dict):
        value = value.get("name") or value.get("title")
    if isinstance(value, list):
        value = ", ".join(_normalize_tags(value))
    text = _clean_text(value)
    return text or fallback

def _extract_source_job_id(item: Dict[str, Any]) -> str:
    value = _get_first_value(
        item,
        ["id", "position_id", "positionId", "job_id", "jobId", "positionID"],
    )
    return _clean_text(value)

def _extract_id_from_url(url: str) -> str:
    match = re.search(r"/wd/(\d+)", url or "")
    if match:
        return match.group(1)
    return ""

def _build_url(item: Dict[str, Any], base_url: str, source_job_id: str) -> str:
    value = _get_first_value(item, ["url", "link", "job_url", "jobUrl"])
    if _has_value(value):
        return _clean_text(value)
    if source_job_id:
        return f"{base_url}/wd/{source_job_id}"
    return ""

def _extract_job_items(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("data", "jobs", "positions", "results", "items", "list"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    for container_key in ("data", "result", "payload"):
        container = payload.get(container_key)
        if isinstance(container, dict):
            for key in ("jobs", "positions", "results", "items", "list"):
                value = container.get(key)
                if isinstance(value, list):
                    return value
    return []

def parse_wanted_list(payload: Any, base_url: str = "https://www.wanted.co.kr") -> List[Dict[str, object]]:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return []

    raw_items = _extract_job_items(payload)
    items: List[Dict[str, object]] = []

    for raw in raw_items:
        if not isinstance(raw, dict):
            continue

        source_job_id = _extract_source_job_id(raw)
        url = _build_url(raw, base_url, source_job_id)
        if not source_job_id and url:
            source_job_id = _extract_id_from_url(url)

        title = _clean_text(
            _get_first_value(
                raw,
                ["position", "title", "name", "position_title", "job_title"],
            )
        )
        company = _extract_company(raw)
        location = _extract_location(raw)
        employment_type = _extract_employment_type(raw)
        max_years = _extract_experience_max_years(raw)
        experience_level = _extract_experience_level(raw, max_years)
        posting_date = _parse_date(
            _get_first_value(
                raw,
                [
                    "created_at",
                    "createdAt",
                    "posted_at",
                    "postedAt",
                    "start_at",
                    "startAt",
                    "published_at",
                    "publishedAt",
                ],
            )
        )
        closing_date = _parse_date(
            _get_first_value(
                raw,
                [
                    "due_time",
                    "dueTime",
                    "end_at",
                    "endAt",
                    "close_at",
                    "closeAt",
                    "deadline",
                    "deadline_at",
                ],
            )
        )

        tags, primary_category = _extract_tags(raw)
        source_category_path = _extract_source_category(raw, primary_category)
        description_snippet = _extract_description_snippet(raw)

        if not source_job_id:
            continue

        items.append(
            {
                "source_code": "wanted",
                "source_job_id": source_job_id,
                "title": title,
                "company": company,
                "location": location,
                "employment_type": employment_type,
                "experience_level": experience_level,
                "experience_max_years": max_years,
                "posting_date": posting_date,
                "closing_date": closing_date,
                "url": url,
                "description_snippet": description_snippet,
                "tags": tags,
                "source_category_path": source_category_path,
            }
        )

    return items
