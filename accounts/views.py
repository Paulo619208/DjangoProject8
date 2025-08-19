from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from jobs.models import JobApplicant

# -----------------------------
# Register view
# -----------------------------
def register_view(request):
    """
    Handles user registration:
    1. Creates a new User with hashed password.
    2. Automatically creates a JobApplicant record linked to the user.
    3. Optionally logs in the user and redirects to homepage.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user (password is hashed automatically)
            user = form.save()

            # Create a corresponding JobApplicant instance (job=None for now)
            JobApplicant.objects.create(user=user, job=None)

            # Optionally log the user in immediately
            login(request, user)

            # Redirect to homepage
            return redirect("jobs:home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


# -----------------------------
# Login view with 'next' handling
# -----------------------------
def login_view(request):
    """
    Handles user login for both regular users and admin.
    Supports 'next' parameter for redirect after login.
    """
    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_to = request.POST.get('next') or '/'
                return redirect(redirect_to)
            else:
                form.add_error(None, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': next_url
    })


# -----------------------------
# Logout view
# -----------------------------
def logout_view(request):
    """
    Logs out the user and redirects to homepage.
    """
    logout(request)
    return redirect('jobs:home')
