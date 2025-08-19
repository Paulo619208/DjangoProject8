from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Job, JobApplicant
from .forms import JobForm, JobApplicantForm
from django.db import models
from django.shortcuts import render
from .models import Job

# -----------------------------
# Job Create (Admin only)
# -----------------------------
class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.admin:
            return render(request, "401.html", status=401)
        return super().dispatch(request, *args, **kwargs)


# -----------------------------
# Job List (Search + FBV)
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
    return render(request, "jobs/job_list.html", {"jobs": jobs, "query": query})


# -----------------------------
# Job Detail (Different views for Admin vs Regular User)
# -----------------------------
@login_required(login_url="/admin/login/")  # redirect anon users to admin login
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user.admin:
        # Admin sees applicants + edit/delete
        applicants = JobApplicant.objects.filter(job=job)
        return render(request, "jobs/job_detail_admin.html", {
            "job": job,
            "applicants": applicants
        })
    else:
        # Regular user can apply
        already_applied = JobApplicant.objects.filter(user=request.user, job=job).exists()
        if request.method == "POST" and not already_applied:
            form = JobApplicantForm(request.POST, request.FILES)
            if form.is_valid():
                applicant = form.save(commit=False)
                applicant.user = request.user
                applicant.job = job
                applicant.save()
                return redirect("job_detail", pk=pk)
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
    success_url = reverse_lazy("job_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.admin:
            return render(request, "401.html", status=401)
        return super().dispatch(request, *args, **kwargs)


# -----------------------------
# Job Delete (Admin only)
# -----------------------------
class JobDeleteView(DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("job_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.admin:
            return render(request, "401.html", status=401)
        return super().dispatch(request, *args, **kwargs)

# Example queryset: jobObjor = Job.objects.filter(job_title="objor")
from django.shortcuts import render

def bootstrap_test(request):
    return render(request, "test.html")

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# Create your views here.
