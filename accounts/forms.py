from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

        labels = {
            "username": "Username",
            "email": "Email Address",
        }

        help_texts = {
            "username": "Choose a unique username.",
            "email": "Email must be from @objor.com domain",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@objor.com"):
            raise forms.ValidationError("Email must be @objor.com domain")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")
        return username

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone and User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("Phone number already taken")
        return phone
