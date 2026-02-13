from django.shortcuts import render

from jobs.models import JobPost, Source

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

    jobs = list(qs[:200])
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
