from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class SourceSpec:
    code: str
    name: str
    priority: int
    base_url: str
    is_active: bool = True

SOURCES: List[SourceSpec] = [
    SourceSpec(code="saramin", name="사람인", priority=1, base_url="https://www.saramin.co.kr"),
    SourceSpec(code="jobkorea", name="잡코리아", priority=2, base_url="https://www.jobkorea.co.kr"),
    SourceSpec(code="wanted", name="원티드", priority=3, base_url="https://www.wanted.co.kr"),
    SourceSpec(code="incruit", name="인크루트", priority=4, base_url="https://www.incruit.com"),
    SourceSpec(code="rocketpunch", name="로켓펀치", priority=5, base_url="https://www.rocketpunch.com"),
]

def get_sources(active_only: bool = True) -> List[SourceSpec]:
    sources = [s for s in SOURCES if (s.is_active or not active_only)]
    return sorted(sources, key=lambda s: s.priority)

def get_source_codes(active_only: bool = True) -> List[str]:
    return [s.code for s in get_sources(active_only=active_only)]