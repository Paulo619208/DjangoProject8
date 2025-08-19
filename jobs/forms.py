from django import forms
from .models import Job, JobApplicant

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'job_description', 'min_offer', 'max_offer', 'location']

    def clean(self):
        cleaned_data = super().clean()
        min_offer = cleaned_data.get("min_offer")
        max_offer = cleaned_data.get("max_offer")

        if min_offer and max_offer and min_offer > max_offer:
            raise forms.ValidationError("Minimum offer cannot be greater than maximum offer")
        return cleaned_data


class JobApplicantForm(forms.ModelForm):
    class Meta:
        model = JobApplicant
        fields = ['resume']
