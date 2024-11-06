from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


urlpatterns = [
        path("register/", views.Register.as_view(), name = "Registerpage"),
        path("login/", views.Login.as_view(), name = "Loginpage"),
        path("password_reset/", PasswordResetView.as_view(template_name = "User_app/password_reset.html", html_email_template_name = "User_app/password_reset_email.html"), name = "Passwordreset"),
        path("password_reset_done/", PasswordResetDoneView.as_view(template_name = "User_app/password_reset_done.html"), name = "password_reset_done"),
        path("password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name = "User_app/password_reset_confirm.html"), name = "password_reset_confirm"),
        path("password_reset_complete/", PasswordResetCompleteView.as_view(template_name = "User_app/password_reset_complete.html"), name = "password_reset_complete"),
        path("logout/", views.Logout, name = "Logoutpage"),
        path("profile_details/", views.ProfileDetails.as_view(), name = "ProfileDetailspage"),
        path("Update_profile/", views.MyProfile.as_view(), name = "UpdateProfilepage"),
]