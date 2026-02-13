from dataclasses import dataclass
from typing import Dict, Iterable, List

@dataclass(frozen=True)
class RequiredFilters:
    location_keyword: str = "서울"
    keyword: str = "QA"
    max_experience_years: int = 1

SOURCE_CATEGORY_MAP: Dict[str, List[str]] = {
    # 예시: 사람인 직종 경로에 QA/테스터가 있을 경우 사용
    "saramin": ["QA", "테스터"],
    "jobkorea": [],
    "wanted": [],
    "incruit": [],
    "rocketpunch": [],
}

def get_required_filters() -> RequiredFilters:
    return RequiredFilters()

def get_source_categories(source_code: str) -> List[str]:
    return SOURCE_CATEGORY_MAP.get(source_code, [])

def normalize_text(value: str) -> str:
    return (value or "").strip().lower()

def matches_required_filters(item: Dict, filters: RequiredFilters) -> bool:
    location = normalize_text(item.get("location", ""))
    if normalize_text(filters.location_keyword) not in location:
        return False
    
    keyword = normalize_text(filters.keyword)
    haystack = " ".join(
        [
            normalize_text(item.get("title", "")),
            normalize_text(item.get("company", "")),
            normalize_text(item.get("tags", "")),
            normalize_text(item.get("description_snippet", "")),
        ]
    )
    if keyword not in haystack:
        return False
    
    max_years = item.get("experience_max_years")
    level = normalize_text(item.get("experience_level", ""))

    if max_years is not None:
        if max_years > filters.max_experience_years:
            return False
    else:
        if not (
            "신입" in level
            or "0~1" in level
            or "1년" in level
        ):
            return False
    
    return True

def apply_required_filters(items: Iterable[Dict], filters: RequiredFilters = None) -> List[Dict]:
    active_filters = filters or get_required_filters()
    return [item for item in items if matches_required_filters(item, active_filters)]