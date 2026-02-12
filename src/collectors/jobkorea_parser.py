from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Dict, Iterable, List, Optional

NEXT_PUSH_PATTERN = re.compile(r"self\.__next_f\.push\(\[1,\"(.*?)\"\]\)", re.DOTALL)

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

def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None
    
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

def _build_url(job_no: Optional[str], base_url: str) -> str:
    if not job_no:
        return ""
    return f"{base_url}/Recruit/GI_Read/{job_no}"

def parse_jobkorea_list(html: str, base_url: str = "https://www.jobkorea.co.kr") -> List[Dict[str, object]]:
    raw_items = _extract_job_items(html)
    items: List[Dict[str, object]] = []

    for item in raw_items:
        if not isinstance(item, dict):
            continue
        job_no = item.get("legacyJobNo") or item.get("id")
        title = item.get("title") or ""
        company = item.get("companyName") or ""
        location = item.get("locationName") or item.get("location") or item.get("locationCode") or ""
        if not location and item.get("areaCodeList"):
            location = " ".join(item.get("areaCodeList", []))

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
                "source_job_id": str(job_no) if job_no else "",
                "title": title,
                "company": company,
                "location": location,
                "employment_type": ",".join(item.get("employmentTypeCodeList", []) or []),
                "experience_level": _experience_level(career_type, career_range),
                "experience_max_years": _experience_max_years(career_type, career_range),
                "posting_date": posting_date,
                "closing_date": closing_date,
                "url": _build_url(str(job_no) if job_no else "", base_url),
                "description_snippet": "",
                "tags": tags,
                "source_category_path": primary_category,
            }
        )

    return items