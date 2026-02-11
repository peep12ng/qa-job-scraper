from __future__ import annotations

import re
from datetime import date, datetime
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup

_DATE_YYMMDD_RE = re.compile(r"(\d{2})/(\d{2})/(\d{2})")
_DATE_MMDD_RE = re.compile(r"(\d{2})/(\d{2})")

def _clean_text(value: str) -> str:
    return " ".join((value or "").split())

def _parse_experience_max_years(text: str) -> Optional[int]:
    text = _clean_text(text)
    if not text:
        return None
    if "무관" in text:
        return None
    numbers = [int(n) for n in re.findall(r"(\d+)", text)]
    if numbers:
        return max(numbers)
    if "신입" in text:
        return 1
    return None

def _extract_source_job_id(card) -> str:
    value = card.get("value")
    if value:
        return value.strip()
    link = card.select_one("h2.job_tit a[href]")
    if link:
        href = link.get("href", "")
        qs = parse_qs(urlparse(href).query)
        if qs.get("rec_idx"):
            return qs["rec_idx"][0]
        match = re.search(r"rec_idx=(\d+)", href)
        if match:
            return match.group(1)
    return ""

def _extract_title_and_url(card, base_url: str) -> tuple[str, str]:
    link = card.select_one("h2.job_tit a[href]")
    if not link:
        return "", ""
    title_node = link.select_one("span") or link
    title = _clean_text(title_node.get_text(" ", strip=True))
    href = link.get("href", "")
    url = urljoin(base_url, href) if href else ""
    return title, url

def _extract_company(card) -> str:
    company_el = card.select_one(".area_corp .corp_name a")
    return _clean_text(company_el.get_text(" ", strip=True)) if company_el else ""

def _extract_job_condition(card) -> tuple[str, str, str]:
    condition = card.select_one(".job_condition")
    if not condition:
        return "", "", ""
    spans = [
        _clean_text(span.get_text(" ", strip=True))
        for span in condition.find_all("span")
    ]
    location = spans[0] if len(spans) >= 1 else""
    experience_level = spans[1] if len(spans) >= 2 else ""
    employment_type = ""
    if len(spans) >= 4:
        employment_type = spans[3]
    elif len(spans) == 3:
        employment_type = spans[2]
    return location, experience_level, employment_type

def _parse_posting_date(card) -> Optional[date]:
    day_el = card.select_one(".job_sector .job_day")
    text = _clean_text(day_el.get_text(" ", strip=True)) if day_el else ""
    match = _DATE_YYMMDD_RE.match(text)
    if not match:
        sector = card.select_one(".job_sector")
        if sector:
            match = _DATE_YYMMDD_RE.search(
                _clean_text(sector.get_text(" ", strip=True))
            )
    if not match:
        return None
    yy, mm, dd = map(int, match.groups())
    return date(2000 + yy, mm, dd)

def _parse_closing_date(card, posting_date: Optional[date]) -> Optional[date]:
    date_el = card.select_one(".job_date .date")
    if not date_el:
        return None
    text = _clean_text(date_el.get_text(" ", strip=True))
    if "채용시" in text or "상시" in text:
        return None
    match = _DATE_MMDD_RE.match(text)
    if not match:
        return None
    month, day = map(int, match.groups())
    year = posting_date.year if posting_date else datetime.now().year
    if posting_date and month < posting_date.month:
        year += 1
    return date(year, month, day)

def _extract_tags(card) -> tuple[str, str]:
    sector = card.select_one(".job_sector")
    if not sector:
        return "", ""
    tags = [
        _clean_text(tag.get_text(" ", strip=True))
        for tag in sector.select("a")
    ]
    tags = [tag for tag in tags if tag]
    primary_el = sector.select_one("b a")
    primary = _clean_text(primary_el.get_text(" ", strip=True)) if primary_el else ""
    if not primary and tags:
        primary = tags[0]
    return ", ".join(tags), primary

def parse_saramin_list(
    html: str,
    base_url: str = "https://www.saramin.co.kr",
) -> List[Dict[str, object]]:
    soup = BeautifulSoup(html, "html.parser")
    items: List[Dict[str, object]] = []

    for card in soup.select("div.item_recruit"):
        source_job_id = _extract_source_job_id(card)
        title, url = _extract_title_and_url(card, base_url)
        company = _extract_company(card)
        location, experience_level, employment_type = _extract_job_condition(card)
        posting_date = _parse_posting_date(card)
        closing_date = _parse_closing_date(card, posting_date)
        tags, primary_category = _extract_tags(card)

        if not source_job_id or not url:
            continue

        items.append(
            {
                "source_code": "saramin",
                "source_job_id": source_job_id,
                "title": title, 
                "company": company,
                "location": location,
                "employment_type": employment_type,
                "experience_level": experience_level,
                "experience_max_years": _parse_experience_max_years(experience_level),
                "posting_date": posting_date,
                "closing_date": closing_date,
                "url": url,
                "description_snippet": "",
                "tags": tags,
                "source_category_path": primary_category,
            }
        )

    return items