from django.shortcuts import render

from jobs.models import JobPost, Source

JOBKOREA_EMPLOYMENT_MAP = {
    "1": "정규직",
    "2": "계약직",
    "3": "인턴",
    "4": "파견직",
    "5": "도급",
    "6": "프리랜서",
    "7": "아르바이트",
    "8": "연수/교육",
}

MAX_LIST_JOBS = 200

def _normalize_jobkorea_employment(raw: str) -> str:
    if not raw:
        return ""
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    labels = []
    for part in parts:
        code = part.split("/")[0].strip()
        label = JOBKOREA_EMPLOYMENT_MAP.get(code)
        if label and label not in labels:
            labels.append(label)
    return ", ".join(labels)

def _format_employment_type(job: JobPost) -> str:
    raw = (job.employment_type or "").strip()
    if not raw:
        return ""
    if job.source and job.source.code == "jobkorea":
        return _normalize_jobkorea_employment(raw)
    return raw

def _select_latest_jobs(qs, limit: int) -> list[JobPost]:
    jobs: list[JobPost] = []
    seen: set[str] = set()

    for job in qs.iterator():
        group_id = job.duplicate_group_id
        key = f"group:{group_id}" if group_id else f"job:{job.id}"
        if key in seen:
            continue
        seen.add(key)
        jobs.append(job)
        if len(jobs) >= limit:
            break

    return jobs

def job_list(request):
    qs = JobPost.objects.for_list()

    keyword = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    max_years_raw = request.GET.get("max_years", "").strip()
    source_code = request.GET.get("source", "").strip()

    if keyword:
        qs = qs.filter_by_keyword(keyword)
    if location:
        qs = qs.filter_by_location(location)

    max_years = None
    if max_years_raw:
        try:
            max_years = int(max_years_raw)
        except ValueError:
            max_years = None
    if max_years is not None:
        qs = qs.filter_by_experience_max(max_years)

    if source_code:
        qs = qs.filter_by_source_codes([source_code])

    jobs = _select_latest_jobs(qs, MAX_LIST_JOBS)
    for job in jobs:
        job.employment_type_display = _format_employment_type(job)

    sources = list(Source.objects.order_by("priority"))

    context = {
        "jobs": jobs,
        "filters": {
            "q": keyword,
            "location": location,
            "max_years": max_years_raw,
            "source": source_code,
        },
        "sources": sources,
    }
    return render(request, "jobs/job_list.html", context)
