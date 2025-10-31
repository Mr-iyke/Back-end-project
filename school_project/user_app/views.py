from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .form import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.views.generic import TemplateView


# Create your views here.
class Register(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy("Homepage")
    template_name = "user_app/register.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Check if the email is already in use
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'This email address is already in use.')
            return self.form_invalid(form)

        user = form.save()
        if user:
            login(self.request, user)
            messages.success(self.request, "You have successfully registered")
            return super().form_valid(form)

# class Register(FormView):
    # form_class = RegisterForm
    # success_url = reverse_lazy("Homepage")
    # template_name = "user_app/register.html"
    # redirect_authenticated_user = True

    # def form_valid(self, form):
    #     user = form.save()
    #     if user:
    #         login(self.request, user)
    #         messages.success(self.request, "you have successfully registered")
    #         return super(Register, self).form_valid(form)


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "user_app/login.html"

    def get_success_url(self):
        messages.success(self.request, "You have been successfully logged in")
        return reverse_lazy("Homepage")
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form = form))

class MyProfile(View, LoginRequiredMixin):
    def get(self, request):
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.profile)
        context = {"user_form" : user_form, "profile_form" : profile_form}
        return render(request, "User_app/Update_profile.html", context)
    
    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been successfully updated")
            return redirect("ProfileDetailspage")
        else:
            messages.error(request, "invalid")
            context = {"user_form" : user_form, "profile_form" : profile_form}
            return render(request, "User_app/Update_profile.html", context)


class ProfileDetails(TemplateView):
    model = Profile
    template_name = "User_app/Profile_details.html"
    
def Logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect("Loginpage")