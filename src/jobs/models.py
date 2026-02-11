from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    priority = models.PositiveSmallIntegerField()
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

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

    def __str__(self):
        return self.title

class RunLog(models.Model):
    STATUS_SUCCESS = "success"
    STATUS_FAIL = "fail"
    STATUS_PARTIAL = "partial"

    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    items_collected = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source.code}:{self.status}"