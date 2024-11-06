from django.shortcuts import render
from .models import Job, Form, Recruit
from .forms import AppForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q


# Create your views here.
class Home(ListView):
    model = Job
    context_object_name = "all"
    template_name = "school_app/home.html"
    queryset = Job.objects.all().order_by('title')
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = Job.objects.order_by('-uploaded_at')[:4]
        return context

class OffCampus(ListView):
    model = Job
    context_object_name = "all"
    template_name = "school_app/off-campus.html"
    queryset = Job.objects.all().order_by("title")
    paginate_by = 16
    
class ApplicationForm(CreateView):
    model = Form
    form_class = AppForm
    template_name = "school_app/application_form.html"
    context_object_name = "form"
    success_url = reverse_lazy("Statuspage")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.cleaned_data.get('Job')
        messages.success(self.request, "Your application was sent successfully")
        return super(ApplicationForm, self).form_valid(form)
    
class Status(ListView):
    model = Recruit
    context_object_name = "all"
    template_name = "school_app/status.html"
    # paginate_by = 8
    # queryset = Recruit.objects.all().order_by("title")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["all"] = context["all"].filter(Form__user=self.request.user)
        return context
    
class SearchStatus(ListView):
    model = Recruit
    template_name = "school_app/status_search.html"
    context_object_name = "search"
    # queryset = Recruit.objects.all().order_by("title")

    # 78 - 89 used to display searched items created by a particular user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querys = self.request.GET.get("query")
        if querys:
            show = context["search"].filter(Q(Job__title__icontains = querys) & Q(Form__user=self.request.user))
            if show:
                context["search"] = show
                context["query"] = querys
            else:
                # messages.error(self.request, f"search result for {querys} not found")
                context["search"] = context["search"].none()
                context["query"] = querys
        else:
            messages.error(self.request, "Please enter a valid query")
            context["search"] = context["search"].none()
        return context

class Details(DetailView):
    model = Job
    context_object_name = "details"
    template_name = "school_app/details.html"
    
class Search(ListView):
    model = Job
    template_name = "school_app/search.html"
    context_object_name = "search"
    queryset = Job.objects.all().order_by("title")

    def get_queryset(self):
        query = self.request.GET.get('query')
        self.query = query  # Store query for template

        if query:
            return Job.objects.filter(title__icontains=query).order_by('title')
        else:
            messages.error(self.request, "Please enter a valid query")
            return Job.objects.none()  # Return an empty queryset if no query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context
