from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

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
