from django import forms
from .models import Form

class FormModelForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['first_name', 'last_name', 'phone_no', 'email', 'message']
