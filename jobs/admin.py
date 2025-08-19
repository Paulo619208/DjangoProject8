from django.contrib import admin
from .models import Job, JobApplicant

# -----------------------------
# Job admin
# -----------------------------
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'location', 'min_offer', 'max_offer', 'created_at', 'updated_at')
    search_fields = ('job_title', 'location')
    readonly_fields = ('created_at', 'updated_at')  # timestamps are read-only

# -----------------------------
# JobApplicant admin
# -----------------------------
@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'created_at')  # show user and job
    search_fields = ('user__username', 'user__email', 'job__job_title')  # allow admin search
    readonly_fields = ('created_at',)  # prevent editing timestamps
    list_filter = ('job',)  # optional: filter by job for easier management
