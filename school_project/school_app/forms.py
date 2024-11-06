from django import forms
from django.contrib.auth.models import User
from .models import Form

class AppForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ["first_name", "last_name", "email", "phone_no", "message", "Job"]