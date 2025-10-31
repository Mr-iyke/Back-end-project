from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Job(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add = True)
    image =  models.ImageField( blank=True, null=True, upload_to = "images")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs_posted",  blank=True, null=True)


    
    def __str__(self):
        return f"{self.title}"


class Form(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    phone_no = models.CharField(max_length = 20)
    email = models.EmailField()
    message = models.TextField()
    jobs  = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AppInfo(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,  null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.form} applied to {self.job}"
