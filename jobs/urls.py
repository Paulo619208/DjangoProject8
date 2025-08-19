from django.urls import path
from .views import (
    home,          # Main homepage for applicants
    job_list,      # List of jobs (admin view)
    job_detail,    # Job detail
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
)

app_name = 'jobs'

urlpatterns = [
    # Main homepage → /
    path("", home, name="home"),

    # Job list (admin) → /jobs/list/
    path("list/", job_list, name="job_list"),

    # Create job (CBV, admin only) → /jobs/create/
    path("create/", JobCreateView.as_view(), name="job_create"),

    # Job detail → /jobs/<int:pk>/
    path("<int:pk>/", job_detail, name="job_detail"),

    # Update job (CBV, admin only) → /jobs/<int:pk>/update/
    path("<int:pk>/update/", JobUpdateView.as_view(), name="job_update"),

    # Delete job (CBV, admin only) → /jobs/<int:pk>/delete/
    path("<int:pk>/delete/", JobDeleteView.as_view(), name="job_delete"),
]
