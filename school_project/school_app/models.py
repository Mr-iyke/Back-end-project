from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Job(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add = True)
    image =  models.ImageField( blank=True, null=True, upload_to = "images")

    
    def __str__(self):
        return f"{self.title}"


class Form(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    phone_no = models.CharField(max_length = 20)
    email = models.EmailField()
    message = models.TextField()
    Job  = models.ManyToManyField(Job, through = "recruit")
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Recruit(models.Model):
    Job = models.ForeignKey(Job, on_delete = models.CASCADE, default = None)
    Form = models.ForeignKey(Form, on_delete = models.CASCADE, default = None)
    uploaded_on = models.DateTimeField(auto_now_add = True)
    recruited = models.BooleanField(default = False)
    declined = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.Job.title} applied by {self.Form.user}"


