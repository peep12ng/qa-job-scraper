from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Dict, Iterable, List, Optional

NEXT_PUSH_PATTERN = re.compile(r"self\.__next_f\.push\(\[1,\"(.*?)\"\]\)", re.DOTALL)
AREA_OBJECT_PATTERN = re.compile(r"\{[^{}]*\"type\":\"area\"[^{}]*\}")
SEOUL_CODES = {"I000"}
SEOUL_PREFIX = "I"
EMPLOYMENT_TYPE_MAP = {
    "1": "정규직",
    "2": "계약직",
    "3": "인턴",
    "4": "파견직",
    "5": "도급",
    "6": "프리랜서",
    "7": "아르바이트",
    "8": "연수/교육",
}

def _decode_next_segments(html: str) -> Iterable[str]:
    for match in NEXT_PUSH_PATTERN.finditer(html):
        raw = match.group(1)
        try:
            yield json.loads(f"\"{raw}\"")
        except json.JSONDecodeError:
            yield bytes(raw, "utf-8").decode("unicode_escape", errors="ignore")

def _extract_json_array(text: str, marker: str) -> Optional[str]:
    start = text.find(marker)
    if start == -1:
        return None
    i = start + len(marker) - 1
    depth = 0
    in_string = False
    escape = False
    for j in range(i, len(text)):
        ch = text[j]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == "\"":
                in_string = False
        else:
            if ch == "\"":
                in_string = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return text[i : j + 1]
    return None

def _extract_job_items(html: str) -> List[Dict]:
    for segment in _decode_next_segments(html):
        if "JOB_PRODUCT_LIST" not in segment:
            continue
        if "\"content\":[" not in segment:
            continue
        array_text = _extract_json_array(segment, "\"content\":[")
        if not array_text:
            continue
        try:
            items = json.loads(array_text)
            if isinstance(items, list):
                return items
        except json.JSONDecodeError:
            continue
    return []


def _extract_area_map(html: str) -> Dict[str, str]:
    area_map: Dict[str, str] = {}
    for segment in _decode_next_segments(html):
        if "\"type\":\"area\"" not in segment:
            continue
        for match in AREA_OBJECT_PATTERN.finditer(segment):
            try:
                obj = json.loads(match.group(0))
            except json.JSONDecodeError:
                continue
            code = obj.get("code")
            name = obj.get("displayName") or obj.get("tagDisplayName") or obj.get("originName")
            if not code or not name:
                continue
            if ">" in name:
                name = name.replace(">", " ").strip()
            area_map.setdefault(code, name)
    return area_map

def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None

def _resolve_location(area_codes: List[str], fallback: str) -> str:
    if any(code in SEOUL_CODES for code in area_codes):
        return "서울"
    if any(code.startswith(SEOUL_PREFIX) for code in area_codes):
        return "서울"
    return fallback

def _resolve_area_name(area_codes: List[str], area_map: Dict[str, str]) -> str:
    names: List[str] = []
    for code in area_codes:
        name = area_map.get(code)
        if not name:
            continue
        if (code in SEOUL_CODES or code.startswith(SEOUL_PREFIX)) and "서울" not in name:
            name = f"서울 {name}"
        if name not in names:
            names.append(name)
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return f"{names[0]} 외 {len(names) - 1}"

def _normalize_employment_type(value: object) -> str:
    if not value:
        return ""
    if isinstance(value, list):
        raw_values = [str(item) for item in value if item]
    else:
        raw_values = [str(value)]
    labels: List[str] = []
    for raw in raw_values:
        code = raw.split("/")[0].strip()
        label = EMPLOYMENT_TYPE_MAP.get(code)
        if label and label not in labels:
            labels.append(label)
    return ", ".join(labels)

def _normalize_tags(raw: Optional[str]) -> List[str, str]:
    if not raw:
        return "", ""
    cleaned = raw.strip(",").replace("&amp;", "&")
    tags = [tag.strip() for tag in cleaned.split(",") if tag.strip()]
    return ", ".join(tags), (tags[0] if tags else "")

def _experience_level(career_type: Optional[str], career_range: Optional[int]) -> str:
    ctype = str(career_type or "").strip()
    if ctype == "1":
        return "신입"
    if ctype == "2":
        if isinstance(career_range, int) and 0 < career_range < 90:
            return f"경력 {career_range}년"
        return "경력"
    if ctype == "3":
        return "신입/경력"
    return ""

def _experience_max_years(career_type: Optional[str], career_range: Optional[int]) -> Optional[int]:
    ctype = str(career_type or "").strip()
    if ctype == "1":
        return 1
    if isinstance(career_range, int) and 0 < career_range < 90:
        return career_range
    return None

def _build_url(job_id: Optional[str], base_url: str) -> str:
    if not job_id:
        return ""
    return f"{base_url}/Recruit/GI_Read/{job_id}"

def parse_jobkorea_list(html: str, base_url: str = "https://www.jobkorea.co.kr") -> List[Dict[str, object]]:
    raw_items = _extract_job_items(html)
    area_map = _extract_area_map(html)
    items: List[Dict[str, object]] = []

    for item in raw_items:
        if not isinstance(item, dict):
            continue
        job_id = item.get("id") or item.get("legacyJobNo")
        title = item.get("title") or ""
        company = item.get("companyName") or ""
        area_codes = item.get("areaCodeList") or []
        if not isinstance(area_codes, list):
            area_codes = []
        location = item.get("locationName") or item.get("location") or item.get("locationCode") or ""
        if not location:
            location = _resolve_area_name(area_codes, area_map)
        if not location:
            location = _resolve_location(area_codes, " ".join(area_codes))

        career_type = item.get("careerType")
        career_range = item.get("careerRange")

        tags, primary_category = _normalize_tags(item.get("jobClassificationOrIndustry"))

        posting_date = _parse_iso_date(item.get("createdAt"))
        closing_date = _parse_iso_date(
            (item.get("applicationPeriod") or {}).get("end")
        )

        items.append(
            {
                "source_code": "jobkorea",
                "source_job_id": str(job_id) if job_id else "",
                "title": title,
                "company": company,
                "location": location,
                "employment_type": _normalize_employment_type(item.get("employmentTypeCodeList")),
                "experience_level": _experience_level(career_type, career_range),
                "experience_max_years": _experience_max_years(career_type, career_range),
                "posting_date": posting_date,
                "closing_date": closing_date,
                "url": _build_url(str(job_id) if job_id else "", base_url),
                "description_snippet": "",
                "tags": tags,
                "source_category_path": primary_category,
            }
        )

    return items