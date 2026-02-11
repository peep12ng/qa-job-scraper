from django.db import models
from django.db.models import Q

class Source(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    priority = models.PositiveSmallIntegerField()
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["priority"], name="source_priority_idx"),
            models.Index(fields=["is_active"], name="source_active_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class DuplicateGroup(models.Model):
    group_key = models.CharField(max_length=200)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_key

class JobPostQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related("source", "duplicate_group")
    
    def for_list(self):
        return self.with_related().order_by("-posting_date", "-collected_at")
    
    def for_detail(self):
        return self.with_related()
    
    def filter_by_location(self, location):
        if not location:
            return self
        return self.filter(location__icontains=location)
    
    def filter_by_keyword(self, keyword):
        if not keyword:
            return self
        return self.filter(
            Q(title__icontains=keyword) 
            | Q(company__icontains=keyword) 
            | Q(tags__icontains=keyword)
            | Q(description_snippet__icontains=keyword)
        )
    
    def filter_by_experience_max(self, max_years):
        if max_years is None:
            return self
        return self.filter(
            Q(experience_max_years__isnull=True)
            | Q(experience_max_years__lte=max_years)
        )
    
    def filter_by_source_codes(self, codes):
        if not codes:
            return self
        return self.filter(source__code__in=codes)

class JobPost(models.Model):
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    duplicate_group = models.ForeignKey(
        DuplicateGroup, on_delete=models.SET_NULL, null=True, blank=True
    )

    source_job_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=100, blank=True)
    experience_max_years = models.PositiveSmallIntegerField(null=True, blank=True)

    posting_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    url = models.URLField(max_length=500)
    description_snippet = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    source_category_path = models.CharField(max_length=500, blank=True)

    collected_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobPostQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source",  "source_job_id"], name="unique_source_job"
            ),
        ]
        indexes = [
            models.Index(fields=["posting_date"], name="job_posting_date_idx"),
            models.Index(fields=["closing_date"], name="job_closing_date_idx"),
            models.Index(fields=["location"], name="job_location_idx"),
            models.Index(fields=["experience_max_years"], name="job_exp_years_idx"),
            models.Index(fields=["collected_at"], name="job_collected_at_idx"),
        ]

    def __str__(self):
        return self.title

class RunLog(models.Model):
    STATUS_SUCCESS = "success"
    STATUS_FAIL = "fail"
    STATUS_PARTIAL = "partial"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAIL, "Fail"),
        (STATUS_PARTIAL, "Partial"),
    ]

    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    items_collected = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"], name="runlog_status_idx"),
            models.Index(fields=["started_at"], name="runlog_started_at_idx"),
        ]

    def __str__(self):
        return f"{self.source.code}:{self.status}"