from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Form, AppInfo
from .forms import FormModelForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.mail import send_mail
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
    

class JobApplyView(CreateView):
    model = Form
    form_class = FormModelForm
    template_name = "school_app/application_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Get the job from URL
        self.job = get_object_or_404(Job, id=self.kwargs['job_id'])

        # Check if user has already applied
        if request.user.is_authenticated:
            if AppInfo.objects.filter(job=self.job, form__user=request.user).exists():
                messages.error(request, "You have already applied for this job, check your applied job.")
                return redirect('Homepage')  # redirect to homepage or job list

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save applicant
        applicant = form.save(commit=False)
        if self.request.user.is_authenticated:
            applicant.user = self.request.user
        applicant.save()

        # Link applicant to job via AppInfo
        AppInfo.objects.create(form=applicant, job=self.job)

        # Send notification email to the job poster
        send_mail(
            subject=f"New Application for {self.job.title}",
            message=f"{applicant.first_name} {applicant.last_name} applied for your job.\n"
                    f"Contact them at: {applicant.email}",
            from_email="none",
            recipient_list=[self.job.posted_by.email],
        )

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect after successful application
        messages.success(self.request, "You application has been submitted successfully.")
        return reverse_lazy('Homepage')

    
class Status(ListView):
    model = AppInfo
    context_object_name = "all"
    template_name = "school_app/applied.html"
    # paginate_by = 8
    # queryset = Recruit.objects.all().order_by("title")
    
    def get_queryset(self):
        # Show only applications for the currently logged-in user
        return AppInfo.objects.filter(form__user=self.request.user).order_by('-applied_at')
    
class SearchStatus(ListView):
    model = AppInfo
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
