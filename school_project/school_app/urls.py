from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name = "Homepage"),
    path("off-campus/", views.OffCampus.as_view(), name = "OffCampuspage"),
    path("details/<int:pk>/", views.Details.as_view(), name = "Detailspage"),
    path("search/", views.Search.as_view(), name = "Searchpage"),
    path('application_form/<int:job_id>/', views.JobApplyView.as_view(), name='ApplyFormpage'),
    path("applied/", views.Status.as_view(), name = "Appliedpage"),
    path("status_search/", views.SearchStatus.as_view(), name = "StatusSearchpage"),
]