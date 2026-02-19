from django.shortcuts import render

from jobs.models import JobPost, RunLog, Source

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

def _build_run_status(sources: list[Source]) -> dict:
    latest_by_source: dict[str, RunLog] = {}
    failed_sources: list[str] = []
    latest_time = None

    for log in RunLog.objects.select_related("source").order_by("-started_at"):
        code = log.source.code
        if code in latest_by_source:
            continue
        latest_by_source[code] = log
        
        if log.status == RunLog.STATUS_FAIL:
            failed_sources.append(log.source.name)
        
        ts = log.finished_at or log.started_at
        if ts and (latest_time is None or ts > latest_time):
            latest_time = ts
        
        if len(latest_by_source) >= len(sources):
            break
    
    return {
        "latest_time": latest_time,
        "failed_sources": failed_sources,
    }

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
    run_status = _build_run_status(sources)

    context = {
        "jobs": jobs,
        "filters": {
            "q": keyword,
            "location": location,
            "max_years": max_years_raw,
            "source": source_code,
        },
        "sources": sources,
        "run_status": run_status,
    }
    return render(request, "jobs/job_list.html", context)
