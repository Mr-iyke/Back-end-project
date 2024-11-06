from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if not email:
    #         raise ValidationError(_('This field is required.'))
    #     return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar","gender"]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]