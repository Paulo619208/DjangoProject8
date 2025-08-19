from django.db import models
from django.conf import settings

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    min_offer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_offer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # 🔹 Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # set once when created
    updated_at = models.DateTimeField(auto_now=True)      # updates every save

    def __str__(self):
        return self.job_title


class JobApplicant(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,      # allow NULL in database
        blank=True      # allow blank in forms
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    # 🔹 Track when someone applied
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'user')  # prevent duplicate applications

    def __str__(self):
        job_title = self.job.job_title if self.job else 'No job yet'
        return f"{self.user} - {job_title}"
