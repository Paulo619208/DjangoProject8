from django.db import models
from accounts.models import User

class Job(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    min_offer = models.DecimalField(max_digits=10, decimal_places=2)
    max_offer = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.job_title

class JobApplicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to="resumes/")

    class Meta:
        unique_together = ('user', 'job')



