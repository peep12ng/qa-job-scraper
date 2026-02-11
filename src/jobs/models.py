from django.db import models

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