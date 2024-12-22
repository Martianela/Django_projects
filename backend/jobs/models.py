from django.db import models
import uuid  # To generate unique IDs


class Job(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # Unique identifier
    title = models.CharField(max_length=255)  # Job title
    company_name = models.CharField(max_length=255)  # Name of the company
    company_profile_url = models.URLField(blank=True, null=True)  # URL to the company's profile (optional)
    location = models.CharField(max_length=255, blank=True, null=True)  # Job location (optional)
    posted_date = models.CharField(max_length=60,blank=True, null=True)  # Date the job was posted (optional)
    pay_details = models.CharField(max_length=255, blank=True, null=True)  # Pay details (optional)
    employment_details = models.TextField(blank=True, null=True)  # Employment type/details (optional)
    skills = models.TextField(blank=True, null=True)  # Required skills (optional, can store as comma-separated values)
    job_description = models.TextField(blank=True, null=True)  # Job description (optional)
    details_url = models.URLField(blank=True, null=True)  # URL for job details (optional)

    def __str__(self):
        return f"{self.title} at {self.company_name}"
