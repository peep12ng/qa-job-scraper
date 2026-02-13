from __future__ import annotations

import re
from typing import Dict, List, Tuple

from django.db import transaction
from django.db.models import Count

from jobs.models import DuplicateGroup, JobPost

_NON_WORD_RE = re.compile(r"[^0-9a-z]+")

def _normalize_text(value: str) -> str:
    text = (value or "").lower().strip()
    text = _NON_WORD_RE.sub(" ", text)
    return " ".join(text.split())

def build_group_key(job: JobPost) -> str:
    company = _normalize_text(job.company)
    title = _normalize_text(job.title)
    location = _normalize_text(job.location)
    return f"{company}|{title}|{location}"

def choose_representative(jobs: List[JobPost]) -> JobPost:
    def sort_key(job: JobPost):
        priority = job.source.priority if job.source else 999
        posting = job.posting_date or job.collected_at.date()
        return (priority, posting)
    return sorted(jobs, key=sort_key)[0]

@transaction.atomic
def dedupe_jobs() -> Dict[str, int]:
    items = (
        JobPost.objects.select_related("source")
        .all()
    )

    groups: Dict[str, List[JobPost]] = {}
    for job in items:
        key = build_group_key(job)
        groups.setdefault(key, []).append(job)

    created_groups = 0
    grouped_jobs = 0

    for key, jobs in groups.items():
        if len(jobs) <= 1:
            continue
        group = DuplicateGroup.objects.create(group_key=key)
        created_groups += 1

        representative = choose_representative(jobs)
        for job in jobs:
            job.duplicate_group = group
            job.save(update_fields=["duplicate_group"])
            grouped_jobs += 1

        # 대표 선정이 필요한 경우 후속 단계에서 처리
        _ = representative

    return {
        "total_jobs": items.count(),
        "grouped_jobs": grouped_jobs,
        "groups_created": created_groups,
    }
