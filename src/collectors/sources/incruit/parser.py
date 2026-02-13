from __future__ import annotations

import re
from datetime import date, datetime
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup

_DATE_YMD_RE = re.compile(r"(20\d{2})[./-](\d{1,2})[./-](\d{1,2})")
_DATE_YYMD_RE = re.compile(r"(\d{2})[./-](\d{1,2})[./-](\d{1,2})")
_DATE_MD_RE = re.compile(r"(\d{1,2})[./-](\d{1,2})")

def _clean_text(value: str) -> str:
    return " ".join((value or "").split())

def _parse_date_from_text(text: str, reference: Optional[date] = None) -> Optional[date]:
    text = _clean_text(text)
    if not text:
        return None

    match = _DATE_YMD_RE.search(text)
    if match:
        year, month, day = map(int, match.groups())
        return date(year, month, day)

    match = _DATE_YYMD_RE.search(text)
    if match:
        yy, month, day = map(int, match.groups())
        return date(2000 + yy, month, day)

    match = _DATE_MD_RE.search(text)
    if match:
        month, day = map(int, match.groups())
        year = (reference.year if reference else datetime.now().year)
        if reference and month < reference.month:
            year += 1
        return date(year, month, day)

    return None

def _parse_posting_and_closing(texts: List[str]) -> tuple[Optional[date], Optional[date]]:
    posting_date = None
    closing_date = None

    for raw in texts:
        text = _clean_text(raw)
        if not text:
            continue

        if "등록" in text or "수정" in text:
            posting_date = _parse_date_from_text(text, posting_date)
            continue

        if "상시" in text or "채용시" in text:
            continue

        if "마감" in text or "D-" in text or "~" in text:
            closing_date = _parse_date_from_text(text, posting_date)
            continue

        if closing_date is None:
            closing_date = _parse_date_from_text(text, posting_date)

    return posting_date, closing_date

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

def _extract_source_job_id(row, url: str) -> str:
    jobno = row.get("jobno")
    if jobno:
        return jobno.strip()
    if url:
        qs = parse_qs(urlparse(url).query)
        if qs.get("job"):
            return qs["job"][0]
        match = re.search(r"job=(\d+)", url)
        if match:
            return match.group(1)
    return ""

def _extract_title_and_url(row, base_url: str) -> tuple[str, str]:
    link = row.select_one(".cell_mid .cl_top a[href]")
    if not link:
        return "", ""
    title = _clean_text(link.get_text(" ", strip=True))
    href = link.get("href", "")
    url = urljoin(base_url, href) if href else ""
    return title, url

def _extract_company(row) -> str:
    company_el = row.select_one(".cell_first .cpname")
    return _clean_text(company_el.get_text(" ", strip=True)) if company_el else ""

def _extract_meta(row) -> tuple[str, str, str]:
    spans = row.select(".cell_mid .cl_md span")
    texts = [_clean_text(span.get_text(" ", strip=True)) for span in spans]
    texts = [text for text in texts if text]

    location = texts[0] if len(texts) >= 1 else ""
    experience_level = texts[1] if len(texts) >= 2 else ""
    employment_type = texts[-1] if len(texts) >= 3 else ""
    return location, experience_level, employment_type

def _extract_tags(row) -> tuple[str, str]:
    tags = [
        _clean_text(tag.get_text(" ", strip=True))
        for tag in row.select(".cell_mid .cl_btm span")
    ]
    tags = [tag.strip(",") for tag in tags if tag]
    primary = tags[0] if tags else ""
    return ", ".join(tags), primary

def parse_incruit_list(
    html: str,
    base_url: str = "https://www.incruit.com",
) -> List[Dict[str, object]]:
    soup = BeautifulSoup(html, "html.parser")
    items: List[Dict[str, object]] = []

    for row in soup.select("ul.c_row[jobno]"):
        title, url = _extract_title_and_url(row, base_url)
        source_job_id = _extract_source_job_id(row, url)
        company = _extract_company(row)
        location, experience_level, employment_type = _extract_meta(row)
        tags, primary_category = _extract_tags(row)

        date_spans = [span.get_text(" ", strip=True) for span in row.select(".cell_last .cl_btm span")]
        posting_date, closing_date = _parse_posting_and_closing(date_spans)

        if not source_job_id or not url:
            continue

        items.append(
            {
                "source_code": "incruit",
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
