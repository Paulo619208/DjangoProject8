from django.urls import path
from .views import (
    JobCreateView, job_list, job_detail,
    JobUpdateView, JobDeleteView
)
from . import views

app_name = 'jobs'

urlpatterns = [
    path("", job_list, name="job_list"),
    path("<int:pk>/", job_detail, name="job_detail"),
    path("create/", JobCreateView.as_view(), name="job_create"),
    path("<int:pk>/update/", JobUpdateView.as_view(), name="job_update"),
    path("<int:pk>/delete/", JobDeleteView.as_view(), name="job_delete"),

    path('', views.job_list, name='home'),

    path('', views.job_list, name='job_list'),
]
