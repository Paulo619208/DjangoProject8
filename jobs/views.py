from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import models

from .models import Job, JobApplicant
from .forms import JobForm, JobApplicantForm

# -----------------------------
# Helper: Admin check
# -----------------------------
def is_admin(user):
    return getattr(user, "admin", False)


# -----------------------------
# Home Page (Applicants)
# -----------------------------
@login_required(login_url="/accounts/login/")
def home(request):
    """
    Main homepage for logged-in users:
    - Shows all available jobs
    - Does NOT show personal info of the logged-in applicant
    """
    jobs = Job.objects.all()

    return render(request, "jobs/home.html", {
        "jobs": jobs
    })


# -----------------------------
# Job Create (FBV, Admin only)
# -----------------------------
@login_required
@user_passes_test(is_admin)
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jobs:job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})


# -----------------------------
# Job Create (CBV, Admin only)
# -----------------------------
class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("jobs:job_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not is_admin(request.user):
            return render(request, "401.html", status=401)
        return super().dispatch(request, *args, **kwargs)


# -----------------------------
# Job List (FBV, login required)
# -----------------------------
def job_list(request):
    query = request.GET.get("q", "")
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(
            models.Q(job_title__icontains=query) |
            models.Q(job_description__icontains=query) |
            models.Q(location__icontains=query)
        )

    if not request.user.is_authenticated:
        return render(request, "jobs/job_list.html", {
            "jobs": [],
            "query": query,
            "show_login_message": True
        })

    return render(request, "jobs/job_list.html", {"jobs": jobs, "query": query})


# -----------------------------
# Job Detail (Admin vs Regular User)
# -----------------------------
@login_required(login_url="/accounts/login/")
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if is_admin(request.user):
        applicants = JobApplicant.objects.filter(job=job)
        return render(request, "jobs/job_detail_admin.html", {
            "job": job,
            "applicants": applicants
        })
    else:
        already_applied = JobApplicant.objects.filter(user=request.user, job=job).exists()
        if request.method == "POST" and not already_applied:
            form = JobApplicantForm(request.POST, request.FILES)
            if form.is_valid():
                applicant = form.save(commit=False)
                applicant.user = request.user
                applicant.job = job
                applicant.save()
                return redirect("jobs:job_detail", pk=pk)
        else:
            form = JobApplicantForm()

        return render(request, "jobs/job_detail_user.html", {
            "job": job,
            "form": form,
            "already_applied": already_applied
        })


# -----------------------------
# Job Update (Admin only)
# -----------------------------
class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("jobs:job_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not is_admin(request.user):
            return render(request, "401.html", status=401)
        return super().dispatch(request, *args, **kwargs)


# -----------------------------
# Job Delete (Admin only)
# -----------------------------
class JobDeleteView(DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("jobs:job_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not is_admin(request.user):
            return render(request, "401.html", status=401)
        return super().dispatch(request, *args, **kwargs)
